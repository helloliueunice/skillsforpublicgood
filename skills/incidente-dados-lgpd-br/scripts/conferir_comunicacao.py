#!/usr/bin/env python3
"""Confere uma minuta de comunicação ou de registro de incidente contra a Res. CD/ANPD 15/2024 e as salvaguardas da skill.

Uso:
    python3 scripts/conferir_comunicacao.py ARQUIVO.md --modo anpd|titular|registro|parcial [--json]

Verifica:
- conteúdo mínimo: à ANPD, art. 6º, § 2º, I a XII; ao titular, art. 9º, I a VII; registro, art. 10, § 1º;
- citações: artigos da LGPD e da Res. CD/ANPD 15/2024 precisam estar em references/normas.json;
  lei, resolução ou decreto fora da base só passam na mesma linha de "não verificado"; o Decreto
  9.637/2018 só passa na mesma linha de "revogado";
- linguagem: proíbe declarar conformidade ou licitude, aprovar em nome do controlador, afirmar ausência
  de risco ou dispensar a comunicação (salvo se atribuído ao controlador), prometer risco zero ou
  segurança total, minimizar o incidente, pedir senha, código ou dados e acusar pessoas; a exceção de
  negação vale só para negação direta do termo ou verbo de relato negado ("não afirmamos que");
- dados pessoais: nenhum CPF, e-mail real, telefone etc. (nem lista de titulares);
- comunicação ao titular: sem detalhe técnico que ajude um ataque (IP, porta, CVE, host interno,
  versão de software) e alertas de linguagem simples (frases longas, jargão);
- aviso final de minuta e revisão humana; marcadores [PREENCHER] e [CONFERIR] que restam.
As verificações são por palavras-chave: passar não prova que o conteúdo está certo.
Sem rede; não grava arquivos. Código de saída: 0 sem erros; 1 há erros; 3 erro de uso.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

from _comum import achar_dados_pessoais, carregar_normas, ler_texto, sem_acento

# (rótulo, dispositivo, regex sobre o texto sem acento e em minúsculas)
ANPD = [
    ("natureza e categoria dos dados afetados", "I", r"natureza[^\n]{0,80}categoria|categoria[^\n]{0,80}natureza"),
    ("número de titulares afetados, com crianças, adolescentes e idosos", "II", r"titulares afetados[\s\S]{0,400}(crianc|adolescent|idos)"),
    ("medidas de segurança antes e após o incidente", "III", r"medidas[^\n]{0,120}antes[\s\S]{0,300}(apos|depois)"),
    ("riscos e possíveis impactos aos titulares", "IV", r"riscos?[\s\S]{0,200}impactos?"),
    ("motivos da demora (ou que não houve demora)", "V", r"demora"),
    ("medidas para reverter ou mitigar os efeitos", "VI", r"reverter|mitiga"),
    ("data da ocorrência e data do conhecimento", "VII", r"ocorr[\s\S]{0,300}conhecimento|conhecimento[\s\S]{0,300}ocorr"),
    ("dados do encarregado ou de quem represente o controlador", "VIII", r"encarregad"),
    ("identificação do controlador e declaração sobre pequeno porte", "IX", r"controlador[\s\S]{0,400}pequeno porte"),
    ("identificação do operador, quando aplicável", "X", r"operador"),
    ("descrição do incidente e causa principal", "XI", r"causa"),
    ("total de titulares tratados nas atividades afetadas", "XII", r"total de titulares"),
]
TITULAR = [
    ("natureza e categoria dos dados afetados", "I", r"(quais|que) dados|dados (afetados|envolvidos|expostos)|tipos? de dados"),
    ("medidas de segurança usadas para proteger os dados", "II", r"medidas de seguranca|protegiamos|protecao dos dados|protegidos"),
    ("riscos e possíveis impactos", "III", r"riscos?"),
    ("medidas adotadas ou a adotar", "V", r"o que (fizemos|estamos fazendo|ja fizemos)|medidas (adotadas|tomadas)|providencias"),
    ("data do conhecimento do incidente", "VI", r"\d{1,2}/\d{1,2}/\d{4}|\d{1,2} de [a-z]+ de \d{4}"),
    ("contato para informações e encarregado", "VII", r"contato|canal|encarregad|atendimento"),
]
REGISTRO = [
    ("data de conhecimento", "I", r"conhecimento"),
    ("circunstâncias do incidente", "II", r"circunstanc|como (ocorreu|aconteceu)|descricao"),
    ("natureza e categoria dos dados", "III", r"natureza[^\n]{0,80}categoria|categoria[^\n]{0,80}natureza"),
    ("número de titulares afetados", "IV", r"titulares afetados|numero de titulares"),
    ("avaliação do risco e possíveis danos", "V", r"avaliacao do risco|risco[\s\S]{0,120}danos?"),
    ("medidas de correção e mitigação", "VI", r"corre[cç]|mitiga"),
    ("forma e conteúdo da comunicação, se houve", "VII", r"comunicac"),
    ("motivos da ausência de comunicação, quando for o caso", "VIII", r"motivos?[\s\S]{0,80}(ausencia|nao comunica)|ausencia de comunicacao|comunicad[oa] (a|em)|comunicacao (a|feita|realizada)"),
]
# Linguagem proibida em qualquer modo (C5 da auditoria AGU/CGU). Quantificadores limitados: tempo linear.
PROIBIDO = [
    (r"\b(est[aá]|est[aã]o|estamos|encontra-se|encontram-se|encontramo-nos|permanece|permanecemos)\s+(plenamente\s+|totalmente\s+|integralmente\s+)?(em\s+)?conform(e|idade)\b",
     "declara conformidade"),
    (r"\b(declaro|aprovo|autorizo|homologo|fica\s+aprovad[oa]|aprova-se)\b", "fala como se fosse o controlador aprovando"),
    (r"\b([eé]|foi|ser[aá]|seria)\s+l[ií]cit[oa]\b", "afirma licitude (juízo do controlador e da assessoria jurídica)"),
    (r"\brisco\s+(([eé]|foi|seria|ser[aá])\s+)?(zero|inexistente|nulo)\b|\bnenhum\s+risco\b", "afirma risco zero"),
    (r"\b(100\s?%|totalmente|completamente)\s+segur", "promete segurança total"),
    (r"\bn[aã]o\s+(houve|h[aá]|existe|existiu|ocorreu|haver[aá])\s+(qualquer\s+|nenhum\s+)?(risco|dano|perigo)", "afirma ausência de risco ou dano (conclusão é do controlador)"),
    (r"\bn[aã]o\s+(acarret\w{0,6}|gerou|gera|representa|representou|trouxe|traz)\s+(qualquer\s+|nenhum\s+)?(risco|dano|perigo)", "afirma ausência de risco ou dano (conclusão é do controlador)"),
    (r"\b(sem|aus[eê]ncia\s+de|inexist[eê]ncia\s+de)\s+(qualquer\s+)?(risco|dano)s?(\s+ou\s+danos?)?\s+relevantes?", "afirma ausência de risco ou dano relevante (conclusão é do controlador)"),
    (r"\bn[aã]o\s+([eé]|seria|foi)\s+(necess[aá]ri[oa]|obrigat[oó]ri[oa]|preciso|exigid[oa])\s+(a\s+)?comunic|\bn[aã]o\s+precisa(m|mos)?\s+(ser\s+)?comunic|\bn[aã]o\s+(h[aá]|existe)\s+(dever|obriga[cç][aã]o|necessidade)\s+de\s+comunic",
     "dispensa a comunicação (decisão do controlador)"),
    (r"\b(fica|ficam|est[aá]|est[aã]o)\s+dispensad[oa]s?\b|\bdispensad[oa]s?\s+(d[ao]s?\s+)?(a\s+)?(comunica|elabora|registro)|\bcomunica[cç][aã]o\s+(n[aã]o\s+([eé]\s+|foi\s+|seria\s+)?|([eé]|foi|seria)\s+n[aã]o\s+)(exigida|necess[aá]ria|obrigat[oó]ria)"
     r"|\bcomunica[cç][aã]o\s+(([eé]|foi|seria)\s+)?(dispensada|desnecess[aá]ria)",
     "dispensa a comunicação (decisão do controlador)"),
    (r"\bfique(m)?\s+tranquil|\bn[aã]o\s+se\s+preocupe|\b(seus|os|suas|as)\s+(dados|informa[cç][oõ]es)\s+(est[aã]o|permanecem|continuam)\s+(totalmente\s+)?(seguros|seguras|a\s+salvo)",
     "minimiza o incidente"),
    (r"\b(respond\w{0,4}|retorn\w{0,4}|envie|mande|informe|digite|confirme|atualize|forne[cç]a|repasse|cadastre)\b[^.\n]{0,40}?\b(senha|c[oó]digo|token|cpf|dados\s+banc[aá]rios|n[uú]mero\s+do\s+cart[aã]o)",
     "pede senha, código ou dados (risco de golpe)"),
    (r"\bculpad[oa]s?\b|\bpor\s+culpa\s+d|\bneglig[eê]ncia\s+d[oa]s?\s+(servidor|servidora|funcion[aá]ri|colaborador|empregad|t[eé]cnic|analista|estagi[aá]ri|operador)",
     "acusa pessoa (apuração é por sindicância ou PAD, Lei 8.112/1990, art. 143)"),
]
# Nome próprio depois de "servidor", "colaborador" etc. seguido de verbo de conduta: sensível a maiúsculas.
ACUSA_NOME = re.compile(r"\b([Ss]ervidora?|[Ff]uncion[aá]ri[oa]|[Cc]olaborador[a]?|[Ee]stagi[aá]ri[oa]|[Tt][eé]cnic[oa]|[Aa]nalista)\s+"
                        r"[A-ZÁÉÍÓÚÂÊÔÃÕ][a-záéíóúâêôãõç]{1,30}(\s+[A-ZÁÉÍÓÚÂÊÔÃÕ][a-záéíóúâêôãõç]{1,30}){0,3}\s+"
                        r"(foi|[eé]|teria|causou|errou|deixou|clicou|enviou|vazou|falhou|permitiu|esqueceu)\b")
SO_TITULAR = [
    (r"n[aã]o\s+(h[aá]|existe)\s+(motivo|raz[aã]o|necessidade)\s+(para|de)\s+(se\s+)?preocup", "minimiza o incidente para o titular"),
    (r"\b(informe|digite|confirme|envie|atualize)\s+(a\s+)?(sua|seu|seus|suas)\s+(senha|cpf|dados|cart[aã]o|conta)", "pede senha ou dados ao titular (risco de golpe)"),
]
RESTRITO = [
    (r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])", "endereço IP"),
    (r"\bporta\s+\d{2,5}\b", "porta de rede"),
    (r"\bCVE-\d{4}-\d{3,}", "identificador de vulnerabilidade"),
    (r"\b[\w-]+\.(?:intra|local|corp|lan)\b", "nome de host interno"),
    (r"\b(?:software|servidor|firmware|sistema operacional|banco de dados|apache|nginx|windows|linux|postgres\w*|mysql|oracle|java|php)\b[^\n]{0,30}?\bv?(?:ers[aã]o\s+)?\d+\.\d+", "versão de software"),
    (r"\b(usu[aá]rio|conta)\s+(admin|root|administrador)\b", "conta privilegiada"),
]
JARGAO = ["ransomware", "exfiltra", "vetor de ataque", "payload", "hash", "phishing", "malware", "backup", "log ", "logs",
          "titular dos dados", "controlador", "operador", "anpd", "lgpd", "incidente de seguranca"]
LEIS_OK = {"13.709/2018", "15.352/2026", "12.527/2011", "662/1949", "6.802/1980", "14.759/2023", "10.607/2002",
           "8.112/1990", "9.093/1995"}
RES_OK = {"15/2024", "2/2022", "1/2021", "18/2024"}
DECRETOS_OK = {"10.748/2021", "12.572/2025"}
DECRETOS_SO_COMO_REVOGADOS = {"9.637/2018"}
JANELA_LGPD = re.compile(r"(?:LGPD|Lei\s+(?:n[ºo°.]\s*)?13\.709(?:/2018)?)([^()\n;]{0,160})")
JANELA_R15 = re.compile(r"(?:15/2024|Regulamento de Comunica[cç][aã]o de Incidente)([^()\n;]{0,160})")
ARTS = re.compile(r"\barts?\.\s*((?:\d{1,2}(?:-[A-Z])?º?(?:\s*(?:,|e|a)\s*(?=\d))?)+)")


def artigos(normas: dict, prefixo: str) -> set[str]:
    ok = set()
    for it in normas["itens"]:
        if it["verificado"] and it["norma"].startswith(prefixo) and "Resolução (não do anexo)" not in it["dispositivo"]:
            for grupo in ARTS.findall(it["dispositivo"]):
                nums = re.findall(r"\d{1,2}(?:-[A-Z])?", grupo)
                if " a " in grupo and len(nums) == 2 and nums[0].isdigit() and nums[1].isdigit():
                    nums = [str(i) for i in range(int(nums[0]), int(nums[1]) + 1)]
                ok.update(nums)
    return ok


NEG_DIRETA = re.compile(r"\b(n[aã]o|nunca|jamais)\s+(se\s+|lhe\s+|nos\s+|o\s+|a\s+)?$", re.I)
NEG_RELATO = re.compile(r"\b(n[aã]o|nunca|jamais)\s+((vou|vamos|devemos|deve|podemos|pode|iremos|ir[aá])\s+)?"
                        r"(afirm\w{0,6}|declar\w{0,6}|garant\w{0,6}|escrev\w{0,6}|diz\w{0,4}|dizer|apont\w{0,6}|atribu\w{0,6}|"
                        r"promet\w{0,6}|acus\w{0,6}|ped\w{0,6}|solicit\w{0,6}|nome\w{0,6}|conclu\w{0,6}|usar|use)\s+"
                        r"(que\s+|nem\s+)?[^.:;!?\n]{0,40}$", re.I)
ATRIBUI_CONTROLADOR = re.compile(r"(\bcontrolador\b[^.;!?\n]{0,60}\b(conclu|decid|avali|entend|registr)\w{0,8}\b[^.;!?\n]{0,40}$)|"
                                 r"conclus[aã]o\s+do\s+controlador", re.I)


def negado(antes: str) -> bool:
    """Exceção estreita: negação gramatical direta do termo ("não está em conformidade", "não informe sua
    senha") ou verbo de relato negado ("não afirmamos que...", "nunca pedimos que você..."). Uma negação
    qualquer antes, separada por dois-pontos ou ponto ("Não há dúvida: está em conformidade"), não conta."""
    return NEG_DIRETA.search(antes) is not None or NEG_RELATO.search(antes) is not None


def atribuido_ao_controlador(antes: str, linha: str) -> bool:
    """A conclusão sobre risco aparece como do controlador ("o controlador pode concluir que...")."""
    return ATRIBUI_CONTROLADOR.search(antes) is not None or re.search(r"conclus[aã]o do controlador", linha, re.I) is not None


def ordinal(a: str) -> str:
    return a + "º" if a.isdigit() and int(a) < 10 else a


def plural(n: int, sing: str, plur: str) -> str:
    return f"{n} {sing if n == 1 else plur}"


def frases(texto: str) -> list[str]:
    corpo = re.sub(r"^\s*(#|>|\||-).*$", "", texto, flags=re.M)
    return [f for f in re.split(r"(?<=[.!?])\s+", corpo) if len(f.split()) >= 3]


def conferir(texto: str, modo: str = "parcial") -> tuple[list[str], list[str]]:
    erros, avisos = [], []
    normas = carregar_normas()
    lgpd_ok, r15_ok = artigos(normas, "LGPD"), artigos(normas, "Resolução CD/ANPD 15/2024")
    plano = sem_acento(texto)
    if not re.search(r"revis[aã]o humana|n[aã]o substitui", texto, re.I) or "minuta" not in plano:
        erros.append("falta o aviso final de minuta e revisão humana")
    lista = {"anpd": ANPD, "titular": TITULAR, "registro": REGISTRO}.get(modo, [])
    art = {"anpd": "art. 6º, § 2º", "titular": "art. 9º", "registro": "art. 10, § 1º"}.get(modo)
    for rotulo, inc, rx in lista:
        if not re.search(rx, plano):
            erros.append(f"falta {rotulo} (Res. CD/ANPD 15/2024, {art}, {inc})")
    if modo == "anpd" and not re.search(r"nivel de acesso|restrit|sigilo", plano):
        avisos.append("indique o nível de acesso no SEI e, se for o caso, peça sigilo (art. 7º): documento público fica visível na pesquisa pública")
    if modo == "titular":
        if not re.search(r"recomend|o que voce pode fazer|orientac|cuidados", plano):
            avisos.append("inclua recomendações ao titular para reduzir os efeitos (pode ser boa prática, art. 9º, § 5º)")
        fr = frases(texto)
        if fr:
            media = sum(len(f.split()) for f in fr) / len(fr)
            longas = [f for f in fr if len(f.split()) > 35]
            if media > 22:
                avisos.append(f"frases longas para o titular (média de {media:.0f} palavras; referência desta skill: até 20; a lei não fixa número)")
            for f in longas[:3]:
                avisos.append(f"frase com {len(f.split())} palavras: \"{f[:60]}...\"")
        for j in JARGAO:
            if j in plano:
                avisos.append(f"termo técnico para o titular: '{j.strip()}' (explique ou troque por palavra comum)")
    for n, linha in enumerate(texto.splitlines(), 1):
        nv = "nao verificad" in sem_acento(linha)
        for m in JANELA_LGPD.finditer(linha):
            for grupo in ARTS.findall(m.group(1)):
                for a in re.findall(r"\d{1,2}(?:-[A-Z])?", grupo):
                    if a not in lgpd_ok and not nv:
                        erros.append(f"linha {n}: LGPD, art. {ordinal(a)}, não está em references/normas.json como verificado")
        for m in JANELA_R15.finditer(linha):
            for grupo in ARTS.findall(m.group(1)):
                for a in re.findall(r"\d{1,2}", grupo):
                    if a not in r15_ok and not nv:
                        erros.append(f"linha {n}: Res. CD/ANPD 15/2024, art. {ordinal(a)}, não está na base como verificado")
        for lei in re.findall(r"\bLei\s+(?:n[ºo°.]\s*)?(\d{1,2}\.?\d{3}/\d{4})", linha):
            if lei not in LEIS_OK and not nv:
                erros.append(f"linha {n}: Lei {lei} sem 'não verificado' (fora da base)")
        for res in re.findall(r"Res(?:olu[cç][aã]o|\.)\s+CD/ANPD\s+(?:n[ºo°.]\s*)?(\d{1,3}/\d{4})", linha):
            if res not in RES_OK and not nv:
                erros.append(f"linha {n}: Resolução CD/ANPD {res} fora da base; marque 'não verificado'")
        for dec in re.findall(r"\bDecreto(?:-Lei)?\s+(?:n[ºo°.]\s*)?(\d{1,2}\.?\d{3}/\d{4})", linha):
            if dec in DECRETOS_SO_COMO_REVOGADOS:
                if "revogad" not in sem_acento(linha):
                    erros.append(f"linha {n}: Decreto {dec} foi revogado (Decreto 12.572/2025, art. 12, I); não o cite como vigente")
            elif dec not in DECRETOS_OK and not nv:
                erros.append(f"linha {n}: Decreto {dec} fora da base; marque 'não verificado'")
        regras = PROIBIDO + (SO_TITULAR if modo == "titular" else [])
        for rx, motivo in regras:
            for m in re.finditer(rx, linha, re.I):
                antes = linha[:m.start()]
                if negado(antes):
                    continue
                if ("conclusão é do controlador" in motivo or "decisão do controlador" in motivo) and atribuido_ao_controlador(antes, linha):
                    continue
                erros.append(f"linha {n}: linguagem proibida: {motivo}")
                break
        m = ACUSA_NOME.search(linha)
        if m and not negado(linha[:m.start()]):
            erros.append(f"linha {n}: linguagem proibida: acusa pessoa nomeada (apuração é por sindicância ou PAD, Lei 8.112/1990, art. 143)")
        if modo == "titular":
            for rx, motivo in RESTRITO:
                if re.search(rx, linha, re.I):
                    erros.append(f"linha {n}: comunicação ao titular com {motivo} (detalhe técnico ajuda um ataque; deixe só no registro interno)")
    for d in achar_dados_pessoais(texto):
        erros.append(f"linha {d['linha']}: dado pessoal ({d['tipo']}); descreva categorias e números, nunca pessoas")
    marcadores = re.findall(r"\[(PREENCHER|CONFERIR)[^\]]*\]", texto)
    if marcadores:
        avisos.append(f"restam {marcadores.count('PREENCHER')} [PREENCHER] e {marcadores.count('CONFERIR')} [CONFERIR] para a equipe")
    return erros, avisos


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("arquivo")
    ap.add_argument("--modo", choices=("anpd", "titular", "registro", "parcial"), default="parcial")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        texto = ler_texto(a.arquivo)
    except OSError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 3
    erros, avisos = conferir(texto, a.modo)
    if a.json:
        print(json.dumps({"erros": erros, "avisos": avisos}, ensure_ascii=False, indent=1))
    else:
        for e in erros:
            print("ERRO:", e)
        for w in avisos:
            print("AVISO:", w)
        print(f"{plural(len(erros), 'erro', 'erros')}, {plural(len(avisos), 'aviso', 'avisos')}")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
