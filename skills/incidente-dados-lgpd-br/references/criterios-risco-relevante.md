# Quando comunicar: risco ou dano relevante

## Sumário
1. É incidente com dados pessoais?
2. A regra do art. 5º da Res. CD/ANPD 15/2024
3. Como responder a cada critério
4. Dados criptografados ou ininteligíveis
5. Exemplos no setor público
6. Uso de `scripts/triagem_incidente.py`

## 1. É incidente com dados pessoais?

Incidente de segurança é **evento adverso confirmado** que viola confidencialidade, integridade,
disponibilidade ou autenticidade de dados pessoais (Res. CD/ANPD 15/2024, art. 3º, XII).

| Situação | É incidente com dados pessoais? |
|---|---|
| Vulnerabilidade descoberta, sem sinal de exploração | Ainda não (orientação da ANPD). Corrija e registre a análise. Órgão federal: comunique a vulnerabilidade ao CTIR Gov (Decreto 10.748/2021, art. 12, IV) |
| Suspeita sem confirmação | Ainda não. Apure com urgência: o prazo corre do conhecimento de que dados pessoais foram afetados |
| Planilha com dados de servidores enviada ao destinatário errado | Sim (confidencialidade) |
| Sistema de agendamento fora do ar por ransomware | Sim (disponibilidade; e confidencialidade, se houve cópia) |
| Alteração indevida de cadastro | Sim (integridade) |
| Base só com dados anonimizados | Não para a LGPD (orientação da ANPD), desde que os dados sejam de fato anonimizados: se for possível reverter a anonimização com esforço razoável, são dados pessoais (LGPD, art. 12) [CONFERIR]; trate como incidente de segurança da informação |

## 2. A regra

A Res. CD/ANPD 15/2024 [CONFERIR vigência] prevê a comunicação à ANPD **e** aos titulares quando o incidente **pode afetar significativamente interesses
e direitos fundamentais** dos titulares **e**, cumulativamente, envolve **pelo menos um** destes
critérios (art. 5º):

1. dados pessoais sensíveis (LGPD, art. 5º, II);
2. dados de crianças, de adolescentes ou de idosos;
3. dados financeiros;
4. dados de autenticação em sistemas (logins, tokens, senhas);
5. dados protegidos por sigilo legal, judicial ou profissional;
6. dados em larga escala.

"Afetar significativamente" inclui, entre outras situações, **impedir o exercício de direitos ou o
uso de um serviço** e causar **danos materiais ou morais**, como discriminação, violação à
integridade física, à imagem e à reputação, fraude financeira ou roubo de identidade (art. 5º, § 1º).
Larga escala considera número de titulares, volume de dados, duração, frequência e extensão
geográfica (art. 5º, § 2º).

## 3. Como responder a cada critério

Responda com **fatos**, não com impressões. Para cada "sim" ou "não", escreva a justificativa.

- **Afeta significativamente?** Pergunte: alguém pode perder acesso a serviço público (saúde,
  benefício, matrícula)? Pode sofrer golpe com os dados? Pode ser exposto (saúde, processo
  disciplinar, denúncia)? Na dúvida, a resposta é "não se sabe" (null), não "não".
- **Sigilo legal, judicial ou profissional:** no setor público, pense em sigilo fiscal, bancário,
  de prontuário, de processo disciplinar ou judicial, de denunciante. Marque [CONFERIR] a norma do sigilo.
- **Larga escala:** não há número fixo. Compare com o total de titulares do serviço e registre o raciocínio.
- **Crianças, adolescentes, idosos:** informe quantos de cada grupo (art. 6º, § 2º, II).

## 4. Dados criptografados ou ininteligíveis

No juízo de gravidade, conta a comprovação de medidas técnicas adequadas que tornem os dados
ininteligíveis para terceiros não autorizados a acessá-los (LGPD, art. 48, § 3º). Isso **não dispensa automaticamente** a comunicação: se a chave
também foi exposta, se a criptografia era fraca ou se não há prova, trate como dado legível. Se o
controlador decidir não comunicar, registre os motivos (Res. CD/ANPD 15/2024, art. 10, § 1º, VIII).

## 5. Exemplos no setor público (fictícios)

| Caso | Afeta significativamente? | Critério | Indicativo (decisão do controlador) |
|---|---|---|---|
| Ransomware com cópia da base de agendamento da saúde (60 mil pacientes) | Sim: atendimento interrompido, exposição de dado de saúde | Sensíveis; larga escala | Indicativo de risco ou dano relevante: a avaliação sugere comunicar |
| E-mail com nome e matrícula de 40 servidores ao destinatário errado, que apagou e confirmou por escrito | Não há indício | Nenhum | Critérios não preenchidos pelas respostas: o controlador decide e registra os motivos |
| Notebook furtado com base de alunos, disco criptografado e senha não exposta | Depende da prova da criptografia | Crianças e adolescentes | Avaliar com o encarregado antes de deixar de comunicar; registrar |
| Senhas de servidores do portal do RH vazadas em fórum | Sim: acesso a contracheque e dados bancários | Autenticação; financeiros | Indicativo de risco ou dano relevante: a avaliação sugere comunicar |

## 6. Uso de `scripts/triagem_incidente.py`

Gere o modelo com `--modelo`, preencha com true, false ou null e rode o script. Ele devolve um
**indicativo** (indicativo de risco ou dano relevante; avaliar com o encarregado; critérios não
preenchidos pelas respostas; sem dados pessoais afetados pelas respostas; incidente não confirmado;
não verificável) e notas (registro, CTIR Gov, operador, pequeno porte, crianças). Os exemplos da
tabela acima também são indicativos. Quem decide é o controlador, com assistência do encarregado,
e a conclusão vai para o registro como "Conclusão do controlador", com os fatos que a sustentam.
