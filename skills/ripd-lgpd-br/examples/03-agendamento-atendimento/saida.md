# Triagem da necessidade de RIPD: agendamento de atendimento presencial

Caso fictício. Pedido parcial: "Precisamos de RIPD para o formulário de agendamento da Central de
Atendimento ao Cidadão? Coleta nome, e-mail, telefone, serviço desejado e horário."

## Resumo para a equipe

Pelos critérios que a ANPD indica como parâmetro (art. 4º da Res. CD/ANPD 2/2022, regulamento de
agentes de pequeno porte que, para órgão público, vale só como parâmetro, no que couber) [CONFERIR],
o alto risco não fica caracterizado: nenhum critério geral nem específico foi marcado, e a equipe não
identificou outro fator de alto risco (resultado de `scripts/triagem_alto_risco.py` sobre
`triagem.json`). Esses critérios não são exaustivos: segundo a ANPD, o controlador pode verificar alto
risco em situações diferentes das indicadas. Isso não equivale a dispensa: a ANPD pode determinar o
RIPD a qualquer tempo (LGPD, art. 38).

## Necessidade do RIPD

| Critério | Resposta | Justificativa |
|---|---|---|
| Geral: larga escala | Não | Cerca de 3 mil agendamentos por mês, só no município, guarda de 90 dias |
| Geral: afetar significativamente direitos | Não | O atendimento sem agendamento continua disponível |
| Específico: tecnologia emergente | Não | Formulário web simples |
| Específico: vigilância de zona pública | Não | Não há monitoramento |
| Específico: decisão unicamente automatizada | Não | O cidadão escolhe o horário |
| Específico: dados sensíveis ou de vulneráveis | Não | Sem campo de dado sensível; o campo livre de observações foi retirado |
| Outro fator de alto risco identificado pelo controlador | Não | O formulário não cruza dados com outros sistemas nem condiciona o atendimento |

## O que fazer mesmo assim

- Manter o registro das operações de tratamento (LGPD, art. 37).
- Publicar a informação do tratamento na página do serviço (art. 23, I) e o canal do encarregado.
- Guardar só o necessário (art. 6º, III) e eliminar após o prazo [PREENCHER: confirmar os 90 dias].
- Refazer a triagem se o formulário passar a pedir dado sensível, atender a um público vulnerável
  específico ou cruzar dados com outros sistemas.

## Pendências

- [CONFERIR: se o agendamento atende a públicos com prioridade legal (pessoa idosa, pessoa com
  deficiência) e coleta essa condição; se sim, o critério de dados de vulneráveis muda.]

> Esta é uma minuta preparada com ajuda de inteligência artificial (IA). Não substitui a análise da
> equipe, do encarregado e da assessoria jurídica, nem declara conformidade com a LGPD. Requer revisão
> humana e aprovação do controlador.
