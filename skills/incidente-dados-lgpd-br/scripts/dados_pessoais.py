#!/usr/bin/env python3
"""Localiza (e, se pedido, mascara) dados pessoais em descrições, planilhas e comunicações de incidente.

Uso:
    python3 scripts/dados_pessoais.py ARQUIVO|-             # lista tipo e linha, nunca o dado
    python3 scripts/dados_pessoais.py ARQUIVO|- --mascarar  # imprime o texto com marcadores
    python3 scripts/dados_pessoais.py ARQUIVO --json

Procura CPF, NIS/PIS, Cartão Nacional de Saúde, e-mail, telefone, CEP, RG e data de nascimento.
E-mails @example.com/.org/.net são tratados como fictícios. Não reconhece nomes nem endereços
por extenso: a leitura humana continua necessária. Roda localmente, sem rede, e não grava arquivos.
Código de saída: 0 nada encontrado (ou --mascarar); 1 há ocorrências; 3 erro de uso.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter

from _comum import achar_dados_pessoais, ler_texto, mascarar


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("arquivo", help="arquivo de texto UTF-8 ou '-' para a entrada padrão")
    ap.add_argument("--mascarar", action="store_true", help="imprime o texto com os dados trocados por marcadores")
    ap.add_argument("--json", action="store_true", help="saída em JSON (tipo e linha)")
    a = ap.parse_args(argv)
    try:
        texto = ler_texto(a.arquivo)
    except OSError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 3
    if a.mascarar:
        sys.stdout.write(mascarar(texto))
        return 0
    achados = achar_dados_pessoais(texto)
    if a.json:
        print(json.dumps([{"tipo": x["tipo"], "linha": x["linha"]} for x in achados], ensure_ascii=False))
    elif not achados:
        print("Nenhum dado pessoal reconhecido pelos padrões. Leia o texto: nomes e endereços não são detectados.")
    else:
        print("Dados pessoais encontrados (o dado não é exibido):")
        for x in achados:
            print(f"- {x['tipo']} na linha {x['linha']}")
        cont = Counter(x["tipo"] for x in achados)
        print("Resumo: " + ", ".join(f"{k}: {v}" for k, v in cont.items()))
        print("Comunicações e registros descrevem categorias de dados e número de titulares, não pessoas. Remova ou use --mascarar.")
    return 1 if achados else 0


if __name__ == "__main__":
    sys.exit(main())
