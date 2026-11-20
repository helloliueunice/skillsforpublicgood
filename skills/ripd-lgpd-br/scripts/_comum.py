"""Funções comuns aos scripts da skill ripd-lgpd-br.

Só biblioteca padrão. Nada aqui acessa a rede ou grava arquivos.
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SKILL = AQUI.parent
NORMAS = SKILL / "references" / "normas.json"


def ler_texto(caminho: str) -> str:
    """Lê arquivo UTF-8 (ou '-' para a entrada padrão)."""
    if caminho == "-":
        return sys.stdin.read()
    return Path(caminho).read_text(encoding="utf-8", errors="replace")


def ler_csv(caminho: str) -> list[dict]:
    """Lê CSV com separador ',' ou ';' (detectado pela primeira linha). Chaves em minúsculas."""
    texto = ler_texto(caminho)
    primeira = texto.splitlines()[0] if texto.strip() else ""
    sep = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.DictReader(io.StringIO(texto), delimiter=sep)
    linhas = []
    for n, linha in enumerate(leitor, 2):
        if None in linha:
            raise ValueError(f"linha {n}: mais colunas que o cabeçalho; ponha entre aspas o campo que contém '{sep}'")
        linhas.append({(k or "").strip().lower(): (v or "").strip() for k, v in linha.items()})
    return linhas


def sem_acento(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn").lower()


def carregar_normas() -> dict:
    return json.loads(NORMAS.read_text(encoding="utf-8"))


# --- Dados pessoais -------------------------------------------------------------------------
# Quantificadores limitados e âncoras de dígito: tempo linear mesmo em textos longos.
PADROES_DADOS = [
    ("CPF", re.compile(r"(?<!\d)\d{3}\.\d{3}\.\d{3}-\d{2}(?!\d)")),
    ("CPF ou NIS (11 dígitos)", re.compile(r"(?<![\d./-])\d{11}(?![\d./-])")),
    ("NIS/PIS", re.compile(r"(?<!\d)\d{3}\.\d{5}\.\d{2}-\d(?!\d)")),
    ("Cartão Nacional de Saúde", re.compile(r"(?<!\d)[1-9]\d{2} ?\d{4} ?\d{4} ?\d{4}(?!\d)")),
    ("e-mail", re.compile(r"[A-Za-z0-9._%+-]{1,64}@[A-Za-z0-9-]{1,63}(?:\.[A-Za-z0-9-]{1,63}){0,4}\.[A-Za-z]{2,24}")),
    ("telefone", re.compile(r"(?<![\d/])(?:\+55 ?)?\(?\d{2}\)? ?9?\d{4}[- ]?\d{4}(?![\d/])")),
    ("CEP", re.compile(r"(?<!\d)\d{5}-\d{3}(?!\d)")),
    ("RG", re.compile(r"\bRG\b[:\s nº°.]{0,6}[\dXx][\d.\-Xx]{4,13}")),
    ("data de nascimento", re.compile(r"(?i)(?:nascid[oa] em|data de nascimento:?|nasc\.:?)\s{0,3}\d{1,2}/\d{1,2}/\d{2,4}")),
]
DOMINIOS_FICTICIOS = ("example.com", "example.org", "example.net")


def achar_dados_pessoais(texto: str) -> list[dict]:
    """Lista {tipo, linha, inicio, fim}. Ignora e-mails @example.* (fictícios por convenção)."""
    achados, ocupados = [], []
    for tipo, rx in PADROES_DADOS:
        if tipo == "e-mail" and "@" not in texto:
            continue
        for m in rx.finditer(texto):
            if tipo == "e-mail" and m.group(0).lower().endswith(DOMINIOS_FICTICIOS):
                continue
            if any(m.start() < f and m.end() > i for i, f in ocupados):
                continue
            ocupados.append((m.start(), m.end()))
            achados.append({"tipo": tipo, "linha": texto.count("\n", 0, m.start()) + 1,
                            "inicio": m.start(), "fim": m.end()})
    return sorted(achados, key=lambda x: x["inicio"])


def mascarar(texto: str) -> str:
    partes, pos = [], 0
    for a in achar_dados_pessoais(texto):
        partes.append(texto[pos:a["inicio"]])
        partes.append(f"[{a['tipo'].upper()} REMOVIDO]")
        pos = a["fim"]
    partes.append(texto[pos:])
    return "".join(partes)


# --- Sinais de risco (rede de segurança determinística) ------------------------------------
# Cada sinal aponta o ponto da LGPD que o RIPD precisa tratar ou o critério de alto risco do art. 4º
# da Res. CD/ANPD 2/2022. Essa resolução é regulamento de agentes de pequeno porte; para órgão
# público, a ANPD indica usá-la só como parâmetro, no que couber: por isso a marca [CONFERIR].
# Encontrar a palavra não prova nada: só obriga a responder à pergunta.
_PARAM = "parâmetro indicado pela ANPD: Res. CD/ANPD 2/2022, art. 4º, "  # orientação, não fundamento legal
SINAIS = {
    "dados_sensiveis": {
        "criterio": "LGPD, art. 5º, II, e art. 11; critério específico d (dados sensíveis), " + _PARAM + "II, d [CONFERIR]",
        "termos": ["saude", "doenca", "cid-10", "cid 10", "prontuario", "laudo", "deficiencia", "raca", "cor/raca",
                   "etnia", "etnico", "indigena", "quilombola", "religi", "opiniao politica", "filiacao partidaria",
                   "sindica", "vida sexual", "orientacao sexual", "genetic", "biometri", "impressao digital",
                   "reconhecimento facial", "biometria facial", "hiv", "gestante", "gravidez"],
    },
    "criancas_adolescentes_idosos": {
        "criterio": "LGPD, art. 14; critério específico d (crianças, adolescentes e idosos), " + _PARAM + "II, d [CONFERIR]",
        "termos": ["crianca", "adolescente", "menor de idade", "menores de 18", "estudante", "aluno", "aluna",
                   "creche", "escola", "matricula escolar", "idoso", "idosa", "pessoa idosa", "60 anos", "eca"],
    },
    "tecnologia_emergente": {
        "criterio": "critério específico a (tecnologias emergentes ou inovadoras), " + _PARAM + "II, a [CONFERIR]",
        "termos": ["inteligencia artificial", " ia ", "ia generativa", "aprendizado de maquina", "machine learning",
                   "modelo de linguagem", "llm", "chatbot", "reconhecimento facial", "visao computacional",
                   "blockchain", "internet das coisas", "iot", "algoritmo"],
    },
    "vigilancia_zona_publica": {
        "criterio": "critério específico b (vigilância ou controle de zonas acessíveis ao público), " + _PARAM + "II, b [CONFERIR]",
        "termos": ["camera", "cftv", "videomonitoramento", "monitoramento por video", "via publica", "praca",
                   "estacao", "terminal", "rodoviaria", "aeroporto", "parque", "vigilancia", "cerco eletronico",
                   "leitura de placas", "lpr"],
    },
    "decisao_automatizada": {
        "criterio": "LGPD, art. 20; critério específico c (decisões unicamente automatizadas), " + _PARAM + "II, c [CONFERIR]",
        "termos": ["automaticamente", "automatica", "automatizad", "score", "pontuacao", "ranqueamento",
                   "ranking", "classificacao de risco", "perfilamento", "perfil do", "elegibilidade", "triagem automatica",
                   "sem intervencao humana", "indeferimento automatico"],
    },
    "afeta_direitos": {
        "criterio": "critério geral b (afetar significativamente interesses e direitos fundamentais), " + _PARAM + "I, b, e § 2º [CONFERIR]",
        "termos": ["beneficio", "auxilio", "bolsa", "indeferi", "negativa", "bloqueio", "suspensao", "cancelamento",
                   "acesso ao servico", "vaga", "matricula", "fiscalizacao", "sancao", "multa", "fraude", "credito",
                   "emprego", "selecao", "discrimina"],
    },
    "larga_escala": {
        "criterio": "critério geral a (larga escala), " + _PARAM + "I, a, e § 1º [CONFERIR]",
        "termos": ["milhoes", "milhao", "mil titulares", "mil pessoas", "mil alunos", "mil usuarios", "toda a populacao",
                   "todos os cidadaos", "todo o estado", "todo o municipio", "nacional", "cadastro unico", "cadunico"],
    },
    "compartilhamento_privado": {
        "criterio": "LGPD, arts. 26 e 27 (uso compartilhado do Poder Público com entes privados) e art. 39 (operador); "
                    "entre órgãos federais, Decreto 10.046/2019 [CONFERIR]",
        "termos": ["empresa contratada", "contratada", "fornecedor", "operador", "terceirizad", "parceiro privado",
                   "convenio", "nuvem", "cloud", "saas", "plataforma privada", "banco conveniado"],
    },
    "transferencia_internacional": {
        "criterio": "LGPD, art. 33 (transferência internacional); regulamento da ANPD: Res. CD/ANPD 19/2024 e, para a "
                    "União Europeia, Res. CD/ANPD 32/2026 [CONFERIR]",
        "termos": ["exterior", "fora do brasil", "estados unidos", "eua", "europa", "servidor internacional",
                   "regiao us-", "us-east", "datacenter estrangeiro", "transferencia internacional"],
    },
    "seguranca_publica": {
        "criterio": "LGPD, art. 4º, III, e § 3º (segurança pública, defesa, investigação: regime próprio; a ANPD deve solicitar RIPD)",
        "termos": ["seguranca publica", "policia", "investigacao criminal", "inteligencia policial", "defesa nacional",
                   "seguranca do estado", "repressao", "infracao penal"],
    },
    "incidente": {
        "criterio": "LGPD, art. 48 (incidente de segurança): fora do escopo do RIPD; acionar o plano de resposta a incidentes. "
                    "A ANPD pode pedir o RIPD no processo do incidente (Res. CD/ANPD 15/2024, art. 8º) [CONFERIR]",
        "termos": ["vazamento", "vazou", "incidente de seguranca", "invasao", "ransomware", "acesso indevido"],
    },
}


def _ocorrencia(termo: str, linha: str) -> int:
    """Posição do termo no início de uma palavra ("raca" casa "raca", não "praca"), ou -1.

    Termo com espaço no fim (" ia ") é palavra inteira: casa "IA", não "iam" nem "ianomâmi".
    """
    inteira = termo.endswith(" ")
    termo = termo.strip()
    pos = linha.find(termo)
    while pos != -1:
        fim = pos + len(termo)
        if (pos == 0 or not linha[pos - 1].isalnum()) and (not inteira or fim >= len(linha) or not linha[fim].isalnum()):
            return pos
        pos = linha.find(termo, pos + 1)
    return -1


def _inicio_de_palavra(termo: str, linha: str) -> bool:
    return _ocorrencia(termo, linha) != -1


def achar_sinais(texto: str) -> dict:
    """Devolve {sinal: {criterio, termos, trechos, linhas}} só para os sinais presentes.

    'termos' são os termos da lista (sem acento); 'trechos', o que está escrito no texto (com acento).
    """
    originais = texto.splitlines()
    linhas = [" " + sem_acento(l) + " " for l in originais]
    res = {}
    for nome, s in SINAIS.items():
        achados, trechos, onde = set(), {}, set()
        for i, l in enumerate(linhas, 1):
            for t in s["termos"]:
                pos = _ocorrencia(t, l)
                if pos == -1:
                    continue
                achados.add(t.strip())
                onde.add(i)
                orig = originais[i - 1]
                trecho = t.strip()
                if len(l) == len(orig) + 2:  # mesma contagem de caracteres: dá para recortar o original
                    trecho = orig[pos - 1:pos - 1 + len(t.strip())].lower()
                trechos.setdefault(trecho, None)
        if achados:
            res[nome] = {"criterio": s["criterio"], "termos": sorted(achados), "trechos": sorted(trechos),
                         "linhas": sorted(onde)}
    return res
