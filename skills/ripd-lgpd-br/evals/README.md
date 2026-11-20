# Avaliação da skill

| Arquivo | Para quê |
|---|---|
| `evals.json` | 13 casos com prompt, expectativas (leitura humana) e asserções mecânicas |
| `referencia/` | Respostas de referência escritas pela autora; passam em todas as asserções |
| `arquivos/` | Entradas fictícias dos casos (inventário com instrução embutida, matriz de riscos) |
| `acionamento.json` | 12 prompts que devem acionar a skill e 12 que não devem |
| `rodar_evals.py` | Confere uma pasta de respostas (`<id>.md`) contra as asserções |
| `testes.py` | Testes unitários dos scripts, dos exemplos e das avaliações |

```bash
python3 evals/testes.py                      # testes dos scripts, exemplos e evals
python3 evals/rodar_evals.py evals/referencia # confere as respostas de referência
python3 evals/rodar_evals.py PASTA_DO_AGENTE  # confere respostas de um agente
```

**Limite honesto:** os casos e os prompts de acionamento **ainda não foram rodados em modelos
reais**. As respostas de referência foram escritas à mão para provar que as asserções são
alcançáveis; não medem a qualidade de um agente. As asserções são mecânicas e não substituem a
leitura das expectativas por alguém que conheça a LGPD.

Tipos de asserção: `contem`, `nao_contem`, `regex`, `nao_regex` e `conferir` (roda
`scripts/conferir_ripd.py` no modo `integral`, `publica` ou `parcial`).
