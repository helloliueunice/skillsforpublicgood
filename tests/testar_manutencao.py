#!/usr/bin/env python3
"""Testa tools/reconferir_fontes.py e os arquivos de manutenção das skills, sem rede.

Uso: python3 tests/testar_manutencao.py   (0 = passou; 1 = falhou)
"""
import contextlib
import hashlib
import io
import sys
import tempfile
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))
import reconferir_fontes as rf  # noqa: E402

falhas = []
# Skills com metadata.proxima_revisao e a versão esperada de cada uma.
SKILLS_COM_REVISAO = {"incidente-dados-lgpd-br": "1.1.0-rc", "ripd-lgpd-br": "1.1.0-rc"}


def rodar(args):
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(io.StringIO()):
        rc = rf.main(args)
    return rc, saida.getvalue()


# 1. Offline de verdade: qualquer tentativa de rede faz o teste falhar.
original = urllib.request.urlopen


def proibido(*a, **k):
    raise AssertionError("acesso à rede sem --rede")


urllib.request.urlopen = proibido
try:
    rc, out = rodar(["--hoje", "2026-11-21"])
    if rc != 0:
        falhas.append(f"offline em dia deveria sair 0; saiu {rc}:\n{out}")
    for skill in SKILLS_COM_REVISAO:
        if skill not in out:
            falhas.append(f"relatório offline sem a skill {skill}")
    rc, out = rodar(["--hoje", "2027-06-01"])
    if rc != 1 or "VENCIDA" not in out:
        falhas.append("revisão vencida deveria sair 1 e mostrar VENCIDA")
    if rodar(["--gravar"])[0] != 2 or rodar(["--opcao-falsa"])[0] != 2 or rodar(["--hoje", "20/11/2026"])[0] != 2:
        falhas.append("erros de uso deveriam sair com código 2")
finally:
    urllib.request.urlopen = original
print("ok  reconferência offline (sem rede, datas, erros de uso)" if not falhas else "..  reconferência offline")

# 2. Coerência das skills: version = versao e CHANGELOG com a versão.
for skill, esperada in SKILLS_COM_REVISAO.items():
    r = rf.conferir_skill(RAIZ / "skills" / skill, rf.dt.date(2026, 11, 21))
    falhas += [f"{skill}: {p}" for p in r["problemas"]]
    if r["versao"] != esperada:
        falhas.append(f"{skill}: versão {r['versao']} (esperada {esperada})")
    if len(r["urls"]) < 5:
        falhas.append(f"{skill}: poucas URLs de fontes encontradas ({len(r['urls'])})")
print("ok  coerência de versão e CHANGELOG" if not falhas else "..  coerência")

# 2b. description: gatilhos nos primeiros 200 caracteres, "Não use" e no máximo 1024 caracteres.
import re  # noqa: E402
for skill in SKILLS_COM_REVISAO:
    t = (RAIZ / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
    desc = re.search(r"^description: (.*)$", t, re.M).group(1)
    pos = re.search(r"\bUse (ao|quando)\b", desc)
    if not pos or pos.start() > 200 or "Não use" not in desc or len(desc) > 1024:
        falhas.append(f"{skill}: description fora do padrão (Use em {pos.start() if pos else None}, {len(desc)} caracteres)")
print("ok  description (gatilhos no início, limites, até 1024)" if not falhas else "..  description")

# 3. Caminho de rede testado com file:// (não sai da máquina).
with tempfile.TemporaryDirectory() as tmp:
    arq = Path(tmp) / "fonte.html"
    arq.write_bytes(b"<html>lei</html>")
    url = arq.as_uri()
    r = rf.baixar(url)
    if r.get("sha256") != hashlib.sha256(b"<html>lei</html>").hexdigest():
        falhas.append(f"baixar(file://) não devolveu o SHA-256 esperado: {r}")
    if rf.comparar(url, r, {}) != "nova" or rf.comparar(url, r, {url: {"sha256": r["sha256"]}}) != "igual" \
            or rf.comparar(url, r, {url: {"sha256": "x"}}) != "mudou" or rf.comparar(url, {"erro": "x"}, {}) != "erro":
        falhas.append("comparar() com situação inesperada")
    if "erro" not in rf.baixar((Path(tmp) / "nao-existe.html").as_uri()):
        falhas.append("baixar() deveria relatar erro para arquivo inexistente")
print("ok  comparação de retratos (file://, sem internet)" if not falhas else "..  retratos")

for f in falhas:
    print("FALHA:", f)
print(f"{len(falhas)} falha(s)")
sys.exit(1 if falhas else 0)
