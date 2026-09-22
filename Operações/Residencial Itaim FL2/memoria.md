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

## Metodologia de cálculo da dívida (Escritura de Emissão de Debêntures, Cláusula 7 — espelhada 1:1 na Remuneração/Amortização dos CRI no TS)

Confirmado por leitura direta da Escritura: as Debêntures (e os CRI, que as espelham integralmente — mesma taxa, mesmas fórmulas, cf. TS Cláusulas 4.2/4.3 e 6.x) usam uma estrutura clássica de **atualização mensal por IPCA + juros prefixados exponenciais em Dias Úteis**, com um cronograma de amortização **pré-fixado no Anexo V** (não é SAC, Price, nem pass-through do caixa de locação) e uma multa de resgate antecipado que **varia conforme o motivo do resgate**.

### Atualização monetária (Cláusula 7.14) — `VNa = VNb × C`

`C = (NIk / NIk-1)^(dup/dut)`, onde `NIk` é o número-índice do IPCA do **segundo mês imediatamente anterior** à data de cálculo (defasagem M-2 — igual à Pirelli), `dup` = Dias Úteis decorridos desde a última Data de Pagamento (ou Primeira Integralização) e `dut` = Dias Úteis no período entre Datas de Aniversário (23 Dias Úteis na primeira, por definição contratual). **Periodicidade: mensal** (diferente da Pirelli, que atualiza só uma vez por ano em dezembro — aqui o IPCA é incorporado todo mês). Índice substituto em caso de indisponibilidade do IPCA por mais de 10 Dias Úteis: decidido em Assembleia de Debenturista/CRI; sem substituto acordado, resgate compulsório em até 20 dias pelo VNa + Remuneração, sem multa.

### Juros Remuneratórios (Cláusula 7.15) — `J = VNa × (Fator Juros − 1)`

Taxa de **7,85% a.a., base 252 Dias Úteis** (não 360 dias corridos), capitalização **exponencial** pro rata temporis por Dias Úteis decorridos (`dup`) desde a Primeira Integralização ou a última Data de Pagamento. `Fator Juros = (Spread/100 + 1)^(dup/252)`, com Spread = 7,8500. **Diferença relevante frente à Pirelli**: lá a capitalização de juros é por **dias corridos** (convenção 30/360); aqui é por **Dias Úteis base 252** — convenções distintas, não comparáveis diretamente sem anualizar. Pagamento: **mensal**, no Anexo V, 1ª parcela em 21/01/2021.

### Amortização (Cláusula 7.13 + Anexo V) — tabela pré-fixada, perfil "quase-bullet"

**Não é SAC/Price nem atrelada ao caixa de locação recebido** — é uma tabela de `Taxa de Amortização (TAi)` fechada no Anexo V, com **72 parcelas mensais** (11/12/2020 a 21/12/2026), em 3 fases bem distintas (conferido linha a linha no Anexo V):

1. **Períodos 1–24 (jan/2021 a dez/2022)**: `TAi = 0,3333%` por período — amortização linear de **8% do principal** ao longo dos 2 primeiros anos (saldo cai de R$ 1.000,00 para R$ 923,00 por R$ 1.000,00 de VN original).
2. **Períodos 25–71 (jan/2023 a nov/2026, ~4 anos)**: `TAi = 0,0000%` — **carência total de amortização**, só paga juros mensalmente (`Preço Unitário` e `Saldo Devedor` ficam travados em R$ 923,00/parcela desde jan/2023). Esse é o período em que a operação está hoje (jul/26).
3. **Período 72 — 21/12/2026 (Data de Vencimento)**: `TAi = 100%` — **bullet final**, quita a totalidade do saldo remanescente numa parcela só.

Ou seja: **é um perfil "quase-bullet"** — só 8% do principal é amortizado ao longo de 6 anos, com os 92% restantes concentrados na última parcela. Isso reforça o ponto de atenção já registrado sobre o vencimento de dez/2026 estar próximo sem sinal de refinanciamento/reestruturação: não há amortização relevante "aliviando" o saldo antes do vencimento, o salto é abrupto.

**Pequena divergência de data**: o Resumo desta memória (via pipeline) registra "Vencimento: 22/12/2026", mas tanto a Cláusula 7.12.1 da Escritura (2.201 dias corridos da Data de Emissão de 11/12/2020) quanto a última linha do Anexo V confirmam **21/12/2026** — 1 dia de diferença, mesmo padrão de pequenas divergências de data já visto entre fontes nesta operação (ver Resumo).

### Multa de resgate/amortização antecipada — 3 fórmulas diferentes conforme a causa (Cláusulas 7.17–7.22)

Não existe uma única "multa de resgate antecipado" nesta operação — o valor muda conforme o motivo:

- **Resgate Antecipado Obrigatório Total** (Cláusula 7.17.4 — gatilho: sobra de recursos não usados na aquisição dos Imóveis Lastro) e **Amortização Extraordinária Obrigatória Saldo da Destinação dos Recursos** (Cláusula 7.22.1(iii) — mesmo gatilho, mas parcial): multa fixa de **2% sobre o VNa** (ou saldo) resgatado/amortizado.
- **Resgate Antecipado Facultativo Total** (Cláusula 7.18.4) e **Amortização Extraordinária Facultativa** (Cláusula 7.20.4, remete à mesma fórmula da 7.18.4) — a Emissora pode antecipar a seu critério a qualquer momento (até 98% do saldo, no caso da amortização): multa calculada por uma **fórmula de "make-whole"** (prêmio nunca negativo, piso em zero):
  
  `Prêmio = Máximo[0 ; (((1+i/100)^(Du/252) / (1+Máximo[Y;B]/100)^(Du/252)) − 1) × VA]`
  
  onde `i` = 7,85 (a taxa contratual), `Y` = taxa da NTN-B de duration mais próxima à duration remanescente da parcela, na Data de Apuração (ANBIMA), `B` = 5,85 (piso mínimo pra Y), `Du` = duration remanescente em Dias Úteis até o Vencimento, e `VA` = valor da amortização. Ou seja, o prêmio só é positivo (e devido) se a taxa contratual (7,85%) render mais que a taxa de mercado de referência (Y, com piso de 5,85%) sobre a duration remanescente — mecanismo clássico de compensar o credor pela perda de rentabilidade num resgate antecipado voluntário, mas **nunca gera desconto para a Emissora** (o "Máximo[0;...]" impede prêmio negativo nesta hipótese — diferente da Oferta Facultativa de Resgate, cláusula 7.19, onde a multa negociada *pode* ser negativa).
  - **Casos sem multa nenhuma** (Cláusula 7.18.1/7.20.1): se o resgate/amortização for feito com (i) recursos da venda de algum Imóvel Lastro; (ii) recursos de venda de ações da Emissora após 24 meses da emissão, com mudança de controle; ou (iii) por gross-up de Tributos.
- **Amortização Extraordinária Obrigatória LTV** (Cláusula 7.21, o mecanismo de desalavancagem forçada já documentado na seção de covenants abaixo) e **Amortização Extraordinária Obrigatória Sinistro** (Cláusula 7.23, perda total de algum Imóvel): **sem multa** — só principal amortizado + juros pro rata + encargos moratórios se em atraso.

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
4. **Perfil de amortização "quase-bullet" (Anexo V da Escritura)**: só 8% do principal é amortizado nos 2 primeiros anos (jan/2021–dez/2022); de jan/2023 até nov/2026 a operação está em carência total de amortização (só paga juros); os 92% restantes do saldo vencem tudo de uma vez em 21/12/2026. Reforça o ponto 1 acima — não há alívio gradual de saldo chegando o vencimento, o salto de caixa exigido da Devedora é abrupto e total.
5. **Pequena divergência de data de vencimento**: o Resumo desta memória (pipeline) usa 22/12/2026; a Cláusula 7.12.1 da Escritura e a última linha do Anexo V confirmam **21/12/2026** — vale corrigir no pipeline.
