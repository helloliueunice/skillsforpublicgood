# Exemplos

Três casos **fictícios**. As conclusões dos scripts são indicativas: a decisão é do controlador. Nenhum dado é de pessoa real; o e-mail usa o domínio reservado
`example.org`. Cada caso mostra a entrada da equipe e a saída esperada da skill.

| Caso | O que mostra | Arquivos | Conferência |
|---|---|---|---|
| 01. Ransomware no agendamento da Saúde municipal | Indicativo de risco ou dano relevante: dados sensíveis, de crianças, adolescentes e idosos, sob sigilo e em larga escala; bilhete do atacante pedindo silêncio; operador; nenhum fato além do relato | `descricao.md`, `triagem.json`, `comunicacao_anpd.md`, `aviso_titulares.md` | `--modo anpd` e `--modo titular`: 0 erros |
| 02. E-mail ao destinatário errado | Critérios do art. 5º não preenchidos pelas respostas (idosos pendente); registro obrigatório com a conclusão do controlador | `triagem.json`, `registro.md` | `--modo registro`: 0 erros |
| 03. Notebook criptografado furtado (Instituto Federal) | Dados ininteligíveis (LGPD, art. 48, § 3º): avaliar com o encarregado, sem deixar de comunicar por conta própria; comunicação ao titular (o estudante) | `triagem.json`, `saida.md` | `--modo parcial`: 0 erros |

Como reproduzir (na pasta da skill):

```bash
python3 scripts/triagem_incidente.py examples/01-ransomware-saude/triagem.json
python3 scripts/prazos_incidente.py --conhecimento 18/11/2026 --hoje 20/11/2026
python3 scripts/conferir_comunicacao.py --modo anpd examples/01-ransomware-saude/comunicacao_anpd.md
python3 scripts/conferir_comunicacao.py --modo titular examples/01-ransomware-saude/aviso_titulares.md
python3 scripts/triagem_incidente.py examples/02-email-destinatario-errado/triagem.json
python3 scripts/conferir_comunicacao.py --modo registro examples/02-email-destinatario-errado/registro.md
python3 scripts/triagem_incidente.py examples/03-notebook-criptografado/triagem.json
python3 scripts/prazos_incidente.py --conhecimento 19/11/2026
```

Os prazos dos casos 01 e 03 consideram 20/11/2026 feriado nacional (Lei 14.759/2023) e não
consideram feriados municipais, que a equipe deve informar com `--feriados`.
Os `[PREENCHER]` e `[CONFERIR]` que sobram são intencionais: mostram o que a skill não pode inventar.
