# Prazos e fluxo da resposta

## Sumário
1. Linha do tempo
2. Primeiras horas: o que a skill orienta, o que não faz e como preservar evidências
3. Comunicação à ANPD: canal, quem assina, preliminar e complementar
4. Comunicação aos titulares
5. Registro
6. Governo federal: CTIR Gov
7. Operador e contratos
8. Uso de `scripts/prazos_incidente.py`

## 1. Linha do tempo

Artigos sem outra indicação são da Res. CD/ANPD 15/2024 [CONFERIR vigência].

| Quando | O quê | Fundamento |
|---|---|---|
| Logo após a detecção | Conter, preservar evidências, acionar encarregado e equipe de resposta | LGPD, arts. 46 e 50, § 2º, I, "g"; Res. CD/ANPD 18/2024, art. 16, I |
| Dia do conhecimento (D) | Data em que o controlador soube que dados pessoais foram afetados | Res. CD/ANPD 15/2024, art. 6º, § 1º |
| D + 3 dias úteis | Comunicar à ANPD e aos titulares, se houver risco ou dano relevante | arts. 6º e 9º |
| Fim do prazo de comunicação aos titulares + 3 dias úteis | Juntar ao processo a declaração de que os titulares foram comunicados, com os meios usados | art. 9º, § 4º |
| Comunicação à ANPD + 20 dias úteis | Complementar, de forma fundamentada, o que faltou | art. 6º, § 3º |
| Divulgação pública | Manter visível por no mínimo três meses | art. 9º, § 3º |
| Sempre | Registrar o incidente, comunicado ou não; guardar no mínimo cinco anos (para órgão público, observadas a tabela de temporalidade e a guarda permanente, art. 10, § 2º) | art. 10 |

Agente de pequeno porte tem prazos em dobro (arts. 6º, § 8º, e 9º, § 6º); órgão público, em regra,
não (ver `references/base-legal.md`).

## 2. Primeiras horas

A skill **orienta a organização da resposta e redige documentos**. Ela **não faz perícia**, não
investiga invasão, não negocia resgate e não decide se o órgão comunica. Oriente a equipe a:

- conter o incidente (isolar o sistema, revogar credenciais) com a equipe técnica;
- preservar registros e evidências antes de apagar ou restaurar (ver "Cadeia de custódia" abaixo);
- anotar desde já datas e horários (ocorrência, detecção, conhecimento);
- avisar o encarregado e quem representa o controlador perante a ANPD;
- não divulgar detalhes técnicos fora da equipe (Decreto 10.748/2021, art. 15, para órgãos federais);
- não apontar culpados: a apuração de responsabilidade é feita depois, em processo próprio
  (sindicância ou processo administrativo disciplinar, Lei 8.112/1990, art. 143, com ampla defesa).

**Cadeia de custódia [CONFERIR com a equipe de resposta e a assessoria jurídica].** Orientação geral,
sem fonte normativa conferida por esta skill: registre quem coletou cada evidência, quando e de onde;
faça cópia íntegra antes de qualquer restauração; calcule e anote o resumo criptográfico (*hash*) de
cada arquivo coletado; guarde as cópias em local de acesso restrito, com registro de quem as acessou.
Em ransomware ou extorsão, preserve o bilhete do atacante e avalie com a assessoria jurídica o registro
de ocorrência policial [CONFERIR]. A skill não conduz perícia nem investigação criminal.

## 3. Comunicação à ANPD

- **Canal:** peticionamento no SEI!ANPD, tipo de processo de comunicação de incidente, com o
  formulário da ANPD (art. 6º, § 4º; art. 18, parágrafo único; orientação da ANPD).
- **Quem:** o encarregado, com documento de vínculo, ou representante com procuração, no mesmo
  prazo (art. 6º, §§ 5º e 6º). Sem isso, a ANPD pode abrir apuração (art. 6º, § 7º).
- **Sem informação completa no prazo:** comunique o que se sabe, justifique e complemente, de
  maneira fundamentada, em vinte dias úteis no mesmo processo (art. 6º, § 3º). A ANPD chama a
  primeira de "preliminar"; ela sozinha não cumpre o art. 48, e a comunicação por etapas é
  excepcional, com justificativa (orientação da ANPD).
- **Nível de acesso:** peça à ANPD, de maneira fundamentada, sigilo das informações protegidas por lei (art. 7º) e confira o nível de acesso
  de cada documento no SEI, porque documento público fica visível na pesquisa pública.
- **Lista de titulares:** não envie (orientação da ANPD). Informe números.
- Modelo: `references/modelo-comunicacao-anpd.md`.

## 4. Comunicação aos titulares

- De forma direta e individualizada, caso seja possível identificá-los, pelos meios usuais
  (telefone, e-mail, mensagem eletrônica ou carta; art. 9º, §§ 1º e 2º).
- Se for inviável, divulgação no sítio eletrônico, nos aplicativos, nas mídias sociais e nos canais de atendimento, com
  visualização fácil, por no mínimo três meses (art. 9º, § 3º).
- Linguagem simples (art. 9º, § 1º, I). Modelo: `references/modelo-comunicacao-titular.md`.

## 5. Registro

Todo incidente é registrado, inclusive o que não foi comunicado (art. 10). Modelo:
`references/modelo-registro.md`.

## 6. Governo federal: CTIR Gov

Órgãos e entidades da administração federal direta, autárquica e fundacional participam
obrigatoriamente da Rede Federal de Gestão de Incidentes Cibernéticos (Decreto 10.748/2021,
art. 1º, § 1º); empresas públicas e sociedades de economia mista federais participam por adesão
(§ 2º). Os participantes comunicam **imediatamente** ao CTIR Gov, por meio de sua equipe de resposta,
a existência de vulnerabilidades ou de incidentes de segurança cibernética que impactem ou possam
impactar os serviços prestados ou contratados (art. 12, IV).

O art. 12, IV, remete ao art. 17 do Decreto 9.637/2018, **revogado** pelo Decreto 12.572/2025,
art. 12, I. O dever continua no Decreto 10.748/2021; forma, canal e prazo detalhados pelo GSI: não
verificado [CONFERIR com a equipe de resposta].

Estados, DF e Municípios: não estão sujeitos a esses decretos federais. Normas locais de resposta a
incidentes: não verificadas; consultem a norma do próprio ente [CONFERIR].

## 7. Operador e contratos

A obrigação de comunicar é do **controlador**. O operador deve avisar o controlador sem demora
injustificada e passar as informações (orientação da ANPD) e trata segundo as instruções do
controlador (LGPD, art. 39). Verifique no contrato o prazo e o canal de aviso [CONFERIR].

## 8. Uso de `scripts/prazos_incidente.py`

```bash
python3 scripts/prazos_incidente.py --conhecimento 18/11/2026 --hoje 20/11/2026 --feriados 04/06/2026
```

Mostra vencimentos, situação (a cumprir, vencido, cumprido com atraso) e alertas, como a
obrigação de explicar a demora (arts. 6º, § 2º, V, e 9º, IV). A contagem é indicativa. O script não
sabe se houve expediente na sede da ANPD nem se o peticionamento eletrônico ficou indisponível
(Res. CD/ANPD 1/2021, art. 8º, §§ 1º e 2º): nesses casos, o prazo se prorroga ao primeiro dia útil
seguinte; informe a data com `--feriados` [CONFERIR]. Pontos facultativos também podem afetar a
contagem [CONFERIR].
