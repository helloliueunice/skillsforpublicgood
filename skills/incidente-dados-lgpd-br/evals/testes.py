#!/usr/bin/env python3
"""Testes dos scripts, exemplos e evals da skill incidente-dados-lgpd-br. Uso: python3 evals/testes.py

Os arquivos temporários ficam num diretório próprio, apagado no fim da execução.
"""
from __future__ import annotations

import datetime as dt
import io
import json
import re
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SKILL = AQUI.parent
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(AQUI))

import _comum  # noqa: E402
import conferir_comunicacao as cc  # noqa: E402
import dados_pessoais  # noqa: E402
import prazos_incidente  # noqa: E402
import rodar_evals  # noqa: E402
import triagem_incidente  # noqa: E402

EX = SKILL / "examples"
AVISO = "> Esta é uma minuta preparada com ajuda de inteligência artificial (IA). Requer revisão humana."
D = dt.date
CPF_FICTICIO = "123.456.789-01"  # DV inválido para CPF e para NIS (ver SemDocumentoValido)
_TMP = tempfile.TemporaryDirectory(prefix="testes_incidente_")


def tearDownModule():  # noqa: N802 (nome exigido pelo unittest)
    _TMP.cleanup()


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


def erros(texto: str, modo="parcial") -> list[str]:
    return cc.conferir(texto + "\n" + AVISO, modo)[0]


class Normas(unittest.TestCase):
    def test_campos_e_data(self):
        dados = _comum.carregar_normas()
        itens = dados["itens"]
        self.assertGreaterEqual(len(itens), 50)
        for n in itens:
            for k in ("id", "norma", "dispositivo", "resumo", "link", "verificado"):
                self.assertIn(k, n, n.get("id"))
            if n["verificado"]:
                data = dt.date.fromisoformat(n["conferido_em"])
                self.assertTrue(D(2026, 11, 19) <= data <= D(2026, 11, 20), n["id"])
                self.assertTrue(n["link"].startswith("https://"), n["id"])
        self.assertEqual(len({n["id"] for n in itens}), len(itens))

    def test_nucleo_verificado(self):
        ids = {n["id"] for n in _comum.carregar_normas()["itens"] if n["verificado"]}
        for i in ("LGPD-48", "LGPD-48-3", "LGPD-52-3", "RES15-5", "RES15-6", "RES15-9", "RES15-10", "D12572-12", "L8112-143"):
            self.assertIn(i, ids)

    def test_decreto_9637_revogado(self):
        it = {n["id"]: n for n in _comum.carregar_normas()["itens"]}
        self.assertIn("REVOGADO", it["D9637"]["resumo"])
        self.assertIn("12.572/2025", it["D9637"]["resumo"])
        self.assertIn("vulnerabilidades", it["D10748-12"]["resumo"])

    def test_contagem_anunciada_no_skill(self):
        itens = _comum.carregar_normas()["itens"]
        n, v = len(itens), sum(1 for i in itens if i["verificado"])
        self.assertIn(f"({n} itens, {v} conferidos", (SKILL / "SKILL.md").read_text(encoding="utf-8"))


class DiasUteis(unittest.TestCase):
    def test_feriado_20_de_novembro(self):
        self.assertFalse(_comum.eh_util(D(2026, 11, 20), set()))
        self.assertEqual(_comum.somar_dias_uteis(D(2026, 11, 18), 3, set()), D(2026, 11, 24))
        self.assertEqual(_comum.somar_dias_uteis(D(2026, 11, 19), 3, set()), D(2026, 11, 25))

    def test_20_de_novembro_so_desde_2024(self):
        self.assertTrue(_comum.eh_util(D(2023, 11, 20), set()))   # segunda-feira; Lei 14.759 é de 21/12/2023
        self.assertFalse(_comum.eh_util(D(2024, 11, 20), set()))

    def test_exclui_dia_do_inicio(self):
        self.assertEqual(_comum.somar_dias_uteis(D(2026, 11, 23), 1, set()), D(2026, 11, 24))

    def test_feriado_extra_e_fim_de_ano(self):
        self.assertEqual(_comum.somar_dias_uteis(D(2026, 11, 18), 3, {D(2026, 11, 23)}), D(2026, 11, 25))
        self.assertEqual(_comum.somar_dias_uteis(D(2026, 12, 23), 3, set()), D(2026, 12, 29))

    def test_ler_data(self):
        self.assertEqual(_comum.ler_data("2026-11-18"), D(2026, 11, 18))
        self.assertEqual(_comum.ler_data("18/11/2026"), D(2026, 11, 18))
        with self.assertRaises(ValueError):
            _comum.ler_data("31/02/2026")


class Prazos(unittest.TestCase):
    def test_basico(self):
        r = prazos_incidente.calcular(D(2026, 11, 18), set())
        v = [l["vencimento"] for l in r["prazos"]]
        self.assertEqual(v[:3], ["24/11/2026", "24/11/2026", "27/11/2026"])

    def test_pequeno_porte_dobra_com_aviso(self):
        r = prazos_incidente.calcular(D(2026, 11, 18), set(), pequeno=True)
        self.assertEqual(r["prazos"][0]["vencimento"], "27/11/2026")
        self.assertTrue(any("direito público" in a for a in r["alertas"]))

    def test_vencido_e_atraso(self):
        r = prazos_incidente.calcular(D(2026, 11, 18), set(), titulares=D(2026, 11, 26), hoje=D(2026, 11, 30))
        self.assertTrue(r["vencido"])
        self.assertIn("atraso (2 dias úteis)", r["prazos"][1]["situacao"])
        self.assertTrue(any("motivos da demora" in a for a in r["alertas"]))

    def test_plural_correto(self):
        r = prazos_incidente.calcular(D(2026, 11, 18), set(), hoje=D(2026, 11, 23))
        self.assertEqual(r["prazos"][0]["situacao"], "falta 1 dia útil")
        r = prazos_incidente.calcular(D(2026, 11, 18), set(), hoje=D(2026, 11, 19))
        self.assertEqual(r["prazos"][0]["situacao"], "faltam 2 dias úteis")
        r = prazos_incidente.calcular(D(2026, 11, 18), set(), titulares=D(2026, 11, 25))
        self.assertIn("(1 dia útil)", r["prazos"][1]["situacao"])
        self.assertNotIn("(s)", json.dumps(r, ensure_ascii=False))

    def test_complementacao(self):
        r = prazos_incidente.calcular(D(2026, 11, 18), set(), anpd=D(2026, 11, 23))
        self.assertTrue(any("Complementar" in l["obrigacao"] for l in r["prazos"]))

    def test_cli(self):
        self.assertEqual(rodar(prazos_incidente.main, "--conhecimento", "18/11/2026", "--hoje", "20/11/2026")[0], 0)
        self.assertEqual(rodar(prazos_incidente.main, "--conhecimento", "18/11/2026", "--hoje", "30/11/2026")[0], 1)
        rc, out = rodar(prazos_incidente.main, "--conhecimento", "21/11/2026")
        self.assertIn("fim de semana", out)


class Triagem(unittest.TestCase):
    BASE = {"incidente_confirmado": True, "dados_pessoais": True, "afeta_significativamente": True}
    IMPERATIVOS = re.compile(r"^(COMUNICAR|COMUNICAÇÃO NÃO EXIGIDA|SEM DADOS PESSOAIS AFETADOS:)")

    def test_indicativo_de_risco(self):
        r = triagem_incidente.avaliar({**self.BASE, "criterios": {"sensiveis": True}})
        self.assertTrue(r["conclusao"].startswith("INDICATIVO DE RISCO OU DANO RELEVANTE"))
        self.assertIn("a decisão é do controlador", r["conclusao"])

    def test_nenhuma_conclusao_imperativa(self):
        casos = [{"incidente_confirmado": False}, {"incidente_confirmado": True, "dados_pessoais": False},
                 {**self.BASE, "criterios": {"sensiveis": True}}, {**self.BASE, "afeta_significativamente": False},
                 {**self.BASE, "criterios": {"larga_escala": True}, "dados_ininteligiveis": True}]
        for c in casos:
            conc = triagem_incidente.avaliar(c)["conclusao"]
            self.assertIsNone(self.IMPERATIVOS.search(conc), conc)
            self.assertEqual(cc.conferir(conc + "\n" + AVISO, "parcial")[0], [], conc)

    def test_vulnerabilidade(self):
        r = triagem_incidente.avaliar({"incidente_confirmado": False, "orgao_federal": True})
        self.assertTrue(r["conclusao"].startswith("INCIDENTE NÃO CONFIRMADO"))
        txt = " ".join(r["notas"])
        self.assertIn("análise da vulnerabilidade", txt)
        self.assertNotIn("Registre o incidente", txt)
        self.assertIn("vulnerabilidades", txt)

    def test_anonimizados_ressalva(self):
        r = triagem_incidente.avaliar({"incidente_confirmado": True, "dados_pessoais": True, "so_dados_anonimizados": True})
        self.assertIn("art. 12", " ".join(r["notas"]))

    def test_ininteligivel_nao_dispensa(self):
        r = triagem_incidente.avaliar({**self.BASE, "criterios": {"larga_escala": True}, "dados_ininteligiveis": True})
        self.assertTrue(r["conclusao"].startswith("AVALIAR"))
        self.assertNotIn("((", r["conclusao"])

    def test_pendente(self):
        r = triagem_incidente.avaliar({**self.BASE, "afeta_significativamente": None, "criterios": {"sensiveis": None}})
        self.assertTrue(r["conclusao"].startswith("NÃO VERIFICÁVEL"))
        self.assertIn("afeta_significativamente", r["pendentes"])

    def test_criterios_nao_preenchidos_e_registro(self):
        r = triagem_incidente.avaliar({**self.BASE, "afeta_significativamente": False})
        self.assertTrue(r["conclusao"].startswith("CRITÉRIOS DO ART. 5º NÃO PREENCHIDOS"))
        self.assertIn("o controlador decide", r["conclusao"])
        self.assertTrue(any("cinco anos" in n for n in r["notas"]))

    def test_notas_federal_operador_pessoas(self):
        r = triagem_incidente.avaliar({**self.BASE, "criterios": {"sensiveis": True}, "orgao_federal": True,
                                       "operador_envolvido": True})
        txt = " ".join(r["notas"])
        for termo in ("CTIR Gov", "operador", "vulnerabilidades", "12.572/2025", "sindicância", "indicativo"):
            self.assertIn(termo, txt)

    def test_criterio_desconhecido(self):
        with self.assertRaises(ValueError):
            triagem_incidente.avaliar({**self.BASE, "criterios": {"inventado": True}})

    def test_exemplos(self):
        esperado = {"01-ransomware-saude": "INDICATIVO DE RISCO", "02-email-destinatario-errado": "CRITÉRIOS DO ART. 5º NÃO PREENCHIDOS",
                    "03-notebook-criptografado": "AVALIAR"}
        for pasta, ini in esperado.items():
            r = triagem_incidente.avaliar(json.loads((EX / pasta / "triagem.json").read_text(encoding="utf-8")))
            self.assertTrue(r["conclusao"].startswith(ini), pasta)

    def test_exemplo_02_coerente_sobre_idosos(self):
        tri = json.loads((EX / "02-email-destinatario-errado" / "triagem.json").read_text(encoding="utf-8"))
        reg = (EX / "02-email-destinatario-errado" / "registro.md").read_text(encoding="utf-8")
        self.assertIn("idosos: [PREENCHER]", reg)
        self.assertIsNone(tri["criterios"]["criancas_adolescentes_idosos"])
        self.assertTrue(any("Critério ainda sem resposta" in n for n in triagem_incidente.avaliar(tri)["notas"]))

    def test_cli_rotulos_legiveis(self):
        rc, out = rodar(triagem_incidente.main, tmp(json.dumps({**self.BASE, "afeta_significativamente": None}), ".json"))
        self.assertEqual(rc, 2)
        self.assertIn("pode afetar significativamente direitos?", out)


class DadosPessoais(unittest.TestCase):
    def test_detecta_e_ignora_ficticio(self):
        self.assertTrue(_comum.achar_dados_pessoais("CPF " + CPF_FICTICIO))
        self.assertEqual(_comum.achar_dados_pessoais("canal encarregado@example.org em 20/11/2026"), [])
        self.assertNotIn(CPF_FICTICIO, _comum.mascarar("CPF " + CPF_FICTICIO))

    def test_marcador_concorda(self):
        self.assertIn("[DATA DE NASCIMENTO REMOVIDA]", _comum.mascarar("nascido em 01/02/1990"))
        self.assertIn("[CPF REMOVIDO]", _comum.mascarar("CPF " + CPF_FICTICIO))

    def test_cli(self):
        self.assertEqual(rodar(dados_pessoais.main, tmp("CPF " + CPF_FICTICIO))[0], 1)
        self.assertEqual(rodar(dados_pessoais.main, str(EX / "01-ransomware-saude" / "comunicacao_anpd.md"))[0], 0)


class Desempenho(unittest.TestCase):
    """Toda regex dos scripts roda em tempo linear: cada uma, sozinha, em 250 mil caracteres adversariais."""
    N = 250_000
    ENTRADAS = ["1" * N, ("a@" + "b" * 60 + ". ") * (N // 64), ("não " * (N // 4)), ("servidor Joao " * (N // 14)),
                ("medidas antes " * (N // 14)), ("riscos " * (N // 7)), ("x." * (N // 2)), (" " * N), ("RG " + "1." * (N // 2))]

    def _todas(self):
        rx = [r for _, r in _comum.PADROES_DADOS]
        rx += [re.compile(p, re.I) for p, _ in cc.PROIBIDO + cc.SO_TITULAR + cc.RESTRITO]
        rx += [re.compile(p) for _, _, p in cc.ANPD + cc.TITULAR + cc.REGISTRO]
        rx += [cc.ACUSA_NOME, cc.NEG_DIRETA, cc.NEG_RELATO, cc.ATRIBUI_CONTROLADOR, cc.JANELA_LGPD, cc.JANELA_R15, cc.ARTS]
        return rx

    def test_cada_regex_em_250_mil_caracteres(self):
        for r in self._todas():
            for e in self.ENTRADAS:
                ini = time.perf_counter()
                list(r.finditer(e[: self.N]))
                self.assertLess(time.perf_counter() - ini, 2.0, r.pattern[:60])

    def test_conferidor_inteiro(self):
        texto = ("1" * 9 + " a@" + "b" * 60 + ". não houve ") * 3000
        ini = time.perf_counter()
        _comum.achar_dados_pessoais(texto)
        cc.conferir(texto + "\n" + AVISO, "titular")
        self.assertLess(time.perf_counter() - ini, 10)


def cpf_valido(n: str) -> bool:
    d = [int(c) for c in n if c.isdigit()]
    if len(d) != 11 or len(set(d)) == 1:
        return False
    return all(sum(d[k] * (i + 1 - k) for k in range(i)) * 10 % 11 % 10 == d[i] for i in (9, 10))


def nis_valido(n: str) -> bool:
    d = [int(c) for c in n if c.isdigit()]
    if len(d) != 11 or len(set(d)) == 1:
        return False
    r = 11 - sum(a * b for a, b in zip(d[:10], (3, 2, 9, 8, 7, 6, 5, 4, 3, 2))) % 11
    return (0 if r >= 10 else r) == d[10]


def cnpj_valido(n: str) -> bool:
    d = [int(c) for c in n if c.isdigit()]
    if len(d) != 14 or len(set(d)) == 1:
        return False
    for i, pesos in ((12, (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)), (13, (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2))):
        r = sum(a * b for a, b in zip(d[:i], pesos)) % 11
        if (0 if r < 2 else 11 - r) != d[i]:
            return False
    return True


class SemDocumentoValido(unittest.TestCase):
    def test_validadores(self):
        base = [5, 2, 9, 9, 8, 2, 2, 4, 7]  # CPF de teste montado em memória, nunca gravado
        for i in (9, 10):
            base.append(sum(base[k] * (i + 1 - k) for k in range(i)) * 10 % 11 % 10)
        self.assertTrue(cpf_valido("".join(map(str, base))))
        self.assertFalse(cpf_valido(CPF_FICTICIO))
        self.assertFalse(nis_valido(CPF_FICTICIO))
        self.assertTrue(cnpj_valido("11222333000181"))  # exemplo didático clássico, montado só em memória

    def test_nenhum_cpf_nis_cnpj_valido_gravado(self):
        onze = re.compile(r"(?<!\d)(\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{3}\.?\d{5}\.?\d{2}-?\d)(?!\d)")
        quatorze = re.compile(r"(?<!\d)\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}(?!\d)")
        for arq in SKILL.rglob("*"):
            if arq.is_file() and arq.suffix in (".md", ".json", ".csv", ".py", ".txt"):
                texto = arq.read_text(encoding="utf-8")
                if arq.name == "testes.py":
                    texto = texto.replace("11222333000181", "")
                for m in onze.findall(texto):
                    self.assertFalse(cpf_valido(m) or nis_valido(m), f"{arq.name}: {m}")
                for m in quatorze.findall(texto):
                    self.assertFalse(cnpj_valido(m), f"{arq.name}: {m}")


class Conferidor(unittest.TestCase):
    def test_exemplos_passam(self):
        for arq, modo in (("01-ransomware-saude/comunicacao_anpd.md", "anpd"),
                          ("01-ransomware-saude/aviso_titulares.md", "titular"),
                          ("02-email-destinatario-errado/registro.md", "registro"),
                          ("03-notebook-criptografado/saida.md", "parcial")):
            e, _ = cc.conferir((EX / arq).read_text(encoding="utf-8"), modo)
            self.assertEqual(e, [], arq)

    def test_sem_aviso(self):
        e, _ = cc.conferir("Texto qualquer.", "parcial")
        self.assertTrue(any("aviso" in x.lower() for x in e))

    # As 14 frases da auditoria AGU/CGU (C5): todas têm de ser barradas.
    FRASES_AUDITORIA = (
        "O órgão está em conformidade com a LGPD.",
        "O risco zero foi atingido.",
        "Não houve risco relevante aos titulares.",
        "O incidente não acarretou risco ou dano relevante.",
        "Não é necessário comunicar a ANPD.",
        "Fica dispensada a comunicação.",
        "Estamos em conformidade com a LGPD.",
        "Não há dúvida: o órgão está em conformidade com a LGPD.",
        "Não houve demora: aprovo o envio.",
        "Fique tranquilo, seus dados estão seguros.",
        "Não se preocupe, não há perigo.",
        "Responda este e-mail com sua senha.",
        "Informe o código recebido por SMS.",
        "O servidor João foi o culpado pelo vazamento.",
    )

    def test_14_frases_da_auditoria_barradas(self):
        for modo in ("parcial", "anpd", "titular", "registro"):
            for frase in self.FRASES_AUDITORIA:
                self.assertTrue(any("linguagem proibida" in x for x in erros(frase, modo)), f"{modo}: {frase}")

    def test_outras_frases_barradas(self):
        for frase in ("O tratamento é lícito.", "Aprova-se a minuta.", "O risco é zero.", "Houve negligência do servidor.",
                      "A comunicação não é exigida.", "Ausência de risco ou dano relevante: dados apagados.",
                      "A servidora Ana Paula Souza clicou no link malicioso.", "O sistema é 100% seguro.", "Declaro encerrado.",
                      "Não há dúvida. Estamos em conformidade."):
            self.assertTrue(erros(frase), frase)

    def test_negacao_legitima_passa(self):
        for frase in ("Não afirmamos que o órgão está em conformidade com a LGPD.",
                      "O órgão não está em conformidade com a LGPD em todos os pontos.",
                      "Não informe sua senha a ninguém.",
                      "Nós nunca pedimos que você informe sua senha.",
                      "Não vou escrever que o risco é zero.",
                      "Não vou apontar culpados: a apuração é feita por sindicância.",
                      "Com comprovação, o controlador pode concluir que não há risco ou dano relevante.",
                      "Conclusão do controlador [PREENCHER]: ausência de risco ou dano relevante, pelos fatos do item II.",
                      "Comunicação no prazo: não houve demora."):
            self.assertEqual(erros(frase), [], frase)

    def test_citacoes(self):
        self.assertTrue(erros("LGPD, art. 99."))
        self.assertTrue(erros("Res. CD/ANPD 15/2024, art. 21."))
        self.assertTrue(erros("Decreto 99.999/2026 obriga."))
        self.assertEqual(erros("Decreto 99.999/2026: não verificado."), [])
        self.assertEqual(erros("LGPD, art. 48, § 3º."), [])
        self.assertEqual(erros("Decreto 12.572/2025, art. 12, I; Lei 8.112/1990, art. 143."), [])
        self.assertIn("art. 7º,", " ".join(erros("LGPD, art. 7.")))

    def test_decreto_revogado(self):
        self.assertTrue(erros("Base: Decreto 9.637/2018, art. 17."))
        self.assertEqual(erros("O Decreto 9.637/2018 foi revogado pelo Decreto 12.572/2025."), [])

    def test_titular_antiphishing_e_restrito(self):
        texto = (EX / "01-ransomware-saude" / "aviso_titulares.md").read_text(encoding="utf-8")
        for vaz in ("Clique no link e informe sua senha.", "O servidor 192.0.2.10 foi atacado.", "Falha CVE-0000-0000.",
                    "Não há motivo para preocupação."):
            self.assertTrue(cc.conferir(texto + "\n" + vaz + "\n", "titular")[0], vaz)

    def test_anpd_item_faltando(self):
        texto = (EX / "01-ransomware-saude" / "comunicacao_anpd.md").read_text(encoding="utf-8")
        e, _ = cc.conferir(re.sub(r"(?i)encarregad\w*", "pessoa", texto), "anpd")
        self.assertTrue(e)

    def test_dado_pessoal(self):
        self.assertTrue(erros("Titular: CPF " + CPF_FICTICIO + "."))

    def test_cli_plural_e_modo_invalido(self):
        rc, out = rodar(cc.main, tmp("Texto [PREENCHER] sem nada.\n" + AVISO))
        self.assertIn("0 erros, 1 aviso", out)
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            rodar(cc.main, "--modo", "xyz", tmp("a"))


class Evals(unittest.TestCase):
    def test_estrutura(self):
        ev = json.loads((AQUI / "evals.json").read_text(encoding="utf-8"))["evals"]
        self.assertGreaterEqual(len(ev), 15)
        self.assertEqual(len({c["id"] for c in ev}), len(ev))
        self.assertIn("inc-14-acusar-servidor", {c["id"] for c in ev})
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
        with tempfile.TemporaryDirectory(dir=_TMP.name) as d:
            for c in json.loads((AQUI / "evals.json").read_text(encoding="utf-8"))["evals"]:
                Path(d, c["id"] + ".md").write_text("Não precisa comunicar. O risco é zero e estamos em conformidade. "
                                                    "O servidor Carlos foi o culpado.", encoding="utf-8")
            self.assertEqual(rodar_evals.rodar(Path(d), AQUI / "evals.json")["passou"], 0)


class Documentacao(unittest.TestCase):
    def test_licenca_mit_completa(self):
        t = (SKILL / "LICENSE.txt").read_text(encoding="utf-8")
        self.assertIn("OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.", t)
        self.assertIn("CC BY-ND 3.0", t)

    def test_sem_arquivos_de_trabalho_nem_caminho_local(self):
        for arq in SKILL.rglob("*"):
            self.assertFalse(arq.name.startswith("_") and arq.suffix == ".md", arq.name)
            if arq.is_file() and arq.suffix in (".md", ".json", ".txt"):
                self.assertNotIn("/workspace/", arq.read_text(encoding="utf-8").replace("/workspace/aud/", ""), arq.name)

    def test_aviso_ia_por_extenso_e_termo_embutida(self):
        for arq in list(SKILL.rglob("*.md")):
            t = arq.read_text(encoding="utf-8")
            self.assertNotIn("apoio de IA", t, arq.name)
            self.assertNotRegex(t, r"(?i)instru[cç][oõ]es? escondid", arq.name)

    def test_regra_nao_acusar(self):
        t = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for termo in ("Não acuse ninguém", "sindicância", "Lei 8.112/1990, art. 143", "art. 52, § 3º"):
            self.assertIn(termo, t)


if __name__ == "__main__":
    unittest.main(verbosity=1)
