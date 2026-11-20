# Relatório de Impacto à Proteção de Dados Pessoais: Sistema de Gestão Escolar (SGE) da rede municipal

Versão 0.1 · 20/11/2026 · Situação: MINUTA PARA REVISÃO · Modalidade: integral (uso interno)

> Caso fictício para demonstração. Município, pessoas e números são inventados.

## 1. Identificação

| Item | Informação |
|---|---|
| Controlador | Município de Exemplópolis, por meio da Secretaria Municipal de Educação (SME) |
| Unidade responsável | [PREENCHER: diretoria da SME responsável pelo SGE] |
| Encarregado | Canal público: encarregado@example.org |
| Operador | Empresa fornecedora do SGE em nuvem [PREENCHER: razão social após assinatura do contrato] |
| Áreas consultadas | [PREENCHER: TI, Procuradoria, segurança da informação, ouvidoria, conselho escolar, com data e parecer de cada uma] |

## 2. Necessidade do RIPD

Motivo: alto risco pelos critérios que a ANPD indica como parâmetro (art. 4º da Res. CD/ANPD 2/2022,
regulamento de agentes de tratamento de pequeno porte; para o município, vale só como parâmetro, no
que couber) [CONFERIR], resultado de `scripts/triagem_alto_risco.py` sobre `triagem.json`. A ANPD não
pediu o RIPD; a elaboração é recomendada antes da entrada em produção. Os critérios não são
exaustivos: o controlador pode identificar outro fator de alto risco.

| Critério | Resposta | Justificativa |
|---|---|---|
| Geral: larga escala | Sim | 18 mil alunos e seus responsáveis, 52 escolas, tratamento contínuo por vários anos |
| Geral: afetar significativamente direitos | Sim | A pontuação define a prioridade de vaga em creche |
| Específico: tecnologia emergente | Não | Sistema convencional; não foram informadas IA nem biometria |
| Específico: vigilância de zona pública | Não | Não há câmeras |
| Específico: decisão unicamente automatizada | Sim | Ordem de prioridade da creche calculada por pontuação |
| Específico: dados sensíveis ou de vulneráveis | Sim | Crianças e adolescentes; laudo de deficiência e restrições alimentares (saúde); cor/raça |
| Outro fator identificado pelo controlador | Não verificável | [PREENCHER: a equipe avalia se há outro fator de alto risco] |

Conclusão da triagem: RIPD recomendado (alto risco). A decisão é do controlador.

## 3. Descrição do tratamento

### 3.1 Contexto e finalidades

O SGE substitui planilhas das escolas. Finalidades:

1. Matrícula e rematrícula na rede municipal.
2. Classificação da fila de vagas em creche por critérios de prioridade.
3. Registro de frequência, avaliação e histórico escolar.
4. Atendimento educacional especializado e segurança alimentar dos alunos.
5. Envio mensal de frequência ao programa social federal que a exige [CONFERIR: norma do programa, não verificado].
6. Envio de dados ao Censo Escolar [CONFERIR: norma que exige os campos, não verificado].

### 3.2 Ciclo de vida e fluxo

Coleta na secretaria da escola (formulário presencial) e pelo responsável (formulário web) →
armazenamento no SGE em nuvem do operador → acesso por secretaria escolar, direção, professores (só da
própria turma) e equipe da SME → exportações mensais de frequência e anuais ao Censo Escolar →
publicação da lista de prioridade da creche → guarda e eliminação [PREENCHER: prazo, ver 3.6].

### 3.3 Dados pessoais e titulares

| Titulares | Dados | Observação |
|---|---|---|
| Alunos (crianças e adolescentes), cerca de 18 mil | Identificação, data de nascimento, filiação, endereço, fotografia, frequência, notas, histórico | Dados de crianças e adolescentes (LGPD, art. 14) |
| Alunos | Laudo de deficiência, alergias e restrições alimentares, cor/raça | Dados sensíveis (art. 5º, II) |
| Responsáveis | Identificação, documento, telefone, e-mail, endereço, recebimento de benefício social | Benefício social revela situação de vulnerabilidade |

Fonte: o próprio responsável e a escola. Volume: [PREENCHER: número de responsáveis].

### 3.4 Hipóteses legais

| Finalidade | Dados | Hipótese legal | Fundamento na norma do serviço | Publicidade (art. 23, I) |
|---|---|---|---|---|
| 1, 3 | Comuns | Art. 7º, III (execução de políticas públicas) | [CONFERIR: lei municipal do sistema de ensino] | [PREENCHER: página do SGE] |
| 2 | Comuns e benefício social | Art. 7º, III | [CONFERIR: norma municipal dos critérios da creche] | [PREENCHER] |
| 4 | Sensíveis | Art. 11, II, b | [CONFERIR: norma do atendimento educacional especializado] | [PREENCHER] |
| 5, 6 | Comuns e cor/raça | Art. 7º, II ou III; art. 11, II, a ou b [CONFERIR com a Procuradoria] | [CONFERIR: normas federais, não verificado] | [PREENCHER] |

Dados de crianças e adolescentes: podem ser tratados com base nas hipóteses dos arts. 7º ou 11, desde
que observado o melhor interesse (art. 14; Enunciado CD/ANPD 1/2023).
ECA Digital (Lei 15.211/2025): aplicabilidade a este sistema não verificada.

### 3.5 Compartilhamento, operadores e transferência internacional

| Com quem | Para quê | Base | Instrumento |
|---|---|---|---|
| Empresa do SGE (operador) | Hospedagem e suporte | Art. 39 (operador segue instruções do controlador) | Contrato [PREENCHER: cláusulas de proteção de dados] |
| Órgão federal do programa social | Frequência | Art. 26 | [CONFERIR: instrumento e norma, não verificado] |
| Censo Escolar | Estatística educacional | Art. 26 | [CONFERIR] |

Transferência internacional: a empresa informou servidores no Brasil. [CONFERIR no contrato: local
dos dados e das cópias de segurança; se houver transferência, aplicar o art. 33 e o mecanismo da
Res. CD/ANPD 19/2024 [CONFERIR].]

### 3.6 Retenção e eliminação

Prazo ainda não definido. [PREENCHER: tabela de temporalidade por categoria (histórico escolar,
laudos, fila da creche, dados de responsáveis) e forma de eliminação.] Fundamento: término do
tratamento e eliminação (arts. 15 e 16).

### 3.7 Metodologia de coleta e de segurança das informações

Coleta: formulário presencial digitado pela secretaria escolar e formulário web preenchido pelo
responsável, com aviso de privacidade [PREENCHER: texto do aviso].

Segurança (art. 46): perfis por função; professores só veem a própria turma; [PREENCHER: autenticação,
criptografia, registro de acessos, cópias de segurança, plano de resposta a incidentes (art. 48)].

## 4. Análise dos princípios

| Princípio (art. 6º) | Como é atendido | Evidência | Lacuna |
|---|---|---|---|
| Finalidade | Seis finalidades listadas em 3.1 | Descrição da SME | Formalizar no aviso de privacidade |
| Adequação | Dados ligados à matrícula e ao ensino | Formulário | Fotografia: confirmar se é necessária |
| Necessidade | Parcial | — | Laudo completo pode ser substituído por indicação do tipo de atendimento [CONFERIR] |
| Livre acesso | Não definido | — | [PREENCHER: como o responsável consulta os dados] |
| Qualidade dos dados | Atualização na rematrícula | — | Dados da pontuação da creche podem estar desatualizados (R3) |
| Transparência | Não definido | — | Publicar aviso e critérios da creche |
| Segurança | Perfis de acesso | Descrição da SME | Ver R1 e R5 |
| Prevenção | RIPD antes da produção | Esta minuta | Plano de resposta a incidentes |
| Não discriminação | Risco no laudo e no benefício social | — | R1 e R2 |
| Responsabilização e prestação de contas | Este RIPD e o contrato | — | Registro das operações (art. 37) [PREENCHER] |

## 5. Direitos dos titulares

Os direitos são exercidos pelo responsável legal do aluno. [PREENCHER: canal e prazo de resposta para
confirmação, acesso, correção, informação sobre compartilhamento (art. 18).] A lista da creche resulta de
decisão automatizada: prever pedido de revisão e informação dos critérios (art. 20).

## 6. Riscos ao titular

Metodologia: escala 1 a 5 de `references/catalogo-riscos.md` (o município não tem metodologia própria
[CONFERIR]); nível = probabilidade × impacto; faixas: pequeno até 3, moderado 4 a 6, alto 7 a 12,
crítico acima de 12. Tabela gerada por `scripts/matriz_risco.py riscos.csv`.

| ID | Risco ao titular | P | I | Nível | Faixa | Residual |
|---|---|---|---|---|---|---|
| R2 | Lista pública da creche identifica crianças e revela benefício social | 4 | 4 | 16 | crítico | 3 (pequeno) |
| R5 | Vazamento por credencial fraca de usuário das escolas | 3 | 5 | 15 | crítico | 8 (alto) |
| R1 | Acesso sem necessidade ao laudo de deficiência | 3 | 4 | 12 | alto | 8 (alto) |
| R3 | Pontuação automática com dado desatualizado nega vaga | 3 | 4 | 12 | alto | 6 (moderado) |
| R4 | Operador usa ou guarda dados fora das instruções | 3 | 4 | 12 | alto | 6 (moderado) |
| R6 | Guarda indefinida de dados de ex-alunos | 4 | 2 | 8 | alto | 4 (moderado) |
| R7 | Exportação de campos além do exigido | 2 | 3 | 6 | moderado | 3 (pequeno) |

## 7. Medidas, salvaguardas e mecanismos de mitigação

| Risco | Medida | Responsável | Prazo |
|---|---|---|---|
| R1 | Laudo visível só à direção e ao atendimento especializado; revisão mensal de acessos | SME e TI | Antes da produção |
| R2 | Publicar só código de inscrição e posição | SME | Antes da primeira lista |
| R3 | Revisão humana antes de indeferir; critérios publicados; canal de revisão | SME | Antes da primeira lista |
| R4 | Cláusulas de operador, dados no Brasil, eliminação no fim do contrato, auditoria | SME e Procuradoria | Antes da assinatura |
| R5 | Dois fatores para perfis administrativos; bloqueio por tentativas; criptografia | TI | Antes da produção |
| R6 | Tabela de temporalidade e eliminação registrada | SME | 6 meses |
| R7 | Exportar só os campos exigidos; registro de cada envio | TI | Antes da produção |

## 8. Conclusão e plano de ação

Restam dois riscos residuais altos (R1 e R5). Opções para o controlador: (a) prosseguir com
justificativa, só depois de implantar as medidas de R1, R2, R4 e R5 e reavaliar o residual; (b) mudar
o tratamento, por exemplo sem anexar o laudo completo; (c) não prosseguir por ora, adiando a entrada
em produção. Esta minuta não escolhe: a decisão é do controlador, com assistência do encarregado
(LGPD, art. 41; Res. CD/ANPD 18/2024, art. 16, III, como orientação) [CONFERIR].

## 9. Pendências e não verificado

- [PREENCHER] e [CONFERIR] acima: SME, TI e Procuradoria.
- Normas do programa social e do Censo Escolar e Lei de Diretrizes e Bases da Educação Nacional (LDB, Lei 9.394/1996): não verificadas.
- Publicação: decisão do controlador. A LGPD, art. 32, diz que a ANPD "poderá solicitar" a publicação;
  a ANPD orienta que órgão público publique o RIPD quando não houver hipótese de sigilo (LAI) [CONFERIR:
  unidade de transparência e Procuradoria].
- ECA Digital (Lei 15.211/2025): artigos aplicáveis não verificados.
- Pareceres das áreas consultadas: não recebidos.

## 10. Histórico de versões e aprovação

| Data | Versão | Mudança | Responsável |
|---|---|---|---|
| 20/11/2026 | 0.1 | Minuta inicial | [PREENCHER] |

Manifestação do encarregado: [PREENCHER]. Aprovação do representante do controlador: [PREENCHER: nome e cargo].

> Esta é uma minuta preparada com ajuda de inteligência artificial (IA). Não substitui a análise da
> equipe, do encarregado e da assessoria jurídica, nem declara conformidade com a LGPD. Requer revisão
> humana e aprovação do controlador.
