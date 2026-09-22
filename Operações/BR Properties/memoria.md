# BR Properties — Memória da Operação

> Leitura derivada de `Pipeline/documents_meta.json`, `Pipeline/obligations_data.json`, `Pipeline/portfolio_data_wrapped.json` e leitura direta do 1º Aditamento à Cessão Fiduciária de Direitos Creditórios, do 1º Aditamento à Alienação Fiduciária de Imóvel, da Escritura de Emissão de Debêntures (18ª Emissão), do Termo de Rerratificação da Ata AGT e das 5 certidões de matrícula "AF Galpão" (Cajamar). A Escritura de Debêntures e a ata/termo de rerratificação AGT são PDFs escaneados sem camada de texto; nesta rodada foi possível lê-los via renderização de página + leitura visual (OCR por visão), contornando a indisponibilidade de Tesseract/poppler no ambiente local — todas as cláusulas e valores abaixo citados da Escritura e da ata foram lidos diretamente, não reconstruídos por citação indireta.
>
> Última atualização: 2026-09-18.

## Resumo

- **CRI**: 179ª Emissão (IF 23H1023846), série única, **Opea Securitizadora S.A.** (CNPJ 02.773.542/0001-22) — lastreado na 18ª Emissão de Debêntures da própria **BR Properties S.A.** (emissora listada, não uma SPE dedicada — diferente do padrão das outras operações mapeadas). **Correção**: o dado financeiro do pipeline e a leitura anterior citavam "True Securitizadora S.A."; os documentos assinados em 2025/2026 (Termo de Rerratificação da Ata, certidões de matrícula) já usam a razão social **Opea Securitizadora S.A.**, mesmo CNPJ — rebranding da securitizadora, não é uma entidade diferente. Vale atualizar o cadastro do pipeline.
- Emitido em 15/08/2023: R$ 80 milhões, majorado para **R$ 90 milhões** via exercício parcial de lote adicional (+12,5%). Remuneração **100% CDI + spread**, com **teto contratual de 3,18% a.a.** definido na Escritura (Cláusula 4.13.1) — o spread efetivamente apurado no Procedimento de *Bookbuilding* e ratificado por aditamento foi **2,00% a.a.**, valor já refletido no dado financeiro do pipeline. Vencimento: 12/08/2031 (2.919 dias corridos da Data de Emissão — a Escritura usa 12/08/2031 como Data de Vencimento; o resumo anterior citava 15/08/2031, pequena divergência de 3 dias a reconciliar, provavelmente por arredondamento de dias úteis/corridos).
- Saldo devedor atual (jul/26): R$ 83,5 milhões. Duration: 2,84 anos.

## Estruturação — deal de renda logística, com histórico de troca de garantia (2 tranches documentadas)

Deal de renda clássico: **Cessão Fiduciária de todos os Contratos de Locação** + **Alienação Fiduciária dos imóveis-garantia**, sem cascata de vendas.

**A garantia já mudou pelo menos uma vez.** O documento datado de out/2023 (1º Aditamento à AF de Imóvel) descreve a garantia original: **3 galpões — Araucária, Centauri e Cupuaçu** (imóveis em Atibaia/SP, matrículas 139.636 a 139.641 e 140.218 do Cartório de Atibaia/SP), locados para L'Oréal e M Cassab.

**Em 2025/2026, a garantia foi integralmente substituída** pelo **Condomínio de Galpões BRPR Cajamar I** (Rodovia Anhanguera, Km 43+420, Fazenda dos Cristais, Cajamar/SP — comarca registral de Jundiaí/SP). Confirmado tanto no dado financeiro do pipeline quanto na leitura direta das 5 certidões de matrícula e do Termo de Rerratificação da Ata AGT (assinado 04/12/2025, referente à Assembleia de 17/11/2025).

**Estrutura de módulos — confirmada e corrigida via leitura das 5 certidões de matrícula**: são 2 galpões físicos, subdivididos em 5 módulos, cada um com sua própria matrícula no 2º Cartório de Registro de Imóveis de Jundiaí/SP:

| Módulo | Matrícula | Subcondomínio | Área privativa total |
|---|---|---|---|
| G100-F | 186.402 | G100 – Galpão 100 | 11.887,110 m² |
| G200-A | 186.403 | G200 – Galpão 200 | 11.070,360 m² |
| G200-B | 186.404 | G200 – Galpão 200 | 10.706,000 m² |
| G200-C | 186.405 | G200 – Galpão 200 | 10.706,000 m² |
| G200-D | 186.406 | G200 – Galpão 200 | (mesma matriz G200, não lida individualmente) |

**Correção importante em relação à leitura anterior**: a leitura anterior (baseada em texto `sobre_operacao`) havia concluído que **o módulo G100 só teria Cessão Fiduciária, sem Alienação Fiduciária de Imóvel**. A leitura direta das certidões de matrícula **contradiz isso**: a matrícula 186.402 (G100-F) tem **R 02 – Constituição de Propriedade Fiduciária**, registrada em 27/02/2026, com base em instrumento de Alienação Fiduciária firmado em 24/11/2025 — ou seja, **todos os 5 módulos têm Alienação Fiduciária de Imóvel constituída**, não apenas 4. Vale corrigir essa premissa na próxima atualização do pipeline e em qualquer análise de risco por módulo que tenha assumido garantia mais fraca em G100.

**A troca de garantia ocorreu em pelo menos 2 tranches distintas de Alienação Fiduciária**, confirmadas pelas próprias certidões:
1. **Tranche 1** — instrumento firmado em 22/07/2025, registrado em 29/08/2025: matrículas **186.403 (G200-A)** e **186.404 (G200-B)**. Avaliação declarada do imóvel (art. 24, VI, Lei 9.514/97): R$ 93.965.554,55.
2. **Tranche 2** — instrumento firmado em 24/11/2025, registrado em 27/02/2026: matrículas **186.402 (G100-F)**, **186.405 (G200-C)** e **186.406 (G200-D)**. Avaliação declarada: R$ 137.902.138,10 (valor idêntico registrado nas 3 matrículas da tranche — provavelmente a avaliação do conjunto, não individual por módulo).

Ambas as tranches têm como fiduciante (garantidora) a **Solid Ativos Imobiliários S.A.** (CNPJ 06.977.751/0001-49, sede na Av. Brigadeiro Faria Lima 4.300, Itaim Bibi/SP) — **não a própria BR Properties S.A.** Isso nuança o ponto de risco #6 abaixo: a Devedora das Debêntures (obrigada pecuniária) é a companhia listada BR Properties S.A., mas o imóvel-garantia (Cajamar) está registrado em nome de uma subsidiária/propco dedicada (Solid Ativos Imobiliários S.A.), que presta a Alienação Fiduciária. Estrutura híbrida: dívida corporativa (risco de balanço da controladora) + garantia real segregada em SPE imobiliária.

**Locatários confirmados via Termo de Rerratificação da Ata AGT** (troca de Direitos Creditórios cedidos, aprovada por 36,82% dos CRI em circulação, 2,22% de abstenção, sem votos contrários, quórum de comparecimento 39,04%): **Yusen Logistics do Brasil Ltda.** (contrato de 22/09/2023), **Girotrade S.A.** e **JSL S.A.** (contratos de 07/02/2023, aditado em 09/10/2023, mais dois contratos adicionais de 12/09/2024 e 30/12/2024). Não há menção a "Antilhas" nesse documento — a divergência sobre um possível 4º locatário citada no `ativo_info` do pipeline permanece não resolvida por esta via.

Card "garantias" do dado financeiro ainda mostra o ativo **antigo** (Araucária/Centauri/Cupuaçu, locatários L'Oréal/M Cassab) — não foi atualizado após a substituição pra Cajamar; vale corrigir na próxima atualização do pipeline.

## Metodologias de cálculo confirmadas (lidas diretamente na Escritura de Emissão de Debêntures)

### Remuneração / cálculo de juros (Cláusula 4.13)

100% da variação acumulada das taxas médias diárias do **DI** (CDI, over extragrupo, base 252 dias úteis, divulgada pela B3), acrescida de sobretaxa (*spread*) fixada no Procedimento de *Bookbuilding*, **limitada contratualmente a 3,18% a.a.** — o valor efetivamente contratado, conforme aditamento de ratificação do *bookbuilding*, foi **2,00% a.a.**, coerente com o dado já cadastrado no pipeline.

Fórmula (Cláusula 4.13.2):

```
J = VNe × (FatorJuros − 1)
FatorJuros = FatorDI × FatorSpread
FatorDI = Produtório [1 + TDIk], k = 1 até n
TDIk = [(DIk / 100) + 1]^(1/252) − 1
```

Cálculo exponencial e cumulativo *pro rata temporis* por dias úteis decorridos. Pagamento **mensal**, sem carência, nas datas do Anexo III (Cláusula 4.14). Não há atualização monetária do Valor Nominal Unitário (Cláusula 4.12).

**Cláusula de fallback do CDI** (4.13.3–4.13.4): se a Taxa DI parar de ser divulgada por até 30 dias, usa-se a última taxa divulgada, sem compensações. Se a ausência ultrapassar 30 dias ou o CDI for extinto/proibido, convoca-se Assembleia de Debenturista para definir novo parâmetro em comum acordo com a Emissora; se não houver acordo, a Emissora se obriga a resgatar a totalidade das Debêntures em até 30 dias.

### Amortização (Cláusula 4.15)

Amortização **mensal** do saldo do Valor Nominal Unitário, com **carência de 12 meses** contados da Data de Emissão (15/08/2023), nas Datas de Pagamento previstas no Anexo III à Escritura.

**Encargos moratórios** em caso de impontualidade (Cláusula 4.18): juros de mora de 1% a.m. *pro rata temporis* + multa convencional não compensatória de 2%, sobre qualquer valor em atraso.

### Resgate Antecipado Facultativo Total / multa (Cláusula 5.1)

A Emissora pode resgatar a totalidade das Debêntures, a seu exclusivo critério, **a partir de 12/08/2025** (2 anos de *lock-out* após a emissão) — **não é permitido resgate parcial** (Cláusula 5.1.3). Aviso prévio de 10 dias úteis.

**Fórmula de mercado (como o desk descreve a multa)**: **0,45% a.a. × Prazo Remanescente × Saldo Devedor** — linear, proporcional ao tempo que falta até o vencimento.

Fórmula textual da Escritura (Cláusula 5.1.2, inciso ii — cálculo exponencial):

```
P = [(1 + 0,45%)^(DU/252) − 1] × VR
```

onde DU = dias úteis entre a data do resgate e a Data de Vencimento, e VR = saldo do Valor Nominal Unitário acrescido da Remuneração *pro rata* e de encargos devidos. A fórmula exponencial da Escritura e a leitura linear do desk convergem para o mesmo resultado prático — 0,45% a.a. pro rata do prazo remanescente — sendo a exponencial apenas a formalização técnica de juros compostos (equivalente a juros simples para essa magnitude de taxa/prazo). Prêmio decrescente conforme se aproxima o vencimento (menos prazo remanescente = prêmio menor).

### Amortização Extraordinária (Cláusula 5.3)

Mesma fórmula de prêmio do resgate facultativo (0,45% a.a. × Prazo Remanescente × Saldo Devedor), mas limitada a **98% do saldo do Valor Nominal Unitário** — ou seja, não pode zerar a dívida por essa via (isso só ocorre via Resgate Antecipado Facultativo Total).

### Oferta de Resgate Antecipado (Cláusula 5.2) — mecanismo distinto, sem prêmio mínimo obrigatório

A Emissora pode, a qualquer momento a partir da Data de Emissão, ofertar resgate antecipado (parcial ou total, a critério dos Titulares de CRI aderirem individualmente) mediante notificação com: valor do resgate, data (até 30 dias da aprovação), e **prêmio opcional definido livremente pela Emissora, desde que não negativo** — diferente do Resgate Antecipado Facultativo Total, aqui não há piso de 0,45% a.a. Pode ser condicionada a adesão mínima.

### Aquisição Facultativa (Cláusula 5.4)

**Vedada** — a Emissora não pode adquirir suas próprias Debêntures antecipadamente por fora dos mecanismos acima.

## Vencimento Antecipado (Cláusula VI da Escritura) — lido integralmente

Estrutura em 2 categorias, com consequências e processos distintos:

### Eventos automáticos (Cláusula 6.1.1) — vencimento antecipado imediato, sem deliberação em assembleia, se não sanados no prazo de cura

Entre os ~20 incisos, destacam-se: (i) inadimplemento pecuniário não sanado em 2 dias úteis; invalidade/nulidade da Escritura ou dos Contratos de Garantia; questionamento judicial da Escritura pela própria Emissora/controladora/controlada; cessão de obrigações a terceiros sem autorização; liquidação, falência, pedido de RJ da Emissora ou de Controlada; transformação societária; **cross-default de dívida ≥ R$ 35 milhões** (atualizado anualmente por IPCA) da Emissora ou Controlada; distribuição de dividendos estando em mora com as Debêntures; descumprimento da destinação de recursos (Cláusula 3.5); declaração falsa/enganosa; decisão judicial desfavorável não suspensa em 10 dias úteis; não auditoria das demonstrações financeiras por auditor independente credenciado na CVM; não constituição/formalização das Garantias nos prazos; sinistro parcial ou total dos Imóveis não recomposto/indenizado em 180 dias; vício não sanado nas Garantias; e **descumprimento do Índice Financeiro** (ver abaixo) — este último item está listado como **evento automático**, não sujeito a deliberação de assembleia, ao contrário do mecanismo do ICSD (que é da Cessão Fiduciária, com camada de retenção antes do vencimento — ver seção específica abaixo).

**Índice Financeiro corporativo (Cláusula 6.1.1, inciso xx)**: Dívida Financeira Líquida / Propriedades para Investimento (ambos conforme Demonstrações Financeiras Consolidadas da Emissora) **≤ 0,50**, apurado **anualmente**, com base na 1ª apuração referente ao exercício findo em 31/12/2023. Confirma e detalha o covenant já identificado na leitura anterior — a novidade é que seu descumprimento **aciona vencimento automático**, não apenas um "covenant monitorado". Atual (jul/26): -33% (caixa líquido positivo) — enquadrado com folga muito ampla.

### Eventos não automáticos (Cláusula 6.1.2) — dependem de deliberação em Assembleia Especial de Titulares de CRI

Inadimplemento não pecuniário (cura 10 dias úteis); inadimplemento pecuniário não relativo à dívida principal — despesas, honorários do Agente Fiduciário etc. (cura 10 dias úteis); invalidade/ineficácia parcial da Escritura; declaração incorreta/inconsistente/incompleta; inadimplemento de decisão judicial/arbitral ≥ R$ 35 milhões (IPCA); desapropriação/confisco de ativos ≥ R$ 50 milhões (IPCA) ou indenização inferior a 40% do valor de mercado; não renovação de licenças/alvarás relevantes; cisão/fusão/incorporação envolvendo a Emissora ou Controlada Relevante (com exceções); redução de capital não autorizada; e **alteração de controle acionário** — este último tem mecanismo de proteção específico: se 2/3 dos CRI em circulação se manifestarem contrariamente em até 90 dias, a Emissora deve assegurar aos Titulares de CRI direito de resgate compulsório dos CRI (prazo mínimo de 6 meses para exercício), pelo saldo do Valor Nominal Unitário acrescido de Remuneração — funciona como um *change of control put*, não como vencimento automático.

**Processo**: na ocorrência de evento não automático, a Debenturista convoca Assembleia Especial de Titulares de CRI em até 3 dias úteis; só há vencimento antecipado se a assembleia (em 1ª ou 2ª convocação) deliberar favoravelmente pelo quórum da Cláusula 8.7.6; se a assembleia não se instalar, não deliberar favoravelmente, ou não houver deliberação em 2ª convocação, a Securitizadora **não deve** declarar o vencimento.

**Pagamento**: declarado o vencimento antecipado (automático ou por deliberação), a Emissora deve pagar a totalidade das Debêntures (saldo + Remuneração *pro rata* + encargos) em até **20 dias úteis**.

## Obrigações da Emissora (Cláusula VII — Obrigações Adicionais da Emissora)

Lista extensa (17 incisos) enquanto o saldo devedor não for integralmente pago. Destaques:
- **Reporte financeiro**: demonstrações financeiras consolidadas auditadas em até 3 meses do fim do exercício social (auditor credenciado CVM — lista fechada incluindo Deloitte, EY, KPMG, PwC, RSM, BDO, Grant Thornton, Martinelli, Boucinhas); memória de cálculo do Índice Financeiro; balancetes trimestrais em até 45 dias; atendimento de solicitações de informação em até 5 dias úteis.
- **Compliance societário**: envio de atas de assembleias/RCA que envolvam interesse da Debenturista/Titulares de CRI em até 7 dias úteis; comparecimento a Assembleias Gerais de Titulares de CRI.
- **Manutenção**: seguros adequados para bens/ativos relevantes conforme práticas de mercado; licenças, alvarás e autorizações válidas (inclusive ambientais); regularidade das Garantias (acompanhamento de registro nos cartórios competentes).
- **Legislação socioambiental, trabalhista e anticorrupção**: cláusulas amplas de conformidade (Lei 12.846/2013, FCPA, UK Bribery Act etc.), extensivas a Controladas, administradores e representantes — vedação a trabalho infantil/escravo, incentivo à prostituição, atos de corrupção.
- **Tributos**: recolhimento integral dos tributos incidentes sobre as Debêntures/CRI sob responsabilidade da Emissora.
- **Guarda documental**: 5 anos (ou mais, se exigido pela CVM em processo administrativo).

Não há, na leitura desta rodada, uma cláusula de *negative pledge* geral (restrição a novas dívidas) além do cross-default e do Índice Financeiro — a proteção contra alavancagem adicional é indireta, via esses dois mecanismos.

## Outras metodologias já confirmadas (leitura anterior, mantidas)

### ICSD — mecanismo em 2 camadas (Cessão Fiduciária, não a Escritura de Debêntures)

**Fórmula** (Cessão Fiduciária, Cláusula 4): `ICSD = Pagamentos Contratos de Locação / (Amortização + Juros Debêntures)`, mínimo **1,20x**, apurado **mensalmente** (3º dia útil de cada mês, com base no extrato da Conta Centralizadora do mês anterior). Primeira verificação só a partir do 3º mês após a liquidação dos CRI.

Duas consequências distintas e progressivas pro desenquadramento:
1. **Evento de Retenção** (mais brando): ICSD apurado < 1,20x → Debenturista **bloqueia imediatamente** o repasse de recursos da Conta Centralizadora pra Conta Livre Movimento — não é vencimento antecipado ainda.
2. **Evento de Vencimento Antecipado não automático**: só ocorre se o ICSD ficar abaixo de 1,20x por **3 meses consecutivos OU 4 meses alternados dentro de 12 meses**, sem reforço/recomposição pela Devedora.

**Caminho de recomposição**: depositar recursos para atingir ICSD de **1,75x** (variante com médias de 6 meses, sustentado por 3 Datas de Apuração consecutivas), ou reforçar a garantia com **novos Contratos de Locação** sem precisar de assembleia (desde que os novos locatários não estejam em RJ/falência nem sejam do grupo econômico da Companhia).

Atual (jul/26): **1,52x** — enquadrado, folga confortável.

Nota: este é um mecanismo **contratual da Cessão Fiduciária**, distinto e adicional ao Índice Financeiro corporativo da Escritura de Debêntures (Dívida Líq./Propriedades p/ Investimento) — os dois operam em paralelo, com periodicidades (mensal vs. anual) e naturezas (automático vs. não automático) diferentes.

### LTV

`LTV = saldo devedor das Debêntures / soma do valor de mercado de todos os Imóveis` (AF de Imóvel, Cláusula 7.1.2), máximo **50%**. Laudo de avaliação atualizado anualmente até 15/fev; verificação do enquadramento em até 7 dias úteis do recebimento do laudo (uma verificação por ano). Desenquadrar sem reforço de garantia → vencimento antecipado. Atual: 36,2% — enquadrado.

### Fundo de Reserva e Fundo de Despesas

Confirmados na Cessão Fiduciária como parte da cascata (repasse pra Conta Livre Movimento só ocorre após recomposição de ambos os fundos). **O texto exato das cláusulas de definição/valores segue não lido** — não estão na Escritura de Debêntures (que já foi lida integralmente nesta rodada e não os contém); provavelmente estão no Termo de Securitização (não presente na pasta de Documentos). Valor do Fundo de Reserva já cadastrado no pipeline: mínimo R$ 1.644.035,32, atual R$ 1.802.247,30 (enquadrado). Não há card de "Fundo de Despesas" com valores separados no dado financeiro atual.

### Rent roll / acompanhamento dos locatários

Campo dedicado (`locatarios`) no schema do portal está **vazio** pra esta operação, apesar de agora termos os 3 locatários confirmados por documento oficial (ver seção de estruturação) — vale preencher.

## Obrigações / última ata — CORRIGIDO nesta rodada

**Correção relevante**: a leitura anterior, baseada em `obligations_data.json`, registrou a ata AGT 17.11.2025 como tendo "0 obrigações pendentes". A leitura direta do documento (que na verdade é um **Termo de Rerratificação da Ata**, assinado em 04/12/2025) revela que seu conteúdo real é a **aprovação formal, pelos Titulares de CRI, da substituição de garantia** (troca dos Direitos Creditórios cedidos e das Alienações Fiduciárias de Imóvel de Atibaia para Cajamar) — não uma ata de rotina sem pauta. Resultado da votação: **36,82% dos CRI em circulação aprovaram**, **2,22% se abstiveram**, **sem votos contrários**; quórum total de comparecimento de 39,04%. Isso é consistente com — e explica formalmente — a substituição de garantia já identificada na seção de estruturação.

## Pontos de atenção / riscos (atualizado)

1. **Card "garantias" do dado financeiro desatualizado** — ainda mostra o ativo antigo (Araucária/Centauri/Cupuaçu) em vez do Cajamar atual.
2. ~~Módulo G100 só tem Cessão Fiduciária, sem Alienação Fiduciária de Imóvel~~ — **CORRIGIDO nesta rodada**: a certidão de matrícula 186.402 confirma que G100-F **tem** Alienação Fiduciária de Imóvel constituída (registrada 27/02/2026). Todos os 5 módulos têm garantia real completa.
3. **Razão social da Securitizadora desatualizada no pipeline** — "True Securitizadora S.A." deveria ser "Opea Securitizadora S.A." (mesmo CNPJ, rebranding).
4. **Fiduciante da Alienação Fiduciária é uma subsidiária dedicada (Solid Ativos Imobiliários S.A.), não a própria BR Properties S.A.** — a dívida (Debêntures) é obrigação direta da companhia listada, mas o imóvel-garantia está segregado em SPE imobiliária. Vale considerar essa camada na análise de risco de crédito (risco de balanço da controladora + segregação patrimonial do ativo-garantia).
5. **Escritura de Debêntures foi lida integralmente nesta rodada** (via renderização + leitura visual) — não há mais lacuna de metodologia de juros/amortização/resgate/vencimento antecipado/obrigações; ver seções acima.
6. **Termo de Securitização não está na pasta de Documentos** — segue sendo a lacuna para os valores/definições exatas de Fundo de Reserva e Fundo de Despesas.
7. Campo de rent roll (`locatarios`) vazio, apesar de os 3 locatários (Yusen Logistics, Girotrade, JSL) já estarem confirmados por documento oficial; divergência sobre um possível 4º locatário ("Antilhas") permanece não resolvida.
8. Devedora das Debêntures é a companhia BR Properties S.A. diretamente (não uma SPE) — exposição ao balanço da companhia inteira — mas ver ponto 4 acima sobre a segregação do imóvel-garantia.
9. Pequena divergência de 3 dias na Data de Vencimento (Escritura cita 12/08/2031; resumo anterior citava 15/08/2031) — provavelmente arredondamento, não investigado a fundo.
