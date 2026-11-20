#!/usr/bin/env python3
"""Confere respostas de um agente contra as asserções de evals/evals.json.

Uso:
    python3 rodar_evals.py PASTA_DE_SAIDAS [--casos evals.json] [--json]

Cada caso precisa de PASTA_DE_SAIDAS/<id>.md com a resposta completa do agente.
Asserções: contem, nao_contem, regex, nao_regex e conferir (roda scripts/conferir_comunicacao.py na
resposta, no modo indicado em "valor": anpd, titular, registro ou parcial). Com "secao", a asserção vale só
para o trecho sob o título que contém esse texto.
Código de saída: 0 tudo passou; 1 alguma asserção falhou ou faltou arquivo; 3 erro de uso.
As asserções são mecânicas: as "expectativas" de cada caso exigem leitura humana. Sem rede.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "scripts"))
from conferir_comunicacao import conferir  # noqa: E402  (script local, sem rede)

TITULO = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)


def secao(texto: str, nome: str) -> str | None:
    titulos = list(TITULO.finditer(texto))
    for i, m in enumerate(titulos):
        if nome.lower() in m.group(2).lower():
            nivel = len(m.group(1))
            fim = next((p.start() for p in titulos[i + 1:] if len(p.group(1)) <= nivel), len(texto))
            return texto[m.end():fim]
    return None


def checar(texto: str, a: dict) -> tuple[bool, str]:
    alvo = texto
    if a.get("secao"):
        alvo = secao(texto, a["secao"])
        if alvo is None:
            return False, f"seção '{a['secao']}' não encontrada"
    tipo, valor = a["tipo"], a["valor"]
    if tipo == "contem":
        return valor in alvo, ""
    if tipo == "nao_contem":
        return valor not in alvo, ""
    if tipo == "regex":
        return re.search(valor, alvo) is not None, ""
    if tipo == "nao_regex":
        return re.search(valor, alvo) is None, ""
    if tipo == "conferir":
        erros, _ = conferir(alvo, valor)
        return not erros, "; ".join(erros[:3])
    return False, f"tipo de asserção desconhecido: {tipo}"


def rodar(pasta: Path, casos_json: Path) -> dict:
    casos = json.loads(casos_json.read_text(encoding="utf-8"))["evals"]
    resultado = {"casos": [], "passou": 0, "falhou": 0}
    for c in casos:
        arq = pasta / f"{c['id']}.md"
        item = {"id": c["id"], "falhas": []}
        if not arq.is_file():
            item["falhas"].append(f"arquivo ausente: {arq.name}")
        else:
            texto = arq.read_text(encoding="utf-8")
            for a in c["assercoes"]:
                ok, info = checar(texto, a)
                if not ok:
                    item["falhas"].append(f"{a['tipo']} {a['valor']!r}" + (f": {info}" if info else ""))
        item["ok"] = not item["falhas"]
        resultado["passou" if item["ok"] else "falhou"] += 1
        resultado["casos"].append(item)
    return resultado


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pasta", type=Path)
    ap.add_argument("--casos", type=Path, default=AQUI / "evals.json")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if not a.pasta.is_dir():
        print(f"Pasta não encontrada: {a.pasta}", file=sys.stderr)
        return 3
    r = rodar(a.pasta, a.casos)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        for c in r["casos"]:
            print(("PASSOU " if c["ok"] else "FALHOU ") + c["id"])
            for f in c["falhas"]:
                print(f"    - {f}")
        p, f = r["passou"], r["falhou"]
        print(f"\n{p} {'passou' if p == 1 else 'passaram'}, {f} {'falhou' if f == 1 else 'falharam'}.")
    return 0 if r["falhou"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
