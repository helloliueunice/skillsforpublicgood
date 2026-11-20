# Avaliações da skill

- `evals.json`: 15 casos com expectativas (leitura humana) e asserções mecânicas.
- `referencia/`: respostas de referência escritas pela autora; servem para provar que as asserções
  são satisfazíveis e para comparação. **Não foram geradas por modelo.**
- `arquivos/`: entradas fictícias usadas nos casos (inclui um relatório com instrução embutida).
- `acionamento.json`: 12 prompts que devem acionar a skill e 11 que não devem.
- `rodar_evals.py`: confere uma pasta de respostas `<id>.md` contra as asserções, sem rede.
- `testes.py`: testes unitários dos scripts, dos exemplos e destas avaliações.

```bash
python3 evals/testes.py
python3 evals/rodar_evals.py evals/referencia
python3 evals/rodar_evals.py caminho/para/respostas_do_modelo
```

**Estado:** os casos e os prompts de acionamento **ainda não foram rodados em modelos de inteligência
artificial (IA) reais**.
As asserções mecânicas não substituem a leitura das expectativas.
