#!/usr/bin/env python3
"""Testes dos scripts, exemplos e evals da skill ripd-lgpd-br. Uso: python3 evals/testes.py"""
from __future__ import annotations

import atexit
import io
import json
import re
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SKILL = AQUI.parent
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(AQUI))

import _comum  # noqa: E402
import conferir_ripd  # noqa: E402
import dados_pessoais  # noqa: E402
import matriz_risco  # noqa: E402
import rodar_evals  # noqa: E402
import sinais_risco  # noqa: E402
import triagem_alto_risco  # noqa: E402

EX = SKILL / "examples"
AVISO = "> Esta é uma minuta preparada com ajuda de inteligência artificial (IA). Requer revisão humana e aprovação do controlador."
# Arquivos temporários num diretório próprio, apagado no fim (nada fica no TMPDIR do sistema).
_TMP = tempfile.TemporaryDirectory(prefix="ripd-testes-")
atexit.register(_TMP.cleanup)


def rodar(main, *args) -> tuple[int, str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = main(list(args))
    return rc, buf.getvalue()


def tmp(texto: str, sufixo=".md") -> str:
    f = tempfile.NamedTemporaryFile("w", suffix=sufixo, delete=False, encoding="utf-8", dir=_TMP.name)
    f.write(texto)
    f.close()
    return f.name


class Normas(unittest.TestCase):
    def test_campos_e_data(self):
        normas = _comum.carregar_normas()
        itens = normas["itens"]
        self.assertGreaterEqual(len(itens), 40)
        for n in itens:
            for k in ("id", "norma", "dispositivo", "resumo", "link", "verificado"):
                self.assertIn(k, n, n.get("id"))
            if n["verificado"]:
                self.assertEqual(n.get("conferido_em"), "2026-11-20", n["id"])
                self.assertTrue(n["link"].startswith("https://"), n["id"])

    def test_artigos_verificados(self):
        arts = conferir_ripd.artigos_lgpd(_comum.carregar_normas())
        for a in ("5", "6", "7", "11", "14", "18", "20", "23", "37", "38", "39", "41", "46", "48"):
            self.assertIn(a, arts)

    def test_atos_aceitos_estao_na_base(self):
        # Cada número que o conferidor aceita sem 'não verificado' precisa estar verificado em normas.json.
        verificados = " ".join(n["norma"] for n in _comum.carregar_normas()["itens"] if n["verificado"])
        for rotulo, numeros in (("Resolução CD/ANPD", conferir_ripd.RES_OK), ("Decreto", conferir_ripd.DECRETOS_OK),
                                ("Portaria SGD/MGI", conferir_ripd.PORTARIAS_OK), ("Enunciado CD/ANPD", conferir_ripd.ENUNCIADOS_OK)):
            for num in numeros:
                self.assertIn(f"{rotulo} {num}", verificados)

    def test_novas_normas_da_v1_1(self):
        ids = {n["id"]: n for n in _comum.carregar_normas()["itens"]}
        for i in ("RES15-2024-8", "RES19-2024", "RES32-2026", "DEC10046-2019", "LAI-8", "LAI-23-24"):
            self.assertTrue(ids[i]["verificado"], i)
        for i in ("RES19-2024", "RES32-2026", "DEC10046-2019"):
            self.assertIn("[CONFERIR]", ids[i]["observacao"], i)
        self.assertIn("ADI 6649", ids["DEC10046-2019"]["observacao"])
        self.assertIn("pequeno porte", ids["RES2-2022-4"]["observacao"])

    def test_contagem_declarada(self):
        itens = _comum.carregar_normas()["itens"]
        n, v = len(itens), sum(1 for i in itens if i["verificado"])
        self.assertIn(f"{n} itens, {v} conferidos", (SKILL / "SKILL.md").read_text(encoding="utf-8"))
        self.assertIn(f"{v} de {n} itens", (SKILL / "README.md").read_text(encoding="utf-8"))


class DadosPessoais(unittest.TestCase):
    def test_detecta_e_mascara(self):
        t = "CPF 123.456.789-01, e-mail fulano@prefeitura.test, CEP 01001-000, nascido em 01/02/2015"
        tipos = {d["tipo"] for d in _comum.achar_dados_pessoais(t)}
        self.assertTrue({"CPF", "e-mail", "CEP", "data de nascimento"} <= tipos)
        m = _comum.mascarar(t)
        self.assertNotIn("123.456.789-01", m)
        self.assertNotIn("fulano@", m)

    def test_ignora_dominio_reservado_e_datas(self):
        self.assertEqual(_comum.achar_dados_pessoais("canal encarregado@example.org em 20/11/2026"), [])

    def test_cli(self):
        self.assertEqual(rodar(dados_pessoais.main, tmp("CPF 123.456.789-01"))[0], 1)
        self.assertEqual(rodar(dados_pessoais.main, str(EX / "01-gestao-escolar-municipal" / "ripd.md"))[0], 0)

    def test_desempenho(self):
        texto = ("1" * 9 + " a@" + "b" * 60 + ". ") * 5000
        ini = time.time()
        _comum.achar_dados_pessoais(texto)
        _comum.achar_sinais(texto)
        self.assertLess(time.time() - ini, 3)

    def test_conferidor_linear_sem_tabela(self):
        # C6: a busca da tabela de riscos era quadrática numa linha longa sem tabela (250 mil caracteres: 105 s).
        for texto in ("| 1 |" * 50000, ("| R1 | x |" * 20000) + "\n" + "a" * 100000):
            ini = time.time()
            conferir_ripd.conferir(texto + "\n" + AVISO, "integral")
            self.assertLess(time.time() - ini, 3)


def cpf_valido(n: str) -> bool:
    d = [int(c) for c in n if c.isdigit()]
    if len(d) != 11 or len(set(d)) == 1:
        return False
    for i in (9, 10):
        s = sum(d[k] * (i + 1 - k) for k in range(i)) * 10 % 11 % 10
        if s != d[i]:
            return False
    return True


def nis_valido(n: str) -> bool:
    d = [int(c) for c in n if c.isdigit()]
    if len(d) != 11:
        return False
    r = 11 - sum(a * b for a, b in zip(d, (3, 2, 9, 8, 7, 6, 5, 4, 3, 2))) % 11
    return (0 if r >= 10 else r) == d[10]


class SemCpfValido(unittest.TestCase):
    def test_nenhum_cpf_valido_gravado(self):
        base = [5, 2, 9, 9, 8, 2, 2, 4, 7]  # CPF de teste montado em memória, nunca gravado
        for i in (9, 10):
            base.append(sum(base[k] * (i + 1 - k) for k in range(i)) * 10 % 11 % 10)
        self.assertTrue(cpf_valido("".join(map(str, base))))
        # Formatado ou não (11 dígitos), nenhum número gravado pode ter DV válido de CPF nem de NIS/PIS.
        rx = re.compile(r"(?<![\d.])(?:\d{3}\.\d{3}\.\d{3}-\d{2}|\d{3}\.\d{5}\.\d{2}-\d|\d{11})(?![\d.])")
        for arq in SKILL.rglob("*"):
            if arq.is_file() and arq.suffix in (".md", ".json", ".csv", ".py", ".txt"):
                for m in rx.findall(arq.read_text(encoding="utf-8")):
                    self.assertFalse(cpf_valido(m), f"{arq.name}: {m} (CPF)")
                    self.assertFalse(nis_valido(m), f"{arq.name}: {m} (NIS/PIS)")

    def test_dominios_de_teste_reservados(self):
        # Domínios de e-mail gravados: só os reservados (example.*, .test, .invalid), RFC 2606 e RFC 6761.
        rx = re.compile(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)")
        for arq in SKILL.rglob("*"):
            if arq.is_file() and arq.suffix in (".md", ".json", ".csv", ".py", ".txt"):
                for dom in rx.findall(arq.read_text(encoding="utf-8")):
                    self.assertTrue(dom.lower().endswith(("example.org", "example.com", "example.net", ".test", ".invalid")),
                                    f"{arq.name}: {dom}")


class Sinais(unittest.TestCase):
    def test_exemplo_escolar(self):
        s = _comum.achar_sinais((EX / "01-gestao-escolar-municipal" / "descricao.md").read_text(encoding="utf-8"))
        for k in ("dados_sensiveis", "criancas_adolescentes_idosos", "decisao_automatizada", "compartilhamento_privado"):
            self.assertIn(k, s)

    def test_inicio_de_palavra(self):
        s = _comum.achar_sinais("Reforma da biblioteca")
        self.assertNotIn("criancas_adolescentes_idosos", s)
        self.assertNotIn("dados_sensiveis", _comum.achar_sinais("obras na praca central"))

    def test_ia_palavra_inteira(self):
        # S14: " ia " não casa com prefixo ("iam", "ianomâmi").
        self.assertNotIn("tecnologia_emergente", _comum.achar_sinais("Eles iam ao posto do povo ianomâmi."))
        self.assertIn("tecnologia_emergente", _comum.achar_sinais("Triagem com IA."))

    def test_trechos_com_acento(self):
        rc, out = rodar(sinais_risco.main, tmp("Campo cor/raça e laudo de deficiência."))
        self.assertEqual(rc, 1)
        self.assertIn("cor/raça", out)
        self.assertIn("deficiência", out)

    def test_novas_normas_nos_sinais(self):
        s = _comum.achar_sinais("Servidor na nuvem nos Estados Unidos; houve vazamento.")
        self.assertIn("19/2024", s["transferencia_internacional"]["criterio"])
        self.assertIn("15/2024", s["incidente"]["criterio"])
        for nome in ("dados_sensiveis", "larga_escala"):
            self.assertIn("[CONFERIR]", _comum.SINAIS[nome]["criterio"])

    def test_cli(self):
        self.assertEqual(rodar(sinais_risco.main, tmp("Ata da reunião sobre o orçamento."))[0], 0)


class Triagem(unittest.TestCase):
    def avaliar(self, g, e, **extra):
        return triagem_alto_risco.avaliar({"criterios_gerais": g, "criterios_especificos": e, **extra})

    def test_alto_risco(self):
        r = self.avaliar({"larga_escala": True}, {"sensiveis_ou_vulneraveis": True})
        self.assertIn("RIPD RECOMENDADO: alto risco", r["conclusoes"][0])
        self.assertIn("pequeno porte", r["conclusoes"][0])
        self.assertIn("[CONFERIR]", r["conclusoes"][0])
        self.assertIn("Critério geral:", r["conclusoes"][0])

    def test_plural_dos_criterios(self):
        r = self.avaliar({"larga_escala": True, "afeta_direitos": True}, {"sensiveis_ou_vulneraveis": True})
        self.assertIn("Critérios gerais:", r["conclusoes"][0])
        self.assertIn("Critério específico:", r["conclusoes"][0])

    def test_outro_fator_nao_exaustivo(self):
        # C2: o rol do art. 4º não é exaustivo; o sétimo item pode caracterizar alto risco sozinho.
        nao_g = {k: False for k in triagem_alto_risco.GERAIS}
        nao_e = {k: False for k in triagem_alto_risco.ESPECIFICOS}
        r = self.avaliar(nao_g, nao_e, outro_fator_alto_risco=True)
        self.assertIn("RIPD RECOMENDADO", r["conclusoes"][0])
        self.assertIn("outro_fator_alto_risco", r["justificativas_faltando"])
        r = self.avaliar(nao_g, nao_e)
        self.assertIn("outro_fator_alto_risco", r["pendentes"])
        r = self.avaliar(nao_g, nao_e, outro_fator_alto_risco=False)
        self.assertIn("não são exaustivos", r["conclusoes"][0])
        rc, _ = rodar(triagem_alto_risco.main, "--nao", ",".join(list(triagem_alto_risco.GERAIS) + list(triagem_alto_risco.ESPECIFICOS)),
                      "--sim", "outro_fator")
        self.assertEqual(rc, 0)

    def test_nota_de_criancas_so_quando_cabe(self):
        # S11: dado sensível sem criança não gera a nota do melhor interesse.
        base = ({"larga_escala": True}, {"sensiveis_ou_vulneraveis": True})
        notas = " ".join(self.avaliar(*base, criancas_adolescentes=False)["notas"])
        self.assertNotIn("art. 14", notas)
        self.assertIn("art. 11", notas)
        notas = " ".join(self.avaliar(*base, criancas_adolescentes=True)["notas"])
        self.assertIn("Dados de crianças e adolescentes: melhor interesse", notas)
        notas = " ".join(self.avaliar(*base)["notas"])
        self.assertIn("Se houver dados de crianças", notas)

    def test_sisp_medida_23_3(self):
        notas = " ".join(self.avaliar({}, {}, orgao_sisp_federal=True)["notas"])
        self.assertIn("medida 23.3", notas)
        self.assertNotIn("controle 23 do framework", notas)

    def test_so_gerais_e_boa_pratica(self):
        r = self.avaliar({"larga_escala": True, "afeta_direitos": True},
                         {k: False for k in triagem_alto_risco.ESPECIFICOS})
        self.assertIn("BOA PRÁTICA", r["conclusoes"][0])

    def test_pendente(self):
        r = self.avaliar({"larga_escala": None, "afeta_direitos": False}, {"sensiveis_ou_vulneraveis": True})
        self.assertIn("larga_escala", r["pendentes"])

    def test_nao_caracterizado_nao_dispensa(self):
        rc, out = rodar(triagem_alto_risco.main, str(EX / "03-agendamento-atendimento" / "triagem.json"))
        self.assertEqual(rc, 0)
        self.assertIn("NÃO CARACTERIZADO", out)
        self.assertIn("art. 38", out)
        self.assertIn("art. 37", out)

    def test_motivo_anpd(self):
        r = self.avaliar({}, {}, motivo_anpd="art38")
        self.assertIn("EXIGÍVEL", r["conclusoes"][0])

    def test_criterio_desconhecido(self):
        with self.assertRaises(ValueError):
            self.avaliar({"inventado": True}, {})


class Matriz(unittest.TestCase):
    CAB = "id;risco;probabilidade;impacto;medidas;probabilidade_residual;impacto_residual;responsavel;prazo\n"

    def test_exemplo_e_pendencias(self):
        res = matriz_risco.calcular(_comum.ler_csv(str(EX / "01-gestao-escolar-municipal" / "riscos.csv")))
        self.assertEqual(res["riscos"][0]["id"], "R2")
        self.assertEqual(res["riscos"][0]["faixa"], "crítico")
        self.assertTrue(any("R5" in p and "residual alto" in p for p in res["pendencias"]))

    def test_alto_sem_medida(self):
        res = matriz_risco.calcular(_comum.ler_csv(tmp(self.CAB + "R1;Exposição de laudo;4;4;;;;;\n", ".csv")))
        txt = " ".join(res["pendencias"])
        self.assertIn("sem medida", txt)
        self.assertIn("sem responsável", txt)

    def test_impacto_baixo_sensivel(self):
        res = matriz_risco.calcular(_comum.ler_csv(tmp(self.CAB + "R1;Acesso a dado de saude;2;2;x;1;1;TI;1 mes\n", ".csv")))
        self.assertTrue(any("parece baixo" in p for p in res["pendencias"]))

    def test_colunas_a_mais(self):
        with self.assertRaises(ValueError):
            _comum.ler_csv(tmp(self.CAB + "R1;a;2;2;x;y;1;1;TI;1\n", ".csv"))

    def test_nota_fora_da_escala(self):
        rc, _ = rodar(matriz_risco.main, tmp(self.CAB + "R1;a;9;2;x;1;1;TI;1\n", ".csv"))
        self.assertEqual(rc, 3)

    def test_so_uma_coluna_residual(self):
        # S13: residual com uma coluna só não pode ser ignorado em silêncio.
        res = matriz_risco.calcular(_comum.ler_csv(tmp(self.CAB + "R1;Atraso no atendimento;2;2;x;1;;TI;1 mes\n", ".csv")))
        self.assertTrue(any("só uma das colunas residuais" in p for p in res["pendencias"]))

    def test_opcoes_ao_controlador(self):
        res = matriz_risco.calcular(_comum.ler_csv(str(EX / "01-gestao-escolar-municipal" / "riscos.csv")))
        self.assertTrue(any("prosseguir com justificativa, mudar o tratamento ou não prosseguir" in p for p in res["pendencias"]))


class Conferidor(unittest.TestCase):
    def test_exemplos_passam(self):
        for arq, modo in (("01-gestao-escolar-municipal/ripd.md", "integral"),
                          ("02-videomonitoramento-placas/ripd_publico.md", "publica"),
                          ("03-agendamento-atendimento/saida.md", "parcial")):
            erros, _ = conferir_ripd.conferir((EX / arq).read_text(encoding="utf-8"), modo)
            self.assertEqual(erros, [], arq)

    def test_sem_aviso(self):
        erros, _ = conferir_ripd.conferir("Texto qualquer.", "parcial")
        self.assertTrue(any("aviso" in e for e in erros))

    def test_linguagem_proibida(self):
        for frase in ("O sistema está em conformidade com a LGPD.", "Declaro aprovado.", "O risco zero foi atingido.",
                      "O órgão está dispensado do RIPD."):
            erros, _ = conferir_ripd.conferir(frase + "\n" + AVISO, "parcial")
            self.assertTrue(any("proibida" in e for e in erros), frase)
        erros, _ = conferir_ripd.conferir("Não afirmamos que o sistema está em conformidade com a LGPD.\n" + AVISO, "parcial")
        self.assertFalse(any("proibida" in e for e in erros))

    def test_linguagem_proibida_contornos(self):
        # C4: as dez frases da auditoria, inclusive com "não" antes, mas fora do verbo.
        for frase in ("Não há dúvida: o sistema está em conformidade com a LGPD.", "Não restam riscos: aprovo o tratamento.",
                      "O tratamento é lícito e atende integralmente à LGPD.", "O sistema é conforme a LGPD.",
                      "Aprova-se o tratamento.", "O órgão fica dispensado da elaboração do RIPD.", "O RIPD não é necessário.",
                      "O risco é inexistente.", "Sem pendências, o sistema está em conformidade com a LGPD.",
                      "A licitude do tratamento está confirmada.", "O tratamento é legal.", "O órgão não precisa de RIPD."):
            erros, _ = conferir_ripd.conferir(frase + "\n" + AVISO, "parcial")
            self.assertTrue(any("proibida" in e for e in erros), frase)
        for frase in ("O sistema não está em conformidade com a LGPD em dois pontos.", "Isso não significa que o tratamento é lícito.",
                      "O órgão não fica dispensado do RIPD.", "Não há risco residual alto.",
                      "Não vou escrever que o sistema está em conformidade com a LGPD."):
            erros, _ = conferir_ripd.conferir(frase + "\n" + AVISO, "parcial")
            self.assertFalse(any("proibida" in e for e in erros), frase)

    def test_citacoes(self):
        erros, _ = conferir_ripd.conferir("LGPD, art. 99.\n" + AVISO, "parcial")
        self.assertTrue(erros)
        erros, _ = conferir_ripd.conferir("Decreto 12.345/2025 trata disso.\n" + AVISO, "parcial")
        self.assertTrue(erros)
        erros, _ = conferir_ripd.conferir("Decreto 12.345/2025: não verificado.\n" + AVISO, "parcial")
        self.assertFalse(erros)
        erros, _ = conferir_ripd.conferir("Lei 15.211/2025 vale.\n" + AVISO, "parcial")
        self.assertTrue(erros)

    def test_citacoes_de_outros_atos(self):
        # S9: outras formas de citar resolução, portaria, enunciado e instrução normativa.
        for ruim in ("Resolução nº 99/2025 trata disso.", "Res. ANPD 99/2024 vale.", "Portaria MGI 1/2024.",
                     "IN SGD/ME 94/2022.", "Enunciado CD/ANPD 2/2024.", "Resolução CNJ 615/2025.", "Decreto-Lei 200/1967."):
            erros, _ = conferir_ripd.conferir(ruim + "\n" + AVISO, "parcial")
            self.assertTrue(erros, ruim)
        for bom in ("Res. CD/ANPD 19/2024 [CONFERIR].", "Resolução nº 32/2026.", "Decreto nº 10.046, de 9 de outubro de 2019.",
                    "Portaria SGD/MGI 9.511/2025.", "Res. CD/ANPD 15/2024, art. 8º."):
            erros, _ = conferir_ripd.conferir(bom + "\n" + AVISO, "parcial")
            self.assertFalse(erros, bom)

    def test_conferir_nao_e_exigido(self):
        # Decisão da autora (v1.1.0-rc): a marca [CONFERIR] nas resoluções da ANPD é regra de redação,
        # não do conferidor. Sem a marca, a citação de resolução da base passa.
        erros, _ = conferir_ripd.conferir("Critérios da Res. CD/ANPD 2/2022, art. 4º.\n" + AVISO, "parcial")
        self.assertFalse(erros)

    def test_publica_restrita(self):
        texto = (EX / "02-videomonitoramento-placas" / "ripd_publico.md").read_text(encoding="utf-8")
        for vaz in ("Servidor 10.20.30.40.", "Banco na porta 5432.", "Falha CVE-2024-12345.", "Troca de senha anual.",
                    "Host sge.intra.", "Servidor Apache versão 2.4.1."):
            erros, _ = conferir_ripd.conferir(texto + "\n" + vaz + "\n", "publica")
            self.assertTrue(erros, vaz)

    def test_integral_sem_art38(self):
        texto = (EX / "01-gestao-escolar-municipal" / "ripd.md").read_text(encoding="utf-8")
        erros, _ = conferir_ripd.conferir(texto.replace("salvaguardas", "cuidados"), "integral")
        self.assertTrue(any("art. 38" in e for e in erros))

    def test_principio_faltando(self):
        texto = (EX / "01-gestao-escolar-municipal" / "ripd.md").read_text(encoding="utf-8")
        erros, _ = conferir_ripd.conferir(texto.replace("| Não discriminação |", "| Outro |"), "integral")
        self.assertTrue(erros)

    def test_dado_pessoal(self):
        erros, _ = conferir_ripd.conferir("Titular: CPF 123.456.789-01.\n" + AVISO, "parcial")
        self.assertTrue(any("dado pessoal" in e for e in erros))


class Evals(unittest.TestCase):
    def test_estrutura(self):
        ev = json.loads((AQUI / "evals.json").read_text(encoding="utf-8"))["evals"]
        self.assertGreaterEqual(len(ev), 10)
        self.assertEqual(len({c["id"] for c in ev}), len(ev))
        for c in ev:
            self.assertTrue(c["expectativas"] and c["assercoes"])
            for a in c.get("arquivos", []):
                self.assertTrue((SKILL / a).exists(), a)
        ac = json.loads((AQUI / "acionamento.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(ac["deve_acionar"]), 10)
        self.assertGreaterEqual(len(ac["nao_deve_acionar"]), 10)

    def test_referencia_passa(self):
        r = rodar_evals.rodar(AQUI / "referencia", AQUI / "evals.json")
        self.assertEqual(r["falhou"], 0, [c for c in r["casos"] if not c["ok"]])

    def test_resposta_ruim_falha(self):
        with tempfile.TemporaryDirectory() as d:
            for c in json.loads((AQUI / "evals.json").read_text(encoding="utf-8"))["evals"]:
                Path(d, c["id"] + ".md").write_text("O sistema está em conformidade com a LGPD. Aprovo.", encoding="utf-8")
            r = rodar_evals.rodar(Path(d), AQUI / "evals.json")
            self.assertEqual(r["passou"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
