# Changelog — ripd-lgpd-br

## [1.1.0-rc] – 20/11/2026 (candidata, não publicada)

Correções da auditoria AGU/CGU da v1.0.0 (commit 01e4852) e da revisão de português.

- **Atos da ANPD como orientação (C1).** Fundamento legal é a LGPD; a Res. CD/ANPD 2/2022 aparece
  como parâmetro indicado pela ANPD, com `[CONFERIR]`, e com o aviso de que é regulamento de agentes
  de tratamento de pequeno porte (para órgão público, só parâmetro, no que couber). A Res. CD/ANPD
  18/2024 entra como orientação sobre o papel do encarregado, ao lado da LGPD, art. 41. Por decisão
  da autora, `conferir_ripd.py` não exige a marca `[CONFERIR]` (há teste disso).
- **Critérios não exaustivos (C2).** A triagem ganhou o sétimo item, `outro_fator_alto_risco`, e a
  conclusão negativa diz que os critérios não são exaustivos. Saiu "na prática, esperado".
- **Dados sensíveis (C3).** O art. 11, II, b, não abrange contrato nem convênio; o art. 23 é
  condição do tratamento pelo Poder Público, não hipótese autônoma.
- **Conferidor de linguagem (C4).** Pega conformidade com outros verbos ("é conforme", "atende à
  LGPD"), licitude ("é lícito", "legal", "regular"), "aprova-se", "não restam riscos", "risco é
  inexistente", "dispensado da elaboração", "RIPD não é necessário". A negação só afasta o alerta
  quando modifica o próprio verbo ou um verbo de dizer. A regra 2 do `SKILL.md` proíbe concluir
  licitude.
- **Publicação (C5).** Continua opcional, por decisão da autora. A minuta registra a orientação da
  ANPD ("deverá ser publicado" quando não houver sigilo) e a divergência com a LGPD, art. 32
  ("poderá solicitar"), em `base-legal.md`, `versao-publica.md`, `modelo-de-saida.md` e exemplos.
- **Desempenho (C6).** A busca da tabela de riscos passou a ser linha a linha, ancorada e com teto;
  teste com 250 mil caracteres.
- **Licença (C7).** `LICENSE.txt` e `base-legal.md` dizem que as faixas da Tabela 11 e a lista de
  conteúdo publicizável do Modelo do PPSI 2.0 são usadas como referência, com crédito, sem cópia de
  texto; registram a licença CC BY-ND 3.0 do rodapé das páginas gov.br.
- **Arquivos de trabalho (C8).** `_notices.md` e `_para_readme.md` saíram da pasta da skill.
- **Normas novas, com `[CONFERIR]`:** Res. CD/ANPD 15/2024, art. 8º (RIPD pedido no incidente),
  19/2024 (transferência internacional, só ementa), 32/2026 (adequação da União Europeia, só ementa),
  Decreto 10.046/2019 (ementa e art. 1º; "Vide ADI 6649"), LAI, arts. 8º, 23 e 24. Base com 53 itens,
  51 conferidos em 20/11/2026. Ação 4 da agenda regulatória (dados biométricos) registrada.
- **Scripts:** `conferir_ripd.py` reconhece outras formas de citar resolução, portaria, enunciado,
  instrução normativa e decreto (S9); `triagem_alto_risco.py` separa dado sensível de criança (S11),
  usa plural nos critérios e cita a medida 23.3 do PPSI 2.0 no lugar de "controle 23"; `matriz_risco.py`
  cita a Tabela 11 (S7) e avisa quando só uma coluna residual vem preenchida (S13); `_comum.py` trata
  " ia " como palavra inteira (S14) e `sinais_risco.py` mostra os termos com acento.
- **Testes:** dados de teste com DV inválido também no NIS/PIS e domínio reservado (S8); arquivos
  temporários apagados no fim; 49 testes unitários (eram 32).
- **Português:** siglas por extenso na primeira menção, "SISP" sem "federal", "instrução embutida",
  regência de "responder" e de "correspondência", concordâncias, "Modalidade" no cabeçalho, uma só
  fórmula para as opções do controlador, aviso final unificado ("preparada com ajuda de inteligência
  artificial (IA)"), metadados em português com `revisado_em` e `proxima_revisao`.

Não verificado nesta versão: artigos do ECA Digital (Lei 15.211/2025); demais artigos das
Res. CD/ANPD 15/2024 e 19/2024; efeito da ADI 6649 sobre o Decreto 10.046/2019; afirmações do guia
da ANPD para o Poder Público.

## 1.0.0 (20/11/2026, não publicada)

Primeira versão.

- `SKILL.md` com termos, oito regras invioláveis (inclusive contra instruções embutidas em documentos),
  triagem, fluxo de dez etapas com laço de verificação e exemplo curto.
- Referências: base legal conferida (47 itens em `references/normas.json`, 45 conferidos em
  20/11/2026 no Planalto, gov.br/ANPD e Diário Oficial), critérios de alto risco, modelo de saída com
  correspondência para a lista da ANPD e o Modelo do PPSI 2.0, princípios e direitos, catálogo de
  riscos, versão pública e checklist.
- Scripts locais sem rede: `sinais_risco.py`, `triagem_alto_risco.py`, `matriz_risco.py`,
  `dados_pessoais.py`, `conferir_ripd.py`.
- Três exemplos fictícios, 13 casos de avaliação com respostas de referência, 24 prompts de
  acionamento e 32 testes unitários.

Não verificado nesta versão: artigos do ECA Digital (Lei 15.211/2025) aplicáveis a RIPD; conteúdo da
Res. CD/ANPD 15/2024 (incidentes), citada no texto consolidado da Res. 2/2022 mas não lida; afirmações do guia da ANPD para o Poder
Público; regulamentos futuros previstos na agenda regulatória da ANPD.
