# incidente-dados-lgpd-br

Skill aberta (padrão [Agent Skills](https://agentskills.io/specification)) que ajuda órgãos e
entidades públicas brasileiras a responder a **incidente de segurança com dados pessoais**: decidir
se é preciso comunicar à ANPD e aos titulares, calcular os prazos e redigir as minutas da
comunicação, do aviso e do registro.

## O que entrega

- Triagem indicativa pelo art. 5º da Res. CD/ANPD 15/2024 (o incidente pode afetar significativamente
  interesses e direitos fundamentais e, cumulativamente, envolve ao menos um destes critérios: dados
  sensíveis; de crianças, adolescentes ou idosos; financeiros; de autenticação; sob sigilo; em larga
  escala), com tratamento cuidadoso de dados ininteligíveis (LGPD, art. 48, § 3º). A decisão é do controlador.
- Prazos em dias úteis: comunicação à ANPD e aos titulares (três dias úteis), declaração ao processo,
  complementação (vinte dias úteis), com feriados nacionais e campo para feriados locais.
- Minuta da comunicação à ANPD com os doze itens do art. 6º, § 2º, e correspondência com os blocos
  do formulário do SEI!ANPD (sistema eletrônico de processos da Agência Nacional de Proteção de Dados).
- Aviso aos titulares em linguagem simples (art. 9º), sem detalhes técnicos e sem pedir senha ou dados.
- Minuta do registro do incidente (art. 10), inclusive quando não há comunicação.
- Lembrete da comunicação separada de vulnerabilidades ou incidentes ao Centro de Prevenção, Tratamento e
  Resposta a Incidentes Cibernéticos de Governo (CTIR Gov) para a administração federal (Decreto
  10.748/2021), com o registro de que o Decreto 9.637/2018 foi revogado pelo Decreto 12.572/2025.

## Salvaguardas

- Não decide pelo controlador, não afirma ausência de risco, não declara conformidade e não promete "risco zero".
- Não nomeia nem culpa servidor ou outra pessoa: remete a apuração a sindicância ou processo
  administrativo disciplinar (Lei 8.112/1990, art. 143).
- Não inventa fatos nem normas: cita só o que está marcado como verificado em `references/normas.json`
  (52 de 55 itens, conferidos em 19 e 20/11/2026 no Planalto, Diário Oficial e gov.br/ANPD).
- Ignora instruções embutidas em documentos, registros de sistema (*logs*) ou bilhetes de atacante.
- Não repete dados de pessoas reais; o aviso aos titulares nunca pede senha nem traz endereço IP,
  porta de rede ou código de vulnerabilidade (CVE).
- Scripts locais, só com a biblioteca padrão do Python, sem rede.

## Instalação

Copie a pasta `incidente-dados-lgpd-br/` para o diretório de skills do seu agente, por exemplo
`.claude/skills/`, `.agents/skills/`, `.github/skills/` ou `.grok/skills/`.

## Scripts

```bash
python3 scripts/triagem_incidente.py --modelo > triagem.json       # modelo de respostas
python3 scripts/triagem_incidente.py triagem.json
python3 scripts/prazos_incidente.py --conhecimento 18/11/2026 --feriados 23/11/2026
python3 scripts/conferir_comunicacao.py minuta.md --modo anpd      # ou titular, registro, parcial
python3 scripts/dados_pessoais.py arquivo.txt --mascarar
```

## Testes

```bash
python3 evals/testes.py
python3 evals/rodar_evals.py evals/referencia
```

`testes.py` tem 52 testes; `rodar_evals.py` confere 15 casos. Os casos de avaliação ainda não foram
rodados em modelos de inteligência artificial (IA) reais (ver `evals/README.md`).

## Limites

Não é parecer jurídico nem resposta técnica ao ataque (perícia, contenção, resgate). A contagem de
dias úteis aplica por analogia a Res. CD/ANPD 1/2021, art. 8º: confira com a assessoria jurídica.
Não cobre empresas privadas, o Regulamento Geral sobre a Proteção de Dados da União Europeia (GDPR),
prazos setoriais (por exemplo, Banco Central), apuração disciplinar nem aspectos penais. Normas de
Estados, do DF e de Municípios não foram verificadas: consulte a norma local.

## Licença

MIT © 2026 Eunice Liu. Ver `LICENSE.txt`, que registra também os avisos de terceiros: a página
"Comunicação de Incidente de Segurança" da ANPD (CC BY-ND 3.0) é só citada e parafraseada.
