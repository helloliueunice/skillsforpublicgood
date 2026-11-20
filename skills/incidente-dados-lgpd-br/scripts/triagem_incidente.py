#!/usr/bin/env python3
"""Triagem: o incidente precisa ser comunicado à ANPD e aos titulares (LGPD, art. 48; Res. CD/ANPD 15/2024)?

Uso:
    python3 scripts/triagem_incidente.py --modelo > respostas.json   # modelo para preencher
    python3 scripts/triagem_incidente.py respostas.json [--json]

Respostas: true, false ou null (não se sabe ainda). A regra é a do art. 5º do Regulamento da
Res. CD/ANPD 15/2024: o incidente pode afetar significativamente interesses e direitos fundamentais
E envolve pelo menos um dos seis critérios. O resultado é apoio: quem decide é o controlador, com
assistência do encarregado; a saída é um indicativo, nunca a decisão. Sem rede. Código de saída: 0 conclusão; 2 faltam respostas; 3 erro de uso.
"""
from __future__ import annotations

import argparse
import json
import sys

from _comum import ler_texto

CRITERIOS = {
    "sensiveis": "dados pessoais sensíveis (art. 5º, I)",
    "criancas_adolescentes_idosos": "dados de crianças, de adolescentes ou de idosos (art. 5º, II)",
    "financeiros": "dados financeiros (art. 5º, III)",
    "autenticacao": "dados de autenticação em sistemas (art. 5º, IV)",
    "sigilo": "dados protegidos por sigilo legal, judicial ou profissional (art. 5º, V)",
    "larga_escala": "dados em larga escala (art. 5º, VI, e § 2º)",
}
CAMPOS = ("incidente_confirmado", "dados_pessoais", "afeta_significativamente", "dados_ininteligiveis")
ROTULOS = {"incidente_confirmado": "incidente confirmado?", "dados_pessoais": "afetou dados pessoais?",
           "afeta_significativamente": "pode afetar significativamente direitos?", **CRITERIOS}


def modelo() -> dict:
    return {
        "incidente_confirmado": None, "dados_pessoais": None, "so_dados_anonimizados": False,
        "afeta_significativamente": None, "criterios": {k: None for k in CRITERIOS},
        "dados_ininteligiveis": None, "orgao_federal": None, "incidente_cibernetico": None,
        "operador_envolvido": None, "agente_pequeno_porte": False, "criancas_ou_adolescentes": None,
        "justificativas": {k: "" for k in ("afeta_significativamente", *CRITERIOS, "dados_ininteligiveis")},
    }


def avaliar(r: dict) -> dict:
    cr = r.get("criterios", {}) or {}
    for k in cr:
        if k not in CRITERIOS:
            raise ValueError(f"critério desconhecido: {k}")
    sim = [k for k in CRITERIOS if cr.get(k) is True]
    nd = [k for k in CRITERIOS if cr.get(k) is None]
    conclusao, pendentes, notas = "", [], []
    conf, dp, af = r.get("incidente_confirmado"), r.get("dados_pessoais"), r.get("afeta_significativamente")

    if conf is False:
        conclusao = ("INCIDENTE NÃO CONFIRMADO PELAS RESPOSTAS: vulnerabilidade ou suspeita ainda não é incidente "
                     "(Res. CD/ANPD 15/2024 [CONFERIR vigência], art. 3º, XII). Apure com urgência; se houver exploração, "
                     "o prazo de três dias úteis corre do conhecimento de que o incidente afetou dados pessoais (art. 6º, § 1º).")
    elif conf is None:
        pendentes.append("incidente_confirmado")
    elif dp is False or r.get("so_dados_anonimizados") is True:
        conclusao = ("SEM DADOS PESSOAIS AFETADOS, PELAS RESPOSTAS INFORMADAS: o indicativo é de que o art. 48 da LGPD não "
                     "se aplica; o controlador decide e registra os motivos. Trate como incidente de segurança da informação.")
        if r.get("so_dados_anonimizados") is True:
            notas.append("Dados anonimizados só deixam de ser dados pessoais se a anonimização não puder ser revertida com "
                         "esforços razoáveis (LGPD, art. 12) [CONFERIR]; se puder, refaça a triagem com dados_pessoais = true.")
    elif dp is None:
        pendentes.append("dados_pessoais")
    else:
        if af is None:
            pendentes.append("afeta_significativamente")
        if not sim and nd:
            pendentes += nd
        if af is True and sim:
            fund = "; ".join(CRITERIOS[k] for k in sim)
            if r.get("dados_ininteligiveis") is True:
                conclusao = ("AVALIAR COM O ENCARREGADO ANTES DE DEIXAR DE COMUNICAR: os critérios do art. 5º estão presentes: "
                             f"{fund}. Mas os dados estariam ininteligíveis para terceiros não autorizados (LGPD, art. 48, § 3º). "
                             "Só se deixa de comunicar com comprovação (por exemplo, chave de criptografia não comprometida) e "
                             "motivos registrados pelo controlador (Res. CD/ANPD 15/2024 [CONFERIR vigência], art. 10, § 1º, VIII) "
                             "[CONFERIR com a assessoria jurídica]. Na dúvida, a orientação é comunicar.")
            else:
                conclusao = ("INDICATIVO DE RISCO OU DANO RELEVANTE: a avaliação sugere comunicar à ANPD e aos titulares; a "
                             "decisão é do controlador. O incidente pode afetar significativamente interesses e direitos "
                             f"fundamentais (Res. CD/ANPD 15/2024 [CONFERIR vigência], art. 5º, caput e § 1º) e envolve: {fund}. "
                             "Prazo: três dias úteis do conhecimento (arts. 6º e 9º). Calcule com scripts/prazos_incidente.py.")
                if r.get("dados_ininteligiveis") is None:
                    notas.append("Informe se os dados estavam criptografados ou ininteligíveis: entra no juízo de gravidade (LGPD, art. 48, § 3º).")
        elif af is False or (not sim and not nd):
            conclusao = ("CRITÉRIOS DO ART. 5º NÃO PREENCHIDOS PELAS RESPOSTAS INFORMADAS (Res. CD/ANPD 15/2024 [CONFERIR "
                         "vigência]): o controlador decide e registra os motivos (art. 10, § 1º, VIII). Reavalie se surgirem "
                         "fatos novos.")
            if nd:
                notas.append(("Critério ainda sem resposta: " if len(nd) == 1 else "Critérios ainda sem resposta: ")
                             + "; ".join(CRITERIOS[k] for k in nd)
                             + (". Responda-o" if len(nd) == 1 else ". Responda-os") + " para completar o registro e reavaliar.")
            pendentes = []
    if pendentes and not conclusao:
        conclusao = ("NÃO VERIFICÁVEL: faltam respostas. O prazo continua correndo; se faltar informação, a comunicação à ANPD "
                     "pode ser feita com o que se sabe e complementada, de maneira fundamentada, em vinte dias úteis "
                     "(Res. CD/ANPD 15/2024 [CONFERIR vigência], art. 6º, § 3º; a ANPD chama essa etapa de comunicação "
                     "preliminar e a considera excepcional, com justificativa).")

    if conf is False:
        notas.append("Registre a análise da vulnerabilidade ou da suspeita e o resultado da apuração.")
    else:
        notas.append("Registre o incidente, comunicado ou não, por no mínimo cinco anos (Res. CD/ANPD 15/2024, art. 10); "
                     "para órgão público, esse prazo cede às regras de guarda permanente da tabela de temporalidade própria ou do "
                     "Conselho Nacional de Arquivos (art. 10, § 2º).")
    if r.get("orgao_federal") is True and r.get("incidente_cibernetico") is not False:
        notas.append("Órgão da administração federal direta, autárquica ou fundacional: comunique imediatamente ao CTIR Gov, por "
                     "meio da equipe de resposta do órgão, a existência de vulnerabilidades ou de incidentes de segurança "
                     "cibernética que impactem ou possam impactar os serviços prestados ou contratados (Decreto 10.748/2021, "
                     "art. 12, IV). É obrigação separada da comunicação à ANPD. O inciso remete ao Decreto 9.637/2018, revogado "
                     "pelo Decreto 12.572/2025: confirme a forma de comunicar [CONFERIR].")
    if r.get("operador_envolvido") is True:
        notas.append("Operador envolvido: a obrigação de comunicar é do controlador; o operador deve informar o controlador sem "
                     "demora injustificada (orientação da ANPD) e seguir as instruções dele (LGPD, art. 39).")
    if r.get("agente_pequeno_porte") is True:
        notas.append("Prazos em dobro só para agente de tratamento de pequeno porte (Res. CD/ANPD 15/2024, art. 6º, § 8º, e art. 9º, § 6º). "
                     "Pessoa jurídica de direito público não consta da definição (Res. CD/ANPD 2/2022, art. 2º, I) [CONFERIR].")
    if r.get("criancas_ou_adolescentes") is True or cr.get("criancas_adolescentes_idosos") is True:
        notas.append("Crianças, adolescentes ou idosos: informe o número de cada grupo à ANPD (Res. CD/ANPD 15/2024, art. 6º, § 2º, II). "
                     "ECA Digital (Lei 15.211/2025): deveres adicionais não verificados por esta skill.")
    notas.append("Não identifique nem culpe pessoas no registro e nas comunicações; responsabilidade se apura por sindicância ou "
                 "processo administrativo disciplinar (Lei 8.112/1990, art. 143; LGPD, art. 52, § 3º).")
    notas.append("Resultado indicativo: a decisão é do controlador, com assistência do encarregado (Res. CD/ANPD 18/2024, art. 16, I).")
    return {"conclusao": conclusao, "pendentes": pendentes, "criterios_presentes": sim, "notas": notas}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("respostas", nargs="?")
    ap.add_argument("--modelo", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.modelo:
        print(json.dumps(modelo(), ensure_ascii=False, indent=1))
        return 0
    if not a.respostas:
        print("erro: informe o arquivo de respostas ou use --modelo", file=sys.stderr)
        return 3
    try:
        res = avaliar(json.loads(ler_texto(a.respostas)))
    except (OSError, ValueError, AttributeError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 3
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print("# Triagem do incidente\n")
        print(f"- **{res['conclusao']}**")
        if res["pendentes"]:
            print("- Responder: " + "; ".join(ROTULOS.get(k, k) for k in res["pendentes"]))
        print("\nNotas:")
        for n in res["notas"]:
            print(f"- {n}")
    return 2 if res["pendentes"] else 0


if __name__ == "__main__":
    sys.exit(main())
