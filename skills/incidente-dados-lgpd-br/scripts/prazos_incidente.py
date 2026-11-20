#!/usr/bin/env python3
"""Calcula os prazos da comunicação de incidente (Res. CD/ANPD 15/2024, arts. 6º, 9º e 10).

Uso:
    python3 scripts/prazos_incidente.py --conhecimento 18/11/2026
    python3 scripts/prazos_incidente.py --conhecimento 18/11/2026 --comunicacao-anpd 24/11/2026 \\
        --comunicacao-titulares 25/11/2026 --feriados 16/02/2026,17/02/2026 --hoje 20/11/2026 [--json]

"Conhecimento" é a data em que o controlador soube que o incidente afetou dados pessoais (art. 6º, § 1º).
Conta dias úteis excluindo o dia do começo e incluindo o do vencimento (Res. CD/ANPD 1/2021, art. 8º,
aplicada por analogia [CONFERIR]); exclui sábados, domingos e feriados nacionais fixos (20/11 só a partir
de 2024, Lei 14.759/2023). Dias sem expediente fora das leis federais de feriado (Carnaval, que não é
feriado em lei federal; Sexta-Feira da Paixão, feriado religioso municipal; Corpus Christi; feriados
estaduais, distritais e municipais, inclusive do DF, onde fica a sede da ANPD; dia de indisponibilidade
do peticionamento eletrônico) entram por --feriados (lista separada por vírgula ou arquivo com uma data
por linha). Prazos em dobro com --pequeno-porte (arts. 6º, § 8º, e 9º, § 6º), que não vale para pessoa
jurídica de direito público. Sem rede. Código de saída: 0 em dia; 1 algum prazo vencido sem
cumprimento; 3 erro de uso.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from _comum import dias_uteis_entre, fmt, ler_data, somar_dias_uteis


def dias(n: int) -> str:
    return "1 dia útil" if n == 1 else f"{n} dias úteis"


def ler_feriados(valor: str) -> set:
    if not valor:
        return set()
    p = Path(valor)
    itens = p.read_text(encoding="utf-8").split() if p.is_file() else valor.split(",")
    return {ler_data(x) for x in itens if x.strip()}


def calcular(conhecimento: dt.date, extras: set, pequeno=False, anpd=None, titulares=None, hoje=None) -> dict:
    f = 2 if pequeno else 1
    prazo = somar_dias_uteis(conhecimento, 3 * f, extras)
    linhas, alertas = [], []

    def item(nome, venc, feito, fundamento):
        st = "a cumprir"
        if feito:
            st = "cumprido no prazo" if feito <= venc else f"cumprido com atraso ({dias(dias_uteis_entre(venc, feito, extras))})"
        elif hoje:
            n = dias_uteis_entre(hoje, venc, extras)
            st = "VENCIDO" if hoje > venc else ("vence hoje" if n == 0 else f"{'falta' if n == 1 else 'faltam'} {dias(n)}")
        linhas.append({"obrigacao": nome, "vencimento": fmt(venc), "situacao": st, "fundamento": fundamento})
        return st

    s1 = item("Comunicar à ANPD (formulário no SEI!ANPD, pelo encarregado ou representante)", prazo, anpd,
              "Res. CD/ANPD 15/2024, art. 6º, caput e §§ 1º, 4º a 6º" + (", e § 8º" if pequeno else ""))
    s2 = item("Comunicar aos titulares (de forma direta e individualizada, caso seja possível identificá-los, e em linguagem simples)", prazo, titulares,
              "Res. CD/ANPD 15/2024, art. 9º, caput e § 1º, I e II" + (", e § 6º" if pequeno else ""))
    item("Juntar ao processo a declaração de comunicação aos titulares", somar_dias_uteis(prazo, 3, extras), None,
         "Res. CD/ANPD 15/2024, art. 9º, § 4º (três dias úteis do fim do prazo do caput)")
    if anpd:
        item("Complementar a comunicação à ANPD, se necessário, de forma fundamentada", somar_dias_uteis(anpd, 20 * f, extras), None,
             "Res. CD/ANPD 15/2024, art. 6º, § 3º" + (" e § 8º" if pequeno else ""))
    for st, quem, inc in ((s1, "à ANPD", "art. 6º, § 2º, V"), (s2, "aos titulares", "art. 9º, IV")):
        if "atraso" in st or st == "VENCIDO":
            alertas.append(f"Comunicação {quem} fora do prazo: informe os motivos da demora (Res. CD/ANPD 15/2024, {inc}).")
    alertas.append("Se a comunicação aos titulares for por divulgação pública (sítio eletrônico, aplicativos, mídias sociais, canais de atendimento), mantenha-a visível "
                   "por no mínimo três meses (art. 9º, § 3º).")
    alertas.append("Registro do incidente: guarda por no mínimo cinco anos, contados da data do registro (art. 10); para órgão público, esse prazo "
                   "cede às regras de guarda permanente da tabela de temporalidade própria ou do Conselho Nacional de Arquivos (art. 10, § 2º).")
    if pequeno:
        alertas.append("Prazos em dobro só para agente de tratamento de pequeno porte (Res. CD/ANPD 2/2022, art. 2º, I): "
                       "pessoa jurídica de direito público não consta da definição. Órgão público: refaça sem --pequeno-porte [CONFERIR].")
    if conhecimento.weekday() >= 5:
        alertas.append("O conhecimento ocorreu em fim de semana: confira com a assessoria jurídica o início da contagem [CONFERIR].")
    alertas.append("Res. CD/ANPD 15/2024 [CONFERIR vigência]: confirme a redação na data do uso. Sem expediente na sede da ANPD "
                   "ou com o peticionamento eletrônico indisponível, o prazo se prorroga (Res. CD/ANPD 1/2021, art. 8º, §§ 1º e 2º): "
                   "informe esses dias com --feriados.")
    vencido = any(l["situacao"] == "VENCIDO" for l in linhas)
    return {"conhecimento": fmt(conhecimento), "pequeno_porte": pequeno, "feriados_extras": sorted(fmt(d) for d in extras),
            "prazos": linhas, "alertas": alertas, "vencido": vencido}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--conhecimento", required=True)
    ap.add_argument("--comunicacao-anpd")
    ap.add_argument("--comunicacao-titulares")
    ap.add_argument("--feriados", default="")
    ap.add_argument("--pequeno-porte", action="store_true")
    ap.add_argument("--hoje")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        res = calcular(ler_data(a.conhecimento), ler_feriados(a.feriados), a.pequeno_porte,
                       ler_data(a.comunicacao_anpd) if a.comunicacao_anpd else None,
                       ler_data(a.comunicacao_titulares) if a.comunicacao_titulares else None,
                       ler_data(a.hoje) if a.hoje else None)
    except (OSError, ValueError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 3
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print(f"Conhecimento de que o incidente afetou dados pessoais: {res['conhecimento']}"
              + (" (agente de pequeno porte: prazos em dobro)" if a.pequeno_porte else ""))
        print("\n| Obrigação | Vence em | Situação | Fundamento |\n|---|---|---|---|")
        for l in res["prazos"]:
            print(f"| {l['obrigacao']} | {l['vencimento']} | {l['situacao']} | {l['fundamento']} |")
        print("\nAlertas:")
        for x in res["alertas"]:
            print(f"- {x}")
        print("- Contagem indicativa: exclui o dia do começo e inclui o do vencimento (Res. CD/ANPD 1/2021, art. 8º, por "
              "analogia [CONFERIR]); feriados nacionais fixos já excluídos" +
              (f"; extras: {', '.join(res['feriados_extras'])}" if res["feriados_extras"] else "; feriados móveis e locais não informados") + ".")
    return 1 if res["vencido"] else 0


if __name__ == "__main__":
    sys.exit(main())
