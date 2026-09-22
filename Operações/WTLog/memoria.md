# WT Log — Memória da Operação

> Leitura derivada de `Pipeline/documents_meta.json`, `Pipeline/obligations_data.json`, `Pipeline/portfolio_data_wrapped.json` e leitura direta de todos os 9 documentos da pasta (todos com camada de texto — sem necessidade de OCR): Termo de Securitização (com o 1º Aditamento), Termo de Emissão de Notas Comerciais, Escritura de CCI, AF de Imóveis, AF de Quotas, e as 3 atas de assembleia da operação (02/05/2023, 30/04/2026 e 09/06/2026).
>
> Última atualização: 2026-09-18.

## Resumo

- **CRI**: 27ª Emissão, série única, **Canal Companhia de Securitização** — lastreado em CCI representativa de Créditos Imobiliários oriundos das **Notas Comerciais Escriturais** emitidas pela **FDR Independência Desenvolvimento Imobiliário Ltda.** ("Emissora" no Termo de Emissão / "Devedora" no Termo de Securitização).
- Emitido em 06/01/2023: R$ 30 milhões. Remuneração **IPCA (M-2) + 8,14% a.a.**, com amortização e juros mensais. Vencimento final: 18/12/2035. Agente Fiduciário: Vórtx.
- Saldo devedor atual (jul/26): R$ 27,9 milhões. Duration: 3,75 anos. LTV atual: 25,2%. IC atual: 1,76x.

## Estruturação — renda logística sobre uma fração ideal (25%) de 2 galpões

Deal de renda com uma particularidade importante: a Devedora **não é dona integral do ativo-garantia**. Ela detém apenas a **fração ideal de 25%** de 2 galpões logísticos do **Condomínio WT Log RBR Franco da Rocha** (Rod. Pres. Tancredo de Almeida Neves, Km 45, Franco da Rocha/SP) — Subcondomínio A (Galpão 100, matrícula 95.140) e Subcondomínio B (Galpão 200, matrícula 95.141), classe AAA, entregues em 2021. Os outros 75% pertencem a um terceiro coproprietário fora da operação — o nome do condomínio ("RBR") e o campo "Preço Venda RBR (22,5%)" já cadastrado no pipeline sugerem que seja a gestora RBR, mas isso não está confirmado por nenhum documento desta pasta.

**Achado na cadeia de matrícula (AF de Imóveis, certidão cartorial)**: antes da estruturação do CRI, a FDR chegou a deter 75% do imóvel (com os outros 25% de outra empresa, "Imobiliária e Construtora Vista Alegre Ltda.") e havia uma Alienação Fiduciária anterior e não relacionada em favor da BRL Trust (já cancelada por quitação em 13/10/2022, antes da emissão). A FDR então vendeu a maior parte de sua posição, ficando com a fração de 25% que hoje lastreia esta operação — não é um dado novo para o covenant (o Termo de Securitização já define a Fração Ideal como 25% desde a emissão), mas explica a origem da posição minoritária.

**Garantias** (Cláusula 4.1 do Termo de Emissão / definição "Garantias" do Termo de Securitização):
1. **Alienação Fiduciária de Imóveis** — sobre a fração ideal de 25% da Devedora nos 2 imóveis.
2. **Alienação Fiduciária de Quotas** — sobre a **totalidade (100%) das quotas da FDR Independência**, tendo a **PMG Desenvolvimento Imobiliário** como fiduciante (é a sócia/controladora da Devedora).
3. **Cessão Fiduciária de Recebíveis** — sobre os recebíveis de locação (e eventual sobejo da excussão dos imóveis) da fração ideal da Devedora. **O contrato não está na pasta** (nem o original de 06/01/2023 nem eventuais aditamentos) — só é conhecido por citação nos outros instrumentos e na ata de 02/05/2023.
4. **Aval** — de 5 avalistas, todos do mesmo grupo econômico da Devedora (aval a título oneroso, conforme declarado no próprio Termo de Emissão): **PMG Investimentos** (Avalista 1), **PMG Desenvolvimento Imobiliário** (Avalista 2 — a mesma que dá a AF de Quotas), e as pessoas físicas **Paulo Eduardo Moreira Torre**, **Marina Moreira Torre Lobo** e **Giuliana Moreira Torre** (Avalistas 3 a 5 — parecem ser a família controladora do grupo PMG).
5. **Fundo de Reserva** — mínimo de **3 próximas parcelas de remuneração + amortização** das Notas Comerciais.
6. **Fundo de Despesas** — mínimo de **12 meses de despesas recorrentes** do CRI.

Não há cascata/waterfall sofisticada nem mecanismo de retenção em 2 camadas (diferente da BR Properties) — aqui o desenquadramento de LTV ou IC sem reforço de garantia é, ele mesmo, diretamente um **Evento de Vencimento Antecipado Não-Automático** (depende de assembleia para não ser decretado).

## Metodologias de cálculo confirmadas (Cláusula 7.2 do Termo de Securitização / 8.1 e 9.1 do Termo de Emissão)

### Atualização monetária, juros e amortização das Notas Comerciais (Cláusulas 6.8 a 7.2 do Termo de Emissão)

- **Atualização monetária**: o Valor Nominal Unitário (ou seu saldo) é atualizado **mensalmente pela variação acumulada positiva do IPCA**, pro rata Dias Úteis, a partir da primeira Data de Integralização dos CRI, incorporado automaticamente ao saldo (fórmula `Vna = Vne × C`, com `C` sendo o fator acumulado do IPCA "M-2", isto é, com defasagem de 2 meses — o índice usado é o do 2º mês imediatamente anterior). Se o número-índice do IPCA do mês ainda não estiver disponível, usa-se uma projeção da ANBIMA, sem compensação posterior quando o dado real sair.
- **Juros remuneratórios**: **8,14% a.a.**, base 252 Dias Úteis, capitalização **exponencial e cumulativa pro rata temporis** sobre o Valor Nominal Atualizado (fórmula `J = VNA × (Fator Juros − 1)`), apurados ao final de cada Período de Capitalização e pagos nas Datas de Pagamento do Anexo I (mensal, na prática).
- **Amortização do principal**: **mensal**, após um período de **carência de 12 meses** contado da Data de Emissão (06/01/2023) — ou seja, amortização só começou a correr a partir de jan/2024, conforme cronograma do Anexo I.
- **Resgate Antecipado Facultativo Total**: permitido a partir de **06/01/2025**, só integral (veda resgate parcial), mediante aviso com 10 dias úteis de antecedência. Valor = saldo + remuneração + **Prêmio de Resgate de 0,95% × duration remanescente** (é esse o "0,95% x duration remanescente" que aparece como "Multa" no dado financeiro do pipeline — na prática é o prêmio de pré-pagamento, não uma penalidade por inadimplência). **Não há amortização extraordinária facultativa** (só o resgate total, sem opção de amortizar parte do saldo antecipadamente).
- **Encargos moratórios** (em caso de atraso imputável à Emissora): multa de **2%** sobre o valor em atraso + juros de mora de **1% a.m.** pro rata, além das despesas de cobrança — cumulativos com a Remuneração normal, não substitutos.
- Notas Comerciais não são conversíveis em participação societária e não têm repactuação programada.

### LTV — Cláusula 7.2 (dd)

`LTV = saldo devedor das Notas Comerciais / (valor de avaliação dos Imóveis × Fração Ideal da Devedora)`, máximo **50%**, apurado **mensalmente** pela Emissora a partir de 17/01/2023 ("Data de Verificação", mesmo dia dos meses seguintes). Laudo de avaliação anual, por avaliador autorizado (lista fechada: Cushman & Wakefield, JLL, CBRE, Colliers ou Binswanger), entregue até 15/jan de cada ano, com base no encerramento do ano anterior.

Se desenquadrado **e** a Devedora não fizer reforço de garantia (Cláusula 7.3) → Evento de Vencimento Antecipado Não-Automático (vai a assembleia).

**Reforço de garantia (Cláusula 7.3)**: Devedora tem 15 dias úteis para apresentar Novos Ativos (livres de ônus, com laudo/DFs comprovando valor); Securitizadora convoca assembleia em até 5 du para aprovar; se aprovado, segue auditoria jurídica (30 dias corridos) e depois celebração + registro dos instrumentos (10 dias corridos em RTD, ou 45 dias corridos — prorrogável por mais 45 — em cartório de imóveis).

Atual (jul/26): **25,2%** (LTV) — bem enquadrado, folga grande frente ao limite de 50%.

### Índice de Cobertura (IC) — Cláusula 7.2 (ee)/(ff)

`IC = Fluxo de Recebíveis / Serviço Mensal`, mínimo **1,25x**, apurado **mensalmente** (mesma Data de Verificação do LTV, a partir de 17/01/2023).

- **Fluxo de Recebíveis** = valores depositados na Conta Centralizadora a título de locação dos Imóveis no mês, ajustados por um fator para representar exatamente a fração ideal de 25% da Devedora (a fórmula corrige tanto para o caso de o locatário depositar o valor total do aluguel do imóvel quanto o valor já proporcional à fração).
- **Serviço Mensal** = amortização + juros remuneratórios das Notas Comerciais devidos no mês.

Desenquadramento do IC (Cláusula 7.2 gg) só vira Evento de Vencimento se, além disso, não houver pagamento do "prêmio" do item (mm) da Cláusula 9.1 — ponto que não foi aprofundado nesta leitura (não achei o texto completo do item "mm").

Atual (jul/26): **1,76x** — enquadrado, folga confortável frente ao mínimo de 1,25x.

### Fundo de Reserva e Fundo de Despesas

Confirmados exatamente como o usuário descreveu: Fundo de Reserva = mínimo de **3 próximas PMTs** (remuneração + amortização); Fundo de Despesas = mínimo de **12 meses de despesas recorrentes** (Anexo II do Termo de Emissão). Ambos ficam retidos na Conta Centralizadora, sob o Regime Fiduciário (Cláusula 10.1 do TS, na redação dada pelo 1º Aditamento). O relatório mensal (ver abaixo) inclui expressamente o acompanhamento do valor mínimo de ambos os fundos (Cláusula 8.1.1 do TS) — confirma a verificação mensal mencionada pelo usuário. Valor mínimo atual do Fundo de Reserva no pipeline: R$ 1.308.813,86 (mínimo) vs. R$ 1.768.936,90 (atual) — enquadrado. Não há um card de Fundo de Despesas com valores no dado financeiro atual (mesma lacuna observada em outras operações do portfólio).

### Eventos de Vencimento Antecipado — panorama completo (Cláusula 8 do Termo de Emissão / 7.2 do Termo de Securitização)

**Estrutura importante**: o título da própria Cláusula 8 do Termo de Emissão é "**DO VENCIMENTO ANTECIPADO NÃO AUTOMÁTICO**" — não existe, em nenhum dos documentos da pasta, uma lista separada de eventos *automáticos*. Ou seja, **todo evento de vencimento antecipado desta operação passa pela Assembleia de Titulares de CRI antes de ser declarado** (Cláusula 7.2.1 do TS, já registrada acima): a Securitizadora convoca a assembleia em até 2 dias úteis da ciência do evento, e só declara o vencimento antecipado se a assembleia não aprovar a não decretação (por falta de quórum ou por decisão contrária) — é exatamente o mecanismo que gerou as 3 atas históricas da operação (ver seção seguinte).

A lista de eventos (Cláusula 8.1, itens "a" a "ii") é extensa (35 hipóteses); agrupando por tema:

- **Societário/controle da Emissora e/ou Avalistas**: falência/recuperação judicial/insolvência (a), mudança de objeto social (b), redução de capital social (c), cisão/fusão/incorporação/reorganização societária (e), mudança de controle direto ou indireto (f).
- **Descumprimento envolvendo as Garantias**: alienação/cessão dos bens dados em Cessão Fiduciária ou AF de Imóveis (g), constrição judicial sobre os Direitos Cedidos (bb), contratação de novas dívidas ou prestação de novas garantias pela Emissora (cc), AF de Quotas deixar de recair sobre 100% das quotas (ii), não regularização dos registros cartoriais das Garantias (v).
- **Financeiro / cross-default** (limiar-padrão de R$ 500 mil, individual ou agregado): inadimplemento de obrigação pecuniária do próprio Termo de Emissão, com cura de **2 dias úteis** (h); vencimento antecipado de outras dívidas financeiras (i); descumprimento de obrigações pecuniárias com terceiros (r); protesto/negativação (s, cura de 10 dias ou prazo legal); disputas/fiscalizações relevantes (t); redução de patrimônio líquido da Emissora/Avalistas em mais de 30% frente à base de 31/12/2021 (p).
- **Covenants financeiros do próprio ativo**: **LTV > 50%** sem reforço de garantia (dd) e **IC < 1,25x** (ee) — os dois únicos eventos com metodologia de cálculo própria, detalhados acima; (gg) trata do IC descumprido sem pagamento de um "prêmio" do item 9.1(mm) do Termo de Emissão — **não consegui localizar o texto do item "mm" nesta leitura** (a numeração de 9.1 vista na íntegra vai só até "jj"; esse ponto fica em aberto).
- **Integridade documental / declarações**: declarações falsas (k, u), invalidade/nulidade de Documentos da Operação (m), rescisão/extinção de Documentos da Operação (n), questionamento judicial da validade dos documentos pela própria Emissora (o), ônus sobre as Notas não decorrente de sua vinculação aos CRI (j), cessão das obrigações do Termo sem anuência (l).
- **Compliance / reputacional / regulatório**: trabalho infantil/escravo/prostituição (z), sanções do Portal da Transparência ou decisão anticorrupção (aa), desapropriação/confisco que gere Efeito Adverso Relevante (x), penhora/sequestro/arresto sobre bens > R$ 500 mil (y), perda de licenças/alvarás relevantes sem regularização em 30 dias (w).
- **Descumprimento genérico de obrigação não pecuniária** (q): cura de **10 dias úteis**, exceto para eventos com cura própria já definida ou para os demais Eventos de Vencimento Antecipado listados — é essa a cláusula "guarda-chuva" que embasou os itens de atraso (relatório mensal, laudo, seguro, DFs) discutidos nas 3 atas da operação.
- (hh) veda distribuição de lucros acima do mínimo legal em caso de mora; (ff) trata da interação entre descumprimento do IC/prêmio e do LTV.

### Obrigações acessórias monitoradas (Cláusula 9.1 do Termo de Emissão) — além dos covenants financeiros

Uma lista longa (itens "a" a "jj") de deveres de reporte e conduta da Emissora/Avalistas, que também podem gerar Evento de Vencimento (via a cláusula "q" acima) se descumpridos. Os principais grupos:

- **Reporte financeiro periódico**: DFs anuais auditadas da Emissora (90 dias do encerramento do exercício) e não auditadas dos Avalistas (f, h, i, v-a); relatório trimestral a partir de 2023 (g); declaração anual assinada atestando ausência de Evento de Vencimento (v-a-2); informações sob demanda ao Titular/Agente Fiduciário em 5-10 dias (b, v-b, v-c).
- **Reporte do ativo-garantia**: laudo de avaliação anual dos imóveis, até 15/jan, por avaliador de lista fechada (gg); **Relatório Mensal com o rent roll completo** (ii — ver seção dedicada abaixo); declaração de IR dos Avalistas anualmente (hh); seguro patrimonial contratado e endossado à Securitizadora, mantido até a liquidação total (jj).
- **Comunicação de eventos relevantes**: avisar sobre qualquer Evento de Vencimento Antecipado ou Efeito Adverso Relevante em até 5 du (c); notificações/correspondências recebidas sobre tais eventos em até 3 du (d); ações judiciais relevantes em até 2 du, com relatórios periódicos dos advogados (e); alterações no contrato social em até 5 du (a).
- **Conduta / manutenção da estrutura**: não alterar objeto social ou natureza dos negócios sem anuência (k); não ceder obrigações do Termo (j); não praticar atos em desacordo com os Documentos da Operação (l); manter contabilidade regular (m); manter licenças/alvarás/autorizações válidos, inclusive ambientais (o); aplicar os recursos exclusivamente conforme previsto (y); recolher tributos em dia (r); enviar cópias registradas dos instrumentos de garantia ao Agente Fiduciário (t).
- **Compliance/indenização**: manter Securitizadora e Agente Fiduciário indenes por danos ambientais/trabalhistas (z) e por declarações falsas/dolo/culpa (u); cumprir leis anticorrupção, ambientais, trabalhistas e de saúde/segurança ocupacional (aa, bb, ff); não fazer operações com partes relacionadas que afetem o cumprimento das obrigações (ee).
- **Governança da própria emissão**: comparecer às assembleias quando solicitado (dd); notificar o Agente Fiduciário e o Titular no mesmo dia de qualquer convocação de assembleia (cc); manter contratados os prestadores de serviço da emissão — Agente Fiduciário, sistemas B3 etc. (w); atender solicitações de informação da B3 em 5 du (x).

Combinando com a seção de covenants já registrada acima (Cláusula 8.1.1 do TS), **o Relatório Mensal (Anexo V) é o documento que concentra a maior parte do acompanhamento recorrente desta operação**: LTV, IC, Fundo de Reserva, Fundo de Despesas e rent roll completo, todos no mesmo relatório e na mesma cadência mensal.

### Rent roll / acompanhamento dos locatários — Relatório Mensal (Anexo V do Termo de Emissão)

Obrigação explícita e detalhada (Cláusula 9.1(ii) do Termo de Emissão): a Emissora deve entregar, **até a Data de Verificação de cada mês** (Termo de Securitização fala em até o 25º dia útil), um relatório mensal contendo, entre outros itens: planilha em Excel com (i) valor atualizado de cada locação, (ii) valor recebido de cada locatário no mês (com inadimplências, descontos, reajustes, multas), (iii) comprovantes bancários de recebimento identificando o locatário, (iv) índice de reajuste, (v) vencimento final da locação, (vi) área locável/locada e vacância, (vii) cópia dos contratos de locação e aditamentos, (viii) gastos com reforma/administração/vacância, e (ix) trocas de correspondência com locatários. É o mesmo relatório (Cláusula 8.1.1 do TS) que também traz o acompanhamento de LTV, IC, Fundo de Reserva e Fundo de Despesas — ou seja, **um único documento mensal cobre todos os 4 pontos de acompanhamento** desta operação. O campo `locatarios` do dado financeiro do pipeline está **vazio** para esta operação (mesma lacuna observada em outras).

## Obrigações / histórico de atas (as 3 atas conhecidas da operação, todas na pasta)

1. **02/05/2023** — Waiver retroativo por (i) atraso no envio do relatório mensal (Anexo V) desde o início da operação até a data da assembleia, e (ii) ausência de cálculo do Índice de Cobertura relativo a jan-fev/2023 — aprovado para não configurar Evento de Vencimento Antecipado. Também aprovou correção de redação do Considerando D do Anexo III do Contrato de Cessão Fiduciária (cláusula correta é a 1.2; periodicidade de aditamento é semestral, não trimestral, como constava por erro na minuta). **O Contrato de Cessão Fiduciária (original e esse aditamento de correção) não estão na pasta.**

2. **30/04/2026** — Aprovação da não decretação de vencimento antecipado por **4 descumprimentos simultâneos**, todos de entrega intempestiva (não de mérito): (i) laudo de avaliação (venceria 17/01/2026, entregue 03/03/2026); (ii) endosso do seguro patrimonial (venceria 25/09/2025, entregue 10/02/2026); (iii) relatório mensal de março (venceria 17/03/2026, entregue 13/04/2026); (iv) Demonstrações Financeiras da Emissora/Avalistas + declaração assinada (venceria 15/04/2026), para a qual foi concedido prazo adicional de 10 dias úteis (até ~14/05/2026).

3. **09/06/2026** — Aprovação da não decretação de vencimento antecipado porque as DFs do item (iv) acima **também vieram atrasadas** mesmo com a prorrogação: Emissora entregou em 22/05/2026, Avalistas em 25 e 26/05/2026 (prazo prorrogado terminava ~14/05/2026). Ata mais recente da operação; não cria nenhuma obrigação nova em aberto.

**Padrão identificado**: as 3 atas da operação são todas sobre atrasos administrativos/documentais recorrentes (relatório mensal, laudo, seguro, DFs) — nunca sobre desenquadramento de LTV ou IC em si (que seguem folgados). Vale acompanhar de perto a pontualidade de entregas no próximo ciclo, dado o histórico.

## Pontos de atenção / riscos

1. **Devedora detém só 25% do ativo-garantia (fração ideal)** — os outros 75% pertencem a um terceiro fora da operação (não identificado com certeza; indício de que seja "RBR", mas não confirmado documentalmente). Em uma excussão, a Securitizadora fica exposta à dinâmica de copropriedade/condomínio com esse terceiro.
2. **Contrato de Cessão Fiduciária de Recebíveis não está na pasta** (nem original nem eventual aditamento de correção aprovado em 02/05/2023) — é uma das 4 garantias centrais e não pôde ser lido diretamente nesta rodada.
3. **Padrão recorrente de atrasos em obrigações não pecuniárias** (relatório mensal, laudo de avaliação, seguro, DFs) — as 3 atas da operação são todas sobre isso; nenhuma envolveu desenquadramento financeiro, mas o histórico de pontualidade é fraco.
4. **Campo `locatarios` vazio** no dado financeiro do pipeline, apesar de a operação ter uma obrigação contratual detalhada de rent roll mensal (Anexo V) — oportunidade de preencher esse campo a partir dos relatórios mensais reais, se disponíveis em alguma outra fonte.
5. **Identidade do coproprietário dos imóveis (75%) e do "prêmio" do item 9.1(mm) do Termo de Emissão** (citado como condição alternativa ao reforço de garantia no desenquadramento do IC) não foram aprofundados nesta leitura — vale investigar se necessário para uma análise de risco mais completa.
