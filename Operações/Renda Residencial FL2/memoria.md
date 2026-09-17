# Renda Residencial FL2 — Memória da Operação

> Primeira leitura completa da operação (ainda não tinha `documents_meta.json`/`obligations_data.json` no pipeline). Construído a partir da varredura dos documentos em `Operações/Renda Residencial FL2/Documentos/` — não é fonte de dados para o `build_data.py`, é um resumo pra revisão humana.
>
> Última atualização: 2026-09-17.

## Resumo

- **CRI**: 178ª (Sênior) e 179ª (Subordinada) Séries da 1ª Emissão, Habitasec Securitizadora S.A. — TS original celebrado em 02/12/2019.
- **Devedora/estrutura**: Promontoria Imóveis 1 S.A. — mesma família de veículos "Project Bread"/Promontoria da Residencial Jardins FL2 (lá é Promontoria Imóveis 5), mas **grupo interno diferente**: aqui é **MCRE**, em Jardins é **MCCI**.
- **Ativo**: 5 edifícios residenciais — **Aurora, Genebra, Time Life, Sé e Quadra** (mais de 10.000 m², valor de aquisição R$ 77,6 milhões, avaliação R$ 109,1 milhões).
- Estrutura Sênior/Subordinada: 178ª (Sênior, 80% da emissão, R$ 41,9 milhões) e 179ª (Subordinada, 20%, R$ 10,5 milhões) — diferente da Jardins, que é série única.
- Saldo devedor atual (jul/26): R$ 26,05 milhões (Sênior R$ 20,84M + Sub R$ 5,21M). LTV atual 23,2% (limite 50%). IC atual 1,63x (mínimo 1,30x).

## Contexto de negócio e reestruturação (14/08/2025 — AEI — e formalização em 12/09/2025)

**Mesma origem da Jardins**: nasceu como deal de renda (aluguel dos 5 prédios fazendo frente ao serviço da dívida) e passou por reestruturação para virar (também) um deal de estoque/venda de unidades. Mas aqui a reestruturação foi **mais profunda** do que na Jardins — não se limitou a criar a cascata de vendas, também **renegociou os termos financeiros do CRI**.

**Ata-base**: AEI de 14/08/2025 (arquivo `1ªE_178ª179ªS - Project Bread - AEI Fundo de Reserva + Reestruturação_vfinal.docx.pdf`), aprovada por 100% dos Titulares, implementada pelo **4º Aditamento ao TS** (Anexo II da própria ata) e depois "espelhada" na Escritura de Debêntures pelo **6º Aditamento à Escritura de Emissão de Debêntures** e no TS de novo pelo **5º Aditamento ao TS** (ambos de 12/09/2025, decorrentes de uma Assembleia Geral de Debenturistas — "AGD 12/09" — realizada na mesma data).

O que foi deliberado:

1. **Waiver do Fundo de Reserva**: não declaração de vencimento antecipado por descumprimento da recomposição vencida em 26/06/2025 (mas já cumprida pela Devedora em 28/07/2025, antes mesmo da assembleia).
2. **Criação da cascata de vendas**: mesmo mecanismo da Jardins — "Conta Arrecadadora Vendas" + conceito de **"Créditos Venda"** (aqui SEM o "Direitos"/"das Vendedoras" — nomenclatura mais enxuta que a da Jardins, e sem o terceiro fluxo de indenização contra vendedores originais que existe lá). R$ 1.923.921,84 já recebidos foram transferidos da Conta do Patrimônio Separado pra nova conta na aprovação.
3. **Repactuação financeira agressiva** (isso NÃO tem equivalente na Jardins):
   - Juros: 178ª Sênior de 6,50% → **8,12% a.a.**; 179ª Subordinada de 14,00% → **15,00% a.a.**
   - **Vencimento estendido em ~7 anos**: de 25/11/2025 para **25/08/2032**.
   - Periodicidade da 179ª (Sub) mudou de mensal para **bullet** (pagamento único no vencimento) — a Sênior continua mensal.
   - **LTV máximo reduzido** de 60% para **50%** (mais apertado, não só monitorado).
   - **Prêmio Extraordinário (waiver fee)** pago aos titulares: R$ 504.744,51 (R$ 438.947,17 Sênior + R$ 65.797,34 Sub).
   - Reforço do Fundo de Reserva em R$ 157.704,80 (prazo de 1 dia útil da assembleia).
   - Liberação à Devedora de R$ 750.000,00, e retenção de R$ 1.837.943,00 na Conta do Patrimônio Separado (parte pra juros de ago/25, parte pra amortização ago/25, pro rata 178ª/179ª).
4. **Hierarquia Sênior/Sub explícita na cascata**: a 178ª (Sênior) é paga integralmente (juros + amortização programada) antes da 179ª (Sub) receber além do seu juro mínimo — diferente da Jardins, que não tem essa camada (série única).
5. **Consultor Especializado**: de novo a **Mauá Capital Real Estate Ltda.** — mesma consultoria que valida o Relatório Créditos mensal na Jardins.

**Situação atual**: em set/26 a arrecadação de vendas (R$ 1,64 milhão) já supera muito a de aluguel (R$ 172,9 mil) — ao contrário da Jardins (que em set/26 estava quase equilibrada, R$ 397k vendas vs R$ 342k aluguéis), essa operação parece estar bem mais avançada na transição pra "estoque puro".

## Acompanhamento mensal (Relatório de Crédito) — o que muda em relação à Jardins

Mesmo princípio da Jardins (Relatório Créditos mensal da Devedora, validado pelo Consultor Especializado em até 5 dias úteis, só venda **escriturada/100% quitada** entra na cascata do mês), mas a estrutura do relatório e da fórmula são diferentes:

**Abas do relatório** (`Relatorio Credito_Set26 - CRI178 e CRI179.xlsb`, salvo em `Documentos/`, não versionado): `CRI_178_179` (cascata principal), `Extrato`, **`Extrato - Conta de Vendas`** (aba própria pra conta de vendas — não existe na Jardins), `Recebimentos Vendas`, `Recebimento Aluguel`, `Unidades`, `Características`, `CRI 178`/`CRI 179`/**`SDI_178`/`SDI_179`** (Saldo Devedor Individual por série — não existe na Jardins, que é série única), `Tabela Amortização`, `Feriados`.

Pontos de checagem mensal (os mesmos 5 da Jardins, mas com fórmula própria):

1. **Vendas escrituradas vs. não escrituradas** — igual à Jardins ("Unidades Não Escrituradas": 135 no exemplo de set/26). Só entra na cascata a venda 100% quitada e escriturada.
2. **Aluguel: usar o "Aluguel Bruto Ajustado"** — não é exatamente igual ao "Aluguel Bruto" simples da Jardins; vem de um **"Relatório Gerencial da Devedora"** separado (entregue no mesmo mês), não é calculado direto no próprio Relatório Créditos.
3. **Descontos Permitidos** (equivalente aos "Vazamentos" da Jardins, nome diferente) — composição bem mais detalhada aqui:
   - **Operacionais Gerais**: 4% do valor de mercado das unidades em estoque, dividido por 12 (simplificação de IPTU/condomínio/manutenção) — não existe na Jardins.
   - **Comissões**: separadas por tipo — até 8% sobre vendas (vs. 5% flat na Jardins) e 1-2 aluguéis por contrato de locação.
   - **Estrutura da Devedora**: desconto fixo de R$ 19.000/mês + R$ 455/imóvel/mês (corrigidos por IPCA anualmente) — mecanismo específico desta operação, sem equivalente na Jardins (que usa uma taxa de R$ 1.031/unidade NÃO escriturada — conceitualmente parecido mas não é a mesma fórmula nem a mesma base de cálculo).
   - **Impostos**: 9% da Receita Bruta — igual à Jardins.
   - **Desconto Adicional**: limite acumulado de **R$ 1.571.464** (vs. R$ 1.444.000 na Jardins), liberável só em **junho e dezembro** (vs. maio e novembro na Jardins).
4. **Cascata com hierarquia Sênior (178ª) / Subordinada (179ª)** — precisa conferir juros e amortização de cada série separadamente antes de chegar no cash sweep (que também é dividido pro rata entre as séries). Isso não existe na Jardins.
5. **Fundo de Reserva e Fundo de Despesas** — mesma lógica de checar mínimo vs. saldo. No exemplo de set/26: Fundo de Reserva com saldo de R$ 693.400,24 (igual ao mínimo — já foi consumido uma vez e está exatamente no piso, conforme observação do covenant no dado financeiro) e Fundo de Despesas com saldo de R$ 28.688,55.
6. **Índice de Cobertura (IC)** — mínimo 1,30x aqui (não 1,25x como na Jardins). Em jun/26 estava em 1,63x (enquadrado).

*Exemplo de referência (Relatório de Crédito de set/26): Receita Bruta R$ 1.956.778,75 (Vendas R$ 1.641.875,61 + Aluguel Bruto Ajustado R$ 314.903,14), Descontos Permitidos R$ 314.200,80, Arrecadação total R$ 1.814.829,16, Amortização Extraordinária Cash Sweep total R$ 1.581.578,61 (178ª: R$ 1.265.262,89 + 179ª: R$ 316.315,72, na proporção 80/20).*

## Instrumentos identificados

Levantamento inicial a partir dos 11 documentos + 1 relatório na pasta (não tem ainda o rigor de cruzamento completo que as 8 operações já mapeadas têm — marcar como pendente de revisão mais profunda se for promover pro `documents_meta.json`):

| Instrumento | Data original | Situação na pasta |
|---|---|---|
| Termo de Securitização (178ª/179ª) | 2019-12-02 | Original **não está na pasta**; 1º, 2º, 3º Aditamentos (2020-12-21, 2021-05-12, 2021-09-28) só citados, não presentes. 4º Aditamento (14/08/2025) está — só como Anexo II da ata AEI. 5º Aditamento (12/09/2025, só ajusta Anexo III/datas de pagamento) está. |
| Escritura de Emissão de Debêntures (Promontoria Imóveis 1) | 2019-11-21 | Original **não está na pasta**; 1º a 5º Aditamentos (2019-2021, inclui uma rerratificação do 5º) só citados. 6º Aditamento (12/09/2025) está. |
| Contrato de Cessão Fiduciária de Recebíveis | não confirmada | Original não está na pasta. **1º Aditamento (12/09/2025)** está — cria os Créditos Venda no lado da cessão fiduciária, espelhando o TS/Escritura. |
| Alienação Fiduciária de Ações (Multiapartamentos 1 FIP + Promontoria Imóveis 3, Fiduciantes) | não confirmada | Original não está na pasta. Só o **6º Aditamento (30/06/2023, registrado RTD-SP em 06/07/2023)** está — confirma que existem pelo menos 5 aditamentos anteriores não presentes. |
| Escritura de CCI | não confirmada | Não identificada na pasta — pendente de confirmação (pode estar embutida em algum dos aditamentos, não verificado nesta rodada). |
| AF de Imóveis (5 edifícios) | não confirmada | Não identificado nenhum instrumento próprio na pasta (nem original, nem aditamento) — pendente. |

**Documentos societários/corporativos correlatos** (não são "Documentos da Operação" no sentido do TS, mas registram eventos relevantes da Devedora): AGT + AGD de conversão de AFAC (Adiantamento para Futuro Aumento de Capital) em 11/11/2022, precedida de AGE da Promontoria Imóveis 1 em 09/11/2022; AGT de aumento de capital em 30/06/2021; AGD assinada em 30/06/2023; Livro de Registro de Ações Nominativas (imagem escaneada, 7 páginas — **não foi possível extrair texto, precisaria de OCR** se algum dado específico dali for necessário).

## Obrigações / última ata

**Ata mais recente relevante**: AEI de 14/08/2025 (ver seção de reestruturação acima — é a mesma ata que traz tanto o waiver quanto a reestruturação). Ainda não foi feita uma curadoria formal de obrigações no padrão `obligations_data.json` das outras 8 operações (histórico completo de atas anteriores/obrigações supersedidas) — o que está registrado aqui é só o que essa ata mais recente determinou:

- Reforço do Fundo de Reserva em R$ 157.704,80 — prazo de 1 dia útil da assembleia (14/08/2025). **Status de cumprimento não confirmado nesta leitura** (não há documento de comprovação na pasta).
- Pagamento do Prêmio Extraordinário de R$ 504.744,51 aos titulares — prazo de 3 dias úteis da ata. **Status não confirmado nesta leitura.**
- Liberação de R$ 750.000,00 à Devedora — prazo de 2 dias úteis. **Status não confirmado.**

## Pontos de atenção / riscos

1. **Cobertura documental bem menor que as outras operações já mapeadas** — esta é a primeira leitura completa, sem o cruzamento exaustivo (ex.: confirmação de todas as datas via múltiplas fontes) que Alianza/Calçada já tiveram. Tratar as datas/instrumentos acima como preliminares.
2. **Arquivo da AGD original estava corrompido** (256KB zerados no início, provável falha de sincronização do OneDrive) — foi substituído pelo usuário pela ata AEI de 14/08/2025 (que já cobre as mesmas deliberações centrais).
3. **Livro de Registro de Ações Nominativas é só imagem** (scan, 7 páginas) — não extraído nesta rodada; OCR pendente se algum dado específico de lá for necessário no futuro.
4. **Nenhum instrumento ORIGINAL está fisicamente na pasta** (TS, Escritura de Debêntures, Cessão Fiduciária, AF de Ações) — só aditamentos recentes/pontuais, igual ao padrão observado na Jardins.
5. Instrumentos de Escritura de CCI e AF de Imóveis **não identificados** na pasta — pode ser lacuna real de documentação ou só não terem sido nomeados de forma óbvia nos 11 arquivos disponíveis.
