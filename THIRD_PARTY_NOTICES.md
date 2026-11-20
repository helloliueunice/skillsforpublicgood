# Avisos de terceiros

Este repositório tem licença MIT (ver `LICENSE`, © 2026 Eunice Liu). **Nenhum texto ou código de
terceiro foi copiado** para as skills `ripd-lgpd-br` e `incidente-dados-lgpd-br`, e por isso nenhum
aviso de licença de terceiro precisa ser reproduzido. O registro abaixo serve para transparência.

## skill `ripd-lgpd-br`

| Fonte | Licença (conferida em 20/11/2026) | Uso nesta skill |
|---|---|---|
| Leis, decretos, resoluções, portarias e enunciado citados (Planalto, ANPD, DOU) | Não protegidos por direito autoral: leis e demais atos oficiais (Lei 9.610/1998, art. 8º, IV) | Citação de dispositivos e resumos próprios |
| Guia e Modelo de RIPD do PPSI 2.0 (SGD/MGI, v1.0, 31/07/2026) | CC BY-NC-ND 4.0 (indicada nos próprios documentos) | Citados e indicados por seção. **Usados como referência, com crédito:** as faixas numéricas da Tabela 11 do Modelo (padrão de `scripts/matriz_risco.py` e `references/catalogo-riscos.md`) e a lista de conteúdo publicizável do Modelo (base de `references/versao-publica.md`, seção 1). Nenhum texto copiado; a escala de impacto de 1 a 5 é própria |
| Páginas da ANPD (perguntas e respostas sobre o RIPD, agenda regulatória, lista de regulamentações) e do DOU | Rodapé das páginas: Creative Commons Atribuição-SemDerivações 3.0 Não Adaptada (CC BY-ND 3.0) | Paráfrase e citação com link; nada copiado |
| AgentsKit-io/agentskit-registry (`compliance-lgpd-assessor`) | MIT | Só a ideia de uma "rede de segurança" determinística (scripts que conferem a saída). Nenhum código ou texto copiado |
| wshobson/agents (`gdpr-data-handling`) | MIT | Só a ideia geral de checklist de avaliação de impacto. Nenhum código ou texto copiado; GDPR fora do escopo |
| anatelgovbr/ai-skills e ai-prompts | GPL-3.0 | **Não usados** (nem ideias) |

Ideias e métodos não são objeto de proteção como direitos autorais (Lei 9.610/1998, art. 8º, I,
conferido em 20/11/2026 no Planalto). Faixas numéricas e listas de itens são ideias e métodos. Essa
é uma avaliação técnica, não um parecer jurídico.

## skill `incidente-dados-lgpd-br`

| Fonte | Licença (conferida em 20/11/2026) | Uso nesta skill |
|---|---|---|
| Leis, decretos e resoluções citados (Planalto, DOU, ANPD) | Não protegidos por direito autoral: leis e demais atos oficiais (Lei 9.610/1998, art. 8º, IV) | Citação de dispositivos e resumos próprios |
| Página "Comunicação de Incidente de Segurança" (CIS) da ANPD (gov.br) | CC BY-ND 3.0, pelo rodapé do portal da ANPD ("Todo o conteúdo deste site está publicado sob a licença Creative Commons Atribuição-SemDerivações 3.0 Não Adaptada", lido em 20/11/2026 em páginas da ANPD; a página específica não foi relida) | Só citada, com link, e parafraseada; nada copiado. Como a CC BY-ND 3.0 não permite obra derivada, a skill não adapta o texto |
| Formulário de Comunicação de Incidente de Segurança da ANPD (.docx) | O arquivo não declara licença (**não verificado**); provavelmente CC BY-ND 3.0, pelo rodapé do portal | Só consultado; os blocos são indicados por paráfrase em `references/modelo-comunicacao-anpd.md`, sem reproduzir perguntas nem layout |
| `ripd-lgpd-br` (mesmo repositório) | MIT, mesma autora | Trechos de `scripts/_comum.py`, `scripts/dados_pessoais.py` e `evals/rodar_evals.py` reaproveitados |
| anatelgovbr/ai-skills e ai-prompts | GPL-3.0 | **Não usados** |
