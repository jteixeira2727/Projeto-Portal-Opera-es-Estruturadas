# Alianza GRU e Maua — Memória da Operação

> Leitura derivada de `Pipeline/documents_meta.json`, `Pipeline/obligations_data.json`, `Pipeline/portfolio_data_wrapped.json` e leitura direta do 2º Aditamento ao TS (instrumento que implementa o Compartilhamento de Garantias). O `documents_meta.json` já tem uma `metodologia_nota` extensa sobre os 11 instrumentos das 2 séries e suas divergências de data — este arquivo foca no contexto de negócio e nas metodologias de cálculo dos covenants, complementando aquela nota.
>
> Última atualização: 2026-09-18.

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

**Ata mais recente**: AGT 16/07/2026 — aprova a não declaração de vencimento antecipado por descumprimento de obrigações não pecuniárias, concedendo 30 dias corridos pro Devedor cumprir as obrigações listadas num **"Anexo II"** dessa mesma ata.

**⚠️ Não é possível confirmar o conteúdo nem o cumprimento dessa obrigação**: o PDF da ata na pasta tem só 5 páginas e termina na assinatura — o Anexo II citado (a lista real das obrigações) **não está presente** entre os documentos indexados. Vale pedir a versão completa da ata (com anexos) pra saber exatamente o que precisa ser cumprido e monitorar o prazo (venceria por volta de 15/08/2026, já vencido sem confirmação).

## Pontos de atenção / riscos

1. **Anexo II da ata de 16/07/2026 ausente** — maior lacuna aberta agora; sem ele não dá pra saber o que está pendente de cumprimento nem se o prazo (já vencido) foi cumprido.
2. **Contrato de Compartilhamento de Garantias nunca está fisicamente na pasta** — o mecanismo inteiro de sobejo cruzado é reconstruído por citação em outros instrumentos, nunca lido diretamente na fonte primária.
3. **Fundo de Despesas sem covenant dedicado visível** no dado financeiro atual (só Fundo de Reserva tem card próprio por série) — confirmar se é lacuna de cadastro.
4. **Campo de rent roll (`locatarios`) vazio** — dado existe nos relatórios mensais da Devedora, mas não estruturado no portal ainda.
5. Gaps de datas/atas já mapeados no `documents_meta.json` (2º/3º Aditamento TS GRU ausentes, conflito de data da AF Imóvel Mauá, atas de 08/07/2022 e 05/04/2024-GRU referenciadas mas ausentes) continuam válidos e não foram revisitados nesta rodada.
