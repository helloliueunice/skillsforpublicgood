#!/usr/bin/env python3
"""Confere uma minuta de RIPD (Markdown) contra a estrutura, as citações e as salvaguardas da skill.

Uso:
    python3 scripts/conferir_ripd.py RIPD.md [--modo integral|publica|parcial] [--json]

Verifica:
- estrutura (modo integral e publica): seções de references/modelo-de-saida.md, conteúdo mínimo
  do art. 38, parágrafo único, da LGPD, os dez princípios do art. 6º e o aviso de revisão humana;
- citações: dispositivos da LGPD e normas citadas (lei, decreto, resolução, portaria, enunciado,
  instrução normativa) precisam estar em references/normas.json com verificado=true; norma fora da
  base só passa na mesma linha de "não verificado". A marca [CONFERIR] nas resoluções da ANPD é
  regra de redação da skill (SKILL.md, regra 4) e não é exigida por este script;
- linguagem: proíbe declarar conformidade ou licitude, aprovar em nome do controlador, afirmar risco
  zero ou dispensa de RIPD. Só a negação do próprio verbo ("não está em conformidade") ou de um
  verbo de dizer ("não afirmamos que…") afasta o alerta;
- dados pessoais: nenhum CPF, e-mail real, telefone etc. no documento;
- modo publica: nada de detalhe técnico de segurança (IP, porta, CVE, senha, host interno, versão
  de software) e aviso de que há conteúdo omitido;
- lista os marcadores [PREENCHER] e [CONFERIR] que restam.
Sem rede; não grava arquivos. Código de saída: 0 sem erros; 1 há erros; 3 erro de uso.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

from _comum import achar_dados_pessoais, carregar_normas, ler_texto, sem_acento

SECOES = [
    ("Identificação", r"identifica"),
    ("Necessidade do RIPD", r"necessidade"),
    ("Descrição do tratamento", r"descri[cç][aã]o do tratamento"),
    ("Dados pessoais e titulares", r"dados pessoais"),
    ("Hipóteses legais", r"hip[oó]teses? lega"),
    ("Compartilhamento", r"compartilhamento"),
    ("Retenção e eliminação", r"reten[cç][aã]o|elimina"),
    ("Metodologia de coleta e de segurança", r"metodologia"),
    ("Princípios", r"princ[ií]pios"),
    ("Direitos dos titulares", r"direitos"),
    ("Riscos", r"riscos"),
    ("Medidas", r"medidas"),
    ("Conclusão e plano de ação", r"conclus"),
    ("Pendências", r"pend[eê]ncias"),
    ("Aprovação", r"aprova"),
]
PUBLICA_DISPENSA = {"Metodologia de coleta e de segurança", "Riscos", "Medidas"}
PRINCIPIOS = ["finalidade", "adequacao", "necessidade", "livre acesso", "qualidade dos dados", "transparencia",
              "seguranca", "prevencao", "nao discriminacao", "responsabilizacao"]
_INTENS = r"(?:plenamente\s+|totalmente\s+|integralmente\s+|inteiramente\s+)?"
PROIBIDO = [
    (r"\b(?:est[aá]|est[aã]o|encontra-se|encontram-se|[eé]|s[aã]o|fica|ficam)\s+" + _INTENS
     + r"(?:em\s+)?conform(?:e|es|idade)\s+(?:com\s+)?(?:a\s+|à\s+)?(?:LGPD|lei)\b",
     "declara conformidade (só a análise humana e a ANPD podem concluir isso)"),
    (r"\batende(?:m)?\s+" + _INTENS + r"(?:à|a|ao)\s+(?:LGPD|lei\b|requisitos\s+da\s+LGPD)",
     "declara conformidade (só a análise humana e a ANPD podem concluir isso)"),
    (r"\b(?:[eé]|s[aã]o|est[aá]|est[aã]o|torna-se)\s+" + _INTENS + r"(?:l[ií]cit[oa]s?|legal|legais|regular|regulares)\b",
     "conclui que o tratamento é lícito ou regular (isso é parecer jurídico, fora do escopo)"),
    (r"\b(?:licitude|legalidade|regularidade)\b[^.;\n]{0,40}?\b(?:confirmad|atestad|comprovad|demonstrad|assegurad|garantid)",
     "conclui que o tratamento é lícito ou regular (isso é parecer jurídico, fora do escopo)"),
    (r"\b(?:declaro|aprovo|aprovamos|aprova-se|homologo|homologa-se|autorizo)\b|\b(?:fica|ficam|est[aá]|est[aã]o)\s+aprovad[oa]s?\b",
     "fala como se fosse o controlador aprovando"),
    (r"\brisco\s+(?:[eé]\s+|ser[aá]\s+|fica\s+)?(?:zero|inexistente|nulo)\b|\briscos\s+(?:s[aã]o\s+)?(?:inexistentes|nulos)\b",
     "afirma risco zero"),
    (r"\b(?:n[aã]o|inexiste[m]?)\s+(?:h[aá]|restam?|existem?)?\s*(?:nenhum\s+)?riscos?\b(?![^.;\n]{0,25}\b(?:alto|altos|cr[ií]tico|cr[ií]ticos|residua))",
     "afirma risco zero"),
    (r"\b(100\s?%|totalmente)\s+segur", "promete segurança total"),
    (r"\bdispensad[oa]s?\s+(?:d[aeo]\s+(?:elabora[cç][aã]o\s+d[eo]\s+)?RIPD|da\s+elabora[cç][aã]o)\b"
     r"|\bdispensa(?:-se)?\s+(?:a\s+elabora[cç][aã]o\s+d[eo]\s+|o\s+)RIPD\b"
     r"|\bRIPD\s+(?:n[aã]o\s+(?:[eé]|ser[aá])\s+necess[aá]rio|[eé]\s+desnecess[aá]rio)"
     r"|\bn[aã]o\s+precisa(?:m)?\s+(?:de\s+|elaborar\s+|fazer\s+)?(?:o\s+|um\s+)?RIPD\b",
     "afirma dispensa de RIPD (a ANPD pode determinar a elaboração a qualquer tempo, art. 38)"),
]
# Negação que afasta o alerta: só a que modifica o próprio verbo ("não está", "não fica") ou um
# verbo de dizer logo antes ("não afirmamos que", "isso não significa que", "sem declarar que").
NEGA_VERBO = re.compile(r"(?:\bn[aã]o|\bnunca|\bnem)\s+(?:se\s+)?(?:(?:est[aá]|est[aã]o|fica|ficam|[eé]|s[aã]o|foi|ser[aá])\s+)?$", re.I)
_DIZER = r"(?:afirm\w*|declar\w*|signific\w*|garant\w*|conclu\w*|quer\s+dizer|diz\w*|dig\w*|escrev\w*|registr\w*)"
NEGA_DIZER = re.compile(r"(?:\b(?:n[aã]o|nunca|nem)\s+(?:se\s+)?(?:vou\s+|vamos\s+|devo\s+|deve\s+|pode(?:mos)?\s+|permite\s+|[eé]\s+poss[ií]vel\s+)?" + _DIZER
                        + r"|\bsem\s+(?:afirmar|declarar|concluir|dizer|escrever)"
                        + r"|\bnenhum[a]?\b[^.;:!?]{0,60}?\b" + _DIZER + r")"
                        + r"(?:\s+que\b|\s+[\"“'«]|\s+nem\b|\s+)[^.;:!?]{0,80}$", re.I)

RESTRITO_PUBLICA = [
    (r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])", "endereço IP"),
    (r"\bporta\s+\d{2,5}\b", "porta de rede"),
    (r"\bCVE-\d{4}-\d{3,}", "identificador de vulnerabilidade"),
    (r"\bsenhas?\b", "menção a senha"),
    (r"\b[\w-]+\.(?:intra|local|corp|lan)\b", "nome de host interno"),
    (r"\b(?:software|servidor|firmware|sistema operacional|banco de dados|apache|nginx|windows|linux|postgres\w*|mysql|oracle|java|php)\b[^\n]{0,30}?\bv?(?:ers[aã]o\s+)?\d+\.\d+", "versão de software"),
    (r"\b(usu[aá]rio|conta)\s+(admin|root|administrador)\b", "conta privilegiada"),
]
LEIS_OK = {"13.709/2018", "15.352/2026", "12.527/2011"}
LEIS_SO_NAO_VERIFICADO = {"15.211/2025"}
# Atos na base (normas.json, verificado=true). Órgão ausente = ANPD (é o caso do RIPD).
RES_OK = {"2/2022", "15/2024", "18/2024", "19/2024", "32/2026"}
DECRETOS_OK = {"10.046/2019"}
PORTARIAS_OK = {"9.511/2025"}
ENUNCIADOS_OK = {"1/2023"}
_ORGAO = r"(?:((?:[A-Z][\w-]*/)*[A-Z][\w-]*)\s+)?(?:n[ºo°.]\s*)?"
_NUM = r"(\d{1,3}(?:\.\d{3})*/\d{4})"
ATOS = [  # (rótulo, regex com grupos órgão e número, números aceitos, órgãos aceitos)
    ("Resolução", re.compile(r"\bRes(?:olu[cç][aã]o|\.)\s+" + _ORGAO + _NUM), RES_OK, {None, "CD/ANPD", "ANPD"}),
    ("Decreto", re.compile(r"\bDecreto(?:-Lei)?\s+()(?:n[ºo°.]\s*)?(\d{1,3}(?:\.\d{3})*(?:/\d{4}|,\s+de\s+\d{4})?)(?![\d.])"), DECRETOS_OK, set()),
    ("Portaria", re.compile(r"\bPortaria\s+" + _ORGAO + _NUM), PORTARIAS_OK, {"SGD/MGI"}),
    ("Enunciado", re.compile(r"\bEnunciado\s+" + _ORGAO + _NUM), ENUNCIADOS_OK, {None, "CD/ANPD", "ANPD"}),
    ("Instrução normativa", re.compile(r"\b(?:Instru[cç][aã]o\s+Normativa|IN)\s+" + _ORGAO + _NUM), set(), set()),
]
TETO_LINHA_TABELA = 2000
LINHA_RISCO = re.compile(r"\s*\|\s*[A-Z]?\d+\s*\|[^\n]{0,500}?\|\s*\d\s*\|\s*\d\s*\|")
JANELA = re.compile(r"(?:LGPD|Lei\s+(?:n[ºo°.]\s*)?13\.709(?:/2018)?)([^()\n;]{0,160})")
ARTS = re.compile(r"\barts?\.\s*((?:\d{1,2}(?:-[A-Z])?º?(?:\s*(?:,|e|a)\s*(?=\d))?)+)")


def artigos_lgpd(normas: dict) -> set[str]:
    ok = set()
    for it in normas["itens"]:
        if it["verificado"] and it["norma"].startswith("LGPD"):
            for grupo in ARTS.findall(it["dispositivo"]):
                ok.update(re.findall(r"\d{1,2}(?:-[A-Z])?", grupo))
    return ok


def atos_fora_da_base(linha: str) -> list[str]:
    """Atos normativos citados na linha que não estão na base verificada (ex.: 'Resolução nº 99/2025')."""
    fora = []
    for rotulo, rx, numeros, orgaos in ATOS:
        for m in rx.finditer(linha):
            orgao = m.group(1) or None
            num = re.sub(r",\s+de\s+", "/", m.group(2))
            if rotulo == "Decreto":
                orgao = None
                aceito = "-Lei" not in m.group(0) and (num in numeros or ("/" not in num and num in {x.split("/")[0] for x in numeros}))
            else:
                aceito = num in numeros and orgao in orgaos
            if not aceito:
                fora.append(m.group(0).strip())
    return fora


def secao(texto: str, padrao: str) -> str:
    """Texto do primeiro título que casa com o padrão até o próximo título de nível igual ou maior."""
    titulos = list(re.finditer(r"^(#{1,6})\s+(.*)$", texto, re.M))
    for i, m in enumerate(titulos):
        if re.search(padrao, m.group(2), re.I):
            fim = len(texto)
            for p in titulos[i + 1:]:
                if len(p.group(1)) <= len(m.group(1)):
                    fim = p.start()
                    break
            return texto[m.end():fim]
    return ""


def conferir(texto: str, modo: str = "integral") -> tuple[list[str], list[str]]:
    erros, avisos = [], []
    normas = carregar_normas()
    arts_ok = artigos_lgpd(normas)
    titulos = "\n".join(m.group(1) for m in re.finditer(r"^#{1,6}\s+(.*)$", texto, re.M))
    plano = sem_acento(texto)
    if not re.search(r"revis[aã]o humana|n[aã]o substitui", texto, re.I) or "minuta" not in plano:
        erros.append("falta o aviso final de minuta e revisão humana")
    if modo in ("integral", "publica"):
        for nome, rx in SECOES:
            if modo == "publica" and nome in PUBLICA_DISPENSA:
                continue
            if not re.search(rx, titulos, re.I):
                erros.append(f"falta a seção '{nome}' (references/modelo-de-saida.md)")
        princ = sem_acento(secao(texto, r"princ[ií]pios"))
        faltam = [p for p in PRINCIPIOS if p not in princ]
        if faltam:
            erros.append("análise dos princípios incompleta (art. 6º): faltam " + ", ".join(faltam))
    if modo == "integral":
        for rotulo, rx in (("tipos de dados", r"tipos de dados|dados pessoais e titulares|categorias de dados"), ("metodologia de coleta", r"metodologia[^\n]{0,80}coleta"),
                           ("metodologia de segurança", r"metodologia[^\n]{0,120}seguran|seguran[cç]a das informa"),
                           ("análise de medidas e salvaguardas", r"salvaguardas")):
            if not re.search(rx, texto, re.I):
                erros.append(f"conteúdo mínimo do art. 38, parágrafo único, não encontrado: {rotulo}")
        # Linha a linha, ancorado no início e com teto: custo linear mesmo sem tabela (C6).
        if not any(len(l) <= TETO_LINHA_TABELA and LINHA_RISCO.match(l) for l in texto.splitlines()):
            avisos.append("não encontrei tabela de riscos com probabilidade e impacto numéricos (scripts/matriz_risco.py)")
    for n, linha in enumerate(texto.splitlines(), 1):
        nv = "nao verificad" in sem_acento(linha)
        for m in JANELA.finditer(linha):
            for grupo in ARTS.findall(m.group(1)):
                for a in re.findall(r"\d{1,2}(?:-[A-Z])?", grupo):
                    if a not in arts_ok and not nv:
                        erros.append(f"linha {n}: LGPD, art. {a}, não está em references/normas.json como verificado")
        for lei in re.findall(r"\bLei\s+(?:n[ºo°.]\s*)?(\d{1,2}\.\d{3}/\d{4})", linha):
            if lei in LEIS_OK:
                continue
            if not nv:
                erros.append(f"linha {n}: Lei {lei} sem 'não verificado' (fora da base ou só com vigência conferida)")
        if not nv:
            for citado in atos_fora_da_base(linha):
                erros.append(f"linha {n}: {citado} fora da base verificada; marque 'não verificado'")
        for rx, motivo in PROIBIDO:
            for m in re.finditer(rx, linha, re.I):
                antes = linha[:m.start()]
                if NEGA_VERBO.search(antes) or NEGA_DIZER.search(antes):
                    continue
                erros.append(f"linha {n}: linguagem proibida: {motivo}")
                break
        if modo == "publica":
            for rx, motivo in RESTRITO_PUBLICA:
                if re.search(rx, linha, re.I):
                    erros.append(f"linha {n}: versão pública com {motivo} (informação crítica; mantenha só na versão integral)")
    for d in achar_dados_pessoais(texto):
        erros.append(f"linha {d['linha']}: dado pessoal ({d['tipo']}); o RIPD descreve categorias, não pessoas")
    if modo == "publica" and not re.search(r"omitid|suprimid|resumid", texto, re.I):
        erros.append("versão pública sem aviso de que informações foram omitidas ou resumidas")
    marcadores = re.findall(r"\[(PREENCHER|CONFERIR)[^\]]*\]", texto)
    if marcadores:
        avisos.append(f"restam {marcadores.count('PREENCHER')} [PREENCHER] e {marcadores.count('CONFERIR')} [CONFERIR] para a equipe")
    return erros, avisos


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("arquivo")
    ap.add_argument("--modo", choices=("integral", "publica", "parcial"), default="integral")
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
        print(f"{len(erros)} erro(s), {len(avisos)} aviso(s)")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
