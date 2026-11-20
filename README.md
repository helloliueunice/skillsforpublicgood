# Skills abertas para o bem público

Skills de IA abertas (licença MIT) para a gestão pública brasileira, no padrão aberto [Agent Skills](https://agentskills.io/specification): uma pasta com `SKILL.md`, referências, scripts, exemplos e avaliações. Funcionam em agentes compatíveis com o padrão, como Claude, Codex, Copilot, Cursor e Grok Build.

## Skills

| Skill | O que faz | Situação |
|---|---|---|
| [`ripd-lgpd-br`](skills/ripd-lgpd-br/SKILL.md) | Faz a triagem e a minuta do Relatório de Impacto à Proteção de Dados Pessoais (RIPD) de órgãos públicos: alto risco pelo parâmetro indicado pela Agência Nacional de Proteção de Dados (ANPD) (Res. CD/ANPD 2/2022, art. 4º, com [CONFERIR]) e outro fator, conteúdo mínimo do art. 38 da Lei Geral de Proteção de Dados Pessoais (LGPD), princípios, direitos, matriz de riscos ao titular e versão pública, com correspondência com o Modelo do PPSI 2.0, sem aprovar nem declarar conformidade | 1.1.0-rc |

## ripd-lgpd-br em resumo

- **Base:** 53 itens de 17 normas e orientações em `references/normas.json`, 51 conferidos em 20/11/2026 (Planalto, gov.br/ANPD, gov.br/governodigital, Diário Oficial); 2 marcados como não verificados.
- **Salvaguardas:** não aprova, não declara conformidade nem licitude, não afirma dispensa de RIPD; ignora instruções embutidas em documentos; não repete dados de pessoas reais; versão pública sem detalhes técnicos de segurança. A publicação do RIPD é decisão do controlador; a minuta registra a orientação da ANPD e a divergência com a LGPD, art. 32.
- **Testes:** `python3 skills/ripd-lgpd-br/evals/testes.py` (49 testes, só biblioteca padrão, sem rede) e `python3 skills/ripd-lgpd-br/evals/rodar_evals.py skills/ripd-lgpd-br/evals/referencia` (13 casos).
- **Limite:** os casos de avaliação e os pedidos de acionamento ainda não foram rodados em modelos reais.

## Como usar

1. Copie a pasta `skills/ripd-lgpd-br/` para a pasta de skills do seu agente (por exemplo, `.agents/skills/`, `.claude/skills/` ou `.grok/skills/`).
2. Peça, por exemplo: "precisamos de RIPD para o novo sistema de matrícula?" ou "monte a minuta do RIPD a partir desta descrição".
3. Uso direto dos scripts: veja `skills/ripd-lgpd-br/README.md`.

## Testes

```bash
python3 tests/validar_skill.py      # frontmatter, boas práticas, referências, evals, segurança
python3 tests/testar_manutencao.py  # reconferência de fontes offline, versões e CHANGELOG
python3 skills/ripd-lgpd-br/evals/testes.py
python3 skills/ripd-lgpd-br/evals/rodar_evals.py skills/ripd-lgpd-br/evals/referencia
```

Validador de referência da [especificação Agent Skills](https://agentskills.io/specification) (opcional, pacote [`skills-ref`](https://github.com/agentskills/agentskills/tree/main/skills-ref)): `pip install skills-ref==0.1.1` e `agentskills validate skills/ripd-lgpd-br`.

## Manutenção

- Cada skill tem `CHANGELOG.md` e, no `SKILL.md`, `metadata.revisado_em` e `metadata.proxima_revisao` (revisão a cada 6 meses).
- `python3 tools/reconferir_fontes.py` confere, sem rede, datas de revisão e coerência de versões, e lista as fontes. Com `--rede` (só quando você pedir), baixa as fontes e compara com o último retrato.
- Como contribuir e política de atualização: [CONTRIBUTING.md](CONTRIBUTING.md).

## Créditos e licença

MIT, © 2026 Eunice Liu. Avisos de terceiros em [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
