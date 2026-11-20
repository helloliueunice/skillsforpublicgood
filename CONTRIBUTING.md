# Como contribuir

Contribuições são bem-vindas por *issue* ou *pull request*. Escreva em português do Brasil.

## Antes de abrir um pull request

1. Mexa só na pasta da skill que você quer mudar (e, se precisar, em `tests/` ou `tools/`).
2. Toda citação de lei, decreto ou norma precisa de fonte oficial conferida, com data
   (Planalto, DOU, gov.br). Na `ripd-lgpd-br`, a citação entra em `references/normas.json`
   (com `verificado`, `conferido_em` e link) antes de aparecer no texto.
3. Não reproduza texto protegido (ABNT, ISO, documentos sob CC BY-NC-ND): cite e resuma com suas palavras.
4. Não use dados pessoais reais em exemplos, testes ou avaliações: CPF e NIS com dígito inválido,
   e-mails em `example.org` ou domínios `.test`, nomes como marcadores (`[INTERESSADO 1]`).
5. Rode os testes e o validador:

```bash
python3 tests/validar_skill.py
python3 tests/testar_manutencao.py
python3 skills/ripd-lgpd-br/evals/testes.py
python3 skills/ripd-lgpd-br/evals/rodar_evals.py skills/ripd-lgpd-br/evals/referencia
agentskills validate skills/<nome-da-skill>   # pip install skills-ref==0.1.1
```

6. Suba a versão no `SKILL.md` (`metadata.version` e `metadata.versao`) conforme o
   [Versionamento Semântico](https://semver.org/lang/pt-BR/) e registre a mudança no `CHANGELOG.md` da skill.

## Política de manutenção

- **Revisão periódica:** a cada 6 meses (`metadata.proxima_revisao`), ou antes, quando uma lei,
  norma ou orientação oficial mudar. `python3 tools/reconferir_fontes.py` avisa quando a revisão vence.
- **Fontes:** `python3 tools/reconferir_fontes.py --rede --gravar` baixa as fontes e guarda um retrato
  (SHA-256) em `tools/fontes_retrato.json`. Fonte que "mudou" exige reconferência humana do
  dispositivo citado; mudança cosmética da página não muda a skill.
- **Regulação em andamento:** quando a ANPD publicar o regulamento do RIPD ou o de compartilhamento
  de dados pelo Poder Público (agenda regulatória), atualize `normas.json`, `base-legal.md` e a versão.
- **Testes em modelos de IA:** roteiro em `skills/*/evals/README.md`. Ao rodar, registre o resultado em
  `evals/resultados/` e no `CHANGELOG.md`; não invente resultados.
