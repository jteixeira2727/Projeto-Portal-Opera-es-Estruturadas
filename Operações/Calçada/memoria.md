# Calçada — Memória da Operação

> Leitura derivada de `Pipeline/documents_meta.json`, `Pipeline/obligations_data.json`, `Pipeline/portfolio_data_wrapped.json` e leitura direta da ata mais recente (AGT 08/04/2026), do 3º Aditamento ao TS (26/02/2025), do **Termo de Securitização original** (20/12/2019), do **2º Aditamento ao TS** (08/09/2021), da **CCB via Negociável** (20/12/2019, cláusulas de juros, amortização, resgate antecipado, vencimento antecipado e obrigações) e do **Contrato de Cessão Fiduciária de Direitos Creditórios** original (cláusula da Razão de Garantia). Não é fonte de dados para o `build_data.py` — é um resumo pra revisão humana. O `documents_meta.json` já tem uma `metodologia_nota` bem detalhada sobre os 9 instrumentos e suas desambiguações (2 cadeias de Cessão Fiduciária quase homônimas, CCB com 2 vias físicas etc.) — este arquivo foca no contexto de negócio/reestruturação e nas metodologias de cálculo, complementando aquela nota, não substituindo. **Atenção**: a CCB (ambas as vias) tem camada de texto de OCR de baixa qualidade (muitos caracteres trocados/faltantes, ex. "seräo", "lmóvel", numeração de itens cortada) — a lista de eventos de vencimento antecipado abaixo foi reconstruída trecho a trecho a partir desse OCR ruim; o conteúdo de cada evento é confiável, mas a letra exata do item (a, b, c...) pode conter pequenos erros de sequência.
>
> Última atualização: 2026-09-18.

## Resumo

- **CRI**: 183ª Série da 1ª Emissão, Habitasec Securitizadora S.A. — TS celebrado em 20/12/2019.
- **Devedora**: Calçada Empreendimentos Imobiliários S.A. — **Em Recuperação Judicial**.
- **Lastro**: CCB emitida pela Devedora, destinada ao financiamento da construção do "Square Design Hotel" (antigo Hotel Vogue Square), Av. das Américas nº 8.585, Barra da Tijuca/RJ. Operador: XR Advisor.
- Emitido: até R$ 30 milhões, IPCA + 12,00% a.a. **Vencimento prorrogado de 21/12/2024 para 21/12/2029** (60 meses) em razão da recuperação judicial.
- Saldo devedor atual (jul/26): R$ 24,2 milhões. Avaliação do ativo: R$ 136,2 milhões (laudo Bolsa de Negócios Imobiliários do RJ).

## Contexto de negócio e reestruturação

**Origem — deal de renda hoteleira.** Nasceu financiando a construção do hotel, com receita vindo da exploração hoteleira (aluguel fixo do operador + participação no resultado) cedida fiduciariamente.

**Gatilho da reestruturação: pedido de Recuperação Judicial da Devedora.** Em decorrência disso, foram realizadas Assembleias em **18/12/2024** (rerratificada 19/12/2024) e **30/01/2025**, implementadas pelo **3º Aditamento ao TS** (26/02/2025) e aditamentos correspondentes aos demais 7 instrumentos (mesma data, arquivos "Terceiro Aditamento..." na pasta). O que foi deliberado:

1. **Prorrogação de 60 meses**: vencimento final da CCB/CRI de 20-21/12/2024 para **20-21/12/2029**.
2. **Prêmio Extraordinário (waiver fee)**: 1% do saldo devedor atualizado = R$ 405.926,17, incorporado ao saldo em 18/12/2024, pago junto com as parcelas de amortização.
3. **Instituição de multipropriedade sobre o Prédio H** (o hotel, matrícula 426.361, 9º Ofício RI-RJ): os 222 quartos viraram **444 matrículas de "Frações de Tempo"** (2 por quarto — uma com direito de uso de 182 dias/ano, outra de 183 dias/ano) — o mecanismo jurídico que efetivamente **transforma o hotel em unidades individualizáveis e vendáveis** (o "deal de estoque" que você mencionou).
4. **"Divisão" entre os 2 coproprietários do imóvel**: Hotel Vogue (82%) e SPE Pontual 4 (18%). Só as frações da **Hotel Vogue** entram nesta operação como garantia — os quartos 101-140, 201-240, 401-440, 501-540, 601-618 e 622 (**179 unidades**, confirmado batendo com o "Unidades Garantia" do dado financeiro). Os quartos da Pontual (301-340, 619-621, **43 unidades**) **não fazem parte desta operação**.
5. **Cessão Fiduciária de Recebíveis Venda e de Recebíveis Exploração** — novo instrumento criado especificamente pra cobrir a venda das Frações de Tempo Hotel Vogue e a exploração residual (locação/pool) das que ainda não foram vendidas.
6. **Contratação de um Servicer** (empresa a ser indicada em assembleia futura) — responsável por acompanhar as vendas e conciliar o recebimento da carteira de recebíveis cedida; custo entra no Fundo de Despesas.

**Refinamento mais recente — AGT de 08/04/2026 ("Repactuação, condomínio residencial")**: converte as 444 Frações de Tempo (multipropriedade hoteleira) em **222 matrículas de Apartamentos residenciais** (mesma numeração dos quartos, agora unificando as 2 frações de cada um), com base na LC Municipal 291/2025. Cronograma: até 180 dias (+90 se diligente) pra aprovação municipal + assembleia de condomínio; depois 30 dias pra aditar a AF de Imóvel; depois 90 dias pra concluir os registros. Essa ata também tratou de 2 waivers pontuais (ver seção de obrigações).

## Metodologias de cálculo confirmadas

### Juros Remuneratórios e Atualização Monetária (Cláusulas 6.1/6.2 do TS — inalteradas pela reestruturação)

**Atualização monetária (IPCA)** — `VNA = VNB × C`, onde `C = (NIk/NIk-1)^(dcp/dct)` é o fator de variação do IPCA, calculado com 8 casas decimais sem arredondamento. `NIk` é o número-índice do **segundo mês imediatamente anterior** ao mês de cálculo (ex.: atualização de junho usa o índice de abril, divulgado em maio) — mesma defasagem M-2 do padrão Habitasec visto em outras operações da casa. Periodicidade: **mensal**, na **Data de Aniversário** (todo dia 21 de cada mês, TS 6.1.2). Índice substituto em cascata se o IPCA for extinto: (i) IGP-M/FGV ou outro índice oficial acordado em Assembleia; (ii) se não houver acordo, a Devedora pode optar por pagar antecipadamente o saldo total em até 30 dias; (iii) se o índice não estiver disponível na Data de Aniversário, usa-se a média dos últimos 12 meses divulgados, compensado depois.

**Juros Remuneratórios** — taxa de **12,00% a.a., capitalizados diariamente de forma exponencial e cumulativa pro rata temporis**, base 360 dias corridos, incidente sobre o Saldo Devedor Atualizado (VNA) desde a Data da Primeira Integralização (ou a Data de Aniversário imediatamente anterior) até a data de cálculo. Fórmula: `J = SDA × (Fator de Juros − 1)`, com `Fator de Juros = [(12,00/100 + 1)^(1/12)]^(dcp/dct)`, calculado com 9 casas decimais. Data do 1º pagamento de juros: 21/01/2020. **Taxa de 12,00% a.a. não foi alterada pelo 3º Aditamento** (repactuação de 26/02/2025) — confirmado na redação atualizada da cláusula 5.1(h) do TS, idêntica à original.

### Estrutura de Amortização — do "bullet" original à trilha de Saldo Devedor Máximo (Cláusula 6.3 do TS)

**Estrutura original (20/12/2019 a 25/02/2025) — bullet loan**: só juros eram pagos mensalmente (60 parcelas); **100% do principal em parcela única na Data de Vencimento Final** (originalmente 21/12/2024). Fórmula original: `AMi = VNA × Tai` (Tai = percentual da i-ésima parcela, tabela do Anexo I — com Tai = 0% em todas as parcelas de juros e 100% só na parcela final).

**Estrutura pós-3º Aditamento (vigente desde 26/02/2025) — amortização por trilha de saldo-alvo, não mais bullet nem tabela Price/SAC fixa**: a fórmula mudou para `AAi = (VNA × Tai) × AMi`, onde `AMi` é uma **amortização mínima condicionante** calculada por comparação entre o VNA corrente e o "Saldo Devedor Máximo" tabelado para a próxima Data de Aniversário semestral (Anexo I, tabela já documentada abaixo em "Saldo Devedor Máximo"):
- Se `VNA − SDi ≤ 0`: `AMi = 0` (saldo já está dentro do limite; não há amortização obrigatória adicional na parcela).
- Se `VNA − SDi > 0`: `AMi = (VNA − SDi)/VNA × Tai` (força a amortização necessária para reenquadrar o saldo ao teto da tabela).
- Parcela mensal total: `Pi = AAi + J` (amortização + juros do período).

Ou seja, diferente do padrão "tabela pré-fixada" visto em Pirelli — aqui a amortização ordinária **persegue dinamicamente o teto semestral de saldo devedor** (a tabela de "Saldo Devedor Máximo" abaixo), o que absorve tanto a amortização ordinária quanto o efeito de qualquer amortização extraordinária (VMD) já realizada no período — explica por que o dado financeiro bate com a leitura de "amortização acumulada já superando a meta do semestre" mencionada na nota de conferência abaixo.

**Prêmio Extraordinário (waiver fee)** incorporado ao saldo em 18/12/2024 (R$ 405.926,17 = 1% do saldo devedor então) segue o mesmo fluxo de pagamento das parcelas de amortização do Anexo I — não é uma parcela à parte.

### Multa de Resgate Antecipado Facultativo — "Prêmio" (Cláusula 3.5 da CCB)

Distinto da VMD/Cash Sweep (que é **isento de multa de pré-pagamento**, ver abaixo): o resgate antecipado **facultativo** da CCB (por iniciativa da Devedora, fora do mecanismo de venda de Frações de Tempo) está sujeito a:
- **Lock-up de 2 anos** contados da Data de Emissão (20/12/2019) — só pode ser exercido a partir de 20/12/2021.
- **Prêmio de 1,5% a.a.** (break funding fee), aplicado de forma **linear (não composta/não é valor presente)** sobre o Saldo Antecipado, pro rata do **prazo remanescente até o vencimento**: `Prêmio = Saldo Antecipado × 1,5% × (n/360)`, onde `n` é o número de dias corridos remanescentes entre a Data de Resgate Antecipado e a Data de Vencimento Final da CCB. Correção de leitura: o OCR da CCB (cláusula 3.5.1) sugeria uma fórmula exponencial/de capitalização, mas a leitura correta é a proporcionalidade simples taxa × prazo remanescente, como confirmado pelo usuário.
- Resgate sempre acompanhado do saldo devedor atualizado + Remuneração + encargos até a data.
- Aviso prévio de 15 dias corridos à Securitizadora.
- Não foi identificada alteração desta cláusula pelos aditamentos de 26/02/2025 (nem o 3º Aditamento à CCB nem ao TS mencionam o Resgate Antecipado Facultativo) — o mecanismo de 1,5% a.a. + lock-up segue valendo tal como na emissão original, em paralelo ao novo mecanismo de amortização obrigatória por venda de unidade (VMD).

### VMD — Cash Sweep por venda de unidade

Toda venda de uma Fração de Tempo Hotel Vogue gera amortização extraordinária obrigatória. **VMD = maior entre R$ 250.000,00 (Valor Mínimo de Venda por Fração de Tempo, TS Cláusula 8.3.3) e 85% do preço de venda daquela fração.** Como cada quarto tem 2 frações, isso equivale a **R$ 500.000 por unidade/quarto inteiro** — o número que já está documentado no dado financeiro (`valor_quarto` do estoque inicial = R$ 500.000) e que você mencionou. Mecânica:
- Apurado **2x por mês** (dias 1 e 15, ou próximo dia útil) — "Datas de Corte".
- O Servicer envia relatório de fechamento em até 3 dias úteis de cada Data de Corte.
- O VMD é pago na **Data de Pagamento semestral** subsequente (sem multa de pré-pagamento), respeitando o percentual mínimo de amortização ordinária do semestre (ver Saldo Devedor Máximo abaixo).
- O que sobra do preço de venda além do VMD volta pra Hotel Vogue (conta corrente própria), desde que não haja inadimplência.
- Distrato/rescisão de venda: responsabilidade de devolução é só da Devedora, não da Securitizadora.

### Saldo Devedor Máximo — verificação semestral (Anexo I do 3º Aditamento ao TS)

| Data | Saldo Devedor Máximo | Taxa de amortização acumulada |
|---|---|---|
| 21/12/2025 | R$ 38.614.905,63 | 5,00% |
| 21/06/2026 | R$ 35.566.360,45 | 12,50% |
| 21/12/2026 | R$ 32.517.815,27 | 20,00% |
| 21/06/2027 | R$ 28.453.088,36 | 30,00% |
| 21/12/2027 | R$ 24.388.361,45 | 40,00% |
| 21/06/2028 | R$ 19.307.452,82 | 52,50% |
| 21/12/2028 | R$ 14.226.544,18 | 65,00% |
| 21/06/2029 | R$ 7.113.272,09 | 82,50% |
| 21/12/2029 | R$ 0,00 | 100,00% |

*Confirmado batendo com o dado financeiro: amortização acumulada de R$ 19,4MM (R$5,7MM principal + R$13,7MM correção monetária) já atende ao saldo devedor máximo de jun/27 (R$28,5MM).*

### Fundo de Reserva

Hoje "**6 PMTs desde o aditamento**" (TS 6.7) — mínimo R$ 1.413.153,15, atual R$ 2.250.908,89 (bem acima do mínimo). Note que isso é o **dobro** do padrão de 3 PMTs visto em Jardins/Itaim — provavelmente reforçado como parte da repactuação da RJ (não confirmado o texto exato da cláusula 6.7 nesta rodada, dado que a CCB tem OCR de baixa qualidade).

### Fluxo Mínimo da Conta Vinculada

Covenant **mensal** (não semestral) — mínimo 1,3x, atual 4,58x, verificado via relatório solicitado no começo de cada mês (documento: "1º aditamento" à Cessão Fiduciária de Conta Vinculada). Foi justamente o descumprimento desse fluxo (out-nov/2025) que motivou parte do waiver da ata de 08/04/2026 (ver obrigações abaixo).

### "IC Gerencial" — acompanhamento informal do hotel

Existe um índice de cobertura "gerencial" (Contrato de Cessão 4.1), atual 1,05x, **sem mínimo exigido formalmente** (`exigido: "-"`) — é o acompanhamento residual da performance do hotel que você mencionou ("de forma gerencial ainda olhamos a performance"), não um covenant com consequência contratual — o foco de fato hoje é o estoque.

## Instrumentos (resumo — ver `documents_meta.json` pra desambiguação completa)

8 instrumentos originais (20/12/2019) + 1 descoberto por referência cruzada (nunca localizado na pasta): TS, Escritura de CCI, 2 cadeias distintas de Cessão Fiduciária (Direitos Creditórios vs. Conta Vinculada — **atenção, não são duplicatas**, ver nota do `documents_meta.json`), Cessão de Crédito, AF de Imóveis, AF de Quotas, CCB (2 vias físicas), e a Cessão Fiduciária de Recebíveis Venda/Exploração (criada em 26/02/2025, ainda sem instrumento próprio identificado na pasta com esse nome exato).

**Documentos da rodada de reestruturação (26/02/2025)** presentes na pasta: 3º Aditamento ao TS, 3º Aditamento à CCB, 3º Aditamento à Cessão de Créditos, 2º/3º Aditamentos às 2 cadeias de Cessão Fiduciária, 3º Aditamento à AF de Quotas.

## Vencimento Antecipado — lista de eventos (CCB Cláusula Nona, "não automático" salvo indicação)

A CCB (item 9.1) prevê que a dívida pode ser declarada antecipadamente vencida na ocorrência de qualquer um de ~36 eventos (itens a-jj — ver ressalva sobre OCR no cabeçalho deste arquivo). Não confirmamos, pelo trecho lido, se há distinção formal entre eventos "automáticos" e "não automáticos" (como em outras operações da casa) — o texto trata a lista de forma unificada. Principais grupos de eventos identificados:

- **Inadimplemento pecuniário** da Emitente/Avalista em qualquer obrigação da CCB ou demais Documentos da Operação, não sanado em **1 Dia Útil**.
- **Inadimplemento não pecuniário**, não sanado em **15 dias** contados da comunicação da Securitizadora (exceto obrigações com prazo de cura próprio já estipulado).
- **Queda patrimonial do Avalista**: redução do patrimônio declarado no IRPF em mais de 30% frente ao IRPF-base de 2018.
- **Cessão das obrigações da CCB a terceiros** sem prévia anuência do Agente Fiduciário/Assembleia.
- **Redução de capital social da Emitente** sem anuência prévia dos Titulares de CRI, **ou** patrimônio líquido da Emissora (Habitasec) cair abaixo de R$ 50.000.000,00 sem anuência.
- Causas de vencimento antecipado dos **artigos 333 e 1.425 do Código Civil** (perda do benefício de prazo — insolvência, garantia deteriorada/diminuída, etc.).
- **Imóvel não mantido em bom estado** de conservação/segurança/habitabilidade, ou obras de demolição/alteração/acréscimo que reduzam a área bruta locável, sem consentimento prévio dos titulares de CRI.
- **Declarações/garantias incorretas** da Emitente e/ou do Avalista (aparece 2x na lista, itens h/w).
- **Endividamento financeiro cruzado (cross default) contraído pela própria Hotel Vogue** — empréstimos, financiamentos, leasing, avais/fianças a terceiros, títulos de renda fixa — acima de limites agregados (referências a R$5.000.000,00 e R$1.000.000,00, atualizados anualmente pelo IPCA; valores exatos truncados no OCR).
- **Cancelamento/suspensão/não renovação de licenças ou autorizações** (inclusive ambientais) que impactem as atividades da Emitente ou a ocupação regular do Imóvel — dois itens distintos na lista (k e ff) tratam disso.
- **Falta de registro das Garantias Reais** (inclusive as decorrentes de aditamentos) nos prazos contratuais.
- **Descumprimento de Leis Anticorrupção** (Lei 12.846/2013, UK Bribery Act, US FCPA).
- **Descumprimento de legislação ambiental/trabalhista/previdenciária**, incluindo uso de mão de obra em condições análogas à escravidão ou trabalho infantil.
- **Alteração do objeto social** da Emitente sem anuência prévia.
- **Mudança de controle societário** da Emitente.
- **Questionamento judicial da própria CCB/Documentos da Operação** pela Emitente e/ou seus controladores.
- **Liquidação, dissolução, falência, autofalência ou pedido de RJ/recuperação extrajudicial** da Emitente e/ou de suas controladas/controladoras.
- **Pagamento de dividendos/JCP** acima do mínimo obrigatório (art. 202 da Lei das S.A.) enquanto a Emitente estiver inadimplente com qualquer obrigação da CCB.
- **Constituição de ônus** sobre os bens objeto da Cessão Fiduciária de Direitos Creditórios, AF de Imóvel ou AF de Quotas, fora dos ônus já constituídos em favor da própria operação.
- **Invalidade/nulidade/rescisão/ineficácia** de qualquer Contrato de Garantia ou da própria CCB.
- **Hotel Vogue assumir/garantir dívida de terceiros** fora do âmbito desta CCB.
- **Falecimento do Avalista** — não é vencimento automático: abre prazo de 20 dias para a Emitente apresentar garantia substituta ao Aval, com decisão sobre decretar ou não o vencimento antecipado tomada em Assembleia Geral de Titulares de CRI.
- **Protesto de títulos** contra Emitente/Avalista/Hotel Vogue acima de R$ 5.000.000,00 (individual ou agregado), salvo elidido/sanado no prazo de cura.
- **Descumprimento de decisão judicial transitada em julgado ou sentença arbitral definitiva** acima de limites por parte (R$5MM Emitente, R$5MM Avalista, R$1MM Hotel Vogue, atualizados anualmente pelo IPCA).
- **Impedimento de operar qualquer área do Imóvel** por falta/irregularidade de licença, não sanado em 30 dias.
- **Imissão provisória de ente expropriante** na posse do Imóvel (desapropriação em curso).
- **Não atendimento do ICSD mínimo de 1,30x, apurado mensalmente** a partir da liberação da 4ª parcela de desembolso da CCB, calculado como `ICSD = Recebimentos (Conta Centralizadora) / Juros` — **este é o mesmo mecanismo/fórmula já documentado como "Fluxo Mínimo da Conta Vinculada"** na seção de metodologias acima (mínimo 1,3x, verificação mensal); a leitura da CCB confirma que se trata de um **Evento de Vencimento Antecipado formal**, não apenas um covenant informal — reforça a gravidade do descumprimento ocorrido em out-nov/2025 (waivado na ata de 08/04/2026, ver abaixo).
- Descumprimento das obrigações de comprovação de destinação de recursos (ver "Prêmio Destinação" abaixo) não configura, pelo texto lido, vencimento antecipado automático — gera apenas a multa de 4%, salvo se a falta de comprovação persistir até 1 mês antes do vencimento/resgate (aí o Fundo de Prêmio é usado para compor a própria multa, TS 6.9.3.1(iii)).

**Não confirmamos, na leitura feita, que esta lista de ~36 eventos tenha sido alterada pelos aditamentos de 26/02/2025** — nem o 3º Aditamento à CCB nem o 3º Aditamento ao TS trazem redação nova para a Cláusula Nona da CCB; presumimos que a lista original de 2019 segue vigente em paralelo aos novos mecanismos de amortização por venda (VMD) e aos covenants específicos (Fluxo Mínimo, Fundo de Reserva) — mas vale confirmar com uma leitura completa e sem ruído de OCR da CCB, dado o histórico de reestruturação intenso desta operação.

## Prêmio Destinação — verificação semestral do uso dos recursos (TS Cláusula 6.9, incluída pelo 2º Aditamento de 08/09/2021)

Mecanismo separado do vencimento antecipado e da multa de resgate: a cada semestre, a Devedora deve comprovar ao Agente Fiduciário (Cronograma Físico-Financeiro, notas fiscais/XML, comprovantes de pagamento) a correta destinação dos recursos captados via CCB (Anexo VI). Se não comprovar:
- **Multa de 4%** sobre o valor dos recursos cuja destinação não foi comprovada no período ("Prêmio Destinação"), paga em até 5 Dias Úteis da manifestação do Agente Fiduciário.
- O pagamento do Prêmio Destinação **exime integralmente** a Devedora de responsabilidade por eventual prejuízo fiscal dos titulares de CRI decorrente da descaracterização da natureza imobiliária da operação (mas não exime de outros encargos, como IOF).
- Os recursos do Prêmio Destinação formam um **Fundo de Prêmio** na Conta do Patrimônio Separado, usado para: (i) devolução à Devedora se a destinação for comprovada depois; (ii) amortização da operação no vencimento, se comprovada no último semestre; ou (iii) composição do próprio Prêmio Destinação, se a pendência persistir até 1 mês antes do vencimento/resgate.
- Não identificamos, nos documentos lidos, se este mecanismo segue relevante hoje (a obra já foi concluída há anos) — pode já estar "dormente" (destinação de recursos 100% comprovada há tempo), mas não há confirmação explícita disso na pasta.

## Obrigações da operação

### Da Emitente/Devedora (Calçada) — CCB Cláusula 4.1.1

Disponibilizar à Securitizadora: (i) demonstrações financeiras consolidadas auditadas em até 5 meses do fim do exercício social; (ii) balancetes trimestrais da Emitente e da Hotel Vogue em até 45 dias do fim do trimestre; (iii) cópia de atas societárias relevantes em até 10 dias úteis; (iv) comunicação de qualquer inadimplemento ou Evento de Vencimento Antecipado em até 5 dias úteis do conhecimento; (v) cópia de notificações judiciais/extrajudiciais recebidas, em até 5 dias úteis; (vi) informações/documentos solicitados pela Securitizadora em até 10 dias; (vii) IRPF anual do Avalista em até 4 meses do fim do exercício. Além disso: cumprir legislação ambiental/trabalhista/anticorrupção; manter licenças e alvarás válidos; manter seguro do Imóvel (mínimo R$ 108.000.000,00 de cobertura, atualizado pelo IPCA, endossado à Securitizadora em até 30 dias da emissão), com renovação comprovada 30 dias antes do vencimento da apólice — sob pena de vencimento antecipado se a Emitente receber indevidamente indenização de seguro e não repassar em 2 dias úteis; atualizar o laudo de avaliação do Imóvel em até 6 meses da emissão; contratar/manter Securitizadora, Agente Fiduciário e Auditor Independente; recolher tributos da CCB; notificar convocação de Assembleias em até 2 dias úteis; cumprir leis e regulamentos aplicáveis (Lei das S.A., Instruções CVM 414/476); dar publicidade às informações econômico-financeiras; destinar os recursos captados conforme o Anexo II (ver "Prêmio Destinação" acima); manter contabilidade atualizada; contestar judicialmente qualquer ação que vise invalidar a CCB/Documentos da Operação; enviar demonstrativo semestral de despesas de condomínio/IPTU/foro do Imóvel (até o 5º Dia Útil de cada semestre); enviar **Relatório Mensal** com informações do hotel/recebimentos (Anexo VIII da CCB) — a Securitizadora pode repassar esse relatório aos titulares de CRI e pedir esclarecimentos complementares em até 5 dias úteis.

### Do Avalista — CCB Cláusula 4.1.2

Manter endereço atualizado junto à Financiadora; informar descumprimento de suas próprias obrigações em até 2 dias úteis do conhecimento; comunicar eventos que possam afetar de forma relevante o cumprimento das obrigações da CCB, em até 2 dias úteis.

### Última ata — waivers concedidos e pendências

**Ata mais recente**: AGT 08/04/2026 ("Repactuação, condomínio residencial") — waivers + conversão pra apartamentos (ver seção de reestruturação). Itens de waiver aprovados nesta ata:
- Não decretação de vencimento antecipado por descumprimento do **Fluxo Mínimo da Conta Vinculada** (ICSD < 1,30x, out-nov/2025) — confirma-se, pela leitura da CCB acima, que este era de fato um Evento de Vencimento Antecipado formal (item "jj"), não um covenant informal.
- Não decretação de vencimento antecipado por descumprimento do **Valor Mínimo do Fundo de Reserva** em agosto/2025 (reenquadrado em setembro/2025).
- Liberação de R$ 1.172.611,12 retidos na Conta Centralizadora.

**⚠️ Obrigação em aberto e JÁ VENCIDA**: aditamento ao Contrato de Cessão Fiduciária de Conta Vinculada (pra ampliar seu objeto aos recebíveis da exploração hoteleira dos Apartamentos) — prazo de 30 dias da ata (venceu **08/05/2026**). Só existe uma **minuta não assinada** na pasta (`3 Aditamento CF Conta Vinculada CRI Calçada - ELA Adv 29 04 2026.docx` — rascunho de advogado, sem nenhum campo preenchido nem assinatura digital). **Vencida há mais de 4 meses sem confirmação de cumprimento** (hoje: 18/09/2026). Vale confirmar com a Securitizadora/Devedora o status real disso.

**Obrigação condicionada, sem prazo fixo ainda**: aditamento à Alienação Fiduciária de Imóvel (pra migrar a garantia das Frações de Tempo pros novos Apartamentos) — prazo de 30 dias a partir da conclusão das aprovações municipais/condominiais (item vi da ata), que ainda não foi confirmada como concluída.

## Pontos de atenção / riscos

1. **Obrigação vencida sem cumprimento confirmado** (aditamento à CF Conta Vinculada, ver acima) — é o ponto mais crítico em aberto agora.
2. **Toda a cadeia de conversão hotel→residencial ainda está em andamento** — múltiplas condições em sequência (aprovação municipal, assembleia de condomínio, aditamento de AF, registros cartoriais) precisam se concluir antes da estrutura de venda ficar 100% "limpa" nos novos Apartamentos.
3. **Só 179 das 222 unidades do hotel são garantia desta operação** — cuidado ao ler qualquer dado de "estoque do empreendimento" pra não misturar com as unidades da Pontual (fora da operação).
4. **Fundo de Reserva em 6 PMTs** (o dobro do padrão visto em outras operações) — a leitura do **TS original** (Cláusula 6.7) mostra uma mecânica em camadas que ajuda a explicar isso, mas não fecha 100%: Valor Inicial = **12 PMT**; cláusula 6.7.1 prevê queda para **3 PMT assim que o Contrato de Cessão Fiduciária de Direitos Creditórios for aditado** (o que aconteceu já em 24/06/2020, 1º Aditamento, ausente da pasta); paralelamente, a cláusula 6.7.2/6.7.2.1 prevê uma via **independente** baseada no índice CCF (Recebimentos/Juros dos Créditos Cedidos): CCF ≥ 100% → reduz para **6 PMT**; CCF ≥ 130% → reduz para **3 PMT**. As duas vias (6.7.1 "automática" após o 1º Aditamento, e 6.7.2 "condicionada ao desempenho") parecem redundantes/conflitantes no texto original (ambas mirando patamares de 3-6 PMT) — não é possível confirmar, sem o 1º Aditamento (ausente) e sem uma leitura limpa da CCB atual (OCR ruim), qual das duas vias explica o patamar de 6 PMT hoje vigente, nem se algum aditamento posterior (2021 ou 2025) alterou a cláusula 6.7 novamente.
5. **Lista de ~36 eventos de Vencimento Antecipado (CCB Cláusula Nona) não foi confirmada como atualizada pelos aditamentos de 2025** — nem o 3º Aditamento à CCB nem ao TS trazem redação nova para essa cláusula; presume-se que a lista original de 2019 segue valendo, mas o texto-fonte tem OCR de baixa qualidade (ver ressalva no cabeçalho) — vale uma leitura limpa (ex.: reprocessar o PDF com melhor OCR, ou obter a CCB em Word) antes de usar a lista de eventos para qualquer decisão formal.
6. Recuperação Judicial da Devedora segue em curso — mudanças no processo de RJ podem gerar novos eventos relevantes pra esta operação além dos já mapeados aqui.
