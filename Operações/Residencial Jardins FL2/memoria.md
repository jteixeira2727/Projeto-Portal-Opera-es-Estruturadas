# Residencial Jardins FL2 — Memória da Operação

> Leitura derivada de `Pipeline/documents_meta.json`, `Pipeline/obligations_data.json` e leitura direta do texto da ata AEI 23/03/2026 (`documents_data.json`). Não é fonte de dados para o `build_data.py` — é um resumo pra revisão humana. Se os JSONs forem atualizados (nova rodada de leitura de documentos), este arquivo deve ser regenerado.
>
> Última atualização: 2026-09-17.

## Resumo

- **CRI**: 1ª Série da 16ª Emissão, Habitasec Securitizadora S.A. — celebrado em 27/09/2022.
- **Devedora/estrutura**: Promontoria Imóveis 5 S.A. (Fundo Multiapartamentos 1).
- **Nenhum instrumento ORIGINAL está fisicamente na pasta** — a pasta só contém aditamentos recentes (todos de maio/2026, decorrentes da Assembleia Especial de Investidores de 23/03/2026) e 2 atas.
- Sem o Termo de Securitização original, **não é possível confirmar a lista canônica completa de "Documentos da Operação"** — a lista abaixo foi reconstruída a partir do que os próprios aditamentos citam uns dos outros.

## Contexto de negócio e reestruturação (23/03/2026)

**Origem — deal de renda.** Na constituição da operação (2022), os 5 prédios (Terraço, Next Paulista, Next França, Next Haddock, Onze22) eram explorados via locação nas modalidades **short stay e long stay**, e a receita de aluguel ("Direitos Creditórios Locação", cedida fiduciariamente via Contrato de Cessão Fiduciária de Recebíveis) era o que fazia frente ao serviço da dívida dos CRI.

**Gatilho da mudança** *(contexto de negócio informado pelo usuário — não está descrito nos documentos lidos)*: no final de 2025 a Devedora passou a receber ofertas de compra por unidades dos empreendimentos, o que levou à decisão de reestruturar a operação para um **deal de estoque** (venda das unidades).

**Formalização — AEI de 23/03/2026** (arquivo `16ªE_1ªS - Bread - AEI 20251003 v. com lista.pdf`), com aprovação unânime (100% dos Titulares de CRI presentes) e implementada pelo 3º Aditamento ao TS (Anexo II da própria ata, assinado em 22/05/2026). O que a ata efetivamente muda:

- Cria o conceito de **"Direitos Creditórios Venda"** (receita de venda de qualquer um dos 5 imóveis), separado — mas cedido fiduciariamente junto — dos já existentes "Direitos Creditórios Locação".
- Também existe um terceiro fluxo, **"Direitos Creditórios das Vendedoras"** — definido no 2º Aditamento à Cessão Fiduciária. **Não tem relação com a venda atual das unidades a novos compradores**: é o direito de indenização que a própria Promontoria Imóveis 5 (a Devedora) tem **contra as "Vendedoras"** — quem vendeu os 5 imóveis *para* a Promontoria na constituição da operação — por eventual **evicção** (perda do imóvel por reivindicação de terceiro com direito melhor) ou outras perdas/danos, nos termos dos Compromissos e Escrituras de Compra e Venda originais. É um direito contingente/de garantia, não um fluxo operacional. Operacionalmente, **Direitos Creditórios Venda** vão para a Conta Arrecadadora Vendas, enquanto **Locação** e **das Vendedoras** vão juntos para a Conta do Patrimônio Separado original (conta 42.629-1, ag. 7307, Itaú Unibanco).
- Abre uma **Conta Arrecadadora Vendas**, exclusiva para receber o produto das vendas dos imóveis, que passa a integrar o Patrimônio Separado (mesmo regime fiduciário dos CRI).
- Institui um **Prêmio Vendas de 1%** sobre o valor de cada imóvel vendido a partir de 01/02/2026, dentro da nova ordem de alocação de pagamentos (cláusula 3.1.2.1(xxi) do TS).
- Cria uma **Amortização Extraordinária Obrigatória "Cash Sweep"**, mensal a partir de mar/2026, com fórmula que soma **Vendas do mês** + **Aluguéis líquidos recebidos no mês anterior** (ou seja, **a receita de locação pré-reestruturação não desapareceu — continua alimentando a cascata**, só que como componente residual, não mais o principal), descontados "Vazamentos Permitidos": 5% de comissão sobre vendas, 9% de impostos sobre vendas+aluguéis, e uma **taxa de manutenção de estoque de R$ 1.031/unidade/mês** (mínimo R$ 95.000/mês) sobre os imóveis ainda não vendidos — evidência direta do caráter "deal de estoque" da nova estrutura.
- Se a Amortização Extraordinária Cash Sweep atingir **98% do Valor Nominal Unitário**, a Devedora fica obrigada a um **Resgate Total Obrigatório** (liquidação antecipada de todos os CRI).
- A **Mauá Capital Real Estate Ltda.** (grupo MCCI, mesmo gestor da operação) foi nomeada **Consultor Especializado**, responsável por validar mensalmente (até 5 dias úteis) o "Relatório Créditos" que a Devedora deve entregar até o dia 15 de cada mês, discriminando o que foi arrecadado a título de venda, locação e "Direitos Creditórios das Vendedoras".
- A ata também tratou do **waiver do Fundo de Reserva** (item já coberto na seção de Obrigações abaixo) — as duas matérias (waiver + reestruturação para deal de estoque) foram deliberadas na mesma assembleia.

**Situação atual (dado financeiro, ago/26):** o portfólio segue **100% locado** (todos os 5 prédios alugados para a Viva) — ou seja, a receita de locação pré-reestruturação continua ativa na prática — mas já há venda de unidades em andamento: **9 unidades vendidas** até jul/26 (R$ 4,22 milhões), sendo a mais recente 1 unidade do Onze22 escriturada em jul/26.

## Acompanhamento mensal (Relatório de Crédito)

Desde a reestruturação, o principal ponto de atenção mensal da operação é o acompanhamento das **vendas**. Todo mês a Devedora entrega o **"Relatório Créditos"** (definido na cláusula 3.20 do TS, incluída pelo 3º Aditamento) — na prática, um Excel (`.xlsb`) chamado "Relatório de Crédito". Exemplo salvo em `Operações/Residencial Jardins FL2/Documentos/Relatorio Credito_Set26 - CRI16E.xlsb` *(não versionado no Git — mesmo tratamento dos demais documentos brutos da operação)*.

**Abas do relatório**: `Ordem de Alocação Pag_16E` (a cascata do mês), `Recebimentos Vendas`, `Recebimento Aluguel`, `Unidades`, `Características` (dados de emissão/integralização do CRI).

Pontos que precisam ser checados todo mês:

1. **Vendas — só a escriturada entra na cascata do mês.** O relatório traz tanto as vendas já **finalizadas/escrituradas** no período quanto as que ainda **não foram 100% recebidas** (aba `Recebimentos Vendas` tem uma coluna de "% Recebimento no período" por unidade — só quando chega a 100% a venda conta). **Importante**: apenas a venda **já escriturada (100% recebida)** compõe a "Amortização Cash Sweep" do mês — vendas parciais/em andamento ficam de fora até serem concluídas. A aba também traz a contagem de "Unidades Não Escrituradas" (159 no exemplo de set/26).
2. **Locação — sempre olhar o valor BRUTO**, não o líquido. O relatório separa "Aluguel Bruto" (usado para calcular o **covenant de Índice de Cobertura/ICSD**) de "Aluguéis Líquidos" (o que efetivamente entra na fórmula da cascata/cash sweep). São dois números diferentes — não confundir qual usar em cada cálculo.
3. **Cascata do mês** (aba `Ordem de Alocação Pag_16E`) — conferir contra o que está nos documentos (3º Aditamento ao TS), prestando atenção a:
   - **Vazamentos** ("Vazamentos Permitidos" do TS): comissão de vendas (5%), impostos sobre receita bruta (9%), e o custo de manutenção de estoque (R$ 1.031/unidade não escriturada).
   - Se há **necessidade de aporte ou consumo do Fundo de Reserva** (campo "Diferença Fundo e Saldo do Fundo de Reserva" — se negativo/positivo indica desenquadramento a corrigir).
4. **Posições de Fundo de Reserva e Fundo de Despesas** — conferir se o saldo está acima do mínimo exigido (campos "Valor Mínimo" vs "Saldo" de cada fundo no relatório) — sinal de desenquadramento se o saldo ficar abaixo do mínimo.
5. **Índice de Cobertura (ICSD)** — covenant de min. 1,25x (cláusula 10.1(xxviii) da Escritura de Debêntures), calculado com o Aluguel Bruto do ponto 2 acima. Em ago/26 estava em 2,06x (enquadrado).

*Exemplo de referência (Relatório de Crédito de set/26): Vendas do mês R$ 397.000, Aluguéis Líquidos R$ 341.902,21, Aluguel Bruto R$ 869.277,25, Vazamentos R$ 297.743,95, Fundo de Reserva com saldo de R$ 1.496.867,18 (mínimo R$ 1.298.478,30 — enquadrado), Fundo de Despesas com saldo de R$ 29.231,18 (mínimo R$ 28.880,17 — enquadrado).*

## Instrumentos (9)

| Instrumento | Data original | Aditamento mais recente na pasta | Situação |
|---|---|---|---|
| Termo de Securitização | 2022-09-27 | 3º (20/05/2026) | Faltam 1º (2022-10-20) e 2º (2024-04-01) na pasta |
| Escritura de Debêntures (Promontoria Imóveis 5) | 2022-09-22 | 4º (20/05/2026) | Faltam 1º, 2º, 3º na pasta |
| Escritura de CCI | não confirmada | 2º (12/05/2026) | 1º aditamento inferido (não presente); data original não confirmada |
| Cessão Fiduciária de Recebíveis | não confirmada | 2º (13/05/2026) | 1º aditamento inferido (não presente); data original não confirmada |
| Alienação Fiduciária de Ações (Promontoria Imóveis 3 / Fundo Multiapartamentos 1) | não confirmada | 4º (13/05/2026) | Faltam 1º, 2º, 3º; data original não confirmada |
| AF de Imóveis — Next Haddock | 2023-05-08 | 2º (20/05/2026) | Falta 1º (01/04/2024, ligação com ata 2023 incerta) |
| AF de Imóveis — Next Paulista | 2023-04-12 | 3º (20/05/2026) | Faltam 1º e 2º (datas não citadas) |
| AF de Imóveis — Next França | 2023-03-08 | 4º (20/05/2026) | Faltam 1º, 2º, 3º (datas não citadas) |
| AF de Imóveis — Onze 22 | não confirmada | 4º (20/05/2026) | Faltam 1º, 2º, 3º; data original não confirmada (trecho cortado na extração) |
| AF de Imóveis — Terraço | 2022-10-19 | 7º (20/05/2026) | Faltam 1º a 6º na pasta (datas não citadas) |

Todos os aditamentos de maio/2026 presentes na pasta decorrem da mesma origem: **Assembleia Especial de Investidores (AEI) de 23/03/2026**.

## Obrigações / Acompanhamento de Atas

- **Revisado**: sim
- **Ata mais recente**: 2026-03-23 (arquivo `16ªE_1ªS - Bread - AEI 20251003 v. com lista.pdf`)
- ⚠️ **Nota da revisão**: a leitura original tinha ficado desatualizada porque a busca só considerava arquivos com "AGT" no nome — a ata mais recente é uma **AEI** (Assembleia Especial de Investidores), que não segue esse padrão. Antes da correção, constava erroneamente a ata de 24/04/2023 como a mais recente.

### Obrigação atual (desta ata)

**Formalização do 3º Aditamento ao Termo de Securitização** (waiver do Fundo de Reserva e nova cascata de recebíveis de venda)
- A ata aprova a **não declaração de vencimento antecipado** por descumprimento da recomposição do Fundo de Reserva (vencida em 27/02/2026), autoriza o uso dos recebíveis do Patrimônio Separado para recompô-lo, e institui uma nova Conta Arrecadadora de recebíveis de venda dos imóveis, nova ordem de alocação de pagamentos e fórmula de amortização extraordinária.
- **Status: cumprido.** Documento de cumprimento: 3º Aditamento ao TS, assinado por todas as partes em 22/05/2026 (confirmado no log de assinaturas Clicksign).
- Não há prazo em dias definido na ata — só autorização para celebrar os instrumentos necessários. Outros aditamentos relacionados (AF dos 4 imóveis, Cessão Fiduciária, Escritura de CCI, Termo de Emissão de Debêntures), todos de maio/2026, formalizam o mesmo conjunto de deliberações desta assembleia.

### Histórico (superado — não é mais pendência)

**Alteração condicional do Valor Equity para aquisição do imóvel Next Haddock** (ata de 24/04/2023)
- Condicionada a saldo mínimo de R$ 1.500.000,00 na conta vinculada da Promontoria Imóveis 5 S.A., aprovou elevar o "Valor Equity" para R$ 3.903.775,66, especificamente para viabilizar a aquisição do Next Haddock.
- **Não é possível confirmar** qual aditamento formalizou esta deliberação: o único aditamento à AF do Next Haddock na pasta é o 2º (20/05/2026, decorrente da ata de 2026, não desta). Deveria existir um 1º Aditamento — o mais próximo cronologicamente seria um de 01/04/2024, mas esse arquivo não está na pasta.
- Irrelevante como pendência hoje: superado pela ata mais recente (23/03/2026).

## Pontos de atenção / riscos

1. **Nenhum instrumento original está na pasta** — toda a lista de 9 instrumentos foi reconstruída por inferência cruzada entre os considerandos dos próprios aditamentos, não por leitura direta de um "quadro de documentos" do TS original.
2. **Datas de celebração não confirmadas** em 4 instrumentos: Escritura de CCI, Cessão Fiduciária de Recebíveis, AF de Ações, AF de Imóveis — Onze 22.
3. **Gaps de aditamentos intermediários** em praticamente todos os instrumentos — só o aditamento mais recente (maio/2026) está fisicamente presente; os anteriores (1º, 2º, 3º...) são conhecidos apenas por citação.
4. **Vínculo incerto** entre o 1º Aditamento à AF Next Haddock (01/04/2024) e a deliberação da ata de 24/04/2023 — não confirmado, mas sem impacto prático (obrigação já superada).
