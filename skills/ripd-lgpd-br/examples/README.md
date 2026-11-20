# Exemplos

Três casos **fictícios** (Município de Exemplópolis). Nenhum dado é de pessoa real; o e-mail usa o
domínio reservado `example.org`. Cada caso mostra a entrada da equipe e a saída esperada da skill.

| Caso | O que mostra | Arquivos | Conferência |
|---|---|---|---|
| 01. Sistema de gestão escolar municipal | Minuta integral completa: crianças, dado sensível, decisão automatizada (fila da creche), operador em nuvem | `descricao.md`, `triagem.json`, `riscos.csv`, `ripd.md` | `conferir_ripd.py ripd.md`: 0 erros |
| 02. Leitura de placas em vias públicas | Versão pública a partir de uma versão interna, com segurança pública como ponto de atenção | `descricao.md`, `triagem.json`, `ripd_publico.md` | `conferir_ripd.py --modo publica`: 0 erros |
| 03. Agendamento de atendimento | Só a triagem: alto risco não caracterizado, sem afirmar dispensa | `triagem.json`, `saida.md` | `conferir_ripd.py --modo parcial`: 0 erros |

Como reproduzir (na pasta da skill):

```bash
python3 scripts/sinais_risco.py examples/01-gestao-escolar-municipal/descricao.md
python3 scripts/triagem_alto_risco.py examples/01-gestao-escolar-municipal/triagem.json
python3 scripts/matriz_risco.py examples/01-gestao-escolar-municipal/riscos.csv
python3 scripts/conferir_ripd.py examples/01-gestao-escolar-municipal/ripd.md
python3 scripts/conferir_ripd.py --modo publica examples/02-videomonitoramento-placas/ripd_publico.md
python3 scripts/conferir_ripd.py --modo parcial examples/03-agendamento-atendimento/saida.md
```

`matriz_risco.py` sai com código 1 no caso 01 de propósito: restam dois riscos residuais altos, que
pedem decisão do controlador (seção 8 da minuta).

Os `[PREENCHER]` e `[CONFERIR]` que sobram são intencionais: mostram o que a skill não pode inventar.
As referências normativas foram conferidas em 20/11/2026; as normas municipais e de programas aparecem só como `[CONFERIR]`, sem número inventado.
