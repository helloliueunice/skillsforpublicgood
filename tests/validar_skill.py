#!/usr/bin/env python3
"""Valida a skill: frontmatter (agentskills.io), boas práticas de autoria, referências,
evals e regras de segurança. Só biblioteca padrão.

Uso: python3 tests/validar_skill.py [nome-da-skill ...]   (código 0 = tudo certo; 1 = há erros)
Sem argumentos, valida todas as skills em skills/.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILLS = RAIZ / "skills"
erros, avisos = [], []


def erro(msg):
    erros.append(msg)


def ler_frontmatter(texto):
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    if not m:
        return None, texto
    campos, chave_atual = {}, None
    for linha in m.group(1).splitlines():
        if re.match(r"^[a-z][a-z0-9-]*:", linha):
            k, _, v = linha.partition(":")
            chave_atual = k.strip()
            campos[chave_atual] = v.strip()
        elif linha.startswith("  ") and chave_atual:
            campos[chave_atual] = (campos[chave_atual] + " " + linha.strip()).strip()
    return campos, texto[m.end():]


def validar_frontmatter(pasta, campos, corpo):
    nome = campos.get("name", "")
    desc = campos.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", nome) or len(nome) > 64:
        erro(f"{pasta.name}: name inválido '{nome}' (kebab-case, até 64, sem hífen duplo/inicial/final)")
    if nome != pasta.name:
        erro(f"{pasta.name}: name '{nome}' difere do nome da pasta")
    if not desc or len(desc) > 1024:
        erro(f"{pasta.name}: description vazia ou com mais de 1024 caracteres ({len(desc)})")
    if not re.search(r"\bUse (ao|quando|para)\b", desc):
        erro(f"{pasta.name}: description não diz quando usar ('Use ao/quando ...')")
    if re.match(r"^(Eu|Você|Vou|I |You )", desc):
        erro(f"{pasta.name}: description deve estar em 3ª pessoa")
    if "<" in desc or ">" in desc:
        erro(f"{pasta.name}: description não deve conter < ou >")
    if "compatibility" in campos and len(campos["compatibility"]) > 500:
        erro(f"{pasta.name}: compatibility com mais de 500 caracteres")
    for k, v in campos.items():
        # Valor YAML sem aspas não pode conter ": " (o parser YAML do validador oficial rejeita).
        if k != "metadata" and ": " in v and not v.startswith(('"', "'", "|", ">")):
            erro(f"{pasta.name}: valor de '{k}' contém ': ' sem aspas (YAML inválido)")
    permitidos = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    extras = set(campos) - permitidos
    if extras:
        erro(f"{pasta.name}: campos de frontmatter fora da especificação: {sorted(extras)}")
    n = len(corpo.splitlines())
    if n >= 500:
        erro(f"{pasta.name}: corpo do SKILL.md com {n} linhas (limite recomendado: 500)")


def validar_referencias(pasta, corpo):
    citados = set(re.findall(r"`((?:references|scripts|examples|evals)/[^`\s]+)`", corpo))
    for c in citados:
        alvo = pasta / c.split(" ")[0]
        if not alvo.exists():
            erro(f"{pasta.name}: SKILL.md cita '{c}', que não existe")
    for arq in (pasta / "references").glob("*"):
        if f"references/{arq.name}" not in corpo:
            erro(f"{pasta.name}: references/{arq.name} não é citado diretamente no SKILL.md (referência a 1 nível)")
    # Ferramentas de desenvolvimento podem ficar fora do SKILL.md (não ajudam na tarefa e ocupam
    # contexto), desde que documentadas no README.md ou no evals/README.md da skill.
    docs_dev = "".join(p.read_text(encoding="utf-8") for p in (pasta / "README.md", pasta / "evals" / "README.md") if p.is_file())
    for arq in (pasta / "scripts").glob("*"):
        if arq.name.startswith(("_", ".")) or arq.name == "__pycache__":
            continue
        if f"scripts/{arq.name}" not in corpo and f"scripts/{arq.name}" not in docs_dev:
            avisos.append(f"{pasta.name}: scripts/{arq.name} não citado no SKILL.md nem no README da skill")
    for md in list(pasta.rglob("*.md")) + list(pasta.rglob("*.py")) + list(pasta.rglob("*.mjs")):
        t = md.read_text(encoding="utf-8")
        if re.search(r"[A-Za-z]:\\\\|\b(?:scripts|references|examples)\\\\", t):
            erro(f"{md.relative_to(RAIZ)}: caminho no estilo Windows")


def validar_evals(pasta):
    arq = pasta / "evals" / "evals.json"
    if not arq.exists():
        erro(f"{pasta.name}: sem evals/evals.json")
        return
    ev = json.loads(arq.read_text(encoding="utf-8"))
    casos = ev if isinstance(ev, list) else next((v for v in ev.values() if isinstance(v, list) and v and isinstance(v[0], dict)), [])
    if len(casos) < 3:
        erro(f"{pasta.name}: são necessários pelo menos 3 evals (há {len(casos)})")
    for c in casos:
        for k in ("id", "prompt"):
            if not c.get(k):
                erro(f"{pasta.name}: eval {c.get('id')} sem '{k}'")
        if not any(c.get(k) for k in ("expectativas", "assercoes", "expected_output", "resultado_esperado")):
            erro(f"{pasta.name}: eval {c.get('id')} sem resultado esperado ou expectativas")
        for a in c.get("arquivos", []):
            if not (pasta / a).exists():
                erro(f"evals: caso {c['id']} cita arquivo inexistente {a}")


def validar_seguranca():
    padroes = {
        "segredo": re.compile(r"(api[_-]?key|secret|password|senha|token)\s*[:=]\s*['\"][^'\"]{8,}", re.I),
        "chave privada": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        "comando destrutivo": re.compile(r"\brm\s+-rf\b|\bmkfs\b|\bdd\s+if=|git\s+push\s+--force"),
    }
    for arq in RAIZ.rglob("*"):
        if not arq.is_file() or ".git" in arq.parts or arq.suffix in {".png", ".jpg"} or arq.name == "validar_skill.py":
            continue
        t = arq.read_text(encoding="utf-8", errors="ignore")
        for nome, rx in padroes.items():
            if rx.search(t):
                erro(f"segurança: possível {nome} em {arq.relative_to(RAIZ)}")
    for py in (SKILLS).rglob("scripts/*.py"):
        t = py.read_text(encoding="utf-8")
        if re.search(r"^\s*(import|from)\s+(urllib|requests|http\.client|socket|ftplib|smtplib)", t, re.M):
            erro(f"segurança: {py.relative_to(RAIZ)} importa biblioteca de rede")


def main():
    pedidas = sys.argv[1:]
    pastas = [p for p in sorted(SKILLS.iterdir()) if (p / "SKILL.md").exists() and (not pedidas or p.name in pedidas)]
    if not pastas:
        erro("nenhuma skill encontrada em skills/")
    for pasta in pastas:
        campos, corpo = ler_frontmatter((pasta / "SKILL.md").read_text(encoding="utf-8"))
        if campos is None:
            erro(f"{pasta.name}: SKILL.md sem frontmatter YAML")
            continue
        validar_frontmatter(pasta, campos, corpo)
        validar_referencias(pasta, corpo)
        validar_evals(pasta)
    validar_seguranca()
    for a in avisos:
        print("AVISO:", a)
    for e in erros:
        print("ERRO:", e)
    print(f"{len(erros)} erro(s), {len(avisos)} aviso(s)")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
