# Changelog — incidente-dados-lgpd-br

## [1.1.0-rc] (20/11/2026, não publicada)

Correções da auditoria AGU/CGU (B1, C1 a C8 e sugestões S1 a S9 e S11 a S13) e da revisão PT-BR
(6 erros e 42 melhorias), com as decisões da autora para a skill de RIPD aplicadas aqui.

- **Licença (B1, C7):** `LICENSE.txt` com o texto MIT completo; registro da licença CC BY-ND 3.0 da
  página "Comunicação de Incidente de Segurança" da ANPD (só citada e parafraseada) e do formulário
  sem licença declarada. Os arquivos de trabalho saíram da pasta (commit 87ec871).
- **Decreto 9.637/2018 revogado (C1):** registrada a revogação pelo Decreto 12.572/2025, art. 12, I
  (conferido no Planalto em 20/11/2026); o Decreto 10.748/2021, art. 12, IV, segue vigente e agora é
  resumido com "vulnerabilidades ou incidentes"; forma de comunicar ao CTIR Gov com [CONFERIR]. O
  conferidor recusa o Decreto 9.637/2018 citado como vigente.
- **Res. CD/ANPD 15/2024 (C2):** continua tratada como regulamento que obriga o órgão (LGPD, art. 48,
  § 1º); [CONFERIR vigência] como alerta nas citações de fundamento; o conferidor não exige a marca.
- **Triagem indicativa (C3, C4):** conclusões como "INDICATIVO DE RISCO OU DANO RELEVANTE", "CRITÉRIOS
  DO ART. 5º NÃO PREENCHIDOS PELAS RESPOSTAS INFORMADAS" etc.; coluna "Indicativo" na tabela de exemplos;
  registro com "Conclusão do controlador [PREENCHER]".
- **Conferidor (C5):** barra as 14 frases da auditoria e outras (ausência de risco, dispensa da
  comunicação, licitude, "fique tranquilo", pedido de código, acusação a pessoa); a exceção de negação
  vale só para negação direta do termo ou verbo de relato negado.
- **Não acusar (C6):** nova regra 9; apuração por sindicância ou processo administrativo disciplinar
  (Lei 8.112/1990, art. 143; LGPD, art. 52, § 3º); caso de avaliação inc-14.
- **Exemplos (C8 e revisão):** exemplo 02 coerente sobre idosos (critério `null`); exemplo 01 sem fatos
  fora do relato; exemplo 03 comunica ao titular (o estudante) e, por serem adolescentes, também aos
  responsáveis [CONFERIR].
- **Sugestões:** prorrogação da Res. 1/2021, art. 8º, §§ 1º e 2º (S1, S2); aviso no `--pequeno-porte`
  (S3); comunicação por etapas excepcional (S4); ressalva do art. 10, § 2º (S5); PNCiber, PPSI e GSI como
  não verificados (S6); Estados e Municípios: LAI, arts. 23 e 24, ou norma local [CONFERIR] (S7); cadeia
  de custódia (S8); números de teste sem DV válido de CPF, NIS ou CNPJ, IP de documentação e CVE fictício
  (S9); LGPD, art. 14, com [CONFERIR] (S11); 20/11 só a partir de 2024 (S12); reidentificação, LGPD,
  art. 12 (S13). S10 (README e THIRD_PARTY_NOTICES da raiz) fica para quem cuida da raiz.
- **Revisão PT-BR:** "instrução embutida" (com o regex do inc-02), aviso "inteligência artificial (IA)",
  metadados em português, siglas por extenso, plural correto ("falta 1 dia útil"), "[DATA DE NASCIMENTO
  REMOVIDA]", "responder a cada critério", rótulos do formulário (Completa, Preliminar, Complementar),
  resumos fiéis ("terceiros não autorizados", "de maneira fundamentada", "caso seja possível
  identificá-los"), Carnaval fora dos feriados federais.
- **Base:** `normas.json` com 55 itens, 52 conferidos (novos: Decreto 12.572/2025, Lei 8.112/1990,
  art. 143, conferida em 19/11/2026, LAI, arts. 23 e 24, Lei 9.093/1995, LGPD, art. 12).
- **Testes:** 52 testes (antes 34), inclusive cada regex em 250 mil caracteres; 15 casos de avaliação
  (novos: inc-14 e inc-15); `testes.py` apaga os temporários.

## [1.0.0] (20/11/2026, não publicada)

Primeira versão.

- `SKILL.md` com termos, nove regras invioláveis com justificativa (inclusive contra instruções
  embutidas em documentos e bilhetes de atacante), triagem, fluxo de nove etapas e exemplo curto.
- Referências: base legal (48 itens em `references/normas.json`, 46 conferidos em 20/11/2026 no
  Planalto, Diário Oficial e gov.br/ANPD), critérios de risco relevante, prazos e fluxo, modelos de
  comunicação à ANPD, aviso aos titulares e registro, e checklist de revisão.
- Scripts locais sem rede: `triagem_incidente.py`, `prazos_incidente.py`, `conferir_comunicacao.py`,
  `dados_pessoais.py`.
- Três exemplos fictícios, 13 casos de avaliação com respostas de referência, 23 prompts de
  acionamento e 34 testes unitários.

Não verificado nesta versão: ECA Digital (Lei 15.211/2025); Decreto 9.637/2018, art. 17 (na 1.1.0-rc:
revogado pelo Decreto 12.572/2025), e normas do
GSI/CTIR Gov sobre forma e prazo; prazos setoriais; aplicação por analogia da Res. CD/ANPD 1/2021,
art. 8º; multa diária a órgão público; empresa pública como agente de pequeno porte; licença das
páginas e do formulário da ANPD.
