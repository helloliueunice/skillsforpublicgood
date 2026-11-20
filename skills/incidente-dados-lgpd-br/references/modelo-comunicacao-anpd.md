# Modelo: minuta da comunicação à ANPD

Use para preparar o conteúdo que a equipe vai lançar no **formulário oficial da ANPD**, no SEI!ANPD.
A minuta organiza as informações; o formulário oficial prevalece (baixe-o na página da ANPD no
momento do uso). Cada seção corresponde a um inciso do art. 6º, § 2º, da Res. CD/ANPD 15/2024
[CONFERIR vigência].

## Sumário
1. Estrutura da minuta
2. Correspondência com os blocos do formulário da ANPD
3. Regras de preenchimento

## 1. Estrutura da minuta

```markdown
# Comunicação de incidente de segurança à ANPD: [serviço ou sistema]

Situação: MINUTA PARA REVISÃO · Tipo: [Completa | Preliminar | Complementar] · Nível de acesso no SEI: [restrito | público, CONFERIR]

## 1. Controlador, encarregado e operador (incisos VIII, IX e X)
Controlador: [nome do órgão]. Declaração sobre agente de pequeno porte: não se aplica a pessoa
jurídica de direito público [CONFERIR]. Encarregado: [nome e canal institucional]. Quem peticiona e
documento de vínculo ou procuração: [PREENCHER]. Operador envolvido: [nome ou "não há"].

## 2. Datas (inciso VII)
Data da ocorrência: [data ou "não determinada"]. Data do conhecimento de que dados pessoais foram
afetados: [data]. Data desta comunicação: [data].

## 3. Descrição do incidente e causa principal (inciso XI)
O que aconteceu, como foi detectado e a causa principal, se identificada, em termos técnicos e
impessoais, sem nomear nem culpar pessoas (a apuração de responsabilidade é feita em processo próprio).

## 4. Natureza e categoria dos dados afetados (inciso I)
Natureza: [gerais | sensíveis]. Categorias: [identificação, contato, saúde, financeiros, autenticação...].

## 5. Titulares (incisos II e XII)
Titulares afetados: [número ou estimativa]; crianças: [n]; adolescentes: [n]; idosos: [n].
Total de titulares tratados nas atividades afetadas: [n].

## 6. Riscos e possíveis impactos aos titulares (inciso IV)
Avaliação pelo art. 5º (resultado de scripts/triagem_incidente.py) e impactos concretos.

## 7. Medidas de segurança antes e após o incidente (inciso III)
Antes: [...]. Após: [...]. Observados os segredos comercial e industrial.

## 8. Medidas para reverter ou mitigar os efeitos (inciso VI)
Adotadas e a adotar, com responsável e prazo. Comunicação aos titulares: [feita em / prevista para / meios].

## 9. Motivos da demora (inciso V)
[Comunicação no prazo: não houve demora | motivos].

## 10. Pendências
[PREENCHER] e [CONFERIR] restantes; informações a complementar em até vinte dias úteis (art. 6º, § 3º).

> Esta é uma minuta preparada com ajuda de inteligência artificial (IA). Não substitui a análise da
> equipe, do encarregado e da assessoria jurídica, nem a decisão do controlador. Requer revisão
> humana antes do envio.
```

## 2. Correspondência com os blocos do formulário da ANPD

Nomes dos blocos resumidos pela skill (o formulário foi consultado em 20/11/2026, não reproduzido):

| Seção da minuta | Bloco do formulário |
|---|---|
| 1 | Dados do controlador; do encarregado; de quem comunica |
| 2 | Tempestividade (datas) |
| — | Tipo de comunicação (completa, preliminar, complementar) |
| 6 | Avaliação do risco |
| — | Como se soube do incidente; dados do operador |
| 8 | Comunicação aos titulares |
| 3 | Descrição do incidente (tipo, como e por que ocorreu, correção da causa) |
| 4 e 5 | Impactos sobre os dados (confidencialidade, integridade, disponibilidade; tipos de dados; titulares) |
| 7 e 8 | Medidas de segurança e de mitigação |

Se o formulário em uso tiver outros campos, preencha-os também: ele prevalece sobre este modelo.

## 3. Regras de preenchimento

- Números, nunca nomes: não anexe lista de titulares.
- Não invente datas, números nem causa: use `[PREENCHER]`. Estimativa só com a palavra "estimativa".
- Informação técnica sensível (endereços, vulnerabilidades) vai em documento com acesso restrito no SEI.
- Se faltar informação no prazo, comunique assim mesmo e marque "Preliminar" no formulário, com a
  justificativa (a comunicação por etapas é excepcional, segundo a ANPD). "Completa" só quando todas
  as informações estiverem disponíveis e os titulares já tiverem sido comunicados. "Complementar" é a
  que completa a preliminar, no mesmo processo, em até vinte dias úteis (art. 6º, § 3º).
- Não identifique nem culpe servidor, colaborador, empresa ou outra pessoa (regra 9 do `SKILL.md`):
  descreva a causa de forma técnica. Responsabilidade se apura por sindicância ou processo
  administrativo disciplinar (Lei 8.112/1990, art. 143), com ampla defesa.
