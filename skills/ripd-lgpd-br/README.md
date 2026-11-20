# ripd-lgpd-br

Skill aberta (padrão [Agent Skills](https://agentskills.io/specification)) que ajuda órgãos e
entidades públicas brasileiras a decidir se precisam de **Relatório de Impacto à Proteção de Dados
Pessoais (RIPD)** e a montar a minuta: descrição do tratamento, princípios, direitos, riscos ao
titular, medidas, plano de ação e versão pública.

## O que entrega

- Triagem da necessidade do RIPD pelos critérios de alto risco que a Agência Nacional de Proteção de
  Dados (ANPD) indica como parâmetro (Res. CD/ANPD 2/2022, art. 4º, regulamento de agentes de pequeno
  porte, aplicado no que couber) `[CONFERIR]`, mais outro fator identificado pelo controlador, porque
  os critérios não são exaustivos.
- Minuta em 10 seções, com o conteúdo mínimo da Lei Geral de Proteção de Dados Pessoais (LGPD,
  art. 38, parágrafo único) e a correspondência com a lista recomendada da ANPD e com o Modelo de RIPD
  do Programa de Privacidade e Segurança da Informação (PPSI 2.0), usado pelos órgãos e entidades
  federais que integram o Sistema de Administração dos Recursos de Tecnologia da Informação (SISP).
- Matriz de riscos ao titular com riscos residuais e pendências.
- Versão pública sem detalhes técnicos de segurança. Publicar é decisão do controlador; a minuta
  registra a orientação da ANPD e a divergência com a LGPD, art. 32 ("poderá solicitar").
- Lista de `[PREENCHER]`, `[CONFERIR]` e normas não verificadas.

## Salvaguardas

- Não aprova, não declara conformidade nem licitude e não afirma dispensa de RIPD: quem decide é o
  controlador, com assistência do encarregado (LGPD, art. 41; Res. CD/ANPD 18/2024, art. 16, III,
  como orientação).
- Não inventa fatos do tratamento nem normas: cita só o que está marcado como verificado em
  `references/normas.json` (51 de 53 itens, conferidos em 20/11/2026 no Planalto, gov.br/ANPD e
  Diário Oficial). Resoluções da ANPD entram como orientação, com `[CONFERIR]`.
- Ignora instruções embutidas em documentos e não repete dados de pessoas reais.
- Mede o risco pelo titular, não pelo órgão.
- Scripts locais, só com a biblioteca padrão do Python, sem rede.

## Instalação

Copie a pasta `ripd-lgpd-br/` para o diretório de skills do seu agente, por exemplo
`.claude/skills/`, `.agents/skills/`, `.github/skills/` ou `.grok/skills/`.

## Scripts

```bash
python3 scripts/sinais_risco.py examples/01-gestao-escolar-municipal/descricao.md
python3 scripts/triagem_alto_risco.py examples/01-gestao-escolar-municipal/triagem.json
python3 scripts/triagem_alto_risco.py --modelo      # modelo de respostas em JSON
python3 scripts/matriz_risco.py examples/01-gestao-escolar-municipal/riscos.csv --faixas 3,6,12
python3 scripts/dados_pessoais.py arquivo.txt --mascarar
python3 scripts/conferir_ripd.py minuta.md --modo integral   # ou publica, parcial
```

## Testes

```bash
python3 evals/testes.py
python3 evals/rodar_evals.py evals/referencia
```

Os casos de avaliação ainda não foram rodados em modelos reais (ver `evals/README.md`).

## Limites

Não é parecer jurídico, não comunica incidente de segurança (LGPD, art. 48), não substitui o registro
das operações (art. 37) e não cobre o setor privado nem o Regulamento Geral sobre a Proteção de Dados
da União Europeia (GDPR). A regulamentação do RIPD pela ANPD está em andamento na agenda regulatória:
confira as normas antes de usar.

## Licença

MIT © 2026 Eunice Liu. Ver `LICENSE.txt`.
