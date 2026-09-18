# Localfrio — Memória da Operação

> Leitura derivada de `Pipeline/documents_meta.json`, `Pipeline/obligations_data.json`, `Pipeline/portfolio_data_wrapped.json` e leitura direta do Termo de Securitização, da ata AGT 29/08/2022, da ata AGT 08/02/2021 e do material de apoio Movecta (jan/2024). Não é fonte de dados para o `build_data.py` — é um resumo pra revisão humana.
>
> Última atualização: 2026-09-18.

## Resumo

- **CRI**: 54ª Série (Sênior) e 55ª Série (Subordinada) da 4ª Emissão, Virgo Companhia de Securitização (hoje Riza Sec, antiga ISEC Securitizadora). TS celebrado em 14/11/2019.
- **Estrutura**: sale-leaseback — **Localfrio Administração de Bens Ltda.** (Cedente, proprietária dos imóveis) e **Localfrio S.A. Armazéns Gerais Frigoríficos** (Devedora, locatária/operadora) — mesma economia (grupo Localfrio), mas 2 pessoas jurídicas distintas no papel de Cedente vs. Devedora.
- Emitido: R$ 100 milhões (R$80MM Sênior 54ª + R$20MM Subordinada 55ª), IPCA + 6,00% a.a. (Sênior), amortização mensal. Vencimento: 16/12/2031. Saldo devedor Sênior atual (jul/26): R$ 61,5 milhões.

## Estruturação

**2 imóveis de armazenagem frigorífica**, ambos 100% ocupados e locados integralmente para a própria Localfrio Armazéns Gerais (locatária única):
- **Armazém Anhanguera** (Rua Jair Afonso Inácio, 800, Pirituba/SP) — 9.832 m², aluguel mensal R$ 453.715,22.
- **Armazém Itajaí** (Rua Francisco Rei, 1205, Itajaí/SC) — 12.680 m², aluguel mensal R$ 705.563,71. No TS, esse imóvel ("Imóvel 1") é registrado sob **2 matrículas** (nº 40 e 40.62X do 2º Ofício de Registro de Imóveis de Itajaí) — o que explica por que um material de apoio de 2024 fala em "3 imóveis (1 São Paulo e 2 Itajaí)": é a mesma estrutura física, só contada por matrícula em vez de por galpão.

**Garantias** (TS, definição "Garantias"): Alienação Fiduciária de Quotas (da Cedente), Alienações Fiduciárias de Imóveis (os 2 armazéns), Cessão Fiduciária (da Conta Vinculada), Fiança, e "outra garantia adicional eventualmente constituída".

## Histórico de movimentos (assembleias)

1. **08/02/2021** — evento administrativo menor: um pagamento de amortização+juros em 16/12/2020 usou recursos do Fundo de Reserva além do previsto, desenquadrando-o temporariamente. Assembleia aprovou compensar o valor pago a maior (R$ 62.062,61) na parcela seguinte (18/02/2021), com um cronograma alternativo (Anexo A) como plano B.

2. **29/08/2022 (AGT, reaberta após 12 suspensões desde 25/04/2022)** — a mais relevante: em troca da aprovação da substituição de um fiador falecido (Sr. Hélio de Athayde Vasone → sua viúva Marilena + Localpar Participações S.A. como nova fiadora corporativa), os Titulares negociaram um pacote de reforço:
   - **Criação do covenant Dívida Líquida/EBITDA** (trajetória decrescente até 3x em 5 anos, incluindo arrendamento no cálculo, EBITDA considerado só "no que transitar em caixa").
   - Alteração do covenant de serviço da dívida existente (mesma regra do EBITDA em caixa).
   - Novas obrigações documentais: balancete trimestral (60 dias), balanço anual auditado (90 dias, +30 se atraso de auditoria comprovado), IR dos fiadores pessoa física (5 dias após prazo legal), comunicação em 5 dias de perda de concessão de terminal ou de licença CLIA.
   - Tecnicamente configurava um "Evento de Recompra Compulsória" (Cláusula 4.1 (i) e (vii) do Contrato de Cessão), mas os Titulares optaram por não decretar, dado o pacote de reforço acordado.

3. **22/01/2024 (material de apoio Movecta — "Assembleia CRI Janeiro 2024")** — propõe 3 mudanças: (a) troca de fiadora Localpar → FHV Participações (extinção da Localpar por eficiência tributária do grupo); (b) redução do Limite Mínimo do Fundo de Reserva de 5 para 3 PMTs (liberando o excedente à Devedora); (c) uso do próprio Fundo de Reserva pra custear os aditamentos necessários. **A redução do Fundo de Reserva (item b) não foi aprovada** (confirmado pelo usuário) — a operação segue com 5 PMTs. Não há, na pasta, nenhuma ata assinada confirmando o resultado dos demais itens (troca de fiadora); só o material de apoio/pleito da consultoria Movecta.

4. **18/09/2025 (Edital de Recompra Facultativa e outros)** — convocação de uma nova assembleia. É só o **edital de convocação**, não a ata do resultado — mesma situação do item anterior, não dá pra confirmar se ocorreu nem o que foi decidido.

## Metodologias de cálculo

### Dívida Líquida / EBITDA (o covenant central desta operação)

Texto da deliberação de 29/08/2022: **trajetória decrescente até 3,0x em 5 anos**, "incluindo arrendamento no cálculo" (ou seja, considera o passivo de arrendamento, coerente com a estrutura de sale-leaseback), com EBITDA considerado apenas "no que transitar em caixa" (apurado por auditoria externa). O material de apoio da Movecta detalha os componentes:
- `Dívida Líquida = Dívida Bruta (Bancos + CRI) − Caixa`
- `EBITDA (ex-IFRS16) = EBITDA Contábil − Amortização − Juros dos Arrendamentos`
- Situação relatada em jan/2024: a empresa já estava em 2,0x (ex-IFRS16) desde 2022, abaixo do limite — folga confortável.

Verificado **anualmente** (documento no pipeline: AGT 29/08/2022; última atualização 30/05/2026). Status atual: Enquadrado.

### ICSD — informal/gerencial, sem mínimo formal

O material da Movecta também define um ICSD complementar: `ICSD = Geração de Caixa CRI / Serviço da Dívida`, onde Geração de Caixa CRI = EBITDA ex-IFRS16 − IR/CSLL pago, e Serviço da Dívida = Pagamento CRI + Principal e Juros da Dívida Bancária. No dado já cadastrado no pipeline, esse índice aparece como "IC Gerencial" — **sem mínimo exigido formalmente**, só acompanhamento (atual: 1,16x).

### Fundo de Reserva — confirmado: segue em 5 PMTs (a redução para 3 PMTs NÃO foi aprovada)

TS original (2019): valor de constituição R$ 4.914.586,53. A proposta da Movecta (jan/2024) de reduzir de 5 para 3 PMTs **não foi aprovada** — confirmado pelo usuário. A operação segue com o Fundo de Reserva em **5 PMTs de Sr + Sub** (mínimo atual R$ 5.648.505,56, saldo R$ 6.467.947,16 — enquadrado). O texto descritivo (`sobre_operacao`) do dado já cadastrado no pipeline, que afirma "reduzido para 3 PMTs em 2024", está **desatualizado/incorreto** e vale corrigir na próxima atualização — o covenant em si (que já mostra 5 PMTs) está certo.

### LTV — acompanhado, sem covenant formal de vencimento antecipado

Documento: Contrato de Cessão (4.5.iii). Obs. já cadastrada: "acompanhar o comportamento de LTV, principalmente nas correções anuais. Não tem necessidade de atualização de laudo anual" — ou seja, diferente de Jardins/Itaim/BR Properties, aqui o LTV parece ser só monitorado, sem um limite formal com consequência de vencimento antecipado atrelada (não confirmado 100% sem o Contrato de Cessão completo). Atual: 49,1%.

### Rent roll / conta vinculada / "Monitori"

Rent roll: dado de aluguel mensal por imóvel já está cadastrado (ver seção de estruturação acima), mas o campo dedicado (`locatarios`) está vazio — mesmo padrão de lacuna observado em outras operações. **Não encontrei nenhuma menção a "Monitori"** em nenhum dos documentos lidos (TS, atas, material Movecta) — pode ser um agente de monitoramento contratado fora dos documentos desta pasta, ou parte do Contrato de Cessão (que não foi lido integralmente nesta rodada).

## Pontos de atenção / riscos

1. **Texto descritivo do dado financeiro desatualizado**: afirma que o Fundo de Reserva foi "reduzido para 3 PMTs em 2024", mas isso não foi aprovado — segue em 5 PMTs. Vale corrigir esse texto no pipeline.
2. **Fiador atual: Localpar ou FHV?** — a troca proposta em jan/2024 não tem confirmação documental de que foi formalizada.
3. **Edital de 18/09/2025 sem ata de resultado na pasta** — não dá pra saber o que foi deliberado (nem se a assembleia ocorreu).
4. **Contrato de Cessão não foi lido integralmente** — é onde estão definidos os detalhes completos do LTV, da Conta Vinculada e possivelmente do "Monitori" — só citações indiretas foram capturadas via TS e atas.
5. Estrutura de sale-leaseback com Cedente e Devedora sendo entidades jurídicas distintas do mesmo grupo — vale ter isso em mente ao avaliar risco de crédito consolidado do grupo Localfrio.
