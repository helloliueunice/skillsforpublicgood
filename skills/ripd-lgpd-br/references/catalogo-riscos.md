# Catálogo de riscos ao titular e medidas

Use na etapa 7. O objetivo é **identificar o maior número de fatores relevantes**, sempre pela ótica
do **titular** (liberdades e direitos), não só do órgão. Os riscos abaixo são pontos de partida:
mantenha só os que se aplicam e acrescente os do caso concreto.

## Sumário
1. Como medir probabilidade e impacto
2. Riscos frequentes e medidas típicas
3. Como escrever o risco
4. Uso de `scripts/matriz_risco.py`

## 1. Como medir probabilidade e impacto

- **Metodologia:** use a do órgão. A ANPD deixa a escolha ao controlador e recomenda métodos
  reconhecidos como boas práticas. Sem metodologia própria, a skill usa escala de 1 a 5 e nível =
  probabilidade × impacto, com as faixas de exemplo do Modelo de RIPD do PPSI 2.0 (SGD/MGI,
  Tabela 11), usadas como referência, com crédito: pequeno até 3, moderado 4 a 6, alto 7 a 12,
  crítico acima de 12 (na escala de 1 a 5, os níveis possíveis nas duas últimas faixas são 8 a 12 e
  15 a 25). Diga no RIPD qual foi usada.
- **Impacto sobre o titular:** 1 desconforto mínimo e reversível; 2 incômodo sem prejuízo; 3 prejuízo
  reversível (tempo, retrabalho, exposição limitada); 4 restrição relevante a direito, dano difícil de
  reverter, discriminação, dado sensível ou de vulnerável exposto; 5 dano grave ou irreversível
  (integridade física, perda de benefício essencial, exposição ampla de dado sensível). Esta escala é
  da skill e é só ponto de partida.
- **Probabilidade:** 1 rara; 2 improvável; 3 possível; 4 provável; 5 quase certa. Justifique com fatos
  (histórico de incidentes, exposição na internet, número de pessoas com acesso, maturidade dos controles).
- **Combinação de fatores:** vários fatores juntos podem elevar o risco. Registre como interagem.

## 2. Riscos frequentes e medidas típicas

| Risco ao titular | Sinais no tratamento | Medidas típicas |
|---|---|---|
| Acesso indevido ou vazamento | Muitos usuários com acesso; sistema exposto na internet; planilhas por e-mail | Perfis de acesso mínimo; autenticação forte; registro e revisão de acessos; criptografia; proibir planilhas soltas |
| Uso para finalidade incompatível | Base reaproveitada por outra área; pedidos de "cruzar com tudo" | Termo de uso compartilhado com finalidade; registro de cada uso; análise prévia do encarregado |
| Coleta excessiva | Formulário pede dados "por precaução"; campos livres | Revisão campo a campo; campos opcionais; pseudonimização |
| Dados desatualizados levam a decisão errada | Cadastro sem rotina de atualização; cruzamento de bases | Rotina de atualização; canal de correção; dupla checagem antes de decisão desfavorável |
| Decisão automatizada injusta ou discriminatória | Indeferimento automático; pontuação; IA | Revisão humana antes de decisão desfavorável; informação sobre critérios (art. 20); testes de viés |
| Exposição de criança, adolescente ou idoso | Dados escolares, de saúde ou de assistência | Acesso mais restrito; melhor interesse documentado (art. 14); aviso adequado à idade |
| Exposição de dado sensível | Saúde, biometria, raça/cor, religião | Segregação; criptografia; acesso por necessidade; publicidade da dispensa de consentimento (art. 11, § 2º) |
| Vigilância desproporcional | Câmeras e reconhecimento em espaço público | Necessidade e proporcionalidade documentadas; avisos; retenção curta; reconhecimento facial só com base legal clara |
| Compartilhamento sem base ou sem controle | Convênio genérico; operador sem contrato | Instrumento com finalidade, prazo e segurança; cláusulas de operador (art. 39); comunicação à ANPD quando exigida (art. 27); entre órgãos federais, regras do Decreto 10.046/2019 `[CONFERIR]` |
| Transferência internacional sem garantia | Nuvem com servidores no exterior | Verificar hipótese do art. 33; mecanismo do regulamento da ANPD (Res. CD/ANPD 19/2024, cláusulas-padrão contratuais) e, para a União Europeia, a Res. CD/ANPD 32/2026 `[CONFERIR]`; localização dos dados |
| Retenção além do necessário | Sem prazo definido; cópias de segurança sem prazo de descarte | Tabela de temporalidade; eliminação registrada (art. 16) |
| Titular sem conseguir exercer direitos | Sem canal; prazos indefinidos | Canal do encarregado; fluxo de atendimento; prazos internos |
| Reidentificação de dados "anonimizados" | Dados publicados com poucos campos raros | Testar reidentificação; agregação; supressão de células pequenas |

## 3. Como escrever o risco

Formato: **evento** + **causa** + **efeito sobre o titular**. Exemplo: "Servidor sem necessidade
acessa o laudo de deficiência do aluno (perfil de acesso amplo), expondo dado sensível e gerando
risco de discriminação."

## 4. Uso de `scripts/matriz_risco.py`

Monte um CSV com `id, risco, probabilidade, impacto, medidas, probabilidade_residual,
impacto_residual, responsavel, prazo`. O script calcula nível e faixa, ordena e aponta pendências:
risco alto ou crítico sem medida, responsável, prazo ou avaliação residual; impacto baixo demais para
dado sensível; só uma das colunas residuais preenchida; risco residual alto ou crítico, que exige
decisão fundamentada do controlador (prosseguir com justificativa, mudar o tratamento ou não prosseguir).
