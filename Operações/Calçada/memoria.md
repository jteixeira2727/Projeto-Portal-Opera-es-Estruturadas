# Calçada — Memória da Operação

> Leitura derivada de `Pipeline/documents_meta.json`, `Pipeline/obligations_data.json`, `Pipeline/portfolio_data_wrapped.json` e leitura direta da ata mais recente (AGT 08/04/2026) e do 3º Aditamento ao TS (26/02/2025). Não é fonte de dados para o `build_data.py` — é um resumo pra revisão humana. O `documents_meta.json` já tem uma `metodologia_nota` bem detalhada sobre os 9 instrumentos e suas desambiguações (2 cadeias de Cessão Fiduciária quase homônimas, CCB com 2 vias físicas etc.) — este arquivo foca no contexto de negócio/reestruturação e nas metodologias de cálculo, complementando aquela nota, não substituindo.
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

## Obrigações / última ata

**Ata mais recente**: AGT 08/04/2026 ("Repactuação, condomínio residencial") — waivers + conversão pra apartamentos (ver seção de reestruturação). Itens de waiver aprovados nesta ata:
- Não decretação de vencimento antecipado por descumprimento do **Fluxo Mínimo da Conta Vinculada** (out-nov/2025).
- Não decretação de vencimento antecipado por descumprimento do **Valor Mínimo do Fundo de Reserva** em agosto/2025 (reenquadrado em setembro/2025).
- Liberação de R$ 1.172.611,12 retidos na Conta Centralizadora.

**⚠️ Obrigação em aberto e JÁ VENCIDA**: aditamento ao Contrato de Cessão Fiduciária de Conta Vinculada (pra ampliar seu objeto aos recebíveis da exploração hoteleira dos Apartamentos) — prazo de 30 dias da ata (venceu **08/05/2026**). Só existe uma **minuta não assinada** na pasta (`3 Aditamento CF Conta Vinculada CRI Calçada - ELA Adv 29 04 2026.docx` — rascunho de advogado, sem nenhum campo preenchido nem assinatura digital). **Vencida há mais de 4 meses sem confirmação de cumprimento** (hoje: 18/09/2026). Vale confirmar com a Securitizadora/Devedora o status real disso.

**Obrigação condicionada, sem prazo fixo ainda**: aditamento à Alienação Fiduciária de Imóvel (pra migrar a garantia das Frações de Tempo pros novos Apartamentos) — prazo de 30 dias a partir da conclusão das aprovações municipais/condominiais (item vi da ata), que ainda não foi confirmada como concluída.

## Pontos de atenção / riscos

1. **Obrigação vencida sem cumprimento confirmado** (aditamento à CF Conta Vinculada, ver acima) — é o ponto mais crítico em aberto agora.
2. **Toda a cadeia de conversão hotel→residencial ainda está em andamento** — múltiplas condições em sequência (aprovação municipal, assembleia de condomínio, aditamento de AF, registros cartoriais) precisam se concluir antes da estrutura de venda ficar 100% "limpa" nos novos Apartamentos.
3. **Só 179 das 222 unidades do hotel são garantia desta operação** — cuidado ao ler qualquer dado de "estoque do empreendimento" pra não misturar com as unidades da Pontual (fora da operação).
4. **Fundo de Reserva em 6 PMTs** (o dobro do padrão visto em outras operações) — texto exato da cláusula 6.7 do TS não confirmado nesta rodada (CCB tem OCR de baixa qualidade, difícil de ler com precisão).
5. Recuperação Judicial da Devedora segue em curso — mudanças no processo de RJ podem gerar novos eventos relevantes pra esta operação além dos já mapeados aqui.
