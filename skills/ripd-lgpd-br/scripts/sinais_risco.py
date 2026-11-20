#!/usr/bin/env python3
"""Rede de segurança: procura na descrição do tratamento sinais que o RIPD precisa enfrentar.

Uso:
    python3 scripts/sinais_risco.py DESCRICAO.md|-  [--json]

Para cada sinal (dados sensíveis; crianças, adolescentes e idosos; tecnologia emergente; vigilância
em zona pública; decisão automatizada; afetação de direitos; larga escala; compartilhamento com
privado; transferência internacional; segurança pública; incidente), mostra os termos achados, as
linhas e o dispositivo que obriga a tratar o ponto. Achar um termo não prova o critério: obriga a
responder à pergunta na triagem (scripts/triagem_alto_risco.py). Sem rede; não grava arquivos.
Código de saída: 0 nenhum sinal; 1 há sinais; 3 erro de uso.
"""
from __future__ import annotations

import argparse
import json
import sys

from _comum import achar_sinais, ler_texto

PERGUNTA = {
    "dados_sensiveis": "Há dado pessoal sensível (art. 5º, II)? Qual hipótese do art. 11 se aplica?",
    "criancas_adolescentes_idosos": "Há dados de crianças, adolescentes ou idosos? Como o melhor interesse (art. 14) foi considerado?",
    "tecnologia_emergente": "O tratamento usa tecnologia emergente ou inovadora (IA, biometria, reconhecimento facial)?",
    "vigilancia_zona_publica": "Há vigilância ou controle de espaço acessível ao público?",
    "decisao_automatizada": "Alguma decisão é tomada unicamente por meio automatizado? Como o titular pede revisão (art. 20)?",
    "afeta_direitos": "O tratamento pode impedir o exercício de direito ou o acesso a serviço, ou causar dano?",
    "larga_escala": "Quantos titulares, por quanto tempo, com que frequência e em que área geográfica?",
    "compartilhamento_privado": "Há operador ou compartilhamento com ente privado? Qual exceção do art. 27 ou do art. 26, § 1º?",
    "transferencia_internacional": "Os dados saem do país (inclusive nuvem)? Qual hipótese do art. 33 e qual mecanismo da Res. CD/ANPD 19/2024 [CONFERIR]?",
    "seguranca_publica": "O tratamento é para fins exclusivos de segurança pública ou investigação (art. 4º, III)? Se sim, regime próprio.",
    "incidente": "Há incidente de segurança em curso? Isso não se resolve no RIPD: acione o plano de incidentes (art. 48).",
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("arquivo")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        texto = ler_texto(a.arquivo)
    except OSError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 3
    sinais = achar_sinais(texto)
    if a.json:
        print(json.dumps(sinais, ensure_ascii=False, indent=1))
        return 1 if sinais else 0
    if not sinais:
        print("Nenhum sinal reconhecido pelos termos. Isso não afasta risco: responda à triagem mesmo assim.")
        return 0
    print("Sinais encontrados (responda a cada pergunta na triagem e no RIPD):")
    for nome, s in sinais.items():
        print(f"\n## {nome}\n- Fundamento: {s['criterio']}\n- Termos: {', '.join(s['trechos'])} (linhas {', '.join(map(str, s['linhas']))})\n- Pergunta: {PERGUNTA[nome]}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
