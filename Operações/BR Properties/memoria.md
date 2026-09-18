# BR Properties — Memória da Operação

> Leitura derivada de `Pipeline/documents_meta.json`, `Pipeline/obligations_data.json`, `Pipeline/portfolio_data_wrapped.json` e leitura direta do 1º Aditamento à Cessão Fiduciária de Direitos Creditórios e do 1º Aditamento à Alienação Fiduciária de Imóvel. A Escritura de Emissão de Debêntures e a ata AGT 17.11.2025 são PDFs escaneados sem camada de texto (precisam de OCR, não disponível nesta rodada — tentativa de instalar Tesseract localmente foi bloqueada por prompt de segurança do Windows) — as informações que dependeriam desses 2 arquivos foram reconstruídas por citação em outros instrumentos e pelo dado financeiro já cadastrado.
>
> Última atualização: 2026-09-18.

## Resumo

- **CRI**: 179ª Emissão, série única, True Securitizadora S.A. — lastreado na 18ª Emissão de Debêntures da própria **BR Properties S.A.** (emissora listada, não uma SPE dedicada — diferente do padrão das outras operações mapeadas).
- Emitido em 15/08/2023: R$ 80 milhões, majorado para **R$ 90 milhões** via exercício parcial de lote adicional (+12,5%). Remuneração **100% CDI + 2,00% a.a.** (indexador diferente da maioria das operações, que são IPCA). Vencimento: 15/08/2031.
- Saldo devedor atual (jul/26): R$ 83,5 milhões. Duration: 2,84 anos.

## Estruturação — deal de renda logística, com histórico de troca de garantia

Deal de renda clássico: **Cessão Fiduciária de todos os Contratos de Locação** + **Alienação Fiduciária dos imóveis-garantia**, sem cascata de vendas.

**A garantia já mudou pelo menos uma vez.** O documento presente na pasta datado de out/2023 (1º Aditamento à AF de Imóvel) descreve a garantia original: **3 galpões — Araucária, Centauri e Cupuaçu** (imóveis em Atibaia/SP conforme matrículas citadas), locados para L'Oréal e M Cassab.

**Em 2025/2026, a garantia foi integralmente substituída** pelo **Condomínio de Galpões BRPR Cajamar I** (Rodovia Anhanguera, km 43, Cajamar/SP) — confirmado no dado financeiro já cadastrado no pipeline. Locatários atuais: Yusen Logistics, Girotrade e JSL. Vacância 0%, contratos de locação com prazo superior a 10 anos (além do vencimento do próprio CRI).

**Estrutura confirmada pelo usuário**: são **2 galpões físicos** (bate com o "ativo_info" do dado financeiro) — **G100** e **G200** — subdivididos em **5 módulos** ao todo (bate com o texto `sobre_operacao`): G200-A, G200-B, G200-C, G200-D (4 módulos do galpão G200) e G100-F (1 módulo do galpão G100) — nomes que batem exatamente com os 5 arquivos "AF Galpão..." da pasta. **Particularidade**: o módulo **G100 só tem Cessão Fiduciária de recebíveis constituída — não tem Alienação Fiduciária de Imóvel** (diferente dos 4 módulos de G200, que têm AF de Imóvel completa). Os 5 arquivos são matrículas escaneadas, só imagem — não foi possível ler o conteúdo/confirmar endereços exatos sem OCR, mas a estrutura acima já está confirmada.

Card "garantias" do dado financeiro ainda mostra o ativo **antigo** (Araucária/Centauri/Cupuaçu, locatários L'Oréal/M Cassab) — não foi atualizado após a substituição pra Cajamar; vale corrigir na próxima atualização do pipeline.

## Metodologias de cálculo confirmadas

### ICSD — mecanismo em 2 camadas (mais sofisticado que o padrão)

**Fórmula** (Cessão Fiduciária, Cláusula 4): `ICSD = Pagamentos Contratos de Locação / (Amortização + Juros Debêntures)`, mínimo **1,20x**, apurado **mensalmente** (3º dia útil de cada mês, com base no extrato da Conta Centralizadora do mês anterior). Primeira verificação só a partir do 3º mês após a liquidação dos CRI.

Há duas consequências distintas e progressivas pro desenquadramento:
1. **Evento de Retenção** (mais brando): assim que o ICSD apurado em qualquer data for < 1,20x, a Debenturista **bloqueia imediatamente** o repasse de recursos da Conta Centralizadora pra Conta Livre Movimento (recursos ficam retidos em Investimentos Permitidos) — não é vencimento antecipado ainda.
2. **Evento de Vencimento Antecipado não automático**: só ocorre se o ICSD ficar abaixo de 1,20x por **3 meses consecutivos OU 4 meses alternados dentro de 12 meses**, sem que a Devedora tenha feito reforço/recomposição.

**Caminho de recomposição**: pra destravar o Evento de Retenção, a Devedora pode depositar recursos suficientes pra atingir um ICSD de **1,75x** (mais exigente que o mínimo de 1,20x), calculado por uma variante da fórmula com **médias de 6 meses** (não apuração pontual), sustentado por 3 Datas de Apuração consecutivas.

Também existe a possibilidade de reforçar a garantia com **novos Contratos de Locação** (novos locatários) em vez de aporte de caixa, sem precisar de assembleia — desde que os novos locatários não estejam em recuperação judicial/falência e não sejam do grupo econômico da Companhia.

Atual (jul/26): **1,52x** — enquadrado, folga confortável.

### LTV

`LTV = saldo devedor das Debêntures / soma do valor de mercado de todos os Imóveis` (AF de Imóvel, Cláusula 7.1.2), máximo **50%**. Laudo de avaliação atualizado anualmente até 15/fev; verificação do enquadramento em até 7 dias úteis do recebimento do laudo (portanto uma verificação por ano, não mensal — diferente do ICSD). Desenquadrar sem reforço de garantia → vencimento antecipado. Atual: 36,2% — enquadrado.

### Dívida Líquida / Propriedades para Investimento — covenant de nível corporativo

Confirmado como covenant real e monitorado: **< 50%**. Esse é um índice de alavancagem da própria BR Properties S.A. (não específico do ativo-garantia) — faz sentido dado que a Devedora aqui é a companhia listada, não uma SPE isolada. Atual: **-33%** (dívida líquida negativa — a companhia está com caixa líquido positivo nessa métrica). Verificação anual (última: 30/05/2026).

### Fundo de Reserva e Fundo de Despesas

Confirmados na Cessão Fiduciária como parte da cascata (repasse pra Conta Livre Movimento só ocorre após recomposição de ambos os fundos), mas o **texto exato das cláusulas de definição/valores não foi lido nesta rodada** (estão na Escritura de Debêntures, que é o PDF escaneado sem OCR). Valor do Fundo de Reserva já cadastrado no pipeline: mínimo R$ 1.644.035,32, atual R$ 1.802.247,30 (enquadrado). **Não encontrei um card de "Fundo de Despesas" com valores separados** — mesma lacuna observada em outras operações (aparece na estrutura contratual, mas sem covenant dedicado visível no dado financeiro atual).

### Rent roll / acompanhamento dos locatários

Mesmo padrão da Alianza: existe um campo dedicado (`locatarios`) no schema do portal, mas está **vazio** pra esta operação. Locatários atuais conhecidos (Cajamar): Yusen Logistics, Girotrade, JSL (e possivelmente uma 4ª — "Antilhas" aparece no `ativo_info`, mas não no texto `sobre_operacao`, mais uma pequena divergência a reconciliar).

## Obrigações / última ata

**Ata mais recente**: AGT 17.11.2025 — segundo o `obligations_data.json` já existente, **sem obrigações pendentes registradas** (0 items). Não foi possível reconfirmar o conteúdo diretamente nesta rodada (PDF escaneado sem OCR) — a leitura anterior já havia processado esse documento antes de virar ilegível para extração de texto simples (ou foi lido por OCR na sessão de nuvem original, que tinha essa capacidade).

## Pontos de atenção / riscos

1. **Card "garantias" do dado financeiro desatualizado** — ainda mostra o ativo antigo (Araucária/Centauri/Cupuaçu) em vez do Cajamar atual (ver seção de estruturação).
2. **Módulo G100 só tem Cessão Fiduciária, sem Alienação Fiduciária de Imóvel** — garantia mais fraca nesse módulo especificamente comparado aos 4 módulos de G200; vale ter isso em mente na análise de risco de crédito por módulo.
3. **Escritura de Debêntures e ata AGT 17.11.2025 não puderam ser lidas diretamente nesta rodada** (scans sem OCR) — véu documentos com definições completas de Fundo de Reserva/Despesas e possíveis obrigações da última ata.
4. **5 arquivos "AF Galpão" (a garantia atual de Cajamar) são só imagem** — não foi possível confirmar endereços/matrículas exatos sem OCR.
5. Campo de rent roll (`locatarios`) vazio, e pequena divergência sobre se são 3 ou 4 locatários atuais.
6. Devedora é a companhia BR Properties S.A. diretamente (não uma SPE) — vale ter isso em mente ao avaliar risco de crédito (exposição ao balanço da companhia inteira, não só ao ativo específico).
