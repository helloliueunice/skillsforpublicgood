# Triagem: furto de notebook com dados de estudantes

Caso fictício. Pedido parcial: "Um notebook da coordenação de um campus do Instituto Federal foi
furtado do carro de um servidor em 19/11/2026. Tinha uma planilha com nome, endereço e telefone de
1.200 estudantes de 14 a 17 anos. O disco é criptografado. Precisamos comunicar?"

## Resumo para a equipe

O teste do art. 5º da Res. CD/ANPD 15/2024 [CONFERIR vigência] aponta critério presente (dados de adolescentes) e
possível afetação significativa, **mas** os dados estariam ininteligíveis para quem furtou
(criptografia integral, senha não exposta). Esse fato entra no juízo de gravidade (LGPD, art. 48,
§ 3º). Indicativo de `scripts/triagem_incidente.py`: **avaliar com o encarregado antes de deixar de
comunicar**. A decisão é do controlador.

## O que decidir e como

1. Peça à TI a **comprovação**: criptografia ativa no momento do furto, algoritmo, senha forte e
   não anotada [PREENCHER].
2. Com comprovação, o controlador pode concluir que não há risco ou dano relevante e registrar os
   motivos (Res. CD/ANPD 15/2024, art. 10, § 1º, VIII).
3. Sem comprovação, trate como dado legível: a orientação é comunicar à ANPD e aos titulares (os
   estudantes) e, por serem adolescentes, também aos pais ou responsáveis (LGPD, art. 14) [CONFERIR],
   até **25/11/2026** (três dias úteis contados de 19/11/2026: 23, 24 e 25/11, porque 20/11 é feriado nacional)
   [CONFERIR feriados locais e do DF].
4. Em qualquer caso, registre o incidente (art. 10) e informe à ANPD, se comunicar, o número de
   adolescentes (art. 6º, § 2º, II).

## Outras obrigações

- O Instituto Federal integra a administração federal autárquica. Furto de equipamento não é, em
  princípio, incidente cibernético; avalie com a equipe de resposta se houve impacto nos serviços
  que exija comunicação ao CTIR Gov (Decreto 10.748/2021, art. 12, IV) [CONFERIR].
- Avalie com a assessoria jurídica o registro de ocorrência policial do furto [CONFERIR].
- Descreva o furto de forma objetiva, sem atribuir culpa ao servidor que transportava o equipamento;
  se houver apuração, ela é feita por sindicância ou processo administrativo
  disciplinar (Lei 8.112/1990, art. 143).

## Pendências

- [CONFERIR com a assessoria jurídica a decisão final; ECA Digital (Lei 15.211/2025): deveres não verificados.]

> Esta é uma minuta preparada com ajuda de inteligência artificial (IA). Não substitui a análise da
> equipe, do encarregado e da assessoria jurídica, nem a decisão do controlador. Requer revisão humana.
