# Versão pública do RIPD

Use na etapa 9 quando o órgão for publicar o RIPD (por solicitação da ANPD, com base na LGPD,
art. 32, ou por iniciativa própria, quando não houver sigilo). A versão integral continua interna.

**A publicação é opcional na skill**, por decisão do controlador, salvo solicitação da ANPD. Registre,
mesmo assim, em "Pendências":
- a orientação da ANPD: para órgãos públicos, a página de perguntas e respostas sobre o RIPD diz que
  ele "deverá ser publicado" por determinação da ANPD ou pelo próprio controlador, quando não
  identificada hipótese de sigilo, em conformidade com a LAI `[CONFERIR]`;
- a divergência: a LGPD, art. 32, diz que a ANPD "poderá solicitar" a publicação; não cria dever
  geral de publicar;
- se o órgão decidir não publicar, a hipótese de sigilo ou de restrição considerada (LAI, arts. 23,
  24 e 31), com `[CONFERIR]` da unidade de transparência e da assessoria jurídica. A transparência
  ativa (LAI, art. 8º) e a publicidade das hipóteses de tratamento (LGPD, art. 23, I) continuam valendo.

## Sumário
1. O que publicar
2. O que resumir ou omitir
3. Revisão antes de publicar

## 1. O que publicar (em termos gerais)

Lista baseada, com crédito, na lista de conteúdo publicizável do Modelo de RIPD do PPSI 2.0
(SGD/MGI); o texto é da skill. Descrição do serviço e escopo do RIPD; finalidades; tipos de dados por categoria; categorias de
titulares; hipóteses legais; com quem há compartilhamento (por tipo de entidade) e se há
transferência internacional; critérios gerais de retenção; canais para exercer direitos e contato do
encarregado; medidas gerais de transparência e governança; histórico de versões e aprovação.

## 2. O que resumir ou omitir

- Fluxos detalhados, arquitetura, nomes de sistemas internos e integrações.
- Controles técnicos detalhados, configurações, versões de software, endereços, portas, testes de
  segurança e vulnerabilidades. Para órgãos e entidades do SISP, isso tende a ser **informação crítica**
  (Portaria SGD/MGI 9.511/2025, art. 2º, III), com acesso restrito a profissionais autorizados (art. 5º).
- A descrição detalhada de riscos e medidas: publique o resumo (por exemplo, "foram identificados
  N riscos; os de nível alto têm plano de ação com prazo"), sem descrever a vulnerabilidade.
- Qualquer informação pessoal (LAI, art. 31), informação classificada (LAI, arts. 23 e 24) e segredo
  comercial ou industrial de parceiros.
- Diga expressamente que **informações foram omitidas ou resumidas** para preservar a segurança e
  as informações protegidas por lei.

`scripts/conferir_ripd.py --modo publica` acusa IP, porta, CVE, senha, host interno, versão de
software e conta privilegiada, e exige o aviso de omissão. A leitura humana continua necessária.

## 3. Revisão antes de publicar

Encarregado, segurança da informação e, quando necessário, assessoria jurídica e a unidade
responsável pela transparência e pelo acesso à informação revisam a versão pública antes da publicação. A skill não publica nada.
