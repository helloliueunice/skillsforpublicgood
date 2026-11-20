#!/usr/bin/env python3
"""Reconferência das fontes e das datas de revisão das skills (manutenção).

Offline por padrão: sem --rede, não acessa a internet. Lê só arquivos do repositório e
nunca altera as skills; quem atualiza conteúdo é a pessoa mantenedora, depois de conferir.

Uso:
    python3 tools/reconferir_fontes.py [--skill NOME] [--hoje AAAA-MM-DD] [--json]
    python3 tools/reconferir_fontes.py --rede [--gravar] [--skill NOME]

Sem --rede (offline), para cada skill que tem metadata.proxima_revisao no SKILL.md:
  - mostra versão, data de revisão e próxima revisão, e se a revisão está vencida;
  - confere se metadata.version = metadata.versao e se o CHANGELOG.md tem a versão;
  - lista as URLs de fontes citadas em SKILL.md e references/.
Com --rede (só quando você pedir):
  - baixa cada URL (GET, tempo-limite de 20 s, até 5 MB) e compara o SHA-256 com o último
    retrato salvo em tools/fontes_retrato.json ("igual", "mudou", "nova", "erro");
  - com --gravar, salva o novo retrato. Página que "mudou" pede reconferência humana: muitas
    páginas mudam por motivo cosmético; a norma só muda se o texto do dispositivo mudar.

Códigos de saída: 0 em dia e coerente; 1 revisão vencida, incoerência ou fonte com erro;
2 erro de uso.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILLS = RAIZ / "skills"
RETRATO = RAIZ / "tools" / "fontes_retrato.json"
URL = re.compile(r"https?://[^\s)\"'<>`|\]]+")
LIMITE_BYTES = 5 * 1024 * 1024


def metadados(skill_md: Path) -> dict:
    """Pares chave: valor do bloco metadata do frontmatter (só strings simples)."""
    t = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    meta, dentro = {}, False
    for linha in (m.group(1) if m else "").splitlines():
        if linha.startswith("metadata:"):
            dentro = True
            continue
        if dentro and linha.startswith("  "):
            k, _, v = linha.strip().partition(":")
            meta[k.strip()] = v.strip().strip('"')
        elif dentro:
            dentro = False
    return meta


def urls_da_skill(pasta: Path) -> list[str]:
    arquivos = [pasta / "SKILL.md"] + sorted((pasta / "references").glob("*.md")) + \
        sorted((pasta / "references").glob("*.json"))
    achadas = set()
    for arq in arquivos:
        if arq.is_file():
            for u in URL.findall(arq.read_text(encoding="utf-8")):
                achadas.add(u.rstrip(".,;:").split("#", 1)[0])  # sem âncora: uma página, um download
    return sorted(achadas)


def conferir_skill(pasta: Path, hoje: dt.date) -> dict:
    meta = metadados(pasta / "SKILL.md")
    r = {"skill": pasta.name, "versao": meta.get("version"), "revisado_em": meta.get("revisado_em"),
         "proxima_revisao": meta.get("proxima_revisao"), "problemas": [], "urls": urls_da_skill(pasta)}
    try:
        prox = dt.date.fromisoformat(meta["proxima_revisao"])
        r["dias_para_revisao"] = (prox - hoje).days
        if prox < hoje:
            r["problemas"].append(f"revisão vencida desde {prox.isoformat()}")
    except (KeyError, ValueError):
        r["problemas"].append("metadata.proxima_revisao ausente ou fora do formato AAAA-MM-DD")
    if meta.get("versao") and meta.get("version") != meta.get("versao"):
        r["problemas"].append(f"metadata.version ({meta.get('version')}) difere de metadata.versao ({meta.get('versao')})")
    changelog = pasta / "CHANGELOG.md"
    if not changelog.is_file() or f"## [{meta.get('version')}]" not in changelog.read_text(encoding="utf-8"):
        r["problemas"].append(f"CHANGELOG.md sem a seção da versão {meta.get('version')}")
    return r


def baixar(url: str, tempo: int = 20) -> dict:
    """GET da URL; devolve status, tamanho e SHA-256 (ou o erro). Aceita file:// para testes."""
    req = urllib.request.Request(url, headers={"User-Agent": "reconferir_fontes/1.0 (skills abertas; manutencao)"})
    try:
        with urllib.request.urlopen(req, timeout=tempo) as resp:  # noqa: S310 (URL vem das fontes da skill)
            corpo = resp.read(LIMITE_BYTES + 1)
            return {"status": getattr(resp, "status", 200), "bytes": len(corpo),
                    "sha256": hashlib.sha256(corpo[:LIMITE_BYTES]).hexdigest()}
    except Exception as e:  # rede, TLS, HTTP 4xx/5xx: tudo vira "erro" no relatório
        return {"erro": f"{type(e).__name__}: {e}"}


def comparar(url: str, atual: dict, retrato: dict) -> str:
    if "erro" in atual:
        return "erro"
    anterior = retrato.get(url)
    if not anterior:
        return "nova"
    return "igual" if anterior.get("sha256") == atual["sha256"] else "mudou"


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        print(__doc__)
        return 0
    conhecidas = {"--rede", "--gravar", "--json", "--skill", "--hoje"}
    hoje, filtro = dt.date.today(), None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a not in conhecidas:
            print(f"Opção desconhecida: {a}\n{__doc__}", file=sys.stderr)
            return 2
        if a in ("--skill", "--hoje"):
            if i + 1 >= len(argv):
                print(f"{a} pede um valor", file=sys.stderr)
                return 2
            try:
                if a == "--hoje":
                    hoje = dt.date.fromisoformat(argv[i + 1])
                else:
                    filtro = argv[i + 1]
            except ValueError:
                print("--hoje deve estar no formato AAAA-MM-DD", file=sys.stderr)
                return 2
            i += 1
        i += 1
    if "--gravar" in argv and "--rede" not in argv:
        print("--gravar só faz sentido com --rede", file=sys.stderr)
        return 2
    pastas = [p for p in sorted(SKILLS.iterdir()) if (p / "SKILL.md").is_file()
              and "proxima_revisao" in metadados(p / "SKILL.md") and (filtro is None or p.name == filtro)]
    if not pastas:
        print("Nenhuma skill com metadata.proxima_revisao encontrada.", file=sys.stderr)
        return 2
    relatorio = [conferir_skill(p, hoje) for p in pastas]
    problemas = sum(len(r["problemas"]) for r in relatorio)

    if "--rede" in argv:
        retrato = json.loads(RETRATO.read_text(encoding="utf-8")) if RETRATO.is_file() else {}
        novo = dict(retrato)
        for r in relatorio:
            r["fontes"] = []
            for u in r["urls"]:
                atual = baixar(u)
                situacao = comparar(u, atual, retrato)
                problemas += situacao == "erro"
                r["fontes"].append({"url": u, "situacao": situacao, **atual})
                if "erro" not in atual:
                    novo[u] = {"sha256": atual["sha256"], "bytes": atual["bytes"], "data": hoje.isoformat()}
        if "--gravar" in argv:
            RETRATO.write_text(json.dumps(novo, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if "--json" in argv:
        print(json.dumps({"hoje": hoje.isoformat(), "skills": relatorio}, ensure_ascii=False, indent=2))
    else:
        print(f"Reconferência de fontes – {hoje.strftime('%d/%m/%Y')} ({'com rede' if '--rede' in argv else 'offline, sem rede'})")
        for r in relatorio:
            dias = r.get("dias_para_revisao")
            prazo = f"faltam {dias} dias" if dias is not None and dias >= 0 else "VENCIDA"
            print(f"\n== {r['skill']} {r['versao']}: revisada em {r['revisado_em']}; próxima revisão {r['proxima_revisao']} ({prazo})")
            print(f"   {len(r['urls'])} URLs de fontes em SKILL.md e references/")
            for f in r.get("fontes", []):
                if f["situacao"] != "igual":
                    print(f"   [{f['situacao']}] {f['url']}" + (f" – {f['erro']}" if "erro" in f else ""))
            for p in r["problemas"]:
                print(f"   PROBLEMA: {p}")
        print("\nSe algo mudou: confira o dispositivo na fonte oficial, atualize references/,"
              " rode os testes, suba a versão e registre no CHANGELOG.md.")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
