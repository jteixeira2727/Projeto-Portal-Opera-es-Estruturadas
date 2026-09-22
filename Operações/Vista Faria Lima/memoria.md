# Vista Faria Lima — Memória da Operação

> Leitura direta dos 9 documentos em `Documentos/`: Termo de Securitização (TS, 256 págs.) e seu 1º Aditamento (Bookbuilding); Escritura de Emissão de CCI; Contrato de Cessão de Créditos (CC) e seu 1º Aditamento; Contrato de Cessão Fiduciária de Direitos Creditórios (CF); Contrato de Alienação Fiduciária de Imóveis (AF) e seus 1º e 2º Aditamentos. Cruzada com `Pipeline/portfolio_data_wrapped.json` (snapshot jul/26). A operação **não tem entradas** em `documents_meta.json` / `obligations_data.json`.
>
> **Nota de leitura**: o corpo do CC (págs. 2-28), da CF (págs. 2-28) e do Aditamento ao CC (págs. 2-10) são **PDFs escaneados, sem texto nativo** (só o carimbo do RTD é texto). Sem OCR local, as páginas foram renderizadas como imagem e lidas visualmente — é o CC (Anexo IV) que contém o ICSD, o LTV, os eventos de vencimento antecipado e as fórmulas de pré-pagamento. O 2º Aditamento à AF tinha fonte "embaralhada" (cifra de deslocamento) e foi decodificado; números conferidos pela soma do Anexo III. O arquivo do 1º Aditamento ao TS é uma **versão comparada** ("v1 cln vs vf (09.12)"), não a via assinada.
>
> Última atualização: 2026-09-22.

## Resumo

- **CRI**: 553ª Emissão, **série única**, Opea Securitizadora S.A. — Agente Fiduciário e Custodiante **Vórtx**. Código CETIP 25K3796700. Coordenador Líder Itaú BBA (garantia firme). Oferta CVM 160 rito automático, só Investidores Profissionais.
- **Emissão**: 19/11/2025, **R$ 317.450.000,00** (317.450 CRI × R$ 1.000). **Vencimento: 16/11/2032** (alterado de 18/11/2032 pelo 1º Aditamento ao TS).
- **Remuneração**: **IPCA + 8,5671% a.a.**, base 252, capitalização composta. Juros mensais (dia 15), **amortização 100% bullet no vencimento**, com Cash Sweep a partir do 37º mês.
- **Devedor**: Catuaí Vista FL FII RL (CNPJ 60.619.575/0001-19) — administrador Banco Daycoval, gestora Catuaí Gestora de Recursos.
- **Cedente**: BREF III FIP Multiestratégia RL (gestor BRL Trust), veículo do grupo GTIS.
- **Ativo**: Edifício Vista Faria Lima, Rua Prof. Atílio Innocenti, 165 (Vila Nova Conceição/Itaim), corporativo AAA. **A garantia cobre só 12 das 17 matrículas do prédio** (ver Estruturação).
- **Garantias**: AF dos Imóveis (12 matrículas) + CF dos recebíveis de locação + Fundo de Reserva (R$ 7.055.000 mínimo + R$ 3.530.000 adicional).
- **Posição Mauá (31/07/26)**: 92.589 CRI (**29,17% da emissão**), R$ 96,5 MM, adquiridos no secundário a **IPCA + 9,44%** (com deságio). Saldo total dos CRI: R$ 331,0 MM. PU: 1.042,60. Duration: 4,9 anos.

## Estruturação

**O lastro não é um CCV de imóvel, e sim uma parcela do preço de uma compra de participações societárias.** O Contrato de Compra e Venda de Quotas e Ações (CCVQA, 18/11/2025, não está na pasta) tem esta estrutura:

- **Vendedores**: BREF III FIP e GTIS Senior Management Feeder LLC.
- **Compradores**: Catuaí Vista FL FII (Devedor) e Safira FII.
- **Objeto**: a totalidade da BREF III Empreendimentos Imobiliários 9 S.A. e da GTIS Atílio Innocenti Empreendimentos Ltda. ("SPE Atílio", dona do edifício). Depois do fechamento, a SPE foi dissolvida e os imóveis passaram por dação em pagamento (escritura de 18/12/2025, retificada em 14/01/2026, citada no 1º Aditamento à AF).
- **Preço de Aquisição global: R$ 616.000.000,00** (CC, Considerando C):

| Componente | Valor | Pagador → Recebedor |
|---|---|---|
| Sinal | R$ 154.255.000,00 | → Cedente |
| Preço de Aquisição – GTIS LLC | R$ 3.693.990,84 | → GTIS LLC |
| **Parcela Securitizada (lastro do CRI)** | **R$ 317.450.000,00** | Devedor → Cedente, a prazo |
| Saldo do Preço | R$ 5.674.215,90 + R$ 134.926.793,26 | Devedor + Safira FII, no fechamento |

- **Cadeia**: o Devedor deve a Parcela Securitizada à Cedente. A Cedente cede esse crédito à Opea pelo **Preço de Cessão de R$ 317.450.000,00, ao par e sem coobrigação** (CC cl. 1.1 e 2.2). A Opea emite 1 CCI integral sem garantia real e, por fim, o CRI. Na prática, o CRI é um **seller financing securitizado**: os recursos da integralização pagam a Cedente. Depois de pago o Preço de Cessão, o CCVQA não pode mais ser resolvido por inadimplência do Devedor (CC cl. 2.2.6).

**Divisão do prédio (achado relevante)**: o edifício tem 17 matrículas no 4º RI-SP.

- **Catuaí Vista FL (garantia do CRI)**: 191.295 a 191.298 e 191.304 a 191.311 (12 matrículas). São os escritórios 201, 301, 401, 501 e 1101 a 1801 (Anexo III do 2º Aditamento à AF).
- **Safira FII ("Imóveis Safira", fora da garantia)**: 191.299 a 191.303 (5 matrículas).
- O pipeline mostra "ABL Total 16.475 m²", mas o campo "ABL Garantia" está corrompido (aparece como a data `1931-10-25`, provavelmente um número lido como data serial do Excel). **Não há na pasta a área própria das 12 unidades**, porque as certidões de matrícula são imagens.

**Rent roll cedido (CF Anexo I)**. O anexo lista contratos, sem áreas nem valores. O valor nominal dos direitos creditórios informado é de **~R$ 104,18 MM** (CF cl. 3.1).

| Locatário | Unidade (matrícula) |
|---|---|
| WeWork | 201, 301, 401, 501 (191.295 a 191.298): **4 andares, maior concentração** |
| Prudential do Brasil + Schonfeld Strategic Advisors | 1101, dividido (191.304) |
| Neste Brazil + Maneira Sociedade de Advogados | 1301, dividido (191.306) |
| Lumina Capital / OKT Capital | 1401 (191.307) |
| BNY Mellon DTVM | 1601 (191.309) |
| GTIS Partners Brasil (**parte relacionada ao vendedor**) | 1701 (191.310) |
| Trend Micro | 1801 (191.311) |

As matrículas **191.305 (1201) e 191.308 (1501) não têm contrato**, o que indica vacância de 2 dos 12 andares, ou 16,7%. Isso bate com a vacância de 16,6% do pipeline. Aluguel no pipeline: R$ 2,54 MM/mês.

A CF também prevê notificar a Cedente por conta de uma **"Renda Garantida"** definida no CCVQA. Ela provavelmente cobre a vacância, mas **os termos (valor e prazo) não estão na pasta**, e a renda não aparece no objeto da cessão (cl. 1.1), só na cl. 6.1 e nas minutas de notificação.

**Contas**: Conta Centralizadora Operacional 1 (Opea SCD, 535, ag. 0001, cc 12553-9) e Conta Centralizadora Operacional 2 (Itaú, 341, ag. 0910, cc 98799-9), ambas da Emissora. O sobejo é liberado para a conta do Devedor no Daycoval (707, ag. 0001-9, cc 723177-8).

**Cascata de Pagamentos (TS cl. 9.2)**:

1. Despesas.
2. Remuneração vencida e encargos.
3. Remuneração vincenda.
4. Recomposição do Fundo de Reserva até R$ 7.055.000.
5. **Até o 37º mês**: liberação do sobejo ao Devedor.
6. **A partir do 37º mês**: Amortização Extraordinária (cash sweep).
7. Resgate.

A cl. 9.2.1 obriga a liberar ao Devedor o suficiente para as despesas do Fundo, conforme um "Relatório Gerencial" que **não é definido em nenhum documento da pasta**. Pela CF, a liberação mensal (cl. 6.2.3) depende apenas de haver saldo para a próxima PMT mais despesas e de não haver vencimento antecipado em curso. A verificação ocorre 3 Dias Úteis antes de cada pagamento. Se faltar saldo, o Devedor tem **2 Dias Úteis** para complementar, sob pena de vencimento antecipado (CF cl. 6.2.2).

**Histórico dos instrumentos**:

| Instrumento | Data | Registro / nota |
|---|---|---|
| CC | 18/11/2025 | 8º RTD nº 1.606.651, 28/11/2025 |
| CCI e TS | 19/11/2025 | — |
| Bookbuilding | 05/12/2025 | 1º Aditamento ao TS, 08-09/12/2025 |
| 1º Aditamento ao CC | 11/12/2025 | Novos Anexos A e B (características e fluxo do lastro); RTD nº 1.608.556, 30/12/2025. CRI ainda não integralizados em 11/12 |
| CF | 15/01/2026 | RTD nº 1.609.355, 20/01/2026 |
| AF | 15/01/2026 | — |
| 1º Aditamento à AF | 04-05/02/2026 | Nota de devolução do cartório de 27/01; corrige o Considerando B: o fiduciante é dono só das 12 matrículas |
| 2º Aditamento à AF | 27/02/2026 | Nova nota de devolução, de 11/02; inclui o Anexo III com valores por unidade para leilão |

## Metodologia de cálculo — juros e atualização (TS cl. 6, 1º Aditamento ao TS)

**Taxa**: antes do bookbuilding, o TS previa o maior entre (i) a NTN-B ago/2030 + 0,75% e (ii) 8,5% a.a. O bookbuilding de 05/12/2025 fixou **8,5671% a.a.**, que é a taxa efetiva.

**Atualização monetária (cl. 6.1)**, mensal, pro rata por Dias Úteis:
- `VNa = VNe × C`, com `C = Π (NIk / NIk-1)^(dup/dut)`, 8 casas decimais e truncamento.
- NIk é o **IPCA do mês anterior** (M-1) quando o cálculo é feito até a Data de Aniversário, que é o **dia 15** de cada mês.
- `dut` do primeiro período = 22.
- Os juros do 1º período (da integralização até 15/12/2025) foram **incorporados** ao VNe (parcela nº 1 do Anexo I: "Incorporação = Sim").

**Juros (cl. 6.2.1)**:
- `J = VNa × (Fator Spread − 1)`, com `Fator Spread = (8,5671/100 + 1)^(DP/252)`, 9 casas decimais e arredondamento.
- DP = Dias Úteis desde o último pagamento.

**Exemplo validado contra o pipeline (PMT de 15/07/2026)**:
- DP de 15/06 a 15/07/2026 = 22 Dias Úteis, logo o Fator Spread = 1,085671^(22/252) = **1,007201845**.
- O juros unitário pago foi R$ 7,469599, o que implica VNa = 7,469599 / 0,007201845 = **R$ 1.037,17853**. Esse valor é exatamente o PU do pipeline na data.
- Resultado: PMT total = 317.450 × 7,469599 ≈ **R$ 2,37 MM**. A posição Mauá (92.589 CRI) recebeu ≈ R$ 691,6 mil.
- O mesmo teste bate em todas as PMTs de fev a jul/26: 22, 18, 21, 20, 20 e 22 Dias Úteis, respeitando os feriados de Carnaval, 03/04, 21/04, 01/05 e 04/06.

**Encargos moratórios**: multa de 2% mais juros de mora de 1% a.m. (TS cl. 19.3; CC cl. 6.3, com correção IPCA pro rata die).

## Amortização

**Programada (TS Anexo I, conforme o 1º Aditamento)**: 84 eventos. A tabela foi lida linha a linha.
- **Nº 1 (15/12/25)**: só incorporação.
- **Nºs 2 a 83 (15/01/26 a 15/10/32)**: juros mensais, Tai = 0,0000%.
- **Nº 84 (16/11/32)**: juros + **Tai = 100,0000%**.

Trata-se de um **bullet puro** de 7 anos. Não há parcela de amortização programada intermediária. O TS cl. 4.1(xix) diz "Taxa de Amortização: Não há", o que é contraditório com a tabela, mas sem efeito prático. A fórmula é `AMi = VNa × TAi`.

O **lastro** (novo Anexo B do CC) tem 83 parcelas, de 13/01/26 a **11/11/32**, com 100% no fim. O lastro paga cerca de 2 Dias Úteis antes do CRI. Por isso a AF cita vencimento em 11/11/2032 e o CRI vence em 16/11/2032.

**Amortização Extraordinária obrigatória (TS cl. 8.1)** tem três gatilhos:
1. **Cash Sweep**: a partir do 37º mês da emissão, 100% do sobejo dos Direitos Creditórios vai para Amex. O primeiro evento é na PMT nº 37, **15/12/2028**. Nem o TS nem a CF (cl. 6.2.4) definem percentual, teto ou reserva para o Devedor, além das "despesas do Fundo" da cl. 9.2.1. Pela leitura literal, o sweep é total.
2. **Antecipação Obrigatória por venda de imóveis**: 70% do produto da venda vai para Amex, mantido o LTV.
3. **Reenquadramento de LTV.**

A Amex é aplicada pro rata ao VNU na PMT seguinte, com **limite de 98% do VNU** e aviso à B3 com 3 Dias Úteis de antecedência.

**Efeito crédito**: até dez/28 não há amortização alguma. O saldo devedor cresce com o IPCA (R$ 317,45 MM na emissão → R$ 329,8 MM em ago/26). Com isso, o **LTV sobe mecanicamente** se o laudo não acompanhar.

## Covenants — metodologia de cálculo

### ICSD (CC Anexo IV, cl. 1.1(v)) — exigível a partir do 13º mês (dez/26)

Texto literal: "ICSD maior ou igual a i) 1,20x sem considerar o Fundo de Reserva; ou ii) maior ou igual a 1,30x incorporando, à Geração de Caixa, o Adicional Fundo de Reserva".

- **ICSD** = Geração de Caixa / Serviço da Dívida.
- **Período de Avaliação**: **os 12 meses anteriores** à data de cálculo, ou seja, **LTM e não spot mensal**.
- **Geração de Caixa**: "Somatório das Receitas decorrentes de locação dos Imóveis, das despesas de manutenção e dos encargos dos Imóveis". O texto não tem sinal de subtração; a leitura econômica é receita líquida de despesas e encargos.
- **Serviço da Dívida**: soma dos pagamentos dos Créditos Imobiliários, **calculados a uma taxa nocional**: o maior entre 8,5% a.a. e "spread sobre o IPCA da B30 + 0,75% a.a.". Não se usa a taxa efetiva de 8,5671%.
- **Adicional Fundo de Reserva**: "1/12 do Fundo de Reserva apurado no último dia útil de cada um dos meses do Período de Avaliação". Somado nos 12 meses, equivale ao **saldo médio do Fundo de Reserva inteiro**, não só do "Valor Adicional" de R$ 3,53 MM.

**Leitura crítica: a alternativa (ii) é muito mais frouxa que a (i).**

| Premissa | Valor |
|---|---|
| Serviço da Dívida LTM | ≈ R$ 26-27 MM (≈ 12 × R$ 2,2 MM) |
| Fundo de Reserva somado ao numerador | R$ 7,06 MM (mínimo) a R$ 10,59 MM (com o Valor Adicional) |
| Ganho no índice | ≈ +0,27x a +0,40x |
| ICSD "puro" que já atende 1,30x | ≈ **1,03x** |

O critério (i) de 1,20x só importa se o Fundo de Reserva for consumido. Além disso, o Devedor pode sacar o Valor Adicional a qualquer momento, desde que não haja inadimplemento. As contas acima são aproximadas e feitas por mim.

**Consequência**: o descumprimento é Evento de Pagamento Antecipado Compulsório **Não Automático** (CC Anexo IV cl. 2.2(i)), com **cura de 3 meses**. O evento não se caracteriza se o Devedor aportar ao Fundo de Reserva o suficiente para reenquadrar.

**Status**: o pipeline marca "Enquadrado", porque o covenant ainda não é exigível. O IC calculado, porém, é **spot mensal com a PMT efetiva**: fev 1,00x, mar 1,27x, abr 1,14x, mai 1,19x, jun 1,18x, **jul 1,07x**. Há duas consequências:
- **A metodologia do pipeline difere da contratual** (LTM, taxa nocional de 8,5%, Adicional do FR no numerador).
- **Sinal de alerta**: o spot rodou abaixo de 1,20x em 5 de 6 meses. Pelo critério (i), o primeiro teste em dez/26 (LTM dez/25 a nov/26) tende a falhar se a vacância de 16,7% persistir. Pelo critério (ii), com o FR somado, tende a passar.

A ser recalculado pelo método contratual assim que houver a DRE/rent roll mensal do Fundo.

### LTV (CC Anexo IV cl. 2.8; AF cl. 2.5.6)

- **LTV = saldo devedor dos Créditos Imobiliários ÷ valor de venda de mercado dos Imóveis** (só as 12 matrículas), com **teto de 70%** observado **mensalmente**.
- Laudo **anual**, contratado pelo Devedor, por Cushman & Wakefield, Colliers, CBRE, JLL, Dexter, B. Internacional ou Engebanc.
- **Consequência**: o LTV **não é evento de vencimento antecipado**. O desenquadramento leva à Antecipação Obrigatória com Amex para reenquadrar (CC cl. 2.9(ii); TS cl. 8.1(ii)). Não há prazo de cura nem de pagamento definido, e **o valor devido é o "maior entre" do make-whole** (ver Pré-pagamento). Se o Devedor não amortizar, o caso cairia genericamente no descumprimento de obrigação, que não está listado.
- **Status (jul/26)**: **63,7%**, enquadrado, com saldo de R$ 329,8 MM sobre avaliação de **R$ 517,2 MM** (pipeline). A folga equivale a uma queda de ~9% no valor do imóvel, e diminui com a correção do saldo pelo IPCA.
- **Atenção**: o Anexo III do 2º Aditamento à AF fixa o **Valor de Liquidação Forçada em R$ 391.075.026,00**, que é o piso do leilão. Sobre esse valor, o LTV seria **~81-84%**. A AF chama o denominador do LTV de "Valor dos Imóveis", termo que não tem valor numérico no Anexo III. O CC é claro ao usar o **valor de venda de mercado**, então o LTV de 63,7% está correto. Vale obter o laudo (data, avaliador, valor de mercado) para arquivar na pasta, porque ele não está lá.

### Fundo de Reserva (CC cl. 6.7; TS definições)

- **Valor Mínimo**: R$ 7.055.000,00, constituído na Conta Centralizadora 1 com recursos retidos na integralização. É recomposto pela cascata, item 4, e aplicado em títulos públicos ou compromissadas.
- **Valor Adicional**: R$ 3.530.000,00, depositado pelo Devedor, que pode sacá-lo a qualquer momento se não houver inadimplemento.
- **Status (jul/26)**: R$ 7.055.000, enquadrado. O pipeline não mostra se o Valor Adicional está depositado.

## Pré-pagamento — como calcular a "multa"

Não há uma multa única. Cada gatilho tem sua fórmula (CC Anexo IV, cl. 2.4, 2.9.1 e 2.10; TS cl. 8):

| Evento | Quando | Valor devido pelo Devedor |
|---|---|---|
| **Antecipação Facultativa Total** (CC 2.10) | Só **após 24 meses** da emissão, a partir de 19/11/2027 (lock-up) | **VP das PMTs remanescentes (juros + principal) descontadas pela TIR da NTN-B** com duration mais próxima da duration remanescente do CRI, cotação ANBIMA do 2º Dia Útil anterior. **Sem spread e sem piso no par.** Soma-se encargos moratórios, se houver |
| **Antecipação Obrigatória**: venda parcial com 70%, reenquadramento de LTV, venda total (CC 2.9.1) | A qualquer momento | **Maior entre** (i) saldo devedor + juros pro rata + encargos e (ii) **VP das PMTs remanescentes descontadas à NTN-B + 0,375% a.a.** |
| **Pagamento Antecipado Compulsório** (vencimento antecipado) (CC 2.4) | Evento automático, ou não automático declarado | **Saldo devedor (par), sem prêmio**, em até **30 Dias Úteis** da notificação. Se atrasar: 2% + 1% a.m. |
| **Cash Sweep** (TS 8.1) | A partir do 37º mês | Amex ao par, sem prêmio |

**Como calcular o make-whole na prática**:
1. Projete as PMTs remanescentes do CRI em termos reais: juros de 8,5671% sobre o VNa e 100% do principal em 16/11/2032.
2. Desconte cada PMT por `(1 + y)^(DU/252)`, com `y` = TIR da NTN-B de duration equivalente. Na Antecipação Obrigatória, use `y + 0,375%`.
3. O resultado sobre o VNa é o PU do pré-pagamento. O prêmio implícito é VP/VNa − 1.

Com duration de ~4,9 anos, cada 1 p.p. de diferença entre 8,5671% e a NTN-B vale **~4,5-5% do saldo** (aproximação por duration, calculada por mim).

**Pontos de atenção**:
- Na Facultativa, se a NTN-B passar de 8,5671%, o VP fica **abaixo do par**, porque não há piso. O Devedor pagaria menos que o saldo.
- No vencimento antecipado não há prêmio.
- Para a Mauá, que comprou a IPCA + 9,44% com deságio, qualquer liquidação ao par ou acima gera ganho sobre o custo.

## Vencimento antecipado (Pagamento Antecipado Compulsório) — CC Anexo IV, cl. 2.1-2.7; TS cl. 8.3 e 13

**Automáticos (cl. 2.1)**. A Cessionária exige o pagamento sem aviso:
1. Anulação, nulidade, ineficácia, rescisão ou transferência do CCVQA e/ou da Cessão, ou vício de validade/existência/exigibilidade dos créditos.
2. Créditos não pagos ou não transferidos à Conta Centralizadora 1 por ato ou omissão do Devedor, com **cura de 2 Dias Úteis**.
3. Questionamento judicial da Cessão pela Cedente e/ou pelo Devedor.

**Não automáticos (cl. 2.2)**. Dependem de assembleia:
1. Descumprimento do ICSD, com **cura de 3 meses**, salvo aporte suficiente ao Fundo de Reserva.
2. Venda ou transferência total ou parcial dos Imóveis, salvo se 70% do produto for para Amex e o LTV for mantido.
3. DFs auditadas não entregues até 16/02/2026, com **cura de 10 Dias Úteis**.
4. Atos de corrupção, conforme o rol das Leis Anticorrupção (inclui FCPA e UK Bribery Act), que impactem o pagamento.
5. Descumprimento da Legislação Socioambiental que impacte o pagamento.
6. **Contratação de novas dívidas pelo Devedor sem anuência prévia da Cessionária.**

A lista é curta: não há cross-default, limite em R$ nem vencimento por LTV. Na CF, a falta de complementação de caixa em 2 Dias Úteis (cl. 6.2.2) também é tratada como "evento de vencimento antecipado", mas **não consta da lista do CC**.

**Rito dos não automáticos**:
1. Encerrado o prazo de cura, a Emissora comunica o Agente Fiduciário e convoca assembleia em **até 7 Dias Úteis** (TS 13.3.4).
2. **O perdão (waiver) exige 75% dos CRI em Circulação**, em qualquer convocação (TS 13.3.4 combinada com a 13.8.2).
3. **Se a assembleia não se instalar, não houver manifestação ou faltar quórum para o waiver, a Emissora deve decretar o pagamento compulsório** (TS 13.3.4; CC 2.3).

O quórum trabalha a favor do credor: **com 29,17%, a Mauá sozinha consegue bloquear qualquer waiver**, o que na prática força o pagamento antecipado. O TS cl. 8.3.2 remete à "cláusula 13.5", remissão errada (o correto é 13.3.4), e usa o termo "Recompra Compulsória", que não é definido.

**Pagamento**: saldo devedor ao par em até 30 Dias Úteis da notificação (CC 2.4). Não pago, incide mora de 1% a.m. + multa de 2% (CC 2.6). A obrigação é qualificada como negócio aleatório (arts. 458 e seguintes do CC). Os CRI são resgatados pelo Resgate Antecipado Obrigatório (TS 8.3), com aviso à B3 de 3 Dias Úteis.

**Excussão**:
- **AF (cl. 6)**:
  - Prazos: carência de 5 Dias Úteis e purga da mora em 15 dias.
  - Leilões: 1º leilão em até 60 dias da consolidação, com lance mínimo no maior entre o "Valor dos Imóveis" e a base do ITBI; 2º leilão em 15 dias, com lance mínimo na Dívida, podendo aceitar 50% do valor com quitação parcial.
  - Saldo remanescente: continua devido, pelo art. 27 §5º-A da Lei 9.514.
- **CF (cl. 7)**: excussão imediata, venda sem leilão e gestão direta dos recebíveis.
- **Recompra**: não existe recompra pela Cedente, que não tem coobrigação.

**Quóruns gerais (TS cl. 13)**:
- Instalação: 50% + 1 dos CRI em Circulação em 1ª convocação; qualquer número em 2ª.
- Deliberação: 50% + 1 dos CRI em Circulação em 1ª convocação, ou dos presentes em 2ª.
- **75% dos CRI em Circulação** para: remuneração, cascata, datas, vencimento, eventos de pagamento/resgate e quóruns.
- Liquidação do Patrimônio Separado: maioria simples.

## Obrigações

### Pecuniárias

| Obrigação | Base | Status |
|---|---|---|
| Juros mensais dia 15 (83 PMTs) e principal bullet em 16/11/2032 | TS Anexo I | Adimplente até jul/26 (pipeline) |
| Manter o Fundo de Reserva em R$ 7.055.000 (recomposição pela cascata) e depositar o Valor Adicional de R$ 3,53 MM | CC 6.7 | FR mínimo OK (jul/26); **Valor Adicional não verificável** no pipeline |
| Complementar insuficiência de caixa em 2 Dias Úteis após notificação | CF 6.2.2 | Não houve evento conhecido |
| Cash sweep integral a partir do 37º mês (dez/28) | TS 8.1/9.2; CF 6.2.4 | Futuro |
| Despesas da operação (Anexo III do CC) | CC 6.1 | Sem evidência de atraso |
| Repassar em 5 Dias Úteis valores recebidos fora da Conta Centralizadora (mora de 2% + 1% a.m. + IPCA) | CC 5.2.2; CF 5.1(x) | — |
| Custear laudos anuais, registros e excussão; indenizar a Cessionária | AF 2.5.5, 4.2.2, 10.13; CC 9.9.7 | — |

Composição das despesas do Anexo III do CC, que o Devedor arca:
- **Iniciais**: R$ 227,2 mil brutos.
- **Recorrentes**: ≈ R$ 105,7 mil/ano brutos. Inclui Opea (R$ 3.250/mês), Vórtx AF (R$ 13.000/ano), custódia (R$ 6.000/ano), escriturador/liquidante (R$ 500/mês), auditoria do Patrimônio Separado (R$ 3.200/ano), contabilidade (R$ 260/mês) e custódia B3 (R$ 2.285,64/mês).

### Não pecuniárias

| Obrigação | Prazo / base | Status |
|---|---|---|
| Registrar o CC no RTD | 5 Dias Úteis da assinatura (CC 2.4) | Registrado em 28/11/2025. Pela contagem do agente, cerca de 1 Dia Útil fora do prazo; sem consequência prática |
| Enviar cópia autenticada do CCVQA à Opea | 15 Dias Úteis (CC 8.3.1) | **Não verificável.** O CCVQA não está na pasta |
| Constituir e registrar a **CF** | 30 + 30 dias da integralização (CC Anexo IV 1.1(iii); CF 1.2) | **Cumprido.** Assinada em 15/01/2026 e registrada em 20/01/2026 |
| Constituir e registrar a **AF** | 60 + 30 dias da integralização; o prazo reinicia a cada aditamento exigido pelo cartório (AF 4.1) | **Não confirmado.** Houve 2 notas de devolução (27/01 e 11/02/2026). Com a contagem reiniciada no 2º Aditamento (27/02), o prazo vai até ~28/05/2026. **Não há matrícula com o registro (R.) da AF na pasta.** As certidões anexadas são de 15/12/2025 e mostram prenotação de cancelamento de garantias anteriores (nº 699.384) |
| Notificar locatários, fiadores e a Cedente (Renda Garantida) e comprovar | 5 Dias Úteis do pagamento do Preço de Cessão (CF 6.1) | **Não verificável.** Ver o risco da conta 2 nos pontos de atenção |
| Aditar a CF semestralmente (até 31/jan e 31/jul) para incluir novas locações | CF 1.1.1 | **Sem evidência do aditamento de jul/26** |
| DFs auditadas | Até 16/02/2026 (CC Anexo IV 1.1(i)) | Cumprido, segundo o pipeline. O CC só fixa essa data; a "próxima 28/02/2027" do pipeline não tem base nos documentos lidos (pode vir do regulamento ou de norma CVM) |
| ICSD a partir do 13º mês; LTV ≤ 70% mensal; laudo anual | CC Anexo IV | Ver Covenants |
| Não contratar novas dívidas sem anuência; não vender ou onerar Imóveis, salvo com 70% para Amex | CC Anexo IV 2.2; AF 2.6.1/7.1 | Sem notícia de descumprimento |
| Informar fato adverso em 2 Dias Úteis; ações ou citações em 5 Dias Úteis; esbulho ou perda de licença em 10 Dias Úteis; defender as garantias; permitir inspeção; cumprir normas anticorrupção e socioambientais | CF 5.1; CC 1.2.1; AF 7.1 | — |
| Seguro patrimonial e de perda de aluguel endossado à Opea | Pipeline cita "AF cl. 2.1.1 e 2.6.5" | **Divergência.** A AF lida **não contém** obrigação de contratar ou endossar seguro; seguro só aparece como despesa. A obrigação pode estar no CCVQA, ou o texto do card veio de outro deal. A confirmar |

Não há na pasta atas de assembleia, comprovantes nem relatórios mensais da securitizadora. Por isso o status acima é "não verificável" quando não há prova, seguindo o padrão recorrente das outras operações.

## Pontos de atenção / riscos

1. **ICSD**: a metodologia contratual (LTM, taxa nocional de 8,5%, FR no numerador) difere da do pipeline (spot mensal). O spot está abaixo de 1,20x na maior parte de 2026 (jul: 1,07x). O critério (ii), de 1,30x com o FR, é bem mais frouxo e provavelmente passa em dez/26.
2. **Vacância e concentração**: 2 dos 12 andares estão sem contrato (1201 e 1501). A WeWork ocupa 4 andares, e a GTIS Partners, parte relacionada ao vendedor, é locatária. A "Renda Garantida" do CCVQA, que provavelmente cobre a vacância, **não tem termos na pasta**. O que acontece quando ela acabar é o principal driver do ICSD.
3. **Garantia é uma fração do prédio**: 12 de 17 matrículas. As outras 5 são do Safira FII. Vale mapear a convenção de condomínio e as áreas comuns.
4. **LTV sobe com o IPCA** até o sweep de dez/28. A folga atual é de ~9% no valor. O valor de liquidação forçada (R$ 391 MM) implicaria LTV de ~84%. **O laudo não está na pasta.**
5. **Registro da AF não comprovado** (duas notas de devolução, sem matrícula atualizada). Vale pedir a certidão com o R. da AF.
6. **Conta Centralizadora 2 com banco divergente**: a cl. 6.1 da CF diz Itaú (341), mas as minutas de notificação aos locatários (Anexo II) dizem Opea SCD (535), com a mesma agência e conta 0910/98799-9. Há risco de aluguel direcionado a uma conta inexistente. Conferir as notificações efetivamente enviadas.
7. **Pré-pagamento assimétrico**: a Antecipação Facultativa (após nov/27) é descontada à NTN-B **sem piso no par**, e o vencimento antecipado é ao par, sem prêmio. Por outro lado, a Mauá detém mais de 25% e bloqueia waivers (quórum de 75%).
8. **Cash sweep sem parametrização**: não há percentual nem valor retido para as despesas do Fundo. O "Relatório Gerencial" da TS 9.2.1 não é definido na CF.
9. **Erros de template e remissões** (não afetam a exigibilidade, mas valem registro):
   - **TS**: "Vne… Segunda/Quarta Série"; "Alienação Fiduciária de Ações" no Regime Fiduciário; destinação "aquisição de terrenos" (cl. 9.4); remissões 8.3.2 → 13.5.
   - **CCI**: diz que não há juros nem atualização e cita "505ª emissão". O novo Anexo A do CC corrige para IPCA + 8,5671%; **não há aditamento da CCI na pasta**.
   - **AF**: procuração do Anexo II menciona "matrícula 9.134 – Deodápolis/MS" e o endereço antigo da Opea, erro que persiste nos 2 aditamentos. **Recomendável retificar**, porque afeta o mandato de excussão.
10. **Documentos ausentes**: CCVQA (Renda Garantida, definição de dívidas e B30), laudo de avaliação, matrículas atualizadas pós-registro, via assinada do 1º Aditamento ao TS, eventual aditamento à CCI, aditamento semestral da CF de jul/26 e relatórios mensais.

## Inconsistências no pipeline (para corrigir)

- `caracteristicas` → "Amortização: Mensal" está **errado**: o principal é bullet (juros mensais).
- `caracteristicas` → "Saldo Devedor Atualizado R$ 96.500.000" é a **exposição Mauá**, não o saldo do CRI (R$ 331,0 MM).
- `garantias` → "ABL Garantia" aparece como `1931-10-25`, erro de parsing de data. O campo "Aluguel (R$/m²) 261,86" também não fecha com ABL 16.475 m² / R$ 2,54 MM.
- Covenant IC: o cálculo é spot mensal, enquanto o contrato usa LTM, taxa nocional e o FR no critério (ii) (ver acima).
- Seguro patrimonial: a cláusula citada da AF não contém essa obrigação.
- DFs: a próxima data (28/02/2027) não tem base nos documentos lidos.
- `sobre_operacao`, `highlights` e `locatarios` estão vazios. O rent roll da CF (Anexo I) pode alimentar `locatarios`.

*Análise informativa; decisões formais seguem as políticas internas e aprovações da JiveMauá.*
