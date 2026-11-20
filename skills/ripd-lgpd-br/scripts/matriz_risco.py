#!/usr/bin/env python3
"""Calcula o nível dos riscos do RIPD (probabilidade × impacto) e aponta o que exige decisão.

Uso:
    python3 scripts/matriz_risco.py RISCOS.csv [--faixas 3,6,12] [--escala 5] [--json]

Colunas do CSV (',' ou ';'): id, risco, probabilidade, impacto, medidas,
probabilidade_residual, impacto_residual, responsavel, prazo. As duas colunas residuais são opcionais.

Nível = probabilidade × impacto, cada um de 1 a --escala (padrão 5). Faixas padrão: as de exemplo
do Modelo de RIPD do PPSI 2.0 (SGD/MGI, Tabela 11, "níveis de risco"; a Tabela 10 é a matriz),
usadas como referência, com crédito: pequeno até 3, moderado até 6, alto até 12, crítico acima.
Use as faixas da metodologia do seu órgão em --faixas (três limites crescentes).
O impacto é sobre o TITULAR, não sobre o órgão. O script avisa quando um risco com dado sensível,
de criança ou decisão automatizada recebeu impacto baixo, e quando risco alto ou crítico não tem
medida, responsável ou prazo. Sem rede; não grava arquivos.
Código de saída: 0 sem pendências; 1 há pendências ou risco residual alto/crítico; 3 erro de entrada.
"""
from __future__ import annotations

import argparse
import json
import sys

from _comum import ler_csv, sem_acento

FAIXAS_NOMES = ("pequeno", "moderado", "alto", "crítico")
SENSIVEL = ("sensive", "saude", "biometri", "crianca", "adolescente", "idoso", "automatizad", "discrimina", "facial", "raca", "religi")


def faixa(nivel: int, limites: tuple[int, int, int]) -> str:
    for nome, lim in zip(FAIXAS_NOMES, limites):
        if nivel <= lim:
            return nome
    return FAIXAS_NOMES[3]


def inteiro(v: str, campo: str, escala: int, linha: int, obrigatorio=True) -> int | None:
    if not v:
        if obrigatorio:
            raise ValueError(f"linha {linha}: '{campo}' vazio")
        return None
    try:
        n = int(v)
    except ValueError as exc:
        raise ValueError(f"linha {linha}: '{campo}' deve ser inteiro de 1 a {escala} (recebido {v!r})") from exc
    if not 1 <= n <= escala:
        raise ValueError(f"linha {linha}: '{campo}' fora da escala 1 a {escala} (recebido {n})")
    return n


def calcular(linhas: list[dict], limites=(3, 6, 12), escala=5) -> dict:
    if not (limites[0] < limites[1] < limites[2] < escala * escala):
        raise ValueError("--faixas precisa de três limites crescentes, menores que escala²")
    riscos, pendencias = [], []
    for i, l in enumerate(linhas, 2):
        rid = l.get("id") or f"R{i - 1}"
        if not l.get("risco"):
            raise ValueError(f"linha {i}: coluna 'risco' vazia")
        p = inteiro(l.get("probabilidade", ""), "probabilidade", escala, i)
        im = inteiro(l.get("impacto", ""), "impacto", escala, i)
        pr = inteiro(l.get("probabilidade_residual", ""), "probabilidade_residual", escala, i, False)
        ir = inteiro(l.get("impacto_residual", ""), "impacto_residual", escala, i, False)
        n = p * im
        r = {"id": rid, "risco": l["risco"], "probabilidade": p, "impacto": im, "nivel": n,
             "faixa": faixa(n, limites), "medidas": l.get("medidas", ""), "responsavel": l.get("responsavel", ""),
             "prazo": l.get("prazo", "")}
        if bool(pr) != bool(ir):
            pendencias.append(f"{rid}: só uma das colunas residuais foi preenchida (probabilidade_residual e "
                              "impacto_residual vão juntas); o residual não foi calculado")
        if pr and ir:
            r["nivel_residual"] = pr * ir
            r["faixa_residual"] = faixa(pr * ir, limites)
            if pr * ir > n:
                pendencias.append(f"{rid}: risco residual maior que o inerente; revise as notas")
        texto = sem_acento(l["risco"] + " " + l.get("medidas", ""))
        if im <= 2 and any(s in texto for s in SENSIVEL):
            pendencias.append(f"{rid}: impacto {im} parece baixo para dado sensível, de criança/adolescente/idoso ou decisão automatizada; "
                              "o impacto é medido sobre o titular")
        if r["faixa"] in ("alto", "crítico"):
            if not r["medidas"]:
                pendencias.append(f"{rid}: risco {r['faixa']} sem medida de tratamento")
            if not r["responsavel"] or not r["prazo"]:
                pendencias.append(f"{rid}: risco {r['faixa']} sem responsável ou prazo")
            if "nivel_residual" not in r:
                pendencias.append(f"{rid}: risco {r['faixa']} sem avaliação residual (probabilidade_residual e impacto_residual)")
        if r.get("faixa_residual") in ("alto", "crítico"):
            pendencias.append(f"{rid}: risco residual {r['faixa_residual']}: exige decisão fundamentada do controlador "
                              "(prosseguir com justificativa, mudar o tratamento ou não prosseguir)")
        riscos.append(r)
    if not riscos:
        raise ValueError("nenhum risco no CSV")
    return {"faixas": dict(zip(FAIXAS_NOMES, (f"até {limites[0]}", f"{limites[0] + 1} a {limites[1]}",
                                               f"{limites[1] + 1} a {limites[2]}", f"acima de {limites[2]}"))),
            "riscos": sorted(riscos, key=lambda x: -x["nivel"]), "pendencias": pendencias}


def tabela(res: dict) -> str:
    out = ["| ID | Risco ao titular | P | I | Nível | Faixa | Residual | Medidas | Responsável | Prazo |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in res["riscos"]:
        resid = f"{r['nivel_residual']} ({r['faixa_residual']})" if "nivel_residual" in r else "—"
        out.append(f"| {r['id']} | {r['risco']} | {r['probabilidade']} | {r['impacto']} | {r['nivel']} | {r['faixa']} | "
                   f"{resid} | {r['medidas'] or '[PREENCHER]'} | {r['responsavel'] or '[PREENCHER]'} | {r['prazo'] or '[PREENCHER]'} |")
    out.append("")
    out.append("Faixas usadas: " + "; ".join(f"{k} {v}" for k, v in res["faixas"].items()) + ".")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv")
    ap.add_argument("--faixas", default="3,6,12")
    ap.add_argument("--escala", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        limites = tuple(int(x) for x in a.faixas.split(","))
        if len(limites) != 3:
            raise ValueError("--faixas precisa de exatamente três números")
        res = calcular(ler_csv(a.csv), limites, a.escala)
    except (OSError, ValueError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 3
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print(tabela(res))
        if res["pendencias"]:
            print("\nPendências:")
            for p in res["pendencias"]:
                print(f"- {p}")
    return 1 if res["pendencias"] else 0


if __name__ == "__main__":
    sys.exit(main())
