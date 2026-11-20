"""Funções comuns aos scripts da skill incidente-dados-lgpd-br.

Só biblioteca padrão. Nada aqui acessa a rede ou grava arquivos.
"""
from __future__ import annotations

import datetime as dt
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


def sem_acento(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn").lower()


def carregar_normas() -> dict:
    return json.loads(NORMAS.read_text(encoding="utf-8"))


# --- Datas e dias úteis ---------------------------------------------------------------------
# Feriados nacionais fixos: Lei 662/1949 (redação da Lei 10.607/2002), Lei 6.802/1980 e
# Lei 14.759/2023, conferidas no Planalto em 20/11/2026. O 20/11 é feriado nacional só a partir de 2024
# (Lei 14.759, de 21/12/2023). Dias sem expediente fora das leis federais de feriado (Carnaval, Sexta-Feira
# da Paixão, Corpus Christi, feriados estaduais, distritais e municipais) entram por --feriados.
FERIADOS_FIXOS = {(1, 1), (21, 4), (1, 5), (7, 9), (12, 10), (2, 11), (15, 11), (25, 12)}
FERIADOS_DESDE = {(20, 11): 2024}


def eh_feriado_nacional(d: dt.date) -> bool:
    if (d.day, d.month) in FERIADOS_FIXOS:
        return True
    ano = FERIADOS_DESDE.get((d.day, d.month))
    return ano is not None and d.year >= ano


def ler_data(texto: str) -> dt.date:
    """Aceita dd/mm/aaaa ou aaaa-mm-dd."""
    texto = texto.strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(texto, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"data inválida: {texto!r} (use dd/mm/aaaa)")


def fmt(d: dt.date) -> str:
    return d.strftime("%d/%m/%Y")


def eh_util(d: dt.date, extras: set) -> bool:
    return d.weekday() < 5 and not eh_feriado_nacional(d) and d not in extras


def somar_dias_uteis(inicio: dt.date, n: int, extras: set) -> dt.date:
    """Exclui o dia do começo e inclui o do vencimento (Res. CD/ANPD 1/2021, art. 8º)."""
    d, contados = inicio, 0
    while contados < n:
        d += dt.timedelta(days=1)
        if eh_util(d, extras):
            contados += 1
    return d


def dias_uteis_entre(inicio: dt.date, fim: dt.date, extras: set) -> int:
    """Dias úteis depois de 'inicio' até 'fim', inclusive."""
    n, d = 0, inicio
    while d < fim:
        d += dt.timedelta(days=1)
        if eh_util(d, extras):
            n += 1
    return n


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
TIPOS_FEMININOS = {"data de nascimento"}


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
        sufixo = "REMOVIDA" if a["tipo"] in TIPOS_FEMININOS else "REMOVIDO"
        partes.append(f"[{a['tipo'].upper()} {sufixo}]")
        pos = a["fim"]
    partes.append(texto[pos:])
    return "".join(partes)


