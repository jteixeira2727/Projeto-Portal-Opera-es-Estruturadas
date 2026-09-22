# Emergent Cold (ECLA Rio) — Memória da Operação

> Leitura direta dos 10 documentos em `Documentos/`: Termo de Emissão de Notas Comerciais (TE, 04/12/2025) e seus 1º (19/12/2025) e 2º (29/12/2025) Aditamentos, cada um com a versão consolidada no Anexo A; Termo de Securitização (TS, 19/12/2025) e 1º Aditamento (29/12/2025); Escritura de Emissão de CCI; Contrato de Cessão Fiduciária de Direitos Creditórios (CF, 22/12/2025); Contrato de Alienação Fiduciária de Imóveis (AF, 04/12/2025), o 1º Aditamento (07/01/2026) e o e-protocolo no RI. Todos têm texto nativo. Só as fórmulas são imagens, e foram lidas renderizando as páginas. Cruzada com `Pipeline/portfolio_data_wrapped.json` (snapshot jul/26, card "ECLA"). A operação **não tem entradas** em `documents_meta.json` / `obligations_data.json`.
>
> **Fonte de verdade**: para cláusulas do TE, vale o **Anexo A do 2º Aditamento ao TE** (consolidado mais recente). Para o TS, vale o texto consolidado no 1º Aditamento ao TS.
>
> Última atualização: 2026-09-22.

## Resumo

- **CRI**: 168ª Emissão da **VERT Companhia Securitizadora**, **2 séries**. Agente Fiduciário e Custodiante **Vórtx**. Coordenador Líder: VERT DTVM, com melhores esforços. Oferta CVM 160 rito automático, só Investidores Profissionais, sem rating.
  - Cetip: 25L3365825 / 25L3365829.
  - ISIN: 1ª série BRVERTCRIDM5; 2ª série BRVERTCRIDN3.
- **Emissão dos CRI**: 19/12/2025, **até R$ 160,0 MM**, em duas séries:
  - **1ª série**: R$ 110,0 MM (110.000 CRI × R$ 1.000), **integralizada em 30/12/2025**.
  - **2ª série**: até R$ 50,0 MM, integralização **a prazo e condicionada**. Financia a expansão refrigerada (ver Estruturação).
- **Vencimento dos CRI**:
  - 1ª série: **21/12/2040**.
  - 2ª série: 21/01/2041.
  - As NCs vencem 2 DU antes: 19/12/2040 e 17/01/2041.
- **Remuneração**: **IPCA (M-2) + 10,2211% a.a.** na 1ª série e **+ 10,2212% a.a.** na 2ª série.
  - Base 252, exponencial.
  - **Juros e amortização mensais** desde jan/26, sem carência. É uma tabela **tipo Price de 180 parcelas**, que amortiza 100% até o vencimento (ver Amortização).
- **Devedora / Emitente**: **Emergent Cold Rio Holdings Ltda.** (CNPJ 51.778.896/0001-75, SP), veículo da Emergent Cold LatAm (administrador/CFO LatAm: Pedro Holmes Monteiro Moreira).
- **Lastro**: 1ª Emissão de **Notas Comerciais escriturais** (Lei 14.195), em 2 séries, com colocação privada para a VERT. As NCs viram 2 CCIs integrais, sem garantia real, que lastreiam os CRI.
- **Ativo**: **Condomínio Multi Modal Duque de Caxias**, Av. OL 03, nº 200, Jardim Gramacho, Duque de Caxias/RJ. São 2 galpões refrigerados (Galpão 01 com 4 módulos e Galpão 02 com 18 módulos), mais o Lote 1 da Quadra F e o Lote remembrado 1 da Quadra G do International Business Park, onde ficam o pátio de manobras e a área de expansão. A Devedora detém o **domínio útil** (enfiteuse, com laudêmio na consolidação, cf. AF), e não a propriedade plena.
- **Garantias**:
  - AF do domínio útil das 24 matrículas, com Valor de Avaliação de **R$ 268,0 MM** (CBRE, 25/07/2025).
  - CF de todos os recebíveis do Imóvel e da Conta Vinculada.
  - Endosso dos seguros patrimoniais.
  - Fundo de Reserva de 3 PMTs e Fundo de Despesas.
- **Papel da Mauá**: há **dupla função**.
  - A **Mauá Capital Real Estate é o "Consultor Especializado da Securitizadora"** (TE 5.8). Valida as liberações, a 2ª série, o Relatório de Medição e o Reforço de Garantia.
  - O **MCCI detém 100% dos CRI** (`fund_positions`: saldo curva R$ 112,3 MM; MtM R$ 106,7 MM; 6,7% do fundo).
- **Posição (pipeline, jul/26)**: saldo de R$ 112,1 MM (PU 1.019,25 em 31/08), **LTV 41,8%**, **ICSD 1,79x** (jun/26) e duration de 5,6 anos.

## Estruturação

**Contexto do negócio**: a Emergent Cold comprou o Imóvel do **Tellus Rio Bravo Renda Logística FII** em 26/01/2024, com escritura complementar em 24/07/2024. O preço foi pago a prazo, garantido por uma **alienação fiduciária em favor do Tellus FII** (a "Alienação Fiduciária Existente", TE 8.2.2). O CRI refinancia esse *seller financing*: os recursos pagam a **penúltima parcela e antecipam a última** do preço. Na data de integralização, esse recebível já havia sido cedido pelo Tellus à **Opea Securitizadora**, o "Novo Credor" (TE 6.6.2). Depois, a AF superveniente passa a ser de 1º grau.

**Cadeia**: a Emergent Cold emite NCs 1ª/2ª série (colocação privada, 100% subscritas pela VERT). A VERT emite 2 CCIs integrais e, com elas, os CRI 1ª/2ª série (regime fiduciário, Patrimônio Separado).

**Desembolso da 1ª série (TE 6.6.2–6.6.3)**: a NC 1ª série é integralizada no mesmo dia do CRI. A **liberação** do Valor Líquido é que depende das CPs (redação esclarecida no 2º Aditamento). Antes, são retidos o Valor Inicial do Fundo de Despesas, o **Prêmio Investidor** (R$ 1,6 MM) e o Fundo de Reserva (R$ 3,4 MM) (TE 14.1). O restante sai em 3 tranches:
1. **Penúltima parcela do preço** → Opea (conta Itaú 15058-0/0910), no dia da integralização. O valor é validado pelo Consultor com carta do Tellus.
2. **Antecipação da última parcela** → Opea, pelo menos 1 DU depois. Com as duas, cancela-se a AF do Tellus.
3. **Saldo** → Conta de Livre Movimentação da Devedora (Itaú 84114-2/3786). Libera em até 2 DU após as CPs e a comprovação, nas matrículas, do **registro da AF e do cancelamento da AF Existente**.

**CPs da 1ª série (TE 6.6.6)**:
- Documentos assinados e ata de sócios arquivada na JUCESP.
- **Anuência do Tellus FII** à AF superveniente.
- AF registrada no RI de Duque de Caxias e CF protocolada no RTD/SP.
- Due diligence satisfatória **à VERT e ao Consultor (Mauá)**.
- Nenhuma MAC ≥ R$ 2 MM, declarações verdadeiras e legal opinion.
- Condição resolutiva: sem CPs em 90 dias da Data de Emissão (≈ 04/03/2026), a operação se desfaz. Nesse caso a Devedora paga **R$ 500 mil de taxa de descontinuidade à Mauá** (TE 14.7). Não ocorreu.

**O ponto específico da operação: volume de R$ 160 MM, com só R$ 110 MM integralizados**

A 2ª série (até R$ 50 MM) financia a **expansão da área refrigerada** e só é integralizada se forem cumpridas as **Condições Precedentes da 2ª Série** (TE 6.6.7; TS 4.2.2):
1. CPs da 1ª série cumpridas e **cancelamento da AF do Tellus averbado**.
2. Notificação da Devedora pedindo a integralização.
3. Registro dos Contratos de Garantia e dos aditamentos.
4. Reconfirmação das declarações (Anexo V).
5. **Agente de Medição de Obras** contratado, com Relatório de Medição mensal até o dia 5.
6. **Orçamento e cronograma físico-financeiro validados pelo Consultor (Mauá)**, com separação entre recursos próprios e recursos da 2ª série. Esse orçamento substitui o Cronograma Tentativo.
7. **Contrato de locação atípico (BTS ou equivalente) da nova área refrigerada**, validado pelo Consultor. O Consultor **não pode recusar** se o locatário for *investment grade* (Fitch/S&P/Moody's), ou se for a BRF ou empresa do grupo BRF com rating IG.
8. **Índice de Cobertura, Índice de Cobertura Obra e LTV *pro forma*** atendidos com a 2ª série.
9. Integralização dos CRI 2ª série.

**Mecânica da 2ª série (TE 6.6.7.2–6.6.10)**:
- **Pedido e validação**: a Devedora pede. Em 3 DU a VERT aciona o Consultor, que define o **"Valor Validado da Segunda Série"** em 2 DU. Esse valor é o orçamento menos os recursos próprios, mais a recomposição dos Fundos, arredondado para cima ao múltiplo de R$ 1.000 e limitado a R$ 50 MM.
- **Chamada**: em mais 3 DU a VERT faz a chamada de capital dos CRI 2ª série. Os investidores têm **até 90 dias** para integralizar.
- **Cancelamento das NCs excedentes**: as NCs além da quantidade validada são canceladas automaticamente, por aditivo e sem assembleia.
- **Fundo de Obras**: o dinheiro fica retido na Conta Centralizadora. É liberado **1 vez por mês, até o dia 10**, com base no Relatório de Medição validado pelo Consultor, que tem 5 DU para orientar a VERT, e a VERT paga em 2 DU. O saldo pós-obra só é liberado com habite-se, AVCB e termo de aceite do locatário.
- **Prazo fatal**: sem as CPs em **24 meses da integralização da 1ª série (≈ 30/12/2027)**, a 2ª série é **cancelada automaticamente**, e os subscritores ficam desobrigados (TS 4.2.5).
- **Fim do mandato da Mauá**: o mandato de Consultor termina (a) em 24 meses, se não houver 2ª série; ou (b) na conclusão da Obra mais a liberação do saldo do Fundo de Obras (TE 5.8.1).
- **Equilíbrio Econômico-Financeiro (TE 6.8.2.2.3)**: é apurado mensalmente durante a Obra: Saldo do Fundo de Obras − Custo a Incorrer ≥ 0.
  - Se o resultado for negativo, as liberações param e a Devedora banca a obra com recursos próprios.
  - Ela tem 6 meses para reequilibrar; senão, aporta na Conta Centralizadora em 5 DU.
  - **Não é evento de inadimplemento**: a única consequência é a obrigação de aporte (6.8.2.2.3.2).
- **Prêmio Waiver** (TE 6.8.1.1): enquanto vigora o Índice de Cobertura Obra (1,0x no lugar de 1,4x), a Devedora paga mensalmente um prêmio extra equivalente a **+1% a.a. sobre (VNa + Ji)**. A fórmula está redigida de forma truncada, `P = (VNa + Ji)^(1+1%)^(DP/252)-1`. A leitura econômica é `P = (VNa+Ji) × [(1,01)^(DP/252) − 1]`. O Prêmio Waiver entra no PMT do Índice de Cobertura.

**Prêmio Investidor** (TE 6.6.11; TS 3.18.1): R$ 1,6 MM (≈ 1,45% da 1ª série), pago aos titulares da 1ª série. A 1ª parcela é de R$ 1.183.333,35, em até 5 DU da integralização, e depois vêm 5 parcelas de R$ 83.333,33, com os rendimentos das aplicações. É um *fee* de originação que o investidor recebe à parte da taxa.

**Imóvel (AF Anexo C, CBRE 25/07/2025)**:

| Bloco | Matrículas | Valor de Avaliação |
|---|---|---|
| Galpão 01 – Módulos 01-04 | 29.702 a 29.705 | R$ 40,8 MM |
| Galpão 02 – Módulos 01-18 | 29.706 a 29.721, 26.441, 26.439 | R$ 183,7 MM |
| Lote 1 Quadra F (prédio nº 200 da Av. SN 2) | 35.480 | R$ 0,26 MM |
| Lote remembrado 1 Quadra G | 26.538 | R$ 43,2 MM |
| **Total** | 24 matrículas (2ª e 4ª Circ. RI Duque de Caxias) | **R$ 268,0 MM** |

O pipeline separa **"Valor de Avaliação Galpões" = R$ 224,5 MM**, que exclui os lotes F e G. O LTV contratual usa os **R$ 268 MM** (valor total do Imóvel Garantia).

**Rent roll cedido (CF Anexo II, valores de dez/25)**:

| Locatário | Área | Aluguel/mês | Índice | Término |
|---|---|---|---|---|
| **BRF S.A.** – Galpão B Mód. 1-6 | 18 docas | R$ 454.557,36 | IGP-M | 29/02/2030 |
| **BRF S.A.** – Galpão B Mód. 9-14 | 18 docas | R$ 454.557,36 | IGP-M | 29/02/2030 |
| **BRF S.A.** – contrato de 30/11/2018 (mat. 16.454-16.462) | provavelmente o pátio de manobras | R$ 291.945,00 | IPCA | 27/12/2028 |
| **BRF S.A.** – Mód. 7 | 3 docas | R$ 76.253,16 | IGP-M | 29/02/2030 |
| **BRF S.A.** – Mód. 15 | 3 docas | R$ 75.486,63 | IGP-M | 29/02/2030 |
| LMH Logistics | G01 tipo 02, 1.992 m² | R$ 50.807,99 | IPCA | 12/03/2027 |
| Zakat Distribuidora de Cosméticos | G02 tipo 16, 1.981 m² | R$ 48.530,09 | IPCA | 21/02/2027 |
| Rio Color | B-08, 2.285 m² | R$ 47.147,79 | IPCA | 15/08/2027 |
| Descalvado Express | A-01, 2.036 m² | R$ 46.550,86 | IPCA | **12/06/2026 (vencido)** |
| Norsulcargo | B-17, 1.981 m² | R$ 43.578,04 | IPCA | 31/12/2027 |
| Transcarapia | B-18, 2.030 m² | R$ 40.606,60 | IGP-M | 30/04/2027 |
| **Total** | | **R$ 1.630.020,88** | | |

- **BRF = 83% do rent roll cedido.** Os contratos de 2012 (Galpão B, com aditamentos até 2021) respondem por R$ 1,06 MM/mês e vencem em fev/2030.
- Os 6 contratos menores (17% da receita) **vencem todos até dez/2027**.
- A arrecadação efetiva no pipeline (≈ R$ 2,09 MM/mês) é **~28% maior** que a soma do Anexo II. Ver Pontos de atenção.

## Metodologia de cálculo — juros e atualização (TE 6.7–6.8; TS 4.3–5.2)

1. **Atualização monetária (IPCA, com defasagem de 2 meses, mensal)**: `VNa = VNe × C`, com `C = (NIk / NIk-1)^(dup/dut)`.
   - **NIk** é o IPCA divulgado no mês anterior ao da Data de Pagamento, que se refere ao 2º mês anterior. Exemplo: na PMT de jan/26 usa-se o IPCA de nov/25, divulgado em dez/25. Essa definição foi corrigida pelo **2º Aditamento ao TE**, cujo único objeto é a redação do NIk.
   - **dup** conta os DU desde a integralização ou a última PMT; **dut** conta os DU entre PMTs.
   - Só vale a **variação positiva**, porque o texto diz "variação positiva acumulada".
   - Sem IPCA divulgado, usa-se a projeção ANBIMA, sem compensação posterior. Se o IPCA ficar indisponível por mais de 30 dias, há AGT para escolher um Índice Substitutivo. Sem acordo, a Devedora resgata ao par, **sem prêmio**, em 15 dias.
   - Se o índice usado no CRI for menor que o do lastro por descasamento de datas, a **Devedora cobre a diferença** (TE 6.7.1(v); TS 4.10.1).
2. **Juros**: `Ji = VNa × (FatorJuros − 1)`, com `FatorJuros = (1 + taxa)^(DP/252)`, calculado com 9 casas e arredondamento.
   - Na 1ª série, taxa = **10,2211%** (TS 5.2; TE 6.8.1).
   - No **primeiro período** o lastro soma **+2 DU** ao dup e ao DP (TE 6.7.1 e 6.8.3). É o carry dos 2 DU entre o recebimento pela VERT e o pagamento ao CRI (TE 6.9.2).
3. **Período de Capitalização**: vai da integralização ou PMT anterior (inclusive) até a próxima PMT (exclusive).
4. **Datas**: as PMTs das NCs são mensais, nos dias 17-20 (Anexo I do TE). Os CRI pagam 2 DU depois, no dia ~21 (TS Anexo II). A Devedora deposita na Conta Centralizadora até 2 DU antes (TS 4.6.1).
5. **Encargos Moratórios**: multa de 2% mais juros de 1% a.m. (base 21 DU/mês), além da Remuneração e do IPCA (TE 6.12).

**Divergência relevante sobre a taxa**: o bookbuilding (1º Aditamento ao TE, 19/12/2025) trocou a taxa de "10,00%" para **10,2211% / 10,2212%** na cl. 6.8.1. Mas a definição de **"taxa" dentro da fórmula do Fator Juros (cl. 6.8.3) continua "10,0000%"** no consolidado do 2º Aditamento, e isso está confirmado visualmente na p. 34. O TS (5.2) e a CCI usam 10,2211%, e o pipeline também (`taxa_juros` 0,102211). Na prática vale 10,2211%, porque é o que a VERT calcula e a cl. 6.8.1 prevalece. Ainda assim, é um **erro de consolidação que deveria ser retificado** num próximo aditamento. Pela TE 16.3(iii), um erro grosseiro de digitação pode ser corrigido sem assembleia. Detalhe menor: a CCI cita 10,2211% "para cada série", mas a 2ª série é 10,2212%.

## Amortização

**Tabela do Anexo I do TE, lida linha a linha.** Não há carência, cash sweep, bullet nem incorporação de juros ("Incorpora Juros = Não" em todas as linhas). `AMi = VNa × Tai` (4 casas).

| | 1ª série | 2ª série (tabela teórica) |
|---|---|---|
| Parcelas | **180 mensais**, de 19/01/2026 a 19/12/2040 | 181, de 19/01/2026 a 17/01/2041 |
| Tai inicial / final | 0,3037% … 49,79% … **100%** | 0,3009% … 49,81% … **100%** |
| Amortizado até dez/26 | 3,2% do VN | 3,2% |
| até dez/30 | 19,1% | 18,9% |
| até dez/35 | 50,0% | 49,4% |
| até dez/38 | 77,1% | 76,3% |
| até dez/39 | 88,0% | 87,1% |

- **Perfil**: é um **Price em termos reais**. O Tai cresce de ~0,24-0,30% para 100%, de modo que o **PMT (juros + amortização) fica praticamente constante em ~1,05-1,07% do VN atualizado por mês** ao longo de 15 anos. A última parcela zera o saldo, que representa ~1,05% do VN inicial, e não há concentração no vencimento.
- A variação mês a mês do PMT (R$ 0,97-1,27 MM no pipeline) vem do número de DU de cada período, que afeta os juros, e do IPCA.
- **2ª série**: a tabela começa em jan/26 por ser teórica. Pela TE 6.10, a amortização só começa na PMT seguinte à integralização. É preciso um aditivo para registrar a quantidade final (6.6.7.2), e é provável que a tabela seja refeita nele.

## Covenants — metodologia de cálculo

### Índice de Cobertura (ICSD) — mensal, a partir de jan/26 (TE 6.8.2.1; TS 4.12.1)

`IC = RL / PMT ≥ 1,40x`
- **RL**: aluguéis **efetivamente recebidos** na Conta Vinculada (QI SCD, conta 1996253-8) ou na Conta Centralizadora (Bradesco 7075-0) **no mês anterior** ao da verificação. É regime de caixa e não usa média LTM.
- **PMT**: Amortização Programada + Remuneração + Prêmio Waiver devidos na **PMT do mês anterior**.
- A VERT calcula 3 DU antes de cada PMT.
- **Índice de Cobertura Obra ≥ 1,00x**: vale se houver 2ª série, da integralização até a conclusão da Obra ou o 1º aniversário, o que vier primeiro. Durante esse período incide o Prêmio Waiver.

**Exemplo com os dados do pipeline (jun/26)**: RL R$ 2.091.411,20 / PMT R$ 1.170.201,60 = **1,787x**. A série de jan a jun/26 foi 2,10 / 1,70 / 1,93 / 1,77 / 1,80 / 1,79. A folga é de cerca de 22% de queda de receita: com PMT de ~R$ 1,2 MM, o piso é RL ≈ R$ 1,68 MM. Sem a BRF, a receita cedida cai para ~R$ 0,28 MM, e o IC para ~0,2x.

**Consequência do desenquadramento (CF cl. 8)**: **não há cash trap nem retenção**. O mecanismo é o **Reforço de Garantia**:
1. A Devedora tem 5 DU após a notificação para indicar Novos Ativos: recebíveis de locação em dia, com aluguel mensal e locatário não falido/RJ.
2. Há um Parecer Servicer (do Consultor ou de servicer) e uma Auditoria Jurídica em 40 dias.
3. São duas AGTs: a primeira aceita em princípio e a segunda aprova os pareceres. O Consultor Mauá pode se manifestar antes, e cada etapa tem prazo de 5 DU.
4. Se o reforço não for feito ou não for aceito e o índice seguir desenquadrado, **a AGT pode declarar o vencimento antecipado**. É uma Hipótese Não Automática, a TE 10.3(xx).

Observação: o excedente da cascata só volta à Devedora "desde que não haja Hipótese de Vencimento Antecipado **em curso**" (CF 5.3). Na prática, **retém-se o caixa** a partir da ocorrência de um evento não curado, mesmo antes de a AGT deliberar.

### LTV ≤ 70% — mensal (TE 6.8.2.2; TS 4.12.2)

`LTV = SD / VI`
- **SD**: saldo do VN Atualizado das NCs **efetivamente integralizadas**.
- **VI**: valor de mercado do Imóvel Garantia no **último Laudo de Avaliação**, feito por Colliers, Cushman, JLL, CBRE ou CB Richard Ellis, pago pela Devedora.
- A VERT verifica 3 DU antes de cada PMT, "a partir da Data de Emissão".
- **Laudo anual**: entregue até **5 DU antes da PMT de janeiro de cada ano**, com data-base de no máximo 3 meses antes. Numa expansão, só entra a área efetivamente em obra.
- Exemplo (jun/26): 111,87 / 268,0 = **41,7%**.
- O teto de 70% comporta SD de até R$ 187,6 MM, ou seja, queda de ~40% no VI. Mesmo com a 2ª série cheia (SD ≈ R$ 162 MM), a folga seria de ~13% sobre o valor atual, antes de a expansão entrar no laudo.
- **Consequência (TE 7.5)**: **Amortização Extraordinária Obrigatória** na PMT seguinte, até reenquadrar em 70%, **com Prêmio de Pré-Pagamento** (piso de 3%, ver abaixo). Se não for paga, vira Hipótese Não Automática, a 10.3(xix).

### Covenants financeiros corporativos — anuais, exercício 2026 em diante (TE 11.1(xix))

A Emitente calcula com as **DFs auditadas consolidadas** e envia à VERT na mesma frequência das DFs, em até 90 dias do fim do exercício (11.1(vi)(c)). **1ª medição: exercício 2026, com DFs até ~31/03/2027.**

| Índice | 2026-2027 | 2028-2029 | 2030 em diante |
|---|---|---|---|
| (a) **EBITDA / Despesas Financeiras Líquidas** | ≥ 1,0x | ≥ 1,1x | ≥ 1,3x |
| (b) **Dívida Líquida / EBITDA Ajustado** | ≤ 5,2x | ≤ 5,2x | ≤ 5,2x |

Durante a Obra, uma variação de 20% no índice (a) **não é quebra**. Exemplo: ≥ 0,8x em 2026-27. A redação tolera só o item (a); a frase "nos índices indicados acima" é ambígua quanto ao (b).

**Definições (LTM, consolidado)**:
- **EBITDA** = receita operacional líquida − custos − despesas comerciais, gerais e administrativas + D&A, pelo fluxo de caixa das DFs.
- **EBITDA Ajustado** = EBITDA sem não recorrentes e **sem o rateio de despesas corporativas**. Isso favorece a SPE, que recebe rateio do grupo.
- **Dívida Líquida** = mercado de capitais + mútuos + empréstimos e financiamentos + **financiamento de aquisição de ativos a prazo com o vendedor** (o saldo com o Tellus, se ainda houver) − caixa e equivalentes, **incluindo contas vinculadas**, ou seja, Fundos e Conta Centralizadora.
- **Despesas Financeiras Líquidas** = encargos + variações monetárias − receitas financeiras, por competência, sobre os itens da Dívida Líquida, excluídos os não recorrentes.

Consequência: o descumprimento é obrigação não pecuniária. Vira **Hipótese Não Automática 10.3(i)**, com cura genérica de 15 DU.

**Ordem de grandeza (estimativa, não contratual)**: a receita anual do rent roll cedido é de ~R$ 19,6 MM (arrecadação de ~R$ 25 MM). A dívida é de ~R$ 112 MM, com juros reais de ~10,2% mais IPCA, o que dá despesa financeira líquida de ~R$ 16-17 MM por ano. Assim, **EBITDA/DFL deve ficar perto de 1,2-1,4x**, apertado para o piso de 1,3x a partir de 2030. DL/EBITDA fica em ~5x, perto do teto de 5,2x, e depende do custo condominial e do rateio. **Não há DFs na pasta** para confirmar.

### Fundo de Reserva (TE 14.3)

- Valor inicial de R$ 3.400.000,00, retido na integralização.
- **Mínimo: as 3 próximas PMTs**, projetadas com o IPCA mais recente ou zero, o que for maior.
- Verificação **diária** pela VERT.
- Recomposição: 1º pela cascata ou pelo saldo de integralização retido; 2º com recursos próprios da Devedora em 10 DU após notificação, **sob pena de vencimento antecipado** (14.3.2).
- Pipeline (jun/26): exigido R$ 3.690.051,86 × saldo R$ 3.770.103,98 → **enquadrado**, com folga de só ~R$ 80 mil. Como o PMT em R$ cresce com o IPCA e com os meses de mais DU, o exigido flutua e **o FR precisa de recomposição periódica pela cascata**.

### Fundo de Despesas (TE 14.2; Anexo VII)

- **Mínimo: as Despesas Recorrentes dos próximos 12 meses.** O valor inicial está no Anexo VII e cobre as iniciais mais 12 meses de recorrentes.
- Verificação diária. Recomposição pela cascata ou em 10 DU com recursos próprios, **sob pena de vencimento antecipado** (14.2.3). Despesas não cobertas pelo FD são pagas em 5 DU após notificação (14.2.7).
- **Despesas recorrentes do Anexo VII**, todas líquidas e com gross-up de ISS/PIS/COFINS, algumas com IGP-M:
  - Administração do Patrimônio Separado da VERT: R$ 3.500/mês.
  - Agente Fiduciário Vórtx: R$ 16.000/ano.
  - Liquidante: R$ 2.400/ano.
  - Escriturador CRI: R$ 3.000/ano, mais R$ 3.000 por série adicional.
  - Escriturador NC: R$ 4.000/ano.
  - Contador do Patrimônio Separado: R$ 620/mês.
  - Custódia B3 (0,00175% a.a.) e clearing B3.
  - Agente de Medição, se houver 2ª série.
  - Horas adicionais da VERT: R$ 770/h.
- A ordem de grandeza é de ~R$ 90-110 mil/ano brutos.
- **Despesas iniciais (flat)**: VERT R$ 30 mil, assessor legal R$ 185 mil, AF R$ 16 mil, escrituradores R$ 7 mil, coordenador R$ 30 mil, custodiante R$ 5 mil por CCI mais R$ 6 mil, ANBIMA e B3.
- **O pipeline não acompanha o Fundo de Despesas**: não há card do FD no `covenants` do ECLA.

## Pré-pagamento — como calcular a "multa" (TE 7.1–7.5; TS 6)

**Prêmio de Pré-Pagamento (TE 7.4.4, fórmula lida na imagem da p. 40)**:

```
Prêmio = [ Σ_{i=1..t}  PMTi / (1 + spread)^(ni/252) ] − Saldo Devedor        com piso 3,0% e teto 8,0%
```
- **PMTi**: juros + amortização ordinária das NCs devidos no i-ésimo mês remanescente, conforme a tabela, em termos do VNa.
- **spread**: TIR da **NTN-B de duration equivalente** ao prazo remanescente.
- **ni**: DU até cada PMT.
- **Saldo Devedor**: saldo na data do evento, sem o prêmio.
- É um **make-whole** que desconta o fluxo contratual (IPCA + 10,22%) à taxa real da NTN-B. O texto não diz sobre qual base incidem o piso de 3% e o teto de 8%. A leitura natural é o saldo devedor pré-pago, ou o valor amortizado na amortização parcial.

**Na prática o teto costuma se aplicar.** Com o fluxo Price remanescente (~171 meses) e curva flat:

| NTN-B (real) | 6,0% | 7,0% | 7,5% | 8,0% | 8,5% | 9,0% | 9,5% |
|---|---|---|---|---|---|---|---|
| Make-whole bruto | 25,8% | 18,8% | 15,5% | 12,4% | 9,4% | 6,5% | 3,8% |
| **Prêmio aplicável** | **8%** | **8%** | **8%** | **8%** | **8%** | 6,5% | 3,8% |

O prêmio fica **abaixo do teto só com NTN-B acima de ~8,75%**, e a duration encurta com o tempo. É uma aproximação: curva flat, sem IPCA, com a duration da NTN-B igual ao prazo.

**Onde o prêmio incide (e onde não incide)**:

| Evento | Base | Prêmio |
|---|---|---|
| **Resgate Antecipado Facultativo Total** (7.1): as duas séries juntas, aviso de 30 dias, só em data de PMT | VNa + juros pro rata | **Sim**, entre 3% e 8% |
| **Amortização Antecipada Facultativa** (7.4): em qualquer PMT, limitada a 98% do VN | parcela do VNa + juros | **Sim** |
| **Resgate Antecipado Obrigatório** (7.2): amortização acima de 98% vira resgate total | VNa + juros + encargos | Sim, se decorrer de amortização facultativa (7.2.2(d)). A 7.4.4 inclui também o decorrente de Amortização Extraordinária Obrigatória |
| **Amortização Extraordinária Obrigatória por LTV** (7.5) | parcela do VNa + juros | **Sim**, "sobre o valor da amortização" (7.5.1.1(iv)) |
| **Vencimento antecipado** (automático e não automático, 10.1/10.3) | Valor Total da Emissão + juros + encargos | **Sim** (10.1 caput; 10.6; 7.4.4) |
| **Oferta de Resgate Antecipado** (7.3): parcial ou total, aviso de 45 dias, AGT, adesão em até 20 DU, rateio pro rata | **VN** (sem "Atualizado", ver nota) + juros | Só o prêmio que a Devedora oferecer |
| **Reorganização Societária intragrupo** vetada pela AGT, com covenants pro forma OK (10.3(ix)(b)) | RAFT em 90 dias | **Não** |
| **Troca de Controle Indireto** + AGT decide pelo VA (10.3(xi)) | Resgate Obrigatório em 90 dias | **Não**, mas há **Prêmio de Troca de Controle de 1% do saldo**, sempre devido |
| **Tributo novo** (13.1) | RAFT em 20 DU | **Não** |
| **Sem Índice Substitutivo do IPCA** (6.7.6) | resgate ao par | **Não** |

**Nota**: a Oferta de Resgate (7.3.4 do TE; 6.4.9 do TS) cita "Valor Nominal Unitário", **sem "Atualizado"**, ao contrário dos demais eventos. Provavelmente é uma omissão, mas lida literalmente exclui o IPCA acumulado. Vale checar numa eventual oferta.

**Recompra**: o sumário do TS informa **"Admite recompra? Não"**. Não há recompra/repactuação. As saídas antecipadas são só as da tabela acima.

## Vencimento antecipado — TE cl. 10; TS cl. 7

**Rito**:
- **Automático** (10.1–10.2): independe de AGT. A Devedora paga em **2 DU** o Valor Total da Emissão + Remuneração + Encargos + **Prêmio de Pré-Pagamento**, e a VERT pode excutir as garantias direto.
- **Não automático** (10.3–10.6):
  1. A VERT ou o AF convoca a AGT **em 2 DU após o fim do prazo de cura**, para deliberar a **não declaração** do vencimento antecipado. O prazo é de 20 dias em 1ª convocação e 8 em 2ª.
  2. **O default favorece o VA**: a AGT decreta se aprovar o VA, e **também se não instalar ou não deliberar em 2ª convocação** (10.5). Mas a instalação acontece com **qualquer número** (TS 12.9).
  3. O quórum para *não* declarar é a maioria dos CRI em Circulação em 1ª convocação e a maioria dos presentes em 2ª (TS 12.13). Os quóruns contam **por série** (TS 12.2.1).
  4. Declarado o VA, a Devedora paga em 2 DU a contar da Notificação de VA.
- A Devedora deve informar qualquer hipótese de VA em **2 DU** (10.4; 11.1(v)).

**Automáticas (10.1)**:
1. Inadimplemento pecuniário não sanado em **2 DU**.
2. **Pedido** de RJ ou homologação de RE pela Devedora ou por empresa do Grupo Econômico no Brasil, independentemente de deferimento.
3. Pedido de falência não elidido no prazo legal; falência, liquidação ou dissolução.
4. Cessão das obrigações pela Devedora.
5. Invalidade dos Documentos por decisão transitada em julgado.
6. A Devedora ou afiliada questionar os Documentos.
7. **Transformação da Ltda. em tipo diferente de S.A.**
8. **Cross-acceleration ≥ R$ 2 MM** (Devedora ou afiliadas; cura de 5 DU para provar que não houve).
9. Distribuição de dividendos ou JCP **estando inadimplente** no pecuniário.
10. **Mútuo com o Grupo Econômico acima de (EBITDA do exercício anterior − dividendos distribuídos no exercício corrente).**

**Não automáticas (10.3, renumeradas pelo 1º Aditamento)**:
- (i) Descumprimento não pecuniário: cura específica ou **15 DU**.
- (ii) Desvio da destinação de recursos: 10 DU para demonstrar o contrário.
- (iii) Arts. 333 e 1.425 do CC.
- (iv) Evento material nas Garantias sem reforço ou substituição.
- (v) Protesto ≥ R$ 10 MM: 10 DU.
- (vi) Decisão judicial ou arbitral ≥ R$ 10 MM não paga.
- (vii) Direito de retirada de sócios.
- (viii) Redução de capital, salvo para absorver prejuízo.
- (ix) Reorganização societária com troca de controle sem AGT. Operações intragrupo com sociedade no exterior não contam. Se for intragrupo no Brasil com covenants pro forma OK e a AGT vetar, a Devedora pode fazer um RAFT **sem prêmio** em 90 dias.
- (x) **Troca de controle direto** para terceiros sem AGT (nova redação do 1º Aditamento).
- (xi) **Troca de Controle Indireto** (item novo, 1º Aditamento): a Devedora notifica em 90 dias e **paga 1% do saldo** em 5 DU, repassado aos titulares. A AGT decide: se não houver VA, fica só o prêmio de 1%; se houver VA, é Resgate Obrigatório **sem Prêmio de Pré-Pagamento** em 90 dias.
- (xii) Desapropriação acima de 5% do PL.
- (xiii) Arresto ou penhora ≥ 5% do PL: 15 DU.
- (xiv) Ato contra o contrato social: 10 DU para reverter.
- (xv) Perda de licenças com paralisação acima de 30 dias.
- (xvi) Condenação em 2ª instância por crime ambiental.
- (xvii) Trabalho escravo ou infantil, ou proveito de prostituição.
- (xviii) **Recebíveis deixarem de cair na Conta Vinculada ou Centralizadora**, ou deixarem de existir, sem reforço.
- (xix) **Não pagar a Amortização Extraordinária Obrigatória por LTV.**
- (xx) **Não fazer o Reforço de Garantia por IC** (CF 8).
- (xxi) Alteração relevante do Imóvel que reduza significativamente o valor do laudo.
- (xxii) Uso de bens contra a lei com Efeito Adverso Relevante.
- (xxiii) Corrupção (trânsito em julgado) ou inclusão no CEIS/CNEP.
- (xxiv) Aumento de capital em controladas que prejudique o pagamento, ou investimento em terceiros sem AGT.
- (xxv) Declaração falsa.
- (xxvi) **Alienação do Empreendimento sem AGT.**
- (xxvii) **Ônus sobre os bens das garantias sem AGT.**
- (xxviii) Descumprimento dos Contratos de Garantia, inclusive de registro: 15 DU após notificação.

Também geram VA, fora da lista: não recompor o FR ou o FD em 10 DU (14.2.3/14.3.2); não repassar em 2 DU aluguel recebido fora da conta (CF 5.1, que equipara a inadimplemento pecuniário, com multa de 2% mais 1% a.m.); e não reemitir a procuração da CF (6.6.1).

**Quóruns gerais (TS cl. 12)**:
- Instalação com qualquer número.
- Deliberação pela maioria dos CRI em Circulação em 1ª convocação e pela maioria dos presentes em 2ª.
- **Quórum qualificado**: maioria dos CRI em Circulação **em 1ª ou 2ª convocação** para alterar cascata, datas, vencimento, remuneração, índice, amortização, encargos, eventos de VA ou de resgate e quóruns (12.14).
- Em caso de falência ou RJ da Devedora, o quórum qualificado cai para a maioria dos presentes (12.15).
- **Conflito (12.18)**: prestadores de serviço da Emissão, como o Consultor Especializado (Mauá), e suas partes relacionadas não votam, **salvo se forem os únicos titulares** (12.19(i)). Como o MCCI detém 100% dos CRI, a exceção provavelmente se aplica. Mesmo assim, vale registrar a dupla função caso entrem outros investidores (por exemplo, na 2ª série). *Leitura informativa; a confirmação cabe ao jurídico.*

## Cascata (TS cl. 15 — Ordem de Pagamentos)

1. Despesas e **composição ou recomposição do Fundo de Despesas, do Fundo de Reserva e do Fundo de Obras**.
2. Multas, prêmios e penalidades, inclusive Encargos Moratórios.
3. Remuneração vencida.
4. Amortização vencida.
5. Remuneração do mês.
6. Amortização Programada do mês.
7. Amortização Extraordinária ou Resgate.

Na **CF 5.3**, o saldo remanescente vai para a Conta de Livre Movimentação em até 2 DU de cada PMT, **se não houver Hipótese de VA em curso**. Na **CF 5.1**, a Conta Vinculada (QI SCD) transfere para a Conta Centralizadora no mesmo DU ou em até 1 DU.

## Obrigações

### Pecuniárias

| Obrigação | Base | Status |
|---|---|---|
| PMT mensal (juros + Amortização Programada), depositada 2 DU antes | TE 6.9/6.10; TS 4.6.1 | Adimplente de jan a jun/26 (pipeline, pela `arrecadacao`). Jul e ago/26 estão sem registro de arrecadação no fluxo |
| Prêmio Investidor de R$ 1,6 MM (retido e pago em 6 parcelas, de jan a jun/26) | TE 6.6.11 | Retido na integralização. **Pagamento não verificável** no pipeline |
| Manter o FR em ≥ 3 PMTs; recompor em 10 DU se a cascata não cobrir | TE 14.3 | **Enquadrado** em jun/26 (R$ 3,77 MM × R$ 3,69 MM exigido) |
| Manter o FD em ≥ 12 meses de Despesas Recorrentes; recompor em 10 DU | TE 14.2 | **Não acompanhado no pipeline** |
| Cobrir o descasamento de IPCA entre lastro e CRI | TE 6.7.1(v); TS 4.10.1 | — |
| Repassar em 2 DU aluguel recebido fora das contas (multa de 2% + 1% a.m.) | CF 5.1 | — |
| Prêmio Waiver de +1% a.a. durante o IC Obra | TE 6.8.1.1 | Futuro, só com 2ª série |
| Prêmio de Troca de Controle Indireto (1% do saldo) | TE 10.3(xi) | Contingente |
| Aporte no Fundo de Obras se o Equilíbrio Econômico-Financeiro não se reestabelecer em 6 meses | TE 6.8.2.2.3.1 | Futuro, só com 2ª série |
| Laudos, registros, seguros, auditoria e despesas da Operação | TE 6.8.2.2.1, 11.1(xii), 14.7.1 | — |
| Indenização à VERT, aos titulares e ao AF, limitada ao Valor Total da Emissão + juros | TE 3.12 | — |

### Não pecuniárias

| Obrigação | Prazo / base | Status |
|---|---|---|
| Arquivar a ata de sócios na JUCESP e enviar à VERT e ao AF | 7 DU para protocolo; 5 DU do arquivamento (TE 2.3.1) | **Cumprido**: registrada em 12/12/2025 (nº 431.325/25-0). Houve uma **rerratificação em 29/12/2025**, protocolada sob nº 5.351.564/25-7 (TS 1.3, 1º Aditamento). O registro final da rerratificação não está na pasta |
| Registrar a **AF** no RI de Duque de Caxias | 60 + 30 dias da prenotação (TE 8.2.1) | **Parcial.** E-protocolo em 05/12/2025 no 3º Ofício de RI de Duque de Caxias; 1º Aditamento à AF em 07/01/2026, assinado no Assinador RI. **Não há matrícula com o R. da AF nem a averbação de cancelamento da AF do Tellus na pasta.** A tranche (iii) da 1ª série depende disso (TE 6.6.3.2) |
| Protocolar e registrar a **CF** no RTD/SP | protocolo em 5 DU; registro em 30 + 30 dias (CF 10.1) | **Não verificável**: não há certidão do RTD na pasta |
| Notificar os locatários vigentes da cessão e da conta de pagamento | 5 DU da 1ª integralização; comprovar em 2 DU (CF 5.1.1) | **Não verificável.** A arrecadação regular desde jan/26 indica que os pagamentos estão caindo nas contas |
| Aditar a CF em 10 dias a cada contrato novo ou aditado | CF 4.1 (Anexo III) | **Provável pendência**: a Descalvado venceu em 12/06/2026 (renovou? novo locatário?), e a arrecadação é 28% maior que o Anexo II. Não há aditamento da CF na pasta |
| Não celebrar, sem AGT, locação que reduza prazo, mude periodicidade, amplie a rescisão, exclua garantias (salvo com covenants pro forma OK) ou mude a conta | CF 4.1(i)-(v) | Renovações sem essas alterações dispensam AGT (4.1.1) |
| **Endosso dos seguros** (patrimonial; RC durante a Obra) | 60 + 30 dias da Data de Emissão, ≈ 04/03/2026 (TE 11.1(viii)); renovação comprovada 15 dias e 2 DU antes do vencimento (11.1(x)) | Pipeline: "OK", atualizado em 31/12/2025 e próximo em 30/06/2027 |
| **Relatório Mensal** (Anexo VI: locações, recebimentos por contrato e conta, Ratio ≥ 1,4) | 7 DU antes de cada PMT (TE 11.1(xxii)) | Não verificável na pasta. É a base do IC |
| **Relatório de Destinação de Recursos** semestral (Anexo IV) | até o último dia de jan e jul; o 1º até 31/01/2026 (TE 3.6) | **Não verificável** (jan/26 e jul/26) |
| **DFs auditadas** (Big4 ou Grant Thornton) + declaração do diretor financeiro + comunicações do auditor | 90 dias do fim do exercício (TE 11.1(vi)(c), (xx)) | DFs 2025 até ~31/03/2026: **não verificável**. DFs 2026, com os 1ºs covenants financeiros, até ~31/03/2027 |
| **Covenants financeiros** EBITDA/DFL e DL/EBITDA Aj. | anual, a partir do exercício 2026 (TE 11.1(xix)) | Futuro. **Não cadastrados no pipeline** |
| **Laudo de avaliação anual** | 5 DU antes da PMT de janeiro, com data-base ≤ 3 meses (TE 6.8.2.2.2) | O laudo vigente é da CBRE, de 25/07/2025. O **próximo vence ~jan/2027**, com data-base de out/26 ou depois. O pipeline marca 18/07/2026, sem base contratual |
| Agente de Medição e relatório mensal da Obra | da integralização da 2ª série até o fim da obra (TE 11.1(xxi)) | Futuro |
| Informar hipótese de VA ou descumprimento | 2 DU (TE 10.4; 11.1(v)) | — |
| Entregar os Documentos Comprobatórios (contratos de locação e aditivos) | 3 DU da celebração (CF 9.3.1) | Não verificável |
| Não onerar ou alienar o Imóvel ou os recebíveis; não fazer mútuo intragrupo acima do limite; não reduzir capital; cumprir a legislação socioambiental e anticorrupção | TE 10.1/10.3; 11.1 | Sem notícia de descumprimento |

Não há na pasta atas, comprovantes, relatórios mensais nem certidões de registro. Por isso o status é "não verificável" onde falta prova, como nas demais operações.

## Pontos de atenção / riscos

1. **Concentração na BRF (83% do rent roll cedido)**. Os contratos do Galpão B vencem em fev/2030, e o de 2018 (R$ 292 mil/mês) em **dez/2028**, com as NCs até 2040. Uma saída ou revisional da BRF derruba o IC para bem abaixo de 1,4x. O único remédio contratual é o Reforço de Garantia com outros recebíveis, que a SPE provavelmente não tem. O caminho real seria o VA ou uma renegociação.
2. **Rollover de curto prazo**: 6 contratos pequenos (17% da receita) vencem entre jun/26 e dez/27. A **Descalvado já venceu em 12/06/2026** e não há aditamento da CF.
3. **Rent roll × arrecadação**: o Anexo II soma R$ 1,63 MM/mês (dez/25), mas o pipeline registra ~R$ 2,05-2,09 MM/mês. Os reajustes não explicam 28% de diferença. É preciso identificar os recebimentos não listados (escritório, estacionamento, condomínio, reembolsos, outro contrato BRF?). **Se forem receitas não recorrentes ou reembolsos de condomínio, o IC de 1,79x está inflado.**
4. **Matrículas divergentes**: o rent roll da CF cita matrículas **24.569/24.570/24.580/24.588/24.589/24.590** ("2ª Circ. – 5º Ofício") e, no contrato BRF 2018, **16.454-16.462**. A AF e o TE usam **29.702-29.721, 26.439/26.441, 35.480, 26.538**. Provavelmente são matrículas antigas, anteriores a desmembramento ou remembramento, ou de outro ofício. Mas é preciso confirmar que todas as áreas locadas, e em especial o **pátio de manobras da BRF**, estão dentro do Imóvel Garantia.
5. **Domínio útil (enfiteuse)**: a garantia recai sobre o domínio útil. Na excussão incidem **laudêmio** e ITBI (AF), e o comprador em leilão herda o foro. Isso reduz a liquidez e o valor líquido de excussão em relação ao laudo.
6. **AF superveniente e cancelamento da AF do Tellus não comprovados**. Enquanto a AF do Tellus não é cancelada, a garantia do CRI é de 2º grau. É preciso pedir as matrículas atualizadas com o R. da AF e a averbação do cancelamento.
7. **Covenants financeiros apertados** a partir de 2030 (EBITDA/DFL ≥ 1,3x) e DL/EBITDA ≤ 5,2x desde 2026. Estimativa grosseira: ~1,2-1,4x e ~5x. **As DFs são necessárias** para calibrar. A 1ª medição com as DFs 2026 chega em ~mar/2027.
8. **2ª série = risco de execução de obra**. Durante a obra, o IC cai para 1,0x (Prêmio Waiver de +1% a.a.) e o LTV sobe para ~60%, antes de a expansão entrar no laudo. O Equilíbrio Econômico-Financeiro não é evento de default. A janela fecha em ~30/12/2027.
9. **FR com pouca folga** (R$ 80 mil em jun/26). Ele cresce em R$ com o IPCA e precisa ser recomposto pela cascata, o que é normal, mas exige monitoramento.
10. **Erros de redação**:
    - **TE 6.8.3: "taxa = 10,0000%"** × 10,2211% da cl. 6.8.1, do TS e da CCI. Deveria ser retificado.
    - **TE 6.5.1**: define "Data de Vencimento das NCs da **Primeira** Série" duas vezes (a 2ª deveria ser Segunda). O mesmo erro está na CF (Anexo I).
    - **TE 6.10**: numerada "5.1.1" e com uma cl. "6.10.1" vazia.
    - **TE 5.2.1**: "R$ 110.00.000,00".
    - **TE 10.1(viii)**: "R$ 2.000.000,000".
    - **TS**: várias "Erro! Fonte de referência não encontrada." (6.3.1, 7.3(ii), 7.3(ix)).
    - **CF**: cl. 5.5.1/5.5.2.
    - **Prêmio Waiver**: fórmula truncada.
    - **Oferta de Resgate**: cita "VN", sem "Atualizado".
11. **Dupla função da Mauá** (Consultor Especializado e investidor único). Ver quóruns. Também é relevante para a taxa de descontinuidade de R$ 500 mil (já superada) e para a validação da 2ª série.

## Inconsistências no pipeline (para corrigir)

- `fund_positions` → "vencimento: Jan/41" é o vencimento da **2ª série**, não integralizada. O da 1ª série é **21/12/2040** (`papel` e `summary` estão corretos).
- `covenants` → Laudo: "próxima 18/07/2026" **não tem base contratual**. O laudo anual é devido **5 DU antes da PMT de janeiro** (próximo ~jan/2027). A data do laudo vigente é 25/07/2025 (AF 6.1), e não 18/07/2025.
- `covenants` → **faltam**: (i) **Fundo de Despesas** (mínimo de 12 meses de recorrentes); (ii) **covenants financeiros** EBITDA/DFL e DL/EBITDA Ajustado (a partir do exercício 2026); (iii) Relatório Mensal e Relatório de Destinação; (iv) prazo da 2ª série (~30/12/2027).
- `covenants` → LTV com status "Verificar" e última atualização em mai/26, enquanto o fluxo tem LTV mensal até jun/26 (41,7%). O LTV está enquadrado.
- `caracteristicas` → "Amortização: Mensal" está correto. Vale detalhar "Price 180 meses, sem carência".
- `papel` → "Indexador: IPCA (M-2)" está correto, e "Multa" está correta (make-whole NTN-B, entre 3% e 8%). Vale acrescentar que o **teto de 8% se aplica com NTN-B abaixo de ~8,75%**.
- `ativo_info` → "valor_avaliacao 224,5 MM" são só os galpões. O LTV usa **R$ 268 MM** (inclui os lotes F e G).
- `fluxo` → jul e ago/26 estão sem `arrecadacao` nem `ic` (a planilha não foi atualizada?).
- `sobre_operacao`, `highlights`, `locatarios`, `quorum_assembleia` e `obrigacoes_pecuniarias` estão vazios. O rent roll da CF (Anexo II) pode alimentar `locatarios`, e as tabelas acima podem alimentar obrigações e quórum.

*Análise informativa; decisões formais seguem as políticas internas e aprovações da JiveMauá.*
