# Modelo de saída: minuta de RIPD

Use esta estrutura. Os títulos numerados são conferidos por `scripts/conferir_ripd.py`.
Preencha com fatos fornecidos pela equipe. O que faltar fica como `[PREENCHER: o que falta]`;
o que depender de validação jurídica ou técnica fica como `[CONFERIR: o quê e com quem]`.

## Sumário
1. Estrutura da minuta
2. Correspondência com a ANPD e com o PPSI 2.0
3. Aviso final obrigatório

## 1. Estrutura da minuta

```markdown
# Relatório de Impacto à Proteção de Dados Pessoais: [produto, serviço ou processo]

Versão [X.Y] · [data] · Situação: MINUTA PARA REVISÃO · Modalidade: integral (uso interno)

## 1. Identificação
Controlador, unidade responsável, encarregado (canal público), operadores, áreas e partes consultadas
(TI, jurídica, segurança da informação, ouvidoria, titulares ou especialistas), com o parecer de cada uma.

## 2. Necessidade do RIPD
Motivo (ANPD, alto risco, boa prática ou decisão do controlador) e tabela dos critérios de alto risco
(critério | sim/não/não verificável | justificativa), com os seis critérios do parâmetro indicado pela
ANPD (Res. CD/ANPD 2/2022, art. 4º [CONFERIR]) e o outro fator identificado pelo controlador, porque
os critérios não são exaustivos. Fonte: references/criterios-alto-risco.md.

## 3. Descrição do tratamento
### 3.1 Contexto e finalidades
Visão geral do serviço e cada finalidade específica, explícita e informada.
### 3.2 Ciclo de vida e fluxo
Da coleta à eliminação: quem coleta, onde guarda, quem acessa, para onde vai.
### 3.3 Dados pessoais e titulares
Tipos de dados coletados (por categoria), dados sensíveis, dados de crianças, adolescentes e idosos,
categorias de titulares, volume e número de titulares, fonte de coleta.
### 3.4 Hipóteses legais
Tabela finalidade | dados | hipótese legal (arts. 7º, 11 ou 14) | fundamento na norma do serviço | publicidade (art. 23, I).
### 3.5 Compartilhamento, operadores e transferência internacional
Com quem, para quê, base (arts. 26, 27 e 39), instrumento (contrato, acordo), e se os dados saem do país (art. 33).
Entre órgãos e entidades federais, aponte as regras do Decreto 10.046/2019 [CONFERIR]. Na transferência
internacional, aponte o mecanismo do regulamento da ANPD (Res. CD/ANPD 19/2024) e, se o destino for a
União Europeia, a Res. CD/ANPD 32/2026 [CONFERIR].
### 3.6 Retenção e eliminação
Prazo ou critério de guarda por categoria, fundamento (art. 16) e forma de eliminação.
### 3.7 Metodologia de coleta e de segurança das informações
Como os dados são coletados e quais medidas técnicas e administrativas garantem a segurança (art. 38, parágrafo único; art. 46).
Sistemas de informação envolvidos no tratamento (item "e" da lista da ANPD).
Na versão pública, só em termos gerais.

## 4. Análise dos princípios
Uma linha por princípio do art. 6º (finalidade, adequação, necessidade, livre acesso, qualidade dos
dados, transparência, segurança, prevenção, não discriminação, responsabilização e prestação de contas):
como é atendido, evidência e lacuna.

## 5. Direitos dos titulares
Como o titular exerce cada direito do art. 18 e a revisão de decisão automatizada (art. 20); canal e prazo.

## 6. Riscos ao titular
Metodologia usada (a do órgão ou a da skill), escalas e faixas, e a tabela de scripts/matriz_risco.py.

## 7. Medidas, salvaguardas e mecanismos de mitigação
Para cada risco: medidas existentes, medidas novas, responsável e prazo.

## 8. Conclusão e plano de ação
Riscos residuais e proposta de encaminhamento ao controlador: prosseguir com justificativa, mudar o
tratamento ou não prosseguir. Quem decide é o controlador.

## 9. Pendências e não verificado
Lista de [PREENCHER], [CONFERIR] e normas não verificadas, com responsável. Inclua a decisão sobre a
publicação: a LGPD, art. 32, diz que a ANPD "poderá solicitar" a publicação; a ANPD orienta que órgão
público publique o RIPD quando não houver hipótese de sigilo (LAI) [CONFERIR].

## 10. Histórico de versões e aprovação
Tabela data | versão | mudança | responsável. Espaço para manifestação do encarregado e aprovação
do representante do controlador (nome e cargo preenchidos pela equipe).

> Esta é uma minuta preparada com ajuda de inteligência artificial (IA). Não substitui a análise da
> equipe, do encarregado e da assessoria jurídica, nem declara conformidade com a LGPD. Requer revisão
> humana e aprovação do controlador.
```

Na **versão pública** (`--modo publica`), mantenha as seções 1 a 5, 8, 9 e 10 em termos gerais,
resuma as seções 3.7, 6 e 7 sem detalhes técnicos e diga que houve omissão (ver `versao-publica.md`).

## 2. Correspondência com a ANPD e com o PPSI 2.0

| Seção da minuta | Lista recomendada da ANPD (perguntas e respostas) | Modelo de RIPD do PPSI 2.0 |
|---|---|---|
| 1. Identificação | a, b | 2.3 |
| 2. Necessidade | c | 1.2 |
| 3.1 Contexto e finalidades | d, f.viii | 1.1, 2.1 |
| 3.2 Ciclo de vida | f.i | 2.1, 2.2 |
| 3.3 Dados e titulares | f.ii a f.vii | 2.1 |
| 3.4 Hipóteses legais | g | 2.1 |
| 3.5 Compartilhamento | f.ix | 2.4, 2.5 |
| 3.6 Retenção | f.x | 2.6 |
| 3.7 Metodologia e sistemas | e | 2.7 |
| 4. Princípios | h | 3.1 a 3.10 |
| 5. Direitos | não listado | 4 |
| 6. Riscos | i, j | 5.1, 5.2 |
| 7. Medidas | k | 5.3 |
| 8. Conclusão | não listado | 5.4 |
| 9. Pendências | não listado | não listado |
| 10. Histórico e aprovação | l | 6, 7 |

Órgão ou entidade do SISP: entregue no Modelo do PPSI 2.0 (baixe o arquivo oficial) e use esta minuta
como rascunho de conteúdo, transportando seção por seção conforme a tabela.

## 3. Aviso final obrigatório

Termine toda minuta com o aviso do bloco acima, sem mudar o sentido: minuta preparada com ajuda de
inteligência artificial (IA), não substitui a análise humana, não declara conformidade, requer
aprovação do controlador.
