# Pirelli — Memória da Operação

> Leitura derivada de `Pipeline/portfolio_data_wrapped.json` e leitura direta (via extração PyMuPDF, já que a máquina local não tinha poppler/pdftoppm para o Read padrão) dos 10 documentos da pasta, todos com camada de texto nativa — sem necessidade de OCR: Termo de Securitização original (07/12/2023) + 1º, 4º e 5º Aditamentos, Contrato de AF do DRS (e sua cópia idêntica), Escritura de Emissão de CCI, Instrumento de Cessão de Créditos Imobiliários, e as 2 atas de assembleia da operação (09/05/2025 e 13/05/2025).
>
> Última atualização: 2026-09-18.

## Resumo

- **CRI**: 1ª e 2ª séries da **69ª Emissão**, **Canal Companhia de Securitização**, lastreados em CCI fracionária (Vórtx, Instituição Custodiante) representativa de Créditos Imobiliários cedidos pela **TZI Citrino Empreendimentos Imobiliários Ltda.** ("Cedente"/"Locadora", a real SPE devedora — não confundir com a "Pirelli" do nome da operação, que é a locatária). Agente Fiduciário: **Oliveira Trust DTVM**.
- Taxa: **IPCA + 8,00% a.a.**, capitalizados diariamente. Vencimento final: **10/09/2039** (5.751 dias corridos de 12/12/2023). Volume total da emissão, após o 5º Aditamento (mai/2025): **R$ 184.885.000,00** — a 1ª série (R$ 170.748.000,00) veio na emissão original (07/12/2023); a **2ª série** (até R$ 14.137.000,00, incl. Lote Adicional) foi criada em jan/2025, pari passu com a 1ª, sem subordinação.
- Prêmio de recompra facultativa (resgate antecipado): 0,5% × Duration — bate com o campo "Multa" do pipeline.
- Saldo devedor (jul/26, pipeline): R$ 211,7 milhões. Duration: 5,51 anos.
- **Não existe cláusula de "vencimento antecipado do CRI" nem de "LTV"** nesta operação — o mecanismo equivalente é a **Recompra Compulsória dos Créditos Imobiliários pela Cedente** (Contrato de Cessão, cláusula 7.1), com uma lista fechada de ~20 eventos-gatilho.

## Estruturação — BTS Pirelli sobre Direito Real de Superfície (DRS)

Operação de renda logística que nasceu para financiar um contrato **BTS (built-to-suit)** com a Pirelli e migrou para um play de renda pura após a conclusão da obra, com o aluguel da Pirelli pagando o serviço da dívida. A particularidade estrutural central:

- A **Pirelli Pneus Ltda.** (CNPJ 59.179.838/0001-37) é proprietária da Gleba em Campinas/SP (matrícula 141.304, 3º RGI) onde também fica sua fábrica. Sobre a parte remanescente do terreno ("Terreno"), a Pirelli **constituiu Direito Real de Superfície (DRS) em favor da TZI Citrino** — é sobre esse DRS, e não sobre a propriedade plena, que a TZI Citrino construiu o galpão BTS (55.802 m² ABL) e loca de volta à própria Pirelli.
- **Prazo do DRS: 195 meses contados de 07/12/2023** (~vence em torno de mar/2040) — **não é exatamente igual ao prazo da dívida** (vencimento final do CRI: 10/09/2039), mas ligeiramente mais longo, com ~5-6 meses de margem de segurança proposital para permitir a execução da garantia sem risco de o direito real expirar antes.
- **Período de Locação**: 15 anos (180 meses) a partir do Termo de Imissão na Posse; os Créditos Imobiliários cedidos cobrem os primeiros **174 meses** (excluem-se os últimos 6 meses da locação).
- A Pirelli pode, a seu critério, desmembrar a matrícula do Terreno ("Individualização da Matrícula") — pré-condição para a eventual constituição da AF do Solo (ver garantias).
- **Origem da 2ª série**: criada em jan/2025 para captar recurso adicional, lastreado no aumento do Aluguel Mensal Líquido (para R$ 1.930.573,97, base 01/06/2023) decorrente do 2º aditamento ao Contrato de Locação/BTS (20/03/2025) — presumivelmente refletindo custo de obra maior ou escopo adicional do galpão.

## Metodologia de valoração da garantia — atenção: divergência entre o valor pactuado e o valor de acompanhamento

Ponto importante identificado na leitura, que **difere do que está pactuado contratualmente**, mas que é a metodologia usada pelo time para acompanhamento do valor do ativo e que deve seguir sendo usada:

- **Metodologia de acompanhamento (usar esta)**: o valor da garantia é calculado **trazendo o contrato de locação a valor presente pela taxa do CRI ao mês**, aplicada sobre os meses restantes de locação e o valor do aluguel (base e corrigido). No pipeline (jul/26): aluguel base (mai/23) R$ 1.930.573,97, aluguel corrigido (mar/26) R$ 2.169.486,14, 174 meses de locação, taxa de desconto (CRI) a.m. de 0,6434% → **Valor de Avaliação (DCF do BTS): R$ 226.723.124,74** — este é o valor correto/atualizado a usar (substitui o "Valor de Avaliação CapRate" de R$ 215.236.285,71, que é o número antigo/desatualizado, calculado por cap rate de mercado 7% e não pela metodologia de VP da locação).
- **Atenção operacional**: no fluxo mensal do pipeline (`Pipeline/portfolio_data_wrapped.json`, série `fluxo`), o LTV está sendo calculado usando o valor de avaliação por **CapRate fixo** (R$ 215.236.285,71) em **todos os meses**, e não o valor por DCF — vale corrigir isso na próxima atualização do pipeline para refletir a metodologia correta (VP da locação).
- **Metodologia contratual efetivamente pactuada (diferente, achado da leitura)**: nenhum dos 10 documentos lidos (nem o Termo de Securitização, nem o Contrato de AF do DRS) menciona "LTV", "valor presente" ou "fluxo de caixa descontado" como método de avaliação da garantia. A Cláusula 5 do Contrato de AF do DRS fixa o valor do Direito Real de Superfície com base no **valor venal do terreno** (Anexo II) — **R$ 85.361.473,80** na origem, contra um saldo devedor então de R$ 170.748.000,00 (ou seja, cobria só ~50% da dívida). A cláusula 5.5 dispensa expressamente qualquer reavaliação periódica obrigatória. O próprio Agente Fiduciário registrou por escrito no Termo de Securitização (cláusula 10.2(i)) que **a garantia da AF do DRS era insuficiente em relação ao saldo devedor** na data de assinatura, justificado pelo fato de que as demais garantias (AF do Solo, Fiança Bancária) ainda não estavam constituídas naquele momento. Não há confirmação, nos documentos lidos, de que essa insuficiência tenha sido formalmente sanada depois.
- Ou seja: o valor de R$ 226,7 mi usado para acompanhamento é uma métrica de gestão de portfólio (racional: valorar um ativo com prazo de "validade" pelo fluxo de caixa que ele efetivamente gera, descontado pela taxa da própria dívida), não o valor formal da garantia registrada em cartório/contrato — que é mais conservador. Vale ter isso em mente em qualquer discussão de suficiência de garantia com o Agente Fiduciário/Securitizadora, que provavelmente ainda opera com base no valor venal registrado no instrumento de AF do DRS.

## Garantias — detalhamento completo

1. **AF do DRS** (Alienação Fiduciária do Direito Real de Superfície) — a TZI Citrino ("Fiduciante") aliena fiduciariamente à Canal ("Fiduciária") o Direito Real de Superfície que detém sobre o Terreno (a Pirelli, dona do solo, não é parte fiduciante desta garantia). Regida pela Lei 9.514/97. **Limitada ao prazo do próprio DRS** (195 meses) — a garantia se extingue junto com o direito real.
2. **AF do Solo e da Propriedade Plena Superveniente** (condicional/eventual) — a ser constituída pela própria **Pirelli** (não pela TZI Citrino), a critério dela, apenas se/quando ocorrer a Individualização da Matrícula. Garante especificamente a Indenização por Rescisão Antecipada devida pela Pirelli, não o CRI como um todo. **Não constituída na data de assinatura do TS**; não há confirmação nos documentos lidos de que tenha sido celebrada depois — checar status atual.
3. **Fiança Bancária** — contratada pela Pirelli, valor mínimo inicial R$ 50.000.000,00, com fórmula de ajuste mensal (9,5% a.a. + IPCA − aluguel do mês). Pode cair a 25% do valor se a AF do Solo for constituída com seguros específicos, ou ser dispensada se a controladora italiana **Pirelli Tyre S.p.A.** prestar fiança solidária equivalente. Status atual não confirmado nos documentos lidos.
4. **Fundo de Despesas** — retenção inicial de R$ 1.534.100,00 do Preço de Cessão; Valor Mínimo R$ 200.000,00; verificação mensal.
5. **Fundo de Obras** — valor líquido retido do Preço de Cessão para custear a construção, liberado conforme Relatórios de Medição; após o 5º Aditamento, ganhou liberações adicionais específicas para a 2ª série.
6. **Fundo de Reserva** — ver seção dedicada abaixo.
7. **Seguros** — Patrimonial (cosseguro Pirelli/Locadora/Securitizadora até a AF do Solo ser constituída), Fiança Locatícia e Perda de Receita de Aluguéis (18 meses de cobertura, condicionados à AF do Solo).
8. **Performance Bond** — contratado pela Construtora durante a obra (20% do custo de construção, Securitizadora como beneficiária única); relevante só durante o Período de Obras, hoje presumivelmente sem função (obra concluída) — sem termo de baixa formal identificado nos documentos.

## Fundo de Reserva (Cláusula 7.7 do Termo de Securitização) — acompanhamento mensal confirmado

- Constituído com Valor Inicial de R$ 360.000,00, retido do Preço de Cessão.
- **Valor Mínimo**: 2x o Aluguel Mensal nos primeiros 18 meses após o Termo de Imissão na Posse; **1x o Aluguel Mensal depois disso**, até a liquidação integral das Obrigações Garantidas.
- **Verificação mensal** pela Securitizadora, a partir da data do Termo de Imissão na Posse — confirma o acompanhamento mensal mencionado pelo usuário.
- Recomposição: prioritariamente com recursos dos Créditos Imobiliários; se insuficiente, aporte direto da Cedente em até 5 dias úteis, sob pena de configurar Evento de Recompra Compulsória.
- Atual (pipeline, jul/26): exigido R$ 4.285.343,78, atual R$ 4.679.180,00 — enquadrado.

## Demais obrigações

- **Relatório Mensal** da Emissora (art. 47, III da Res. CVM 60) — Fundos.NET + envio ao Agente Fiduciário em até 30 dias do encerramento do mês.
- **Relatório Anual** — organograma, dados financeiros, atos societários (Res. CVM 17), até 90 dias antes do prazo de disponibilização na CVM.
- Demonstrações financeiras anuais auditadas da Emissora, publicadas no site.
- Declaração anual da Cedente atestando a inocorrência de Eventos de Recompra Compulsória.
- Comunicação de fatos relevantes, eventos de antecipação de pagamento, substituição de auditores etc.

## Histórico de aditamentos e atas

1. **07/12/2023** — Termo de Securitização original (1ª série), Contrato de Cessão, AF do DRS, Escritura de Emissão de CCI.
2. **12/12/2023** — 1º Aditamento: ajustes de definições/endereço da Securitizadora, sem alteração econômica (CRI ainda não integralizados, dispensada AGT).
3. **07/06/2024** — 2º Aditamento (não lido diretamente, só referenciado): alterou a definição de "Prazo de Colocação" e cláusulas 3.5.2/4.1.
4. **02/01/2025** — Aditamento que criou a **2ª série** de CRI, compartilhando o mesmo lastro/Patrimônio Separado/Garantias da 1ª série, sem subordinação. Rotulado por erro material como "Segundo Aditamento", quando cronologicamente era o terceiro.
5. **10/01/2025 (assinado 13/01/2025)** — **4º Aditamento**: puramente correcional — retifica o erro de nomenclatura do aditamento anterior (passa a ser oficialmente "Terceiro Aditamento") e corrige a descrição da Securitizadora ("Companhia Aberta" → "Securitizadora S1"). Sem efeito econômico.
6. **09/05/2025** — **AGT**: pauta para aprovar (i) Modificação da Oferta da 2ª Série para permitir Lote Adicional de até R$ 5.000.000 (teto subindo a até R$ 14.386.000), lastreado no aumento do Aluguel Mensal Líquido decorrente do 2º aditamento ao Contrato de Locação/BTS (20/03/2025); (ii) alteração dos Documentos da Operação correspondentes; (iii) autorização de atos. Com 32,32% dos CRI em circulação presentes, **todos os itens foram aprovados apenas para suspensão**, com reabertura marcada para 12/05/2025 — adiamento procedimental, não rejeição.
7. **13/05/2025** — **AGT reaberta**: mesma pauta, mesmo quórum (32,32%), **aprovação unânime**, sem contrários/abstenções. Valor final do Lote Adicional ajustado para **R$ 4.751.000,00** (teto final da 2ª série: R$ 14.137.000,00).
8. **14/05/2025** — **5º Aditamento**, assinado no dia seguinte à AGT, formaliza exatamente a deliberação de 13/05/2025: incorpora a Modificação da Oferta (Lote Adicional R$ 4.751.000,00), atualiza definições dos Documentos da Operação, eleva o "Valor dos Créditos Imobiliários" para R$ 341.957.490,11, mantém o "Preço de Cessão" em R$ 184.885.000,00, insere a Cláusula 3.9 ("Lote Adicional") e ajusta a liberação do Fundo de Obras da 2ª série.

## Pontos de atenção / riscos

1. **Metodologia de valoração da garantia usada para acompanhamento (VP da locação, R$ 226,7 mi) diverge da metodologia formalmente pactuada no Contrato de AF do DRS (valor venal do terreno, R$ 85,4 mi na origem)** — ver seção dedicada acima. O time optou por manter a metodologia de VP da locação para fins de gestão do portfólio; vale ter isso em mente ao discutir suficiência de garantia com o Agente Fiduciário.
2. **AF do DRS declaradamente insuficiente na origem** (R$ 85,4 mi vs. R$ 170,7 mi de saldo devedor então) — reconhecido por escrito pelo próprio Agente Fiduciário no Termo de Securitização. Sem confirmação de que essa insuficiência tenha sido sanada depois (ex.: novo laudo, reforço de garantia).
3. **AF do Solo e da Propriedade Plena Superveniente**: sem confirmação de que tenha sido constituída até hoje — se nunca foi, a operação depende ainda mais da Fiança Bancária e da AF do DRS como garantias reais efetivas.
4. **Fiança Bancária e Performance Bond**: status atual (valor vigente, se já reduzida/dispensada, se já baixada) não confirmado nos documentos lidos.
5. **Pipeline calcula LTV com o valor de avaliação antigo (CapRate, R$ 215,2 mi fixo)** em vez do valor de VP da locação (R$ 226,7 mi) — vale corrigir na próxima atualização do pipeline.
6. **Prazo do DRS (195 meses / ~mar-2040) é ligeiramente mais longo que o vencimento do CRI (10/09/2039)**, não idêntico — margem de segurança proposital, não coincidência.
7. **Documentos citados mas não presentes nesta pasta**: a própria Escritura de Constituição do DRS, o Contrato de Locação/BTS original e seus aditamentos (1º e 2º), o eventual laudo de avaliação que fundamente os R$ 226,7 mi / R$ 215,2 mi do pipeline, e o eventual Contrato de AF do Solo (se já celebrado) — relevantes para fechar as lacunas acima, se precisar de uma análise mais completa.
