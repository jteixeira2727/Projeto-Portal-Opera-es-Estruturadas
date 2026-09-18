# Residencial Itaim FL2 — Memória da Operação

> Leitura derivada de `Pipeline/documents_meta.json`, `Pipeline/obligations_data.json`, `Pipeline/portfolio_data_wrapped.json` e leitura direta do Termo de Securitização, da Escritura de Emissão de Debêntures, do Contrato de Cessão Fiduciária de Recebíveis e do Contrato de Alienação Fiduciária de Imóveis (os 4 originais presentes na pasta). Não é fonte de dados para o `build_data.py` — é um resumo pra revisão humana.
>
> Última atualização: 2026-09-18.

## Resumo

- **CRI**: 195ª Série da 1ª Emissão, Habitasec Securitizadora S.A. — TS celebrado em 16/12/2020 (a Escritura de Emissão de Debêntures foi firmada na mesma data, segundo a ata de 29/06/2022, embora o dado financeiro registre 11/12/2020 como "Data de Emissão" — pequena divergência de datas entre fontes, não crítica).
- **Devedora**: Promontoria Imóveis 4 S.A. (mesma família Promontoria/Habitasec das outras operações — Jardins é Imóveis 5, Renda Residencial é Imóveis 1).
- **Emitido**: R$ 33.611.000, IPCA + 7,85% a.a. **Vencimento: 22/12/2026** — ou seja, **faltam poucos meses** (duration atual de apenas ~0,41 anos em jul/26). Diferente da Jardins e da Renda Residencial (vencimentos estendidos até 2032), esta operação está perto do fim do prazo original, sem reestruturação de prazo até o momento.
- Saldo devedor atual (jul/26): R$ 42,4 milhões. LTV atual ~49% (limite 60%).

## Estruturação: ainda é um deal de renda

Ao contrário da Jardins FL2 e da Renda Residencial FL2 (que nasceram como deal de renda e migraram pra deal de estoque), a **Residencial Itaim FL2 continua sendo um deal de renda**, sem cascata de vendas nem "Créditos Venda" — a operação segue estruturada só em cima da exploração locatícia (long-stay e short-stay, conforme contexto de negócio) dos imóveis.

**O ativo — Upper Itaim** (incorporadora Canopus, entrega mai/2016), Rua João Cachoeira nº 1.577, Vila Olímpia/Vila Nova Conceição, SP:
- **122 unidades no total do edifício**, mas **apenas 80 unidades compõem a garantia** da operação (adquiridas pela Promontoria Imóveis 4 especificamente pra essa estruturação) — as outras 42 unidades do prédio são de terceiros, fora da operação.
- ABL da garantia: 3.176 m² (40 m²/unidade em média). Valor de aquisição R$ 45,4 milhões; avaliação atual R$ 85,4 milhões.
- **Confirmado em 18/09/2026**: o Anexo I do Contrato de Alienação Fiduciária de Imóveis lista exatamente **80 matrículas** (192.575 a 192.66x, 4º Cartório de Registro de Imóveis de SP, todas do Condomínio Üpper Itaim) — o número certo é 80, como você indicou. O "70 unidades autônomas" que aparecia no texto descritivo (`sobre_operacao`) do dado financeiro estava **incorreto**; os campos estruturados (`garantias`/`ativo_info`), que já diziam 80, é que estavam certos. Vale corrigir o texto de `sobre_operacao` na próxima atualização do pipeline.

**Garantias** (conforme definição do próprio TS): Cessão Fiduciária de Recebíveis + Alienação Fiduciária de Imóveis (as 80 unidades) + Alienação Fiduciária de Ações (Fiduciantes: FIP Multiapartamentos 1 + Promontoria Imóveis 3).

**Confirmação de que é renda pura (não "aluguéis e vendas")**: o texto descritivo do dado financeiro (`sobre_operacao`) fala em "cessão fiduciária de recebíveis (aluguéis e vendas)", o que parecia contradizer a ideia de deal de renda puro. Lendo o Contrato de Cessão Fiduciária de Recebíveis diretamente: os "Direitos Creditórios Cedidos Fiduciariamente" são só (i) **Direitos Creditórios Locação** (aluguéis dos Contratos de Locação) e (ii) **Direitos Creditórios da Vendedora** — que, igual ao conceito equivalente já mapeado na Jardins FL2, **não é receita de venda de unidades pela operação**, e sim um direito de indenização/garantia contra a "Vendedora" (quem vendeu os imóveis originalmente pra Promontoria Imóveis 4) por eventual evicção ou outras perdas, nos termos do Compromisso e da Escritura de Compra e Venda originais. Ou seja: **confirmado, não há cascata de vendas nem receita de venda de unidades nesta operação** — a menção a "vendas" no dado financeiro é sobre essa garantia contingente, não sobre um fluxo operacional de venda de estoque.

## Metodologias de cálculo dos covenants (o que a documentação confirma)

### Fundo de Reserva (TS, Cláusula 15.1/15.1.1) — confirma os "3 PMTs"

Constituído com **3x (três vezes) a remuneração das Debêntures** incidente sobre o saldo do Valor Nominal Unitário Atualizado dos CRI, calculada sobre um período de **21 (vinte e um) Dias Úteis** (proxy de "1 mês" pra esse cálculo) — por isso o dado financeiro anota "3 PMTs (calculada sobre 21 dias úteis)". Valor mínimo (jul/26): R$ 801.848; saldo atual: R$ 822.280 (enquadrado). Recomposição: se cair abaixo do mínimo, a Devedora tem **3 Dias Úteis** (a partir da notificação da Emissora) pra recompor com recursos próprios. Verificação: **mensal**, até 3 Dias Úteis antes de cada Data de Pagamento (TS 15.1.2).

### Fundo de Despesas (TS, Cláusula 15.2)

Depósito inicial de R$ 199.028,70 (R$ 149.028,70 pras despesas iniciais do CRI + R$ 50.000,00 de reserva permanente), com **mínimo de R$ 25.000,00**. Se cair abaixo disso, complementação com recursos que transitarem pela Conta do Patrimônio Separado no mesmo mês — ou, se não houver recursos suficientes, a Devedora tem **20 dias corridos** (a partir da notificação) pra complementar.

### Índice de Cobertura (ICSD) — confirmado na Escritura: dois papéis diferentes no mesmo número

**Fórmula oficial** (Escritura de Emissão de Debêntures, definições): `ICSD = Locações / Juros`, onde **Locações** = somatório dos aluguéis dos Imóveis recebidos no mês, **brutos** de impostos/condomínio/qualquer dedução, e **Juros** = Remuneração das Debêntures no mês de apuração. Repara que essa fórmula usa só os **juros** no denominador (não juros + amortização) — mais simples do que ICSDs de outras operações que incluem amortização.

- **Como covenant "puro"** (Cláusula 9.1.2(xxvii)(b) da Escritura, confirmada na leitura direta): mínimo de **1,30x**, verificado **mensalmente a partir do 12º mês da 1ª Integralização**. Atual (jul/26): 2,34x — bem enquadrado. **Importante**: esse é um "Evento de Vencimento Antecipado NÃO AUTOMÁTICO" (Cláusula 9.3) — desenquadrar não vence a dívida automaticamente; obriga a Debenturista a convocar uma AGD em até 2 Dias Úteis pra deliberar se declara ou não o vencimento antecipado. Mesma regra vale pro covenant de LTV (item "a" da mesma cláusula xxvii).
- **Como gatilho de amortização extraordinária obrigatória** (TS, Cláusula 3.10 — usa o MESMO ICSD definido na Escritura): enquanto o **LTV for superior a 40%**, se o ICSD for **maior que 1,3x**, a Devedora tem até 5 Dias Úteis para usar 50% do valor calculado pela fórmula abaixo numa amortização extraordinária de até 98% do saldo:
  
  `Amortização Obrigatória LTV = 50% × (Locação − 1,3 × Parcela Mensal)`
  
  onde "Locação" = recebimentos do mês na Conta do Patrimônio Separado por exploração econômica dos imóveis, e "Parcela Mensal" = juros + amortização ordinários do mês (repare que aqui SIM entra a amortização, diferente da fórmula do ICSD em si). **Ou seja: o mesmo ICSD serve dois propósitos opostos** — baixo demais (<1,3x) pode levar a uma AGD decidir vencimento antecipado (risco de crédito); alto demais (>1,3x, com LTV>40%) obriga a Devedora a acelerar pagamento (mecanismo de desalavancagem forçada). Não é só um número "quanto maior melhor" nessa estrutura.

### LTV — dois limites diferentes, não confundir

- **40%**: limite dentro da Cláusula 3.10 do TS — abaixo disso, a Amortização Extraordinária Obrigatória LTV deixa de ser exigida (TS 3.10.1).
- **60%**: limite do covenant "oficial" (Cláusula 9.1.2(xxvii)(a) da Escritura, confirmada) — verificado **anualmente, no término de cada exercício social**, prazo de até 5 Dias Úteis da Emissora reportar após receber as informações da Cláusula 10.1(a). Também é Evento de Vencimento Antecipado NÃO AUTOMÁTICO (precisa de AGD). Atual: ~49% (enquadrado, com folga confortável dos dois limites).
- **Fórmula oficial** (Escritura): `LTV = SD / Valor de Mercado`, onde SD = saldo devedor da Debênture no mês, e Valor de Mercado = valor dos Imóveis com AF registrada, conforme laudo anual (entregue até 31/01), **descontado de eventuais passivos relacionados a esses Imóveis ou à Emissora** (fora desta operação) — ou seja, não é só o valor bruto do laudo, pode ser líquido de outros passivos.

## Instrumentos identificados

| Instrumento | Data original | Situação na pasta |
|---|---|---|
| Termo de Securitização (195ª Série) | 2020-12-16 | **Original presente.** |
| Escritura de Emissão de Debêntures (Promontoria Imóveis 4) | 2020-12-16 | **Original presente** (adicionado 18/09/2026) — confirma as definições "oficiais" de ICSD (1,30x) e LTV (60%), detalhadas acima. |
| Contrato de Cessão Fiduciária de Recebíveis | não confirmada (documento não traz a data de celebração no início do texto lido) | **Original presente** (adicionado 18/09/2026), inclusive com uma 2ª via já registrada no RTD-SP (`Cessão Fiduciária_Registrado RTD SP.pdf`). |
| Contrato de Alienação Fiduciária de Imóveis | **2021-01-04** | **Original presente** (adicionado 18/09/2026) — data confirmada na capa do próprio instrumento (diferente da suposição inicial de 16/12/2020). |
| Escritura de CCI | 2020-12-16 | Original **não presente**. |
| Alienação Fiduciária de Ações (Multiapartamentos 1 / Promontoria Imóveis 3) | não confirmada | Original **não presente**. A ata de 29/06/2022 autoriza expressamente um **novo aditamento** a este contrato (pra refletir redução de capital de até R$ 3,5 milhões) — **não é possível confirmar se esse aditamento foi de fato celebrado**, pois nem ele nem o contrato original estão na pasta. |

## Obrigações / última ata

**Ata mais recente na pasta**: AGT de 29/06/2022 — **única ata disponível**, e sem obrigação pecuniária com prazo específico (por isso `obligations_data.json` registra 0 items pra esta operação). O que ela aprovou:
- Anuência à **redução de capital social da Devedora em até R$ 3.500.000,00**, sem redução do número de ações.
- Autorização para celebrar um novo aditamento ao Contrato de AF de Ações refletindo essa redução (aditamento não confirmado como celebrado — ver gap acima).

Não há evidência na pasta de nenhuma assembleia posterior a 29/06/2022 — o que é consistente com uma operação de renda estável (sem eventos de waiver/reestruturação como Jardins e Renda Residencial), mas vale considerar que pode haver atas mais recentes fora desta pasta que ainda não foram coletadas (dado o vencimento próximo em dez/2026, seria esperado haver alguma assembleia de renegociação/quitação se a operação não for paga integralmente no prazo original).

## Pontos de atenção / riscos

1. **Vencimento em 22/12/2026 — bem próximo.** Diferente das outras duas operações de renda mapeadas (que já passaram por reestruturação/extensão de prazo), não há nenhum sinal na pasta de que a Itaim tenha sido renegociada — vale confirmar com a Devedora/Securitizadora se há um plano de quitação, refinanciamento ou extensão em andamento, já que faltam poucos meses. **Sem waiver/reestruturação registrada, os covenants oficiais valem como estão**: ICSD < 1,30x ou LTV > 60% (anual) levam a uma AGD ter que decidir sobre vencimento antecipado (não é automático).
2. **Gap do aditamento à AF de Ações** autorizado em 2022 — ainda não confirmado se foi celebrado (esse instrumento continua sem nenhum documento na pasta).
3. **Escritura de CCI ainda não está na pasta** — único instrumento "central" (dos 6 originalmente mapeados) que falta.
