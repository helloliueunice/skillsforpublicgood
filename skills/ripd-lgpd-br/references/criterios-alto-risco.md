# Necessidade do RIPD e critérios de alto risco

Use este arquivo na etapa 3 do fluxo. O resultado vai para a seção "2. Necessidade do RIPD".

## Sumário
1. Quando o RIPD é exigível ou recomendado
2. Regra do alto risco (parâmetro indicado pela ANPD: Res. CD/ANPD 2/2022, art. 4º)
3. Perguntas para cada critério, com exemplos do setor público
4. Situações especiais
5. Como registrar a análise

## 1. Quando o RIPD é exigível ou recomendado

| Situação | Fundamento | Efeito |
|---|---|---|
| A ANPD determinou a elaboração | LGPD, art. 38 | Exigível; observar prazo e forma pedidos pela ANPD |
| A ANPD solicitou a publicação a órgão público | LGPD, art. 32 ("poderá solicitar") | Atender à solicitação (ver `versao-publica.md`) |
| Tratamento baseado em legítimo interesse e a ANPD pediu | LGPD, art. 10, § 3º | Exigível quando solicitado |
| Segurança pública, defesa, segurança do Estado, investigação | LGPD, art. 4º, III, e § 3º | Regime próprio; a ANPD deve solicitar RIPD. Confirme com a assessoria jurídica |
| A ANPD pediu o RIPD no processo de um incidente de segurança | Res. CD/ANPD 15/2024, art. 8º (orientação regulatória) `[CONFERIR]` | Atender ao pedido no prazo fixado pela ANPD |
| Alto risco pelo art. 4º da Res. CD/ANPD 2/2022 | Orientação da ANPD (perguntas e respostas sobre o RIPD): a resolução serve de parâmetro, no que couber `[CONFERIR]` | Recomendado (orientação da ANPD) `[CONFERIR]` |
| Outro fator de alto risco identificado pelo controlador | Orientação da ANPD: os critérios do art. 4º não são exaustivos `[CONFERIR]` | Recomendado (orientação da ANPD) `[CONFERIR]` |
| Dois ou mais fatores sem a combinação geral + específico | Guia de RIPD do PPSI 2.0, seção 3.1 (boa prática) | Recomendado como boa prática |
| Nenhum dos casos acima | LGPD, art. 6º, X, e art. 50, § 2º, I, d | Opcional, por decisão do controlador. Registre a análise |

Nunca escreva que o órgão está "dispensado" do RIPD: a ANPD pode determinar a elaboração a qualquer
tempo (art. 38). Escreva "alto risco não caracterizado pelos critérios informados".

## 2. Regra do alto risco

A Res. CD/ANPD 2/2022 aprova o regulamento de aplicação da LGPD para **agentes de tratamento de
pequeno porte**. Ela não rege órgão público: enquanto não houver regulamento específico do RIPD, a
ANPD indica usar o conceito de alto risco do seu art. 4º como **parâmetro, no que couber**
(perguntas e respostas sobre o RIPD). Cite-a como orientação, com `[CONFERIR]`, nunca como
fundamento legal. O fundamento legal do RIPD é a LGPD (art. 5º, XVII, e art. 38).

Pelo parâmetro, há alto risco quando o tratamento atende a **pelo menos um critério geral e a pelo
menos um critério específico** (art. 4º). Esses critérios **não são exaustivos**: segundo a ANPD, o
controlador pode verificar alto risco em situações diferentes das indicadas. Por isso a triagem tem
um sétimo item, "outro fator de alto risco identificado pelo controlador".

- Gerais: (a) larga escala; (b) pode afetar significativamente interesses e direitos fundamentais.
- Específicos: (a) tecnologia emergente ou inovadora; (b) vigilância ou controle de zona acessível ao
  público; (c) decisão tomada unicamente com base em tratamento automatizado, inclusive perfis;
  (d) dados sensíveis ou de crianças, adolescentes e idosos.

Rode `scripts/triagem_alto_risco.py` com as respostas. Resposta "não sei" fica `null` e o script
mostra se ela pode mudar o resultado.

## 3. Perguntas para cada critério

| Critério | Pergunte | Exemplos no setor público (ilustrativos) |
|---|---|---|
| Larga escala (§ 1º) | Quantos titulares? Que volume de dados? Por quanto tempo, com que frequência e em que área? | Cadastro de programa social estadual; matrícula de toda a rede municipal; sistema nacional de agendamento |
| Afetar direitos (§ 2º) | O tratamento pode impedir um direito ou o acesso a um serviço? Pode causar discriminação, dano à imagem, fraude ou roubo de identidade? | Concessão ou corte de benefício; seleção para vaga em creche; fiscalização com sanção |
| Tecnologia emergente | Há inteligência artificial, aprendizado de máquina, biometria, reconhecimento facial, internet das coisas (IoT)? | Assistente virtual (*chatbot*) de atendimento que lê documentos; triagem por modelo de linguagem |
| Vigilância de zona pública | Há câmeras, leitura de placas ou monitoramento em espaço aberto ao público? | Videomonitoramento de praças, terminais e escolas |
| Decisão automatizada | Alguma decisão sai do sistema sem revisão humana? Há pontuação, ranqueamento ou perfil? | Indeferimento automático por cruzamento de bases; nota de risco de fraude |
| Sensíveis ou vulneráveis | Há saúde, biometria, raça/cor, religião, deficiência? Há crianças, adolescentes ou idosos? | Prontuário, laudo de deficiência, cor/raça no cadastro, dados de alunos |
| Outro fator (o rol não é exaustivo) | Há algo que, mesmo fora dos seis critérios, possa gerar alto risco ao titular? | Cruzamento de bases de órgãos diferentes; dado de localização contínua; público em situação de rua |

Os exemplos não substituem a análise: o mesmo sistema pode ou não ser de larga escala conforme o
número de titulares, a duração e a área. Justifique cada "sim" e cada "não" com fatos do tratamento.

Para achar sinais na descrição antes de responder, rode `scripts/sinais_risco.py`. O script só
aponta palavras; quem responde é a equipe.

## 4. Situações especiais

- **Crianças e adolescentes:** o melhor interesse prevalece (LGPD, art. 14). As hipóteses dos arts. 7º
  ou 11 podem ser usadas (Enunciado CD/ANPD 1/2023). O ECA Digital (Lei 15.211/2025) está vigente
  desde 17/03/2026; seus artigos não foram verificados por esta skill: marque "não verificado".
- **Um RIPD por finalidade:** um relatório por projeto ou processo com a mesma finalidade. Operações
  parecidas em natureza, finalidade e riscos podem ficar no mesmo RIPD. Controladores diferentes que
  compartilham plataforma podem precisar de RIPDs próprios (perguntas e respostas da ANPD).
- **Momento:** antes de iniciar o tratamento. Se o tratamento já existe, faça agora e registre isso.
- **Incidente em curso** não se resolve no RIPD: acione o plano de resposta a incidentes (LGPD, art. 48).
  No processo do incidente, a ANPD pode pedir o RIPD (Res. CD/ANPD 15/2024, art. 8º) `[CONFERIR]`.
- **Dados biométricos:** a ação 4 da agenda regulatória da ANPD (dados biométricos) está em andamento
  `[CONFERIR]`; reconfira antes de afirmar que não há regulamento.

## 5. Como registrar a análise

Na seção 2 do RIPD, inclua uma tabela com os seis critérios e o outro fator, a resposta (sim, não,
não verificável) e a justificativa factual, mais o motivo da elaboração (ANPD, alto risco, boa
prática ou decisão do controlador). Se o controlador integrar o SISP, diga que o formato segue o
Modelo de RIPD do PPSI 2.0.
