# Alianza GRU e Maua — Memória da Operação

> Leitura derivada de `Pipeline/documents_meta.json`, `Pipeline/obligations_data.json`, `Pipeline/portfolio_data_wrapped.json` e leitura direta dos Termos de Securitização e aditamentos de ambas as séries (TS original + 1º/4º Aditamento GRU; 1º/2º/3º Aditamento TS Mauá + 2º Aditamento ao Contrato de Cessão Mauá). O `documents_meta.json` já tem uma `metodologia_nota` extensa sobre os 11 instrumentos das 2 séries e suas divergências de data — este arquivo foca no contexto de negócio e nas metodologias de cálculo de juros, amortização, resgate antecipado/multa, vencimento antecipado e nos covenants, complementando aquela nota.
>
> Última atualização: 2026-09-19.

## Resumo

- **CRI**: duas séries sob a mesma 4ª Emissão da Virgo Companhia de Securitização (hoje Riza Securitizadora) — **435ª Série (Guarulhos/"GRU")** e **447ª Série (Mauá)**.
- **Devedor/estrutura**: financia a aquisição de 2 galpões logísticos pelo **Alianza Urban Hub Renda FII**.
- **Ativos**: Urbanhub Guarulhos (Estrada da Olaria nº 600, ABL 21.098 m², ocupação 100%, laudo R$ 88,6MM) e Alianza Urbanhub Mauá (Av. Papa João XXIII nº 3.580, ABL 29.723 m², ocupação 92,3%, laudo R$ 83,5MM).
- Emitido: R$ 80 milhões (total das 2 séries), IPCA + 7,2% a.a. Saldo devedor atual (jul/26): R$ 90,4 milhões. Vencimento: jan/32 (GRU) e fev/32 (Mauá).

## Estruturação — deal de renda com garantias compartilhadas

Deal de renda clássico: **Cessão Fiduciária de todas as locações** de ambos os imóveis + **Alienação Fiduciária de ambos os imóveis**. A particularidade desta operação é que, embora sejam 2 séries de CRI juridicamente distintas (cada uma com seu próprio TS, Escritura de CCI, AF de Imóvel), elas foram estruturadas pra **compartilhar garantias entre si**, tornando a operação mais robusta como um todo.

### Compartilhamento de Garantias e Sobejo Cruzado (2º Aditamento ao TS)

Formalizado pelo **"Instrumento Particular de Compartilhamento de Garantias e Outras Avenças"** (citado nos aditamentos, mas — como já registrado no `documents_meta.json` — **esse contrato em si nunca está fisicamente na pasta**, só é referenciado por outros instrumentos). O que ele estabelece, confirmado no 2º Aditamento ao TS:

- A **Cessão Fiduciária de Direitos Creditórios Mauá é compartilhada** entre os titulares dos CRI Mauá e os titulares dos CRI Guarulhos — o produto de uma eventual execução é aplicado na quitação das Obrigações Garantidas de ambas as séries, seguindo a ordem/proporcionalidade do Contrato de Compartilhamento de Garantias.
- **Sobejo cruzado é bidirecional**: existe uma "Cessão Fiduciária Sobejo Mauá" (excedentes da execução da AF de Imóvel Mauá, ou qualquer recurso remanescente no Patrimônio Separado dos CRI Mauá após o resgate desses CRI, revertem em favor dos titulares do **CRI Guarulhos**) e, simetricamente, uma "Cessão Fiduciária Sobejo Guarulhos" (beneficia os titulares do **CRI Mauá**). Ou seja, cada série tem um "sobejo" que reforça especificamente a outra série — não é uma via única.
- O Regime Fiduciário sobre os Créditos Imobiliários Mauá, contas e garantias é instituído "observado o compartilhamento" — formalizando isso no nível do regime fiduciário, não só contratual.

## Metodologia de cálculo de juros e amortização — idêntica nas duas séries

As duas séries seguem exatamente o mesmo modelo contratual (mesmo estruturador/período de emissão, cláusulas com a mesma numeração e redação em ambos os TS) — confirmado lendo o TS original + 1º/4º Aditamento da GRU e reconstruindo o TS Mauá (cujo original não está na pasta) a partir da versão consolidada reproduzida no 1º/2º/3º Aditamento.

### Juros remuneratórios — IPCA + 7,20% a.a., base 252, capitalização composta

- **Índice**: IPCA/IBGE. Atualização monetária mensal do saldo (Cláusula 3.5): `VNa = VNe x C`, C = produtório das variações mensais do IPCA desde a Primeira Data de Integralização.
- **Taxa**: fixa de **7,20% a.a.** para as duas séries (item "Remuneração" da Cláusula Terceira, idêntico em GRU e Mauá).
- **Convenção de dias / capitalização** (Cláusula 3.6): base de **252 Dias Úteis** (não 360), regime de **capitalização composta pro rata temporis**: `J = VNa x (Fator de juros - 1)`.
- **Periodicidade**: mensal, nas datas do Anexo I de cada série.
- Confirmado sem alteração de taxa/índice em nenhum dos aditamentos lidos (1º/4º GRU; 1º/2º/3º Mauá).

### Amortização — tabela de percentuais por Anexo I (não é SAC/Price padrão) + cash sweep obrigatório

- **Fórmula** (Cláusula 3.7, idêntica nas duas séries): `AMi = VNa x Tai`, onde `Tai` é a taxa de amortização do mês *i* definida na tabela do Anexo I de cada série — uma tabela de percentuais customizada (crescente ao longo do tempo), não um sistema SAC ou Price genérico.
- **Carência original diferente entre as séries**: GRU tem 12 meses de carência (emissão 12/01/2022, Tai = 0% até o mês 12/jan-2023, amortização começa no mês 13/fev-2023); Mauá tem 24 meses de carência (emissão 04/03/2022, 1º pagamento de amortização em 22/03/2024) — ou seja, apesar de seguirem o mesmo modelo de cláusulas, os *parâmetros* (prazo de carência) foram calibrados separadamente por série.
- **Vencimento final**: 120 parcelas mensais em ambas — GRU quita 100% em 15/07/2031 (Anexo I original), com data de vencimento formal em 15/01/2032; Mauá quita 100% no mês 120 (24/02/2032), conforme a nova Tabela de Amortização do 3º Aditamento.
- **Deliberação de 05/04/2024 (assembleias separadas por série, mesma pauta)**: nova carência de amortização — abr/2024 a dez/2024 (Mauá) e período equivalente na GRU (a partir de mar/2024) —, mantendo a obrigação de pagar Juros Remuneratórios e atualização monetária durante a carência, em troca de um **waiver fee de 0,50% sobre o saldo devedor**, pago em 6 parcelas mensais via B3 (R$ 56.179.430,96 de base na Mauá; R$ 33.153.933,28 na GRU). Formalizada em nova Tabela de Amortização anexa ao 3º Aditamento TS (Mauá) e ao 4º Aditamento TS (GRU) — os percentuais represados na carência são redistribuídos nos meses seguintes (ex. Mauá: Tai sobe de ~0,34%-0,35% para ~0,68%-0,70% no período pós-carência), sem alterar a data de vencimento final de nenhuma das séries.
- ⚠️ **Nota de confiabilidade**: a tabela do Anexo I da GRU tem inconsistências de layout/OCR em trechos intermediários (percentuais linha a linha nem sempre extraídos de forma confiável) — os pontos de início/fim (carência, retomada, 100% final) são confiáveis, mas a tabela completa mês a mês não deve ser tomada como 100% exata sem conferência visual do PDF.
- **Amortização Extraordinária Obrigatória / cash sweep** (Cláusula 6.2, idêntica nas duas séries): sempre que a Conta Centralizadora recebe Créditos Imobiliários em valor superior ao necessário para a parcela mensal do CRI (inclusive por vencimento antecipado), o excedente deve ser usado para amortização extraordinária compulsória, **até o limite de 98% do Valor Nominal Unitário Atualizado**.

### Resgate antecipado e multa de pré-pagamento ("Prêmio") — mesma fórmula make-whole nas duas séries

- **Resgate discricionário da Emissora**: vedado (Cláusula 6.1, ambas séries).
- **Amortização Extraordinária Obrigatória / Resgate Antecipado Total** (por vencimento antecipado, pagamento antecipado ou amortização extraordinária dos Créditos Imobiliários — Cláusula 6.2.2): não tem multa própria listada nesta cláusula, mas a Cláusula 6.4 (vencimento antecipado) prevê que o valor devido pode incluir "o Prêmio" por remissão expressa — ou seja, o Prêmio abaixo pode incidir também em cenário de aceleração, não só no resgate voluntário.
- **Resgate Antecipado Facultativo do Devedor** (Cláusula 6.3): sujeito a *lock-up* de 48 meses contados do pagamento do Preço da Cessão (Cláusula 6.3.1). Depois do lock-up, incide o **Prêmio** — um make-whole sobre o fluxo remanescente, não indexado a título público (NTN-B) como em outras operações do portfólio, mas calculado com spread fixo (Cláusula 6.3.4(iv)):
  `Prêmio = [Σ (PMTi / (1 + i)^(du/252))] − Saldo Devedor`, com **spread de 5% a.a.**, `du` = dias úteis entre a data de cálculo e cada parcela remanescente (base 252), `PMTi` = i-ésima parcela da tabela de amortização/juros, `Saldo Devedor` = saldo da Parcela Securitização na data do pagamento antecipado. Fórmula idêntica (mesma numeração de cláusula, mesmo spread) em GRU e Mauá, confirmada sem alteração em nenhum aditamento lido.
- **Resgate facultativo TOTAL da GRU condicionado à simultaneidade com Mauá**: a versão consolidada do TS GRU (via 4º Aditamento) traz a Cláusula 6.3.2 condicionando o pagamento antecipado facultativo *total* a ocorrer **concomitantemente** com o pagamento antecipado facultativo total do lado Mauá — essa condicionante **não existe** no TS original nem no 1º Aditamento GRU (ambos permitem resgate total "a exclusivo critério" do Devedor sem essa amarração), então foi introduzida por um dos aditamentos ausentes da pasta (2º ou 3º Aditamento TS GRU — ver gap já mapeado no `documents_meta.json`), provavelmente o mesmo instrumento de 08/07/2022 que formaliza o Compartilhamento de Garantias.
- **Multa moratória** (atraso simples de pagamento, não resgate antecipado): 2% de multa + 1% a.m. de juros moratórios sobre valores em atraso (Cláusula 3.4, idêntica nas duas séries).
- ⚠️ Não encontrada a fórmula da "remuneração proporcional" que também compõe o valor total do pagamento antecipado facultativo (Cláusula 6.3.4(ii), remete ao item 1.4 do Anexo 3.6.1 do Compromisso de Venda e Compra Mauá) — está no CVC original ou seu 1º Aditamento, não lidos nesta rodada.

## Vencimento antecipado — automático vs. assembleia, com vencimento cruzado entre as séries

Estrutura idêntica nas duas séries: Cláusula 6.4, dividida em **6.4.1 (eventos automáticos)** e **6.4.2 (eventos não automáticos)**.

- **6.4.1 — Automáticos**: declarados diretamente pela Emissora se não sanados no prazo de cura da própria alínea, **sem necessidade de assembleia**. Lista original (ambas séries): (i) inadimplemento de obrigação pecuniária, cura de 2 dias úteis; (ii) atos de repúdio/anulação dos Documentos da Securitização; (iii) cessão/oneração não autorizada de direitos/obrigações; (iv) liquidação/dissolução do Devedor não revertida em 20 dias; (v) invalidade/nulidade do CVC ou dos Documentos por decisão judicial.
- **Achado central — vencimento cruzado entre as séries, com exceção de "perdão simultâneo"**: em algum aditamento ausente da pasta (entre o 1º e o 4º da GRU; confirmado presente na consolidada do 4º Aditamento, mas **ausente** no TS original e no 1º Aditamento GRU), foram incluídos os itens 6.4.1(vi) — não registro dos instrumentos de compartilhamento de garantias nos prazos — e 6.4.1(vii) — qualquer Evento de Aceleração de Pagamento da série irmã, **"exceto se verificado o perdão tanto no âmbito dos CRI como no âmbito dos CRI [série irmã]"**. Confirmado espelhado: o 2º Aditamento ao TS Mauá (08/07/2022, já citado na seção de Estruturação) tem a cláusula equivalente do lado Mauá com a mesma exceção de perdão simultâneo. Ou seja, as duas séries têm vencimento cruzado automático mútuo, mas com uma válvula de escape caso ambas as séries perdoem o mesmo evento ao mesmo tempo.
- **6.4.2 — Não automáticos**: dependem de deliberação em assembleia de titulares; **sem quórum de instalação, a Emissora NÃO declara** o vencimento antecipado (regra oposta à dos automáticos, onde a falta de quórum leva à declaração). Lista extensa (~30 hipóteses, alíneas "a" a "ee"), incluindo — e isto confirma/detalha o que as seções de covenants abaixo já diziam de forma resumida — **LTV > 60% sem reforço de garantia (alínea "l")** e **Índice de Cobertura abaixo do mínimo sem reforço (alínea "m")**: ambos são hipóteses NÃO automáticas, sempre passam por assembleia antes de qualquer aceleração efetiva. Outras hipóteses relevantes: descumprimento de obrigação não pecuniária (cura 10 dias úteis — é essa a base da ata AGT 16.07.2026, ver seção de Obrigações), inadimplemento cruzado com terceiros (>R$500 mil individual / R$1 milhão agregado), sinistro total/parcial sem recomposição (180 dias), ônus não autorizado sobre o imóvel (30 dias), não renovação de seguro (15 dias) ou de licenças (90 dias), entre outras — cada alínea com seu próprio prazo de cura embutido.
- O 4º Aditamento GRU (12/07/2024) e o 3º Aditamento Mauá (16/06/2024) **não alteraram** a Cláusula 6.4 além do já registrado nas seções de LTV/ICSD abaixo (data de entrega do laudo, lista de Avaliador Autorizado).

## Metodologias de cálculo confirmadas

### ICSD (Índice de Cobertura) — consolidado, com visão segregada gerencial

**Fórmula oficial** (TS, Cláusula 6.4.7): `Índice de Cobertura = Fluxo de Recebíveis / Serviço Mensal dos CRI Mauá e dos CRI Guarulhos`, onde:
- **Fluxo de Recebíveis** = soma dos Direitos Creditórios Locação (receita de locação/exploração comercial) de **ambos** os imóveis, depositados na Conta Arrecadadora no mês.
- **Serviço Mensal** = soma de (amortização programada + juros remuneratórios) das **duas séries somadas** (CRI Mauá + CRI Guarulhos).
- **Mínimo: 1,30x**, apurado mensalmente (10 dias corridos após fechamento do mês pra Devedora enviar relatório, 5 dias úteis pra Emissora calcular). Desenquadrar → 10 dias de cura (reforço de garantia) ou vencimento antecipado.

**Confirmado — é mesmo consolidado**, exatamente como você descreveu: não existe uma fórmula formal separada por série no TS. Mas o dado financeiro já cadastrado no pipeline tem um acompanhamento gerencial segregado (`ic_by_group`): em jul/26, consolidado 1,36x (Mauá 1,13x / GRU 1,75x) — confirma a prática de "olhar onde estão as diferenças" que você mencionou, mesmo sem consequência contratual própria por série.

### LTV — verificação mensal, laudo anual (nuance importante)

`LTV = saldo devedor dos CRI / valor de avaliação do imóvel`, máximo **60%**. Duas frequências diferentes que não devem ser confundidas:
- A **verificação do LTV em si é mensal** (recalcula o saldo devedor contra o último laudo disponível) — TS Cláusula 6.4.6.
- O **laudo de avaliação é anual** (entregue até 15/jan de cada ano, com data-base de dezembro do ano anterior) — TS Cláusula 6.4.6.1, por um dos 5 Avaliadores Autorizados definidos no contrato (Cushman & Wakefield, Colliers, JLL, CBRE, Capright).
- Desenquadrar (LTV > 60%) → Devedor tem 30 dias pra oferecer reforço de garantia (novo laudo + parecer legal), submetido à aprovação em assembleia; sem acordo, vencimento antecipado.
- LTV atual consolidado (jul/26): 52,5% — enquadrado, com folga.

### Fundo de Reserva — base dinâmica de 3 parcelas futuras (confirmado)

Um fundo **por série** (GRU e Mauá, valores/cláusulas distintos):
- **Mauá**: valor inicial R$ 586.876,18 (TS Cláusula 5.2). Mínimo dinâmico: (i) 2 próximas parcelas de juros durante o período entre a 1ª e a 2ª Parcela do Preço de Cessão (fase de aquisição do imóvel); depois (ii) **3 próximas parcelas de juros + amortização dos CRI** (fase operacional normal — é essa a "base dinâmica de 3 parcelas futuras" que você mencionou). Recomposição: 5 dias úteis.
- **GRU**: valor inicial R$ 342.828,66, mesma lógica das 3 parcelas futuras (Cláusula 5.2 do 3º Aditamento ao TS GRU).
- Atual (jul/26): GRU R$ 978.553,04 (mínimo R$ 971.428,07); Mauá R$ 1.662.396,85 (mínimo R$ 1.634.569,40) — ambos enquadrados, folga pequena.

### Fundo de Despesas — existe, mas não achei acompanhamento separado por série no dado financeiro atual

Confirmado no TS (Mauá): equivalente a ~12 meses de despesas recorrentes, inicial R$ 60.069,64. **Ponto de atenção**: diferente do Fundo de Reserva, não encontrei um item de covenant "Fundo de Despesas (GRU)"/"(MA)" separado na lista de covenants já cadastrada no pipeline — pode ser que esteja sendo acompanhado só internamente/manualmente, sem um card dedicado no portal ainda. Vale confirmar se isso é uma lacuna a preencher.

### Rent roll / acompanhamento dos locatários

Existe um campo dedicado no schema de dados do portal pra isso (`locatarios`), mas está **vazio** pra esta operação no momento — a informação em si existe (vem do relatório mensal que a Devedora envia, conforme minuta do Anexo IV à Cessão Fiduciária de Direitos Creditórios Mauá — é a mesma fonte que alimenta o cálculo do ICSD), só ainda não foi estruturada nesse campo específico do portal. Exemplos recentes de reajuste captados nos *highlights* (jul/26): inquilino AGI reajustado pra R$ 331.514 (R$ 24,77/m²), Platinum Log pra R$ 104.856 (R$ 29,80/m²).

## Instrumentos

Ver `documents_meta.json` pra lista completa (11 instrumentos, com toda a desambiguação de datas de nome-de-arquivo vs. corpo do documento, e os gaps já mapeados: 2º/3º Aditamento ao TS GRU ausentes, o próprio Contrato de Compartilhamento de Garantias nunca presente na pasta, conflito de data não resolvido na AF de Imóvel Mauá). Este arquivo não repete esse levantamento — só acrescenta o contexto de negócio e as fórmulas acima.

## Obrigações / última ata

**Checagem geral**: `Pipeline/obligations_data.json` já tem `"reviewed": true` para esta operação, com 11 itens cobrindo todo o histórico de atas (14/03/2022 a 16/07/2026, ambas as séries) — cada um com status de verificação (`cumprido`, `provável`, ou `não é possível confirmar`). Nenhum comprovante de pagamento/registro cartorial está fisicamente na pasta para nenhum item (padrão recorrente já visto em outras operações do portfólio — atas registram a obrigação, mas o comprovante de cumprimento raramente está no mesmo lugar), então a maioria dos itens mais antigos fica em "não é possível confirmar" mesmo com prazo já vencido, exceto onde há evidência documental indireta (ex. covenants já refletindo a mudança aprovada, como o "Laudo de Avaliação (MA)" mostrando enquadramento sob a nova data-limite de 15/jun).

**Ata mais recente**: AGT 16/07/2026 — aprova a não declaração de vencimento antecipado por descumprimento de obrigações não pecuniárias, concedendo 30 dias corridos pro Devedor cumprir as obrigações listadas num **"Anexo II"** dessa mesma ata.

**⚠️ Não é possível confirmar o conteúdo nem o cumprimento dessa obrigação**: o PDF da ata na pasta tem só 5 páginas e termina na assinatura — o Anexo II citado (a lista real das obrigações) **não está presente** entre os documentos indexados. Vale pedir a versão completa da ata (com anexos) pra saber exatamente o que precisa ser cumprido e monitorar o prazo (venceria por volta de 15/08/2026, já vencido sem confirmação).

## Pontos de atenção / riscos

1. **Anexo II da ata de 16/07/2026 ausente** — maior lacuna aberta agora; sem ele não dá pra saber o que está pendente de cumprimento nem se o prazo (já vencido) foi cumprido.
2. **Contrato de Compartilhamento de Garantias nunca está fisicamente na pasta** — o mecanismo inteiro de sobejo cruzado é reconstruído por citação em outros instrumentos, nunca lido diretamente na fonte primária.
3. **Fundo de Despesas sem covenant dedicado visível** no dado financeiro atual (só Fundo de Reserva tem card próprio por série) — confirmar se é lacuna de cadastro.
4. **Campo de rent roll (`locatarios`) vazio** — dado existe nos relatórios mensais da Devedora, mas não estruturado no portal ainda.
5. Gaps de datas/atas já mapeados no `documents_meta.json` (2º/3º Aditamento TS GRU ausentes, conflito de data da AF Imóvel Mauá, atas de 08/07/2022 e 05/04/2024-GRU referenciadas mas ausentes) continuam válidos e não foram revisitados nesta rodada.
6. **Conteúdo provável dos aditamentos GRU ausentes (2º/3º ao TS)**: a leitura desta rodada (comparando o TS original + 1º Aditamento GRU contra a versão consolidada reproduzida no 4º Aditamento) revela que um desses aditamentos ausentes introduziu pelo menos duas mudanças relevantes de crédito: (i) o vencimento cruzado automático com a série Mauá (Cláusula 6.4.1(vi)/(vii)) e (ii) o condicionamento do resgate facultativo TOTAL da GRU à simultaneidade com o resgate total da Mauá (Cláusula 6.3.2) — prováveis efeitos colaterais da formalização do Compartilhamento de Garantias em 08/07/2022. Vale localizar esses instrumentos para confirmar a data exata e se há mais alterações não capturadas pela consolidada.
7. **Fórmula da "remuneração proporcional" do pagamento antecipado facultativo** (Cláusula 6.3.4(ii), remete ao item 1.4 do Anexo 3.6.1 do Compromisso de Venda e Compra Mauá) não encontrada nos documentos lidos — precisa do CVC original ou seu 1º Aditamento para fechar a conta completa do valor de resgate facultativo.
8. **Tabela de amortização (Anexo I) da GRU não confere linha a linha com 100% de certeza** — extração via `pdftotext` teve inconsistências de layout em trechos intermediários; os pontos de início/fim (carência, retomada pós-carência, 100% final) são confiáveis, mas para uso operacional (ex. conferência de parcela específica) vale checar visualmente o PDF.
