#!/usr/bin/env python3
"""Triagem da necessidade do RIPD pelos critérios de alto risco indicados pela ANPD como parâmetro.

Uso:
    python3 scripts/triagem_alto_risco.py RESPOSTAS.json [--json]
    python3 scripts/triagem_alto_risco.py --sim larga_escala,sensiveis_ou_vulneraveis --nao vigilancia_zona_publica
    python3 scripts/triagem_alto_risco.py --modelo          # imprime um RESPOSTAS.json vazio

Critérios gerais: larga_escala, afeta_direitos. Critérios específicos: tecnologia_emergente,
vigilancia_zona_publica, decisao_automatizada, sensiveis_ou_vulneraveis.
Sétimo item: outro_fator_alto_risco (true/false), porque, segundo a ANPD, os critérios não são
exaustivos e o controlador pode identificar alto risco em outras situações.
Outros campos: motivo_anpd (art38, art32, art10, art4 ou vazio), seguranca_publica_exclusiva,
orgao_sisp_federal (true/false; o órgão ou entidade integra o SISP), criancas_adolescentes
(true/false). Valor null = não informado.

Os critérios vêm do art. 4º do regulamento anexo à Res. CD/ANPD 2/2022, que é regulamento de
agentes de tratamento de pequeno porte. Para órgão público, a ANPD indica usá-lo só como parâmetro,
no que couber, enquanto não houver regulamento de RIPD [CONFERIR]. Há alto risco quando o
tratamento atende a pelo menos um critério geral e a pelo menos um critério específico. Dois ou
mais fatores sem essa combinação: RIPD recomendado como boa prática (Guia de RIPD do PPSI 2.0,
seção 3.1). O resultado é apoio à decisão: quem decide é o controlador, com o encarregado.
Sem rede; não grava arquivos.
Código de saída: 0 resultado; 2 faltam respostas que podem mudar o resultado; 3 erro de uso.
"""
from __future__ import annotations

import argparse
import json
import sys

GERAIS = {
    "larga_escala": "tratamento em larga escala (art. 4º, I, a, e § 1º)",
    "afeta_direitos": "pode afetar significativamente interesses e direitos fundamentais (art. 4º, I, b, e § 2º)",
}
ESPECIFICOS = {
    "tecnologia_emergente": "uso de tecnologias emergentes ou inovadoras (art. 4º, II, a)",
    "vigilancia_zona_publica": "vigilância ou controle de zonas acessíveis ao público (art. 4º, II, b)",
    "decisao_automatizada": "decisões tomadas unicamente com base em tratamento automatizado (art. 4º, II, c)",
    "sensiveis_ou_vulneraveis": "dados sensíveis ou de crianças, adolescentes e idosos (art. 4º, II, d)",
}
OUTRO = "outro_fator_alto_risco"
MOTIVOS = {
    "art38": "a ANPD determinou a elaboração (LGPD, art. 38)",
    "art32": "a ANPD solicitou a publicação ao Poder Público (LGPD, art. 32)",
    "art10": "a ANPD solicitou o RIPD de tratamento baseado em legítimo interesse (LGPD, art. 10, § 3º)",
    "art4": "a ANPD solicitou o RIPD de tratamento de segurança pública ou investigação (LGPD, art. 4º, § 3º)",
}


def modelo() -> dict:
    return {"criterios_gerais": {k: None for k in GERAIS}, "criterios_especificos": {k: None for k in ESPECIFICOS},
            OUTRO: None,
            "justificativas": {k: "" for k in list(GERAIS) + list(ESPECIFICOS) + [OUTRO]},
            "motivo_anpd": None, "seguranca_publica_exclusiva": None, "orgao_sisp_federal": None,
            "criancas_adolescentes": None}


def _rotulo(singular: str, plural: str, itens: list[str]) -> str:
    return f"{plural if len(itens) > 1 else singular}: {'; '.join(itens)}."


def avaliar(r: dict) -> dict:
    g = r.get("criterios_gerais", {}) or {}
    e = r.get("criterios_especificos", {}) or {}
    for k in list(g) + list(e):
        if k not in GERAIS and k not in ESPECIFICOS:
            raise ValueError(f"critério desconhecido: {k}")
    g_sim = [k for k in GERAIS if g.get(k) is True]
    e_sim = [k for k in ESPECIFICOS if e.get(k) is True]
    g_nd = [k for k in GERAIS if g.get(k) is None]
    e_nd = [k for k in ESPECIFICOS if e.get(k) is None]
    alto = bool(g_sim and e_sim)
    outro = r.get(OUTRO)
    pendentes = []
    if not alto:
        if not g_sim and g_nd and (e_sim or e_nd):
            pendentes += g_nd
        if not e_sim and e_nd and (g_sim or g_nd):
            pendentes += e_nd
        if outro is None:
            pendentes.append(OUTRO)
    fatores = len(g_sim) + len(e_sim)
    motivo = r.get("motivo_anpd") or None
    if motivo and motivo not in MOTIVOS:
        raise ValueError(f"motivo_anpd inválido: {motivo} (use {', '.join(MOTIVOS)})")
    conclusoes, notas = [], []
    if motivo:
        conclusoes.append(f"RIPD EXIGÍVEL: {MOTIVOS[motivo]}.")
    if alto:
        conclusoes.append("RIPD RECOMENDADO: alto risco pelo art. 4º da Res. CD/ANPD 2/2022, usado como parâmetro indicado "
                          "pela ANPD (a resolução é regulamento de agentes de pequeno porte; para órgão público, vale só como "
                          "parâmetro, no que couber) [CONFERIR]. "
                          + _rotulo("Critério geral", "Critérios gerais", [GERAIS[k] for k in g_sim]) + " "
                          + _rotulo("Critério específico", "Critérios específicos", [ESPECIFICOS[k] for k in e_sim]))
    elif outro is True:
        conclusoes.append("RIPD RECOMENDADO: alto risco por outro fator identificado pelo controlador. Segundo a ANPD, os "
                          "critérios do art. 4º não são exaustivos [CONFERIR]. Descreva o fator na justificativa.")
    elif fatores >= 2:
        conclusoes.append("RIPD RECOMENDADO COMO BOA PRÁTICA: dois ou mais fatores sem a combinação geral + específico "
                          "(Guia para Elaboração de RIPD do PPSI 2.0, seção 3.1).")
    elif pendentes:
        conclusoes.append("NÃO VERIFICÁVEL: faltam respostas que podem caracterizar alto risco.")
    elif not motivo:
        conclusoes.append("ALTO RISCO NÃO CARACTERIZADO pelos critérios informados. Esses critérios não são exaustivos: "
                          "segundo a ANPD, o controlador pode verificar alto risco em situações diferentes das indicadas "
                          "[CONFERIR]. Registre a análise e a justificativa. Isso não dispensa nada: a ANPD pode determinar o RIPD a qualquer tempo (LGPD, art. 38), o registro das "
                          "operações continua obrigatório (art. 37) e o controlador pode elaborar o RIPD por decisão própria "
                          "(art. 6º, X, e art. 50, § 2º, I, d). Refaça a triagem se o tratamento mudar.")
    if r.get("seguranca_publica_exclusiva") is True:
        notas.append("Fins exclusivos de segurança pública, defesa, segurança do Estado ou investigação: a LGPD remete a "
                     "legislação específica (art. 4º, III, e § 1º) e a ANPD deve solicitar RIPD (art. 4º, § 3º). [CONFERIR] com a assessoria jurídica.")
    if r.get("orgao_sisp_federal") is True:
        notas.append("Órgão ou entidade do SISP: o PPSI 2.0 (Portaria SGD/MGI 9.511/2025) prevê o RIPD na medida 23.3 da sua "
                     "estrutura de controles (quadro de medidas do Modelo de RIPD do PPSI 2.0); use o Modelo como formato de entrega.")
    elif r.get("orgao_sisp_federal") is False:
        notas.append("Fora do SISP: o PPSI 2.0 serve como referência, não como obrigação.")
    if "sensiveis_ou_vulneraveis" in e_sim:
        notas.append("Se houver dado sensível: só com hipótese do art. 11 da LGPD; nos casos do art. 11, II, a e b, o órgão "
                     "dá publicidade à dispensa de consentimento (art. 11, § 2º).")
        crian = r.get("criancas_adolescentes")
        if crian is not False:
            notas.append(("Dados de crianças e adolescentes" if crian is True else "Se houver dados de crianças ou adolescentes")
                         + ": melhor interesse (LGPD, art. 14; Enunciado CD/ANPD 1/2023). "
                         "ECA Digital (Lei 15.211/2025, vigente desde 17/03/2026): artigos não verificados por esta skill.")
    notas.append("Resultado de apoio: a decisão e a aprovação do RIPD são do controlador, com assistência do encarregado "
                 "(Res. CD/ANPD 18/2024, art. 16, III, como orientação sobre o papel do encarregado) [CONFERIR].")
    return {"alto_risco": alto, "fatores": fatores, "gerais": g_sim, "especificos": e_sim,
            "pendentes": pendentes, "conclusoes": conclusoes, "notas": notas,
            "justificativas_faltando": [k for k in g_sim + e_sim + ([OUTRO] if outro is True else [])
                                        if not (r.get("justificativas") or {}).get(k)]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("respostas", nargs="?")
    ap.add_argument("--sim", default="", help="critérios presentes, separados por vírgula")
    ap.add_argument("--nao", default="", help="critérios ausentes, separados por vírgula")
    ap.add_argument("--motivo-anpd", default=None)
    ap.add_argument("--modelo", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.modelo:
        print(json.dumps(modelo(), ensure_ascii=False, indent=1))
        return 0
    try:
        if a.respostas:
            with open(a.respostas, encoding="utf-8") as f:
                r = json.load(f)
        else:
            r = modelo()
            for lista, valor in ((a.sim, True), (a.nao, False)):
                for k in filter(None, (x.strip() for x in lista.split(","))):
                    if k in (OUTRO, "outro_fator"):
                        r[OUTRO] = valor
                        continue
                    alvo = "criterios_gerais" if k in GERAIS else "criterios_especificos" if k in ESPECIFICOS else None
                    if not alvo:
                        raise ValueError(f"critério desconhecido: {k}")
                    r[alvo][k] = valor
            r["motivo_anpd"] = a.motivo_anpd
        res = avaliar(r)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 3
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print("# Triagem da necessidade do RIPD\n")
        for c in res["conclusoes"]:
            print(f"- **{c}**")
        if res["pendentes"]:
            print("\nResponda antes de concluir: " + ", ".join(res["pendentes"]))
        if res["justificativas_faltando"]:
            print("\nFalta justificativa para: " + ", ".join(res["justificativas_faltando"]))
        print("\nNotas:")
        for n in res["notas"]:
            print(f"- {n}")
    return 2 if res["pendentes"] else 0


if __name__ == "__main__":
    sys.exit(main())
