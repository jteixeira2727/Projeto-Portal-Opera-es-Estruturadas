# Evolution — Memória da Operação

> Leitura derivada de `Pipeline/documents_meta.json`, `Pipeline/obligations_data.json`, `Pipeline/portfolio_data_wrapped.json` e leitura direta do Termo de Securitização (`TS.pdf`), do 1º Aditamento ao Termo de Securitização, do 1º e 5º Aditamentos ao Contrato de Cessão Fiduciária, e da ata assinada da Assembleia Especial de 28/11/2024 (`CRI_1E181S_EVOLUTION_AGT_LOCAÇÕES_v.sign off.pdf`, adicionada nesta rodada). O "Instrumento Particular de Cessão Fiduciária de Direitos Creditórios" original (12/12/2019) também foi adicionado à pasta nesta rodada (`CRI Evolution - Cessão Fiduciária ASSINADO.pdf`), mas é um PDF **integralmente escaneado, sem nenhuma camada de texto nativo** (confirmado via PyMuPDF e `pdftotext`) — sem OCR disponível localmente nesta rodada (mesma limitação já registrada na memória da BR Properties), não foi possível ler seu conteúdo. Continua sendo o gap mais relevante da operação: é o instrumento que define a fórmula de LTV (Cláusula 4.5) e provavelmente outras cláusulas centrais das Garantias.
>
> Última atualização: 2026-09-18.

## Resumo

- **CRI**: 181ª Série, 1ª Emissão, Habitasec Securitizadora S.A. — Agente Fiduciário Vórtx.
- **Devedora**: FUNDO DE INVESTIMENTO IMOBILIÁRIO – FII REC RENDA IMOBILIÁRIA (RECT11).
- **Garantia**: Edifício Evolution Corporate, Alameda Xingu 512, Alphaville — Barueri/SP. Triple A, Green Building, 31 andares, 110 unidades. O FII é dono de apenas **14.929 m² dos 52.043 m² totais do prédio (28,7%)**.
- Emitido em 12/12/2019: **R$ 63 milhões**, remuneração **IPCA + 6,25% a.a.**, juros e amortização **mensais**, sem carência. Vencimento final: **12/12/2034**.
- Saldo devedor total dos CRI (jul/26): R$ 61,3 milhões. Exposição Mauá/FII: 63,49% do CRI (R$ 38,9 milhões). Duration: 3,86 anos. LTV atual: ~41-43% (ver divergência na seção de riscos).

## Estruturação — deal de renda corporativa, com reforço de garantia por ativo externo ao prédio

Estrutura clássica de renda: **Fundo de Reserva** (constituído na própria emissão) + **Cessão Fiduciária dos recebíveis dos Contratos de Locação** + **Alienação Fiduciária do Imóvel**. Não há cascata de vendas (não é deal de estoque).

**Particularidade confirmada**: em 2024/2025, para reforçar o Índice de Cobertura (ver covenants abaixo), a Cessão Fiduciária foi ampliada para incluir os recebíveis de um contrato de locação de um **imóvel distinto do Evolution Corporate** — o chamado "Imóvel Corteva" (matrículas 165.222, 165.223 e 165.224, Registro de Imóveis de Barueri/SP), inicialmente locado para a Corteva Agriscience e, desde ago/2026, parcialmente substituído pela CTVA Proteção de Cultivos. Essa cessão fiduciária adicional aparece separada no rent roll (`CF - Corteva Agrisource`, R$ 167.988,77/mês) — é isso que o usuário descreveu como "inclusão de recebíveis de outros ativos para compor a arrecadação mensal".

**Garantia de Rentabilidade histórica (já extinta)**: no Contrato de Promessa de Compra e Venda original, a GIEDI (Cedente) se comprometeu a pagar R$ 38.400,00/mês na Conta do Patrimônio Separado durante jan-dez/2020, como reforço de renda no período de ramp-up do imóvel — cláusula 8.2 do TS, sem efeito hoje.

**Contrato de Cessão Fiduciária de Direitos Creditórios**: é o instrumento com mais aditamentos entre as operações mapeadas até agora — **5 aditamentos**. Só o 1º (16/06/2021) e o 5º (12/08/2026) estão na pasta; o 2º (07/07/2022), 3º (29/11/2022) e 4º (10/01/2025) são conhecidos só por citação nos considerandos do 5º. O instrumento original (12/12/2019) também não está na pasta.

**Histórico do rent roll (Elo/Digio)** — confirmado via atas:
- **jun/2021**: waiver aprovado em assembleia por descumprimento de trâmite ao celebrar o 6º Aditamento à locação da Elo Participações (mudança de reajuste IGP-M→IPCA + redução de aluguel) sem seguir a Cláusula 5.2(b)/(c) da Cessão Fiduciária. Autoexecutável, sem vencimento antecipado declarado.
- **out/2022**: rescisão parcial da locação Elo Participações (unidades 701-704, 7º andar), condicionada a novo contrato com o **Banco Digio** — formalizada depois no 4º Aditamento à CF (10/01/2025, não presente na pasta). Confirmado pelo rent roll atual, que já traz o Banco Digio como locatário ativo.
- **dez/2023**: isenção do reajuste IPCA/2023 e prorrogação da locação Elo Participações por 24 meses (novo vencimento 19/11/2026).
- **28/11/2024 — uma única Assembleia Especial, com 100% dos CRI em circulação presentes** (Mauá Capital Recebíveis Imobiliários FII, Mauá Capital High Grade FII, VBI Rendimentos Imobiliários I FII, Guardian Multiestratégia/Logística, e o investidor pessoa física Gustavo Sanchez Asdourian). **Correção importante em relação à leitura anterior**: o rascunho não assinado que eu tinha lido antes (arquivo `.docx`) e o 1º Aditamento ao TS (que traz o covenant do IC) **não são dois eventos distintos** — são a mesma Assembleia, cuja ata assinada foi adicionada à pasta nesta rodada (`AGT_LOCAÇÕES_v.sign off.pdf`). Nela foram deliberados, em conjunto:
  - Rescisão parcial da locação Elopar (unidades 501-504 e 601-604, 5º/6º andar), sem multa, condicionada a um novo contrato com a **Elo Serviços** (antes sublocatária) em até 30 dias do 13º Aditamento à locação Elopar — aluguel de R$ 238.912,80/mês com desconto de R$ 52.751,36/mês até 19/11/2026, líquido R$ 186.161,44/mês (R$ 53,00/m²); desconto reembolsável proporcionalmente em caso de rescisão antecipada;
  - Inclusão das unidades 201/202 (2º andar) na locação Elopar, sem cobrança de aluguel até 19/11/2026 (Elopar paga só encargos/tributos dessas unidades);
  - Desconto de R$ 131.969,74/mês no aluguel Elopar a partir de 01/12/2024, líquido R$ 465.461,90/mês (R$ 53,00/m²), também reembolsável em caso de rescisão antecipada;
  - Congelamento dos aluguéis Elopar e Elo Serviços (sem reajuste) até 19/11/2026;
  - **Inclusão do covenant de Índice de Cobertura** (mesma fórmula/mínimo 1,20x já descrita abaixo), condicionada à aprovação dos itens acima, com reforço da Cessão Fiduciária via inclusão dos recebíveis do Contrato de Locação Corteva;
  - Liberação automática da cessão fiduciária do Contrato de Locação Corteva em caso de venda do imóvel correspondente pelo Fundo, mediante simples comunicação prévia — desde que o Fundo proponha reforço equivalente da garantia em até 10 dias da liberação.
  
  O próprio Agente Fiduciário registrou nesta ata (item 8.4) que a renegociação da locação Elopar **aumenta o risco de crédito temporariamente** (redução das Garantias pelos descontos e ausência de reajuste), mitigado pelo reforço via Cessão Fiduciária do Contrato Corteva.
- **jul/2026**: rescisão parcial da locação Corteva (unidades 61-A e 81-A, mantendo 71-A por +3 anos) condicionada a novo contrato com a **CTVA Proteção de Cultivos** — formalizada no 5º Aditamento à CF (12/08/2026, registrado em cartório 27/08/2026), dentro do prazo de 30 dias.

## Metodologias de cálculo confirmadas (Termo de Securitização, Cláusula Quinta)

- **Atualização Monetária**: mensal, pela variação do IPCA, fórmula padrão `VNA = VNB x C` com fator `C` calculado por `(NIk/NIk-1)^(dup/dut)`, 8 casas decimais sem arredondamento. Índice substituto em caso de extinção do IPCA: IGP-M, ou novo índice acordado em assembleia — se não houver acordo, a Devedora pode pedir resgate antecipado total em até 30 dias.
- **Juros Remuneratórios**: 6,25% a.a. base 252 dias úteis, exponencial e cumulativo pro rata temporis: `J = VNA x (Fator de Juros - 1)`.
- **Amortização**: `AMi = VNA x TAi`, onde TAi é a taxa de amortização da i-ésima parcela **conforme tabela do Anexo I** (curva variável, não é SAC nem Price padrão — é uma tabela específica do cronograma).
- **Encargos moratórios**: multa de 2% + juros de mora de 1% a.m. sobre valor em atraso.
- **Prêmio de Antecipação** (para amortização extraordinária facultativa e para vencimento antecipado): `Prêmio = Pi x [(1+Spread/100)^(dup/252) - 1] x Saldo Devedor` com Spread de 5,75%.

## Vencimento antecipado (Cláusula Sexta do TS) — nenhum evento é automático

Lista de **22 eventos** (itens i a xxii) na Cláusula 6.7 — cobre desde descumprimento de obrigações não pecuniárias (10 dias úteis pra sanar), inexatidão de declarações, não constituição das garantias, desapropriação, ônus sobre os imóveis, cross-default (dívidas ≥ R$ 5 milhões), até questionamento judicial dos Documentos da Operação.

**Mecanismo importante**: diferente de outras operações mapeadas (ex.: BR Properties, que tem bifurcação automático vs. não-automático), aqui **nenhum evento gera vencimento antecipado automático**. Na ocorrência de qualquer um dos 22 eventos, a Securitizadora deve convocar Assembleia Geral em até 3 dias úteis; o vencimento antecipado só é declarado se titulares de **pelo menos 50% dos CRI em Circulação (do total, não apenas dos presentes na assembleia)** votarem favoravelmente — quórum mais exigente que o quórum geral de deliberação (50%+1 dos presentes). Em caso de vencimento antecipado declarado, o Fundo tem 10 dias úteis para pagar o saldo devedor + Prêmio de Antecipação.

Existe também a **Recompra Compulsória**: se a Alienação Fiduciária de Imóveis não for registrada em até 180 dias por fato imputável à Cedente, os titulares podem deliberar a retrocessão dos créditos à Cedente, que pagaria 100% do saldo devedor.

**Quóruns de Assembleia** (Cláusula 13 do TS): instalação com 2/3 dos CRI em Circulação em 1ª convocação (qualquer quórum em 2ª); deliberações gerais por 50%+1 dos CRI presentes; matérias sensíveis (datas de pagamento, redução de remuneração, prazo de vencimento, eventos de liquidação do Patrimônio Separado, alteração de quóruns) exigem **75% dos CRI em Circulação**.

## Covenants monitorados

### Índice de Cobertura (IC) — incluído a partir de 10/jan/2025

Fórmula (Cláusula 8.1/definições do TS, incluída pelo 1º Aditamento ao TS de 10/01/2025, decorrente da Assembleia Especial de 28/11/2024): **média dos últimos 3 meses do fluxo de recebíveis depositados na Conta do Patrimônio Separado ÷ média dos últimos 3 meses das parcelas de Amortização Programada + Juros Remuneratórios dos CRI ≥ 1,20x**, apurado mensalmente. Para viabilizar o covenant, a Cessão Fiduciária foi reforçada com os recebíveis do Novo Contrato de Locação (Corteva/Imóvel Corteva, ver estruturação acima).

Atual (jul/26): **1,25x** — enquadrado. **Alerta relevante já sinalizado no highlight do mês**: o Banco Digio comunicou intenção de descontinuar a locação dos conjuntos 701-704 (7º andar); se isso se concretizar, o IC spot cairia para **1,05x** (desenquadrado) e a média móvel de 3 meses cairia para **1,20x** (exatamente no limite).

**Mecanismo de desenquadramento — confirmado na ata da Assembleia de 28/11/2024** (gap da leitura anterior, agora resolvido): não é um mecanismo de retenção em camadas como o da BR Properties. Aqui é um **direito de cura**: apuração mensal, até 30 dias de cada Data de Pagamento, com base na média dos 3 meses anteriores (1ª apuração: Março/2025, 4 meses após a assembleia). Se o Índice de Cobertura Mínimo não for atingido em qualquer Data de Verificação, a Emissora notifica o Devedor, que tem **10 dias** para apresentar proposta de reforço da garantia — via **amortização parcial extraordinária dos CRI** ou **inclusão de novo direito creditório na cessão fiduciária** — em montante suficiente para reenquadrar o índice. Não há bloqueio automático de repasse de caixa nem vencimento antecipado automático associado especificamente ao IC; a inadimplência desse dever de reforço cairia, na prática, nos eventos genéricos de descumprimento de obrigação não pecuniária da Cláusula 6.7 do TS (10 dias úteis pra sanar, depois vencimento antecipado sujeito a assembleia).

### LTV

Cláusula 4.5(iii) do Contrato de Cessão Fiduciária (instrumento original, não presente na pasta — não consegui ler o texto exato da fórmula). Laudo de avaliação anual, sempre em dezembro, por CBRE, Cushman ou JLL. Laudo atual: **JLL, R$ 143,9 milhões**, avaliado em 01/12/2025 (próxima atualização 01/12/2026). Atual: **41,4%** — enquadrado (ver nota de divergência nos riscos).

### Fundo de Reserva

Constituído na própria emissão (Cláusula 8.1(i) do TS): **R$ 1.068.563,08 (2 PMTs)**. Atual: **R$ 1.796.803,77 (~2,06 PMTs)** — enquadrado, acima do mínimo.

### Seguro Patrimonial

Manutenção do seguro patrimonial contratado e endossado à Securitizadora (Cláusula 4.4 do Contrato de Cessão). O card do pipeline mostra ciclo de renovação 21/04/2024→21/04/2025, o que sugere que o dado não vem sendo atualizado a cada renovação anual.

### Rent roll / locatários (jul/26)

Acompanhamento mensal confirmado (campo `locatarios` preenchido, diferente de outras operações onde está vazio):

| Locatário | Área (m²) | % ocupação | Aluguel/mês | R$/m² |
|---|---|---|---|---|
| Elo Serviços | 3.512,48 | 25,0% | R$ 186.161,44 | R$ 53,00 |
| Elo Participações | 8.782,30 | 62,5% | R$ 465.461,90 | R$ 53,00 |
| Banco Digio | 1.756,24 | 12,5% | R$ 135.947,93 | R$ 77,41 |
| CF - Corteva/CTVA (imóvel separado) | — | — | R$ 167.988,77 | — |

Ocupação do Evolution Corporate (fração do FII): **100%**. Total considerado para o IC (prédio + Corteva/CTVA): R$ 955.560,04/mês.

## Obrigações / última ata

**Ata mais recente**: 14/07/2026 (arquivo "Nova Locatária_14.07.26.pdf") — aprovou a rescisão parcial da locação Corteva condicionada ao novo contrato CTVA, com prazo de 30 dias para aditar a Cessão Fiduciária. **Cumprido**: 5º Aditamento à CF assinado em 12/08/2026 e registrado em cartório em 27/08/2026, dentro do prazo (venceria 15/08/2026).

Demais itens históricos (todos cumpridos ou sem prazo em aberto): waiver de jun/2021 (trâmite do 6º aditamento à locação Elo), rescisão parcial Elo→Digio (out/2022), isenção IPCA + prorrogação Elo (dez/2023), e a Assembleia Especial de 28/11/2024 (Elo→Elo Serviços + inclusão do covenant de IC, ver estruturação acima) — ata assinada confirmada nesta rodada, 100% de presença dos CRI em circulação, prazo de 45 dias pra formalizar os aditamentos decorrentes (cumprido: 1º Aditamento ao TS assinado 10/01/2025).

## Pontos de atenção / riscos

1. **Contrato de Cessão Fiduciária original (12/12/2019) está na pasta mas é um PDF integralmente escaneado, sem OCR disponível localmente** — é o instrumento que define a fórmula de LTV (Cláusula 4.5) e provavelmente outras cláusulas-chave das Garantias (ex.: mecânica completa do Fundo de Reserva). Continua sendo o principal gap documental da operação; os aditamentos 2º, 3º e 4º também não estão na pasta (conhecidos só por citação no 5º Aditamento).
2. **Risco de concentração/saída do Banco Digio**: já sinalizado no highlight do mês — a saída dos conjuntos 701-704 levaria o IC spot a 1,05x (abaixo do mínimo) e a média móvel para exatamente 1,20x (no limite, sem folga). O próprio Agente Fiduciário já havia sinalizado (ata 28/11/2024) que a redução de receita de locação por renegociações aumenta o risco de crédito, mesmo com reforço de garantia.
3. **"Imóvel Corteva/CTVA" é um ativo distinto do Evolution Corporate** cuja cessão fiduciária de recebíveis foi incorporada à garantia para sustentar o IC — pode ser liberada automaticamente se o Fundo vender esse imóvel (mediante reforço equivalente em até 10 dias). Vale mapear esse ativo separadamente em uma próxima rodada (não há ficha própria dele no card de garantias do pipeline).
4. **Nenhum evento de vencimento antecipado é automático** — todos os 22 eventos da Cláusula 6.7 do TS passam por assembleia com quórum de 50% dos CRI em Circulação (do total, não só presentes) — estrutura diferente da bifurcação automático/não-automático vista em outras operações. O desenquadramento do IC especificamente tem seu próprio direito de cura de 10 dias (ver covenants acima), antes de cair nos eventos genéricos do TS.
5. **Pequena divergência entre dois campos de LTV no mesmo dado financeiro**: `papel.LTV atual` = 41,4% vs. `summary.ltv_atual` = 42,8% — vale reconciliar na próxima atualização do pipeline.
6. **Seguro patrimonial** com data de renovação aparentemente desatualizada no card do pipeline (ciclo 2024-2025 mostrado, sem indicação de renovações mais recentes).
