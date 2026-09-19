# Localfrio — Memória da Operação

> Leitura derivada de `Pipeline/documents_meta.json`, `Pipeline/obligations_data.json`, `Pipeline/portfolio_data_wrapped.json`, `Pipeline/documents_data.json` e leitura direta do Termo de Securitização original (Cláusulas 5ª a 23ª, na íntegra, incluindo Anexos I a VII — 2 cópias na pasta, mesmo conteúdo), do **Segundo Aditamento ao TS** (17/11/2022) e do **Terceiro Aditamento ao TS** (10/10/2024) (ambos na íntegra, adicionados à pasta em 19/09/2026), do **Contrato de Cessão de Créditos Imobiliários e Outras Avenças** (na íntegra, 39 páginas de conteúdo substantivo + assinaturas — adicionado à pasta em 18/09/2026), da Escritura de Emissão da CCI (busca textual pontual, não leitura integral), da ata AGT 07/07/2020 (na íntegra — "DocuSign_CRI_-_4E54-55S_-_LOCALFRIO_-_AGT_20 (1).pdf", só lida por completo em 19/09/2026), da ata AGT 29/08/2022, da ata AGT 08/02/2021, do material de apoio Movecta (jan/2024) e do Edital de Recompra Facultativa de 18/09/2025 (na íntegra). **Falta na pasta**: o Primeiro Aditamento ao TS (13/07/2020). Não é fonte de dados para o `build_data.py` — é um resumo pra revisão humana.
>
> Última atualização: 2026-09-19.

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

1. **07/07/2020 (AGT, reaberta — arquivo "DocuSign_CRI_-_4E54-55S_-_LOCALFRIO_-_AGT_20 (1).pdf", lida na íntegra em 19/09/2026 — não mapeada nas versões anteriores desta memória)** — assembleia de waiver por causa da Covid-19, muito relevante e até então não documentada aqui:
   - Pauta original: confirmar ou não uma **Recompra Compulsória** (item **xxi** da Cláusula 4.1 do Contrato de Cessão — insuficiência da Conta Vinculada por 2 meses consecutivos). Os Titulares (85,95% dos CRI) **não decretaram** a Recompra Compulsória, condicionado a: **(i) pagamento de waiver fee de 0,25% sobre o Saldo Devedor**, dividido em 6 parcelas mensais a partir de fev/2021 — **este é o único "0,25%" que existe em qualquer documento desta pasta**, e não é multa de resgate antecipado, é uma taxa de waiver por tolerância a um desenquadramento específico da Conta Vinculada; e **(ii) criação do covenant ICSD** (Índice de Cobertura de Serviço da Dívida) = Geração de Caixa da Atividade / Serviço da Dívida, com **mínimo formal de 1,0x a partir do exercício de 2022** — isso corrige a seção de covenants abaixo (o ICSD não é "informal", tem covenant formal desde 2020).
   - Também aprovou: redução temporária do Valor Mínimo da Conta Vinculada (pra 150% da PMT, jul–dez/2020), Bloqueio Obrigatório da Conta Vinculada, contratação de monitoramento externo da Conta Vinculada, liberação de R$1,3MM retidos, e redução temporária do aluguel mensal (de R$983.000 pra R$650.000) com redefinição do Fluxo Financeiro dos CRI (novo cronograma, Anexo I desta ata).
   - **Crucial para o gap da "Deságio Implícito"**: a ata condiciona expressamente todas as aprovações à **celebração de aditamentos aos Documentos da Operação em até 5 Dias Úteis** — ou seja, deveria existir pelo menos um **Primeiro Aditamento ao Termo de Securitização, celebrado em 13/07/2020** (data confirmada pelo preâmbulo dos 2º e 3º Aditamentos, lidos em 19/09/2026 — ver abaixo), formalizando o novo ICSD, o novo cronograma e o Bloqueio Obrigatório. **Esse Primeiro Aditamento ainda não está nesta pasta** — é o único aditamento numerado que falta (o 2º e o 3º já foram adicionados e lidos).

2. **08/02/2021** — evento administrativo menor, sequência direta do item acima (mesmo cronograma-base): um pagamento de amortização+juros em 16/12/2020 usou recursos do Fundo de Reserva além do previsto, desenquadrando-o temporariamente. Assembleia aprovou compensar o valor pago a maior (R$ 62.062,61) na parcela seguinte (18/02/2021), com um cronograma alternativo (Anexo A) como plano B.

3. **29/08/2022 (AGT, reaberta após 12 suspensões desde 25/04/2022)** — em troca da aprovação da substituição de um fiador falecido (Sr. Hélio de Athayde Vasone → sua viúva Marilena + Localpar Participações S.A. como nova fiadora corporativa), os Titulares negociaram um pacote de reforço:
   - **Criação do covenant Dívida Líquida/EBITDA** (trajetória decrescente até 3x em 5 anos, incluindo arrendamento no cálculo, EBITDA considerado só "no que transitar em caixa") — **covenant adicional ao ICSD já existente desde 2020** (ver item 1 acima), não substitui o ICSD.
   - Alteração do covenant de serviço da dívida existente (mesma regra do EBITDA em caixa) — provavelmente uma atualização do próprio ICSD criado em 2020, dado que ambos usam a mesma lógica de "caixa efetivamente recebido".
   - Novas obrigações documentais: balancete trimestral (60 dias), balanço anual auditado (90 dias, +30 se atraso de auditoria comprovado), IR dos fiadores pessoa física (5 dias após prazo legal), comunicação em 5 dias de perda de concessão de terminal ou de licença CLIA.
   - Tecnicamente configurava um "Evento de Recompra Compulsória" (Cláusula 4.1 (i) e (vii) do Contrato de Cessão), mas os Titulares optaram por não decretar, dado o pacote de reforço acordado.
   - **Confirmado formalmente pelo Segundo Aditamento ao Termo de Securitização** (celebrado 17/11/2022, adicionado à pasta e lido em 19/09/2026): substituição do fiador (Hélio Vasone → Marilena Rodrigues Vasone + Localpar Participações S.A., e inclusão de Alceu Rodrigues Vasone como 3º fiador) e criação da definição formal de "Dívida Líquida" no TS. Não traz nenhuma fórmula de multa/deságio.

4. **13/08/2024 (AGT — data real, confirmada pelo Terceiro Aditamento; o material Movecta de 22/01/2024 era só a proposta/pleito prévio)** — aprovou 2 das 3 mudanças propostas pela Movecta, **confirmadas formalmente pelo Terceiro Aditamento ao Termo de Securitização** (celebrado 10/10/2024, adicionado à pasta e lido em 19/09/2026):
   - **Troca de fiadora Localpar → FHV Participações e Empreendimentos S.A.** (CNPJ 96.612.585/0001-70) — confirmada, extinção da Localpar por eficiência tributária do grupo.
   - **Redução do Limite Mínimo do Fundo de Reserva para 4 PMTs — não chegou a valer na prática.** O Terceiro Aditamento redefine formalmente o Limite Mínimo para 4 parcelas vincendas, mas, segundo o usuário, o patamar reforçado de 5 PMTs (estipulado durante os episódios de troca de fiador) foi mantido — a operação segue em 5 PMTs até hoje (ver seção de covenants abaixo).
   - Nenhuma fórmula de multa/deságio no Terceiro Aditamento tampouco.

5. **18/09/2025 (Edital de Recompra Facultativa e outros)** — convocação de assembleia para 18/09/2025, 10h (Microsoft Teams), com 3 itens de pauta (lidos na íntegra):
   - **(i)** Usar a **totalidade** do Fundo de Reserva (R$ 4.646.621,27 do CRI Sênior + R$ 1.161.655,49 do CRI Subordinado, base 25/08/2025) para **Recompra Facultativa** com amortização extraordinária dos CRI, **sem incidência de qualquer prêmio**, sem observar o prazo mínimo de notificação da Cláusula 4.2 do Contrato de Cessão, e **sem recomposição posterior** do Fundo de Reserva.
   - **(ii)** Usar o excedente do Fundo de Despesas acima de R$ 100.000,00 (R$ 390.103,74 Sr + R$ 97.525,93 Sub) para o mesmo tipo de amortização extraordinária, também sem prêmio.
   - **(iii)** Se (i) for aprovado, **extinguir o Fundo de Reserva** — a operação passaria a não ter mais essa reserva de liquidez para cobrir inadimplência.
   - É só o **edital de convocação**, não a ata do resultado — não dá pra confirmar se a assembleia ocorreu nem se os itens foram aprovados. Mas o conteúdo já é muito relevante: se aprovado, é uma mudança estrutural (extinção do Fundo de Reserva), não um evento menor.

## Metodologias de cálculo da dívida (Termo de Securitização, Cláusulas 5ª, 6ª, 7ª e 8ª — lidas na íntegra)

Confirmado por leitura direta do TS + Contrato de Cessão (ambos na íntegra): estrutura clássica de **atualização monetária anual por IPCA + juros prefixados exponenciais em dias corridos**, com um cronograma de amortização **pré-fixado no Anexo I** (não é SAC nem Price) que combina amortização gradual crescente com um salto final tipo balão. Já a multa de resgate antecipado tem uma **divergência não resolvida**: o pipeline registra "Deságio Implícito - 0,25%", mas o texto do TS e do Contrato de Cessão que li só confirma resgate "ao par" (saldo devedor + encargos, sem prêmio) — ver detalhamento e hipóteses de reconciliação na seção abaixo.

### Atualização Monetária (Cláusula 5.1) — `VNa = VNb × C`

`C = NIk / NI0`, onde `NIk` é o número-índice do IPCA do **segundo mês imediatamente anterior** ao mês da Data de Atualização Monetária (defasagem M-2) e `NI0` é o número-índice da atualização anterior (outubro/2019 na primeira). **Periodicidade: anual**, sempre em janeiro (primeira em jan/2021, aplicada só após o pagamento da PMT do mês) — diferente da Residencial Itaim FL2 (atualização mensal), mas igual ao padrão da Pirelli. Índice substituto em caso de indisponibilidade do IPCA por mais de alguns dias: IGP-M ou índice acordado em Assembleia Geral; sem penalidade pela defasagem temporária (Cláusula 5.1.2).

### Juros Remuneratórios (Cláusula 5.1.5) — `Ji = VNa × (FJ − 1)`

Taxa de **6,00% a.a. para o CRI Sênior (54ª Série) e 7,00% a.a. para o CRI Subordinado (55ª Série)**, base **360 (trezentos e sessenta) dias corridos** (não dias úteis/252, diferente da Itaim) — `FJ = {[(1 + i/100)^(30/360)]}^(dcp/dcf)`, capitalização exponencial pro rata temporis por dias corridos decorridos desde a última Data de Pagamento/Aniversário. Pagamento **mensal**, conforme Cronograma de Pagamentos (Anexo I), 1ª parcela em 17/12/2019 (mesmo dia da emissão, sem juros a incorporar nessa primeira data).

### Amortização (Cláusula 5.1.7 + Anexo I) — tabela pré-fixada, perfil crescente com salto final tipo balão

`AMi = VNa × Tai`, onde `Tai` é a i-ésima taxa de amortização programada, fixada percentual a percentual no Anexo I (**145 parcelas mensais**, de 17/12/2019 a 16/12/2031, com tabelas ligeiramente diferentes para o Sênior e o Subordinado, mas mesmo formato). Não há carência total como na Itaim — a amortização já começa na 2ª parcela (~0,45–0,48% ao mês em 2020) e **cresce geometricamente ao longo do tempo**: ainda modesta em 2024–2025 (~0,8–1,1%/mês), passa a acelerar visivelmente a partir de ~2028 (2%+/mês), e dispara nos últimos meses — últimas 5 parcelas do Sênior: 133 (17/12/2030) 7,47%, 134 (16/01/2031) 8,11%, ... até **143 (16/10/2031) 33,17%, 144 (18/11/2031) 49,88%, 145 (16/12/2031) 100,00%** (quita a totalidade do saldo remanescente na última parcela). Ou seja: é um perfil de amortização crescente (não linear, não SAC/Price) com uma parcela final bullet — o "estouro" de amortização já é perceptível desde 2028/2029, não é uma surpresa concentrada só no último mês, mas ainda assim as últimas 3 parcelas somam sozinhas mais de 80% do saldo remanescente àquela altura.

### Resgate Antecipado e Multa/Prêmio de Pré-Pagamento (TS Cláusulas 6ª/8ª + Contrato de Cessão Cláusula 4ª, lidas na íntegra) — **campo do pipeline diz "Deságio Implícito - 0,25%"; texto contratual lido não confirma essa fórmula**

O pipeline (`Pipeline/portfolio_data_wrapped.json`, campo `Multa` da Localfrio, confirmado pelo usuário em 19/09/2026) registra a multa de resgate antecipado como **"Deságio Implícito - 0,25%"**. É um formato compatível com o padrão usado em outras operações do portfólio (ex.: Pirelli "0,5% x Duration", WT Log "0,95% x duration remanescente", GT "0,25% (venda do imóvel) ou 1,00% x duration") — ou seja, não é um valor genérico/placeholder, é um dado específico desta operação.

**Ponto em aberto, mas agora com uma pista concreta do que falta**: relendo o TS (Cláusulas 6ª/8ª) e o Contrato de Cessão na íntegra (Cláusula 4ª — Recompra Compulsória, Recompra Facultativa e Multa Indenizatória) e a Escritura de Emissão da CCI, **não encontrei o texto "Deságio Implícito" nem o percentual 0,25% associados a uma fórmula de prêmio de resgate** em nenhum dos três instrumentos. O que os documentos dizem literalmente:
- **Valor de Recompra** (TS 6.1.1 + Contrato de Cessão 4.3) = saldo devedor do CRI + encargos e despesas devidas + correção monetária pro rata die — sem termo de deságio na fórmula.
- **Recompra Compulsória** (Contrato de Cessão 4.1.5): expressamente "**sem aplicação de Prêmio**".
- O único "0,25%" que aparece nos documentos da pasta é um **waiver fee** distinto (não é multa de resgate): a ata de 07/07/2020 (ver Histórico, item 1 — só encontrada e lida na íntegra nesta rodada) menciona um waiver fee de 0,25% sobre o saldo devedor, pago em 6 parcelas a partir de fev/2021, como contrapartida por não decretar a Recompra Compulsória por insuficiência da Conta Vinculada — evento e mecânica completamente diferentes de uma multa de pré-pagamento.

**Atualização de 19/09/2026 — Segundo e Terceiro Aditamentos ao TS lidos, formula ainda não encontrada; falta especificamente o Primeiro Aditamento (13/07/2020)**: o usuário adicionou à pasta o **Segundo Aditamento** (17/11/2022, formaliza a AGT de 29/08/2022 — troca de fiador + define "Dívida Líquida") e o **Terceiro Aditamento** (10/10/2024, formaliza a AGT de 13/08/2024 — troca de fiador pra FHV + reduz Fundo de Reserva pra 4 PMTs), e também uma cópia limpa do **TS original** (14/11/2019, mesmo conteúdo do que já estava na pasta). **Nenhum dos três traz a fórmula "Deságio Implícito" ou qualquer prêmio de resgate** — o Segundo e o Terceiro só tratam de fiador/covenants/Fundo de Reserva, nada sobre resgate antecipado.

O preâmbulo de ambos os aditamentos confirma a data do aditamento que ainda falta: **"Primeiro Aditamento ao Termo de Securitização, celebrado em 13 de julho de 2020"** — esse é o único aditamento numerado que ainda não está na pasta, e é o que formaliza exatamente a AGT de 07/07/2020 (criação do ICSD, novo cronograma, Bloqueio Obrigatório da Conta Vinculada — ver Histórico, item 1). Ele é o candidato mais forte a conter a fórmula do "Deságio Implícito", se ela existir formalmente em algum lugar.

**Hipótese alternativa, que ganhou força com essa investigação**: o único "0,25%" que aparece em qualquer documento desta operação — em qualquer dos 4 TS/aditamentos lidos, no Contrato de Cessão, na Escritura de CCI — é o *waiver fee* de 0,25% sobre o saldo devedor da AGT de 07/07/2020 (contrapartida por não decretar Recompra Compulsória por insuficiência da Conta Vinculada, pago em 6 parcelas a partir de fev/2021). É possível que o campo `Multa` do pipeline tenha **confundido esse waiver fee com uma multa de resgate antecipado**, rotulando-o "Deságio Implícito" — mesmo sendo, na origem, um evento totalmente diferente (waiver de covenant, não pré-pagamento). Recomendo checar essa hipótese com quem preencheu o campo antes de buscar o Primeiro Aditamento como próximo passo.

**Conclusão**: uso o valor do pipeline ("Deságio Implícito - 0,25%") como o dado de referência da operação, mas registro que **não consegui verificar essa fórmula no TS original (2019), no Contrato de Cessão original (2019) nem na Escritura de Emissão da CCI** — os três só confirmam resgate "ao par" (saldo devedor + encargos, sem prêmio). A explicação mais provável é que a fórmula foi introduzida por um aditamento posterior (2020 ou 2022) que ainda não está nesta pasta.

### Vencimento Antecipado / Eventos de Recompra Compulsória (Contrato de Cessão, Cláusula 4.1 — lista completa confirmada, 22 eventos)

A Cláusula 4.1 do Contrato de Cessão lista **22 Eventos de Recompra Compulsória** — a operação equivalente a "vencimento antecipado" aqui não é um evento único, é uma lista longa e bem mais abrangente do que a AGT de 2022 (que só citava os itens "(i) e (vii)") deixava entender:

- **(i)** descumprimento de obrigação não pecuniária dos Documentos da Operação (cura: 30 dias);
- **(ii)** descumprimento de obrigação pecuniária pela Cedente e/ou Fiadores (cura: 7 Dias Úteis);
- **(iii)** rescisão/resilição/término de qualquer Documento da Operação;
- **(iv)** mudança de controle societário da Cedente sem a nova controladora se tornar fiadora (salvo anuência dos Titulares);
- **(v)** não constituição das Alienações Fiduciárias de Imóveis (Cláusula 3.2);
- **(vi)** extinção/limitação da vigência das Garantias antes do pagamento integral (cura: 30 dias, com possibilidade de reforço);
- **(vii)** Garantias tornarem-se inábeis/insuficientes e a Cedente não oferecer nova garantia (cura: 30 dias) — **este é o item citado na ata de 2022**;
- **(viii)** declarações e garantias da Cedente enganosas ou incorretas, com efeito adverso relevante;
- **(ix)** qualquer situação relacionada aos Imóveis, por culpa/dolo da Cedente e/ou Locatária, que impacte o pagamento dos Créditos Imobiliários;
- **(x)** não comprovação da transferência dos Seguros (Patrimonial/Lucros Cessantes) ou da renovação das apólices;
- **(xi)/(xii)** desapropriação total ou parcial dos Imóveis que impacte o pagamento;
- **(xiii)** CRI integralizados sem cumprimento das Condições Precedentes;
- **(xiv)** inadimplemento de obrigação pecuniária da Cedente ≥ R$ 1 milhão (individual ou agregado);
- **(xv)** protesto legítimo de títulos contra a Cedente ≥ R$ 1 milhão, não sanado;
- **(xvi)** Seguro de Lucros Cessantes insuficiente para cobrir a diferença de aluguel durante reconstrução;
- **(xvii)** falência, recuperação judicial/extrajudicial da Cedente e/ou da Locatária;
- **(xviii)** Cedente concorrer, culposa ou dolosamente, para configurar um Evento de Recompra Compulsória visando evitar a caracterização de Recompra Facultativa;
- **(xix)** **não recomposição do Fundo de Reserva**;
- **(xx)** recursos de Seguros não direcionados à Conta Centralizadora em até 5 Dias Úteis;
- **(xxi)** insuficiência dos Recursos na Conta Vinculada por 2 meses consecutivos;
- **(xxii)** não comprovação da formalização do Contrato de Conta Vinculada.

Ou seja: além do item (vii) já mapeado (garantias insuficientes) e do item (xix) que cobre diretamente o Fundo de Reserva, a lista inclui hipóteses bem amplas — inclusive qualquer inadimplemento pecuniário >R$1MM, falência da Locatária, ou mudança de controle sem novo fiador. **Nenhuma dessas 22 hipóteses tem, por si só, o efeito automático de vencer a dívida** — todas passam pela mecânica de Assembleia Geral abaixo.

**Mecânica de decisão** (TS + Contrato de Cessão, Cláusula 4.1.1 a 4.1.5):
- Vencido o prazo de cura (quando houver) sem sanar, a Cessionária tem até **5 Dias Úteis** para convocar Assembleia Geral, para que os Titulares deliberem se decretam ou não a Recompra Compulsória.
- Quórum: **75% dos CRI em Circulação em 1ª convocação, 50%+1 em 2ª convocação** (Cláusula 4.1.2).
- **Se não houver instalação em nenhuma das duas convocações por falta de quórum**, a Recompra Compulsória é considerada **automaticamente configurada** (Cláusula 4.1.3) — exceção relevante à regra de "não é automático": omissão dos Titulares também gatilha o evento.
- Configurado o evento (por deliberação favorável ou por falta de quórum), a Cedente tem **12 Dias Úteis** da notificação para pagar o Valor de Recompra, "de forma definitiva, irrevogável e irretratável" (Cláusula 4.1.5/4.3.1) — **sem aplicação de prêmio**, como já detalhado acima.

### Ordem de Prioridade de Pagamentos (Cláusula Sétima)

Em caso de excussão de Garantias ou uso da Conta Centralizadora: (i) despesas do Patrimônio Separado; (ii) recomposição do Fundo de Reserva; (iii) encargos moratórios vencidos; (iv)–(vi) juros capitalizados, juros vincendos e amortização programada do **CRI Sênior** (nessa ordem); (vii)–(ix) o mesmo para o **CRI Subordinado**. Confirma a subordinação estrutural entre as séries também na fila de pagamento, não só nas garantias.

## Metodologias de cálculo dos covenants

### Dívida Líquida / EBITDA (o covenant central desta operação)

Texto da deliberação de 29/08/2022: **trajetória decrescente até 3,0x em 5 anos**, "incluindo arrendamento no cálculo" (ou seja, considera o passivo de arrendamento, coerente com a estrutura de sale-leaseback), com EBITDA considerado apenas "no que transitar em caixa" (apurado por auditoria externa). O material de apoio da Movecta detalha os componentes:
- `Dívida Líquida = Dívida Bruta (Bancos + CRI) − Caixa`
- `EBITDA (ex-IFRS16) = EBITDA Contábil − Amortização − Juros dos Arrendamentos`
- Situação relatada em jan/2024: a empresa já estava em 2,0x (ex-IFRS16) desde 2022, abaixo do limite — folga confortável.

Verificado **anualmente** (documento no pipeline: AGT 29/08/2022; última atualização 30/05/2026). Status atual: Enquadrado.

### ICSD — **correção: TEM covenant formal (≥1,0x), criado na AGT de 07/07/2020**

Versão anterior desta memória dizia que o ICSD era "informal/gerencial, sem mínimo formal" — **isso estava errado**. Relendo a ata de 07/07/2020 na íntegra (ver Histórico, item 1), o ICSD foi criado ali como **covenant financeiro formal**: `ICSD = Geração de Caixa da Atividade / Serviço da Dívida`, onde Geração de Caixa da Atividade = EBITDA − IR/CSLL pagos pela Devedora, e Serviço da Dívida = Amortização de Principal + Pagamento de Juros da Devedora (bases consolidadas). **Mínimo formal: ≥ 1,0x, verificado anualmente a partir do exercício de 2022** (calculado com base na Demonstração Financeira de encerramento de cada ano, a partir da publicação de mar/2023 referente a 2022).

O material da Movecta (jan/2024) descreve essencialmente a mesma fórmula sob o nome "IC Gerencial" (`Geração de Caixa CRI / Serviço da Dívida`, com EBITDA ex-IFRS16 − IR/CSLL no numerador) — é muito provavelmente **a mesma métrica**, não um índice informal à parte; o texto da Movecta só não deixa claro que há um mínimo contratual de 2020 por trás dela. Atual: 1,16x — **enquadrado, mas com menos folga do que um índice "sem mínimo" sugeriria** (1,16x vs. mínimo de 1,0x é uma margem mais estreita que a impressão anterior de "só acompanhamento"). Vale corrigir o campo do pipeline/memória interna se ele também descrever esse índice como sem covenant formal.

### Fundo de Reserva — **confirmado: 5 PMTs (não 4, apesar do texto do Terceiro Aditamento)**

**Definição original do TS** (Seção II — Termos Definidos, página 11 do "TS.pdf", confirmada pelo usuário em 19/09/2026): "**Limite Mínimo do Fundo de Reserva**" = "O montante equivalente às 5 (cinco) primeiras parcelas de pagamento dos CRI, o qual deverá ser mantido no Fundo de Reserva durante toda a Operação." Valor de constituição: R$ 4.914.586,53.

A Cláusula 1.2 do **Terceiro Aditamento ao Termo de Securitização** (celebrado 10/10/2024, formalizando a AGT de 13/08/2024) tentou redefinir esse termo para "o montante equivalente às próximas 4 (quatro) parcelas vincendas de pagamento dos CRI". Segundo o usuário, essa redução **não chegou a valer na prática**: quando surgiram os problemas com fiador (substituição por falecimento em 2022, depois extinção da Localpar em 2024), foi estipulado um Fundo de Reserva maior como reforço de garantia, e esse patamar de **5 PMTs — o mesmo da definição original do TS — ficou mantido**, em vez de reduzir para 4 como o Terceiro Aditamento previa. Isso é consistente com o covenant cadastrado no pipeline (`Pipeline/portfolio_data_wrapped.json`, dado de 2026-07: "Fundo de Reserva — 5 PMTs de Sr + Sub na constituição"). **Conclusão confirmada**: o Fundo de Reserva desta operação está e permanece em **5 PMTs** — a tentativa de redução para 4 (Terceiro Aditamento, 2024) não vingou.

### LTV — confirmado: NÃO existe covenant de LTV no Contrato de Cessão nem no TS

Depois de ler o Contrato de Cessão na íntegra (39 páginas de conteúdo, Cláusulas 1ª a 7ª), **não há nenhuma cláusula de LTV** — nem a citação "4.5.iii" do pipeline corresponde a nada real (a Cláusula 4.5 trata da Multa Indenizatória e só tem 3 subcláusulas, 4.5.1 a 4.5.3, sem incisos romanos, e nenhuma delas menciona LTV). A observação já cadastrada no pipeline ("acompanhar o comportamento de LTV... não tem necessidade de atualização de laudo anual") parece então ser um controle gerencial interno (da equipe que acompanha a operação), não um covenant contratual documentado no TS ou no Contrato de Cessão. Ou seja: **confirmado — diferente de Jardins/Itaim/BR Properties, a Localfrio realmente não tem um limite formal de LTV com consequência de vencimento antecipado atrelada** (nem na Cláusula 4.1 do Contrato de Cessão, que lista os 22 Eventos de Recompra Compulsória — LTV não está entre eles). Atual: 49,1% (monitorado, sem covenant).

### Rent roll / conta vinculada / "Monitori"

Rent roll: dado de aluguel mensal por imóvel já está cadastrado (ver seção de estruturação acima), mas o campo dedicado (`locatarios`) está vazio — mesmo padrão de lacuna observado em outras operações. **Não encontrei nenhuma menção a "Monitori"** em nenhum dos documentos lidos, incluindo agora o Contrato de Cessão na íntegra — segue sem explicação; pode ser um agente de monitoramento contratado fora dos documentos desta pasta (não faz parte do TS nem do Contrato de Cessão).

## Obrigações presentes na operação

### Obrigações da Emissora (TS, Cláusula 11ª — lida na íntegra)

São obrigações de "prestação de contas" da Securitizadora, não covenants de crédito da Devedora/Cedente: (i) informar fatos relevantes da Emissão; (ii) elaborar **relatório trimestral** com valor atual por CRI, valor atual da emissão, lastro (fluxo recebido nos últimos 30 dias, créditos em atraso >90 dias), garantias e Fundos, a disponibilizar aos Titulares e enviar ao Agente Fiduciário até o **dia 20 de cada mês**; (iii) fornecer dados societários/financeiros para o relatório anual do Agente Fiduciário (Instrução CVM 583), até 30 dias antes do prazo de disponibilização na CVM; (iv) responder pela exatidão das informações prestadas. Padrão, comum a todas as securitizações da Isec/Virgo — não é específico da Localfrio.

### Obrigações documentais da Devedora/Cedente (pacote negociado na AGT 29/08/2022 — já mapeado no Histórico, item 2)

As obrigações de reporte específicas desta operação (fora do TS, negociadas como contrapartida à troca de fiador) são: balancete trimestral em até 60 dias; balanço anual auditado em até 90 dias (+30 dias com atraso de auditoria comprovado); IR dos fiadores pessoa física em até 5 dias após o prazo legal; comunicação em até 5 dias de perda de concessão de terminal ou de licença CLIA. Essas obrigações, mais o cumprimento dos covenants de Dívida Líquida/EBITDA e Fundo de Reserva (ver acima), formam o conjunto de obrigações "vivas" de monitoramento desta operação identificável nos documentos da pasta.

### Obrigações relacionadas às Garantias e Seguros (Contrato de Cessão, Cláusula 3ª — confirmada na íntegra)

A Cedente tem obrigações específicas de constituição e manutenção das Garantias, que também funcionam como covenants operacionais (o descumprimento de várias delas é, ao mesmo tempo, Evento de Recompra Compulsória — ver seção acima):
- **Alienação Fiduciária de Imóveis**: constituir em até 60 dias do recebimento dos termos de liberação das Dívidas anteriores (prorrogável 1x por mais 60 dias corridos, só se o atraso for do cartório). Enquanto vigente, os Imóveis não podem ser alienados/onerados sem aprovação prévia dos Titulares em assembleia — exceto venda por valor ≥ ao valor previsto no Contrato de Alienação Fiduciária, corrigido pelo IPCA, que a Cessionária pode autorizar sozinha.
- **Alienação Fiduciária de Quotas**: 100% das quotas da Cedente alienadas fiduciariamente; a Cessionária se obriga a liberá-las assim que comprovados os registros das Alienações Fiduciárias de Imóveis.
- **Cessão Fiduciária** da Conta Vinculada + Recursos, mantida válida até o cumprimento integral das Obrigações Garantidas; os créditos garantidos por propriedade fiduciária **não se submetem aos efeitos de recuperação judicial** (art. 49, §3º, Lei 11.101), cláusula expressamente registrada no contrato.
- **Fiança**: os Fiadores comparecem ao próprio Contrato de Cessão para anuir e renunciam expressamente ao benefício de ordem e ao direito de exoneração.
- **Seguro Patrimonial**: transferir (com efeito de endosso) à Cessionária como beneficiária, cobertura atual de **R$ 31.000.000,00 (Imóvel 1 — Anhanguera/Itajaí) + R$ 28.000.000,00 (Imóvel 2 — São Paulo)**. Indenização recebida deve ser usada para reconstrução dos Imóveis (laudo de empresa especializada, cronograma de até 10 meses); se o laudo apontar mais de 10 meses de obra, a Cessionária pode usar a indenização para **amortização/resgate dos CRI** em vez de reconstruir.
- **Seguro de Lucros Cessantes**: cobertura de até **R$ 10.000.000,00**, cobre a diferença entre o aluguel pago pela Locatária e o Aluguel Mensal esperado, por até 10 meses de sinistro; recursos vão só para a Conta Vinculada. Se insuficiente para cobrir a diferença durante a reconstrução, é o próprio Evento de Recompra Compulsória (xvi) da lista acima.
- **Multiplicidade de Garantias**: todas garantem o cumprimento integral das Obrigações Garantidas, podem ser executadas individual ou conjuntamente, e a ordem de excussão é decidida pelos Titulares em assembleia (não é automática/pré-definida).

### Obrigações de administração dos Créditos Imobiliários e penalidades gerais (Contrato de Cessão, Cláusulas 5ª e 7ª)

- A **Cedente** administra ordinariamente os Créditos Imobiliários (cobrança da Locatária, inclusive judicial); a **Cessionária** só acompanha e recebe os pagamentos diretamente na Conta Centralizadora (Cláusula 5.1). A Cedente pode renegociar cobranças de penalidade com a Locatária, mas qualquer negociação que afete o fluxo financeiro dos recebíveis precisa de anuência prévia da Cessionária e aprovação dos Titulares em assembleia.
- Pagamentos da Locatária recebidos por engano pela Cedente devem ser repassados à Conta Centralizadora em até **3 Dias Úteis**, sob pena de juros de mora de 1% a.m. + multa não indenizatória de 2% sobre o valor (Cláusula 5.2).
- **Multa genérica** (Cláusula 7.2): qualquer descumprimento de obrigação do Contrato de Cessão sem multa específica prevista gera multa de **2% sobre o valor da obrigação pecuniária descumprida + juros de mora de 1% a.m.**, pro rata die — é o "catch-all" de penalidade para obrigações não cobertas pelas multas específicas já mapeadas acima.
- O Contrato de Cessão constitui **título executivo extrajudicial** (Cláusula 7.14), sujeito a execução específica (Cláusula 7.15) — reforça a robustez jurídica das obrigações listadas.

## Pontos de atenção / riscos

1. **Fundo de Reserva — confirmado em 5 PMTs.** O Terceiro Aditamento ao TS (10/10/2024, lido na íntegra) redefine formalmente o Limite Mínimo para 4 parcelas vincendas, mas essa redução não chegou a valer na prática: segundo o usuário (19/09/2026), quando surgiram os problemas de fiador (2022/2024), foi estipulado um Fundo de Reserva maior como reforço de garantia, e esse patamar de 5 PMTs ficou mantido — consistente com o covenant do pipeline (`Pipeline/portfolio_data_wrapped.json`, 2026-07), que também registra 5 PMTs. Ver detalhamento completo na seção "Fundo de Reserva" acima. O texto `sobre_operacao` do pipeline, que fala em "reduzido para 3 PMTs em 2024", está incorreto — o valor certo é 5. **Atenção**: o Edital de 18/09/2025 (item 5 do Histórico) propõe algo bem mais drástico — a **extinção total** do Fundo de Reserva, não uma simples redução.
2. **Fiador atual: FHV Participações — confirmado formalmente.** O Terceiro Aditamento ao TS (10/10/2024) confirma a substituição Localpar → FHV Participações e Empreendimentos S.A. (CNPJ 96.612.585/0001-70). Gap anterior resolvido.
3. **Edital de 18/09/2025 propõe zerar e extinguir o Fundo de Reserva — sem ata de resultado na pasta.** Lido na íntegra (ver Histórico, item 5, e seção de Resgate Antecipado acima): propõe usar a totalidade do Fundo de Reserva (~R$ 5,8MM) e o excedente do Fundo de Despesas para amortização extraordinária **sem prêmio**, e depois **extinguir** o Fundo de Reserva definitivamente (sem recomposição). Não há ata confirmando se a assembleia ocorreu nem o resultado — mas se aprovado, é uma mudança estrutural relevante: a operação perderia o colchão de liquidez (hoje 4 PMTs, ver item 1) que cobre eventual inadimplência, e não haveria mais fundo pra recompor. Vale muito confirmar o desfecho dessa assembleia antes de qualquer análise de risco atualizada.
4. **Contrato de Cessão lido na íntegra em 18/09/2026 — resolveu o gap anterior, com 1 achado que merece destaque**: **não existe covenant de LTV** em nenhum dos instrumentos principais (TS, Contrato de Cessão, Escritura de Emissão da CCI) — a citação "Contrato de Cessão (4.5.iii)" que estava no pipeline não corresponde a nenhuma cláusula real do documento (a 4.5 trata da Multa Indenizatória, só tem 3 subcláusulas). Vale avisar quem mantém o pipeline sobre essa citação incorreta.
5. **Multa de resgate antecipado ("Deságio Implícito - 0,25%"): ainda não localizada, mesmo após ler TS original, Contrato de Cessão, Segundo e Terceiro Aditamentos.** Só falta um documento: o **Primeiro Aditamento ao TS (13/07/2020)** — confirmado pelo preâmbulo dos Aditamentos 2º/3º, formaliza a AGT de 07/07/2020, mas não está na pasta. Hipótese mais provável, porém: o único "0,25%" que existe em qualquer documento lido é o *waiver fee* da AGT de 07/07/2020 (evento de insuficiência da Conta Vinculada, não resgate antecipado) — pode ser que o campo `Multa` do pipeline tenha confundido esse waiver fee com uma multa de pré-pagamento. **Próximo passo sugerido**: (a) confirmar com quem preencheu o pipeline se "Deságio Implícito - 0,25%" não é na verdade esse waiver fee mal rotulado; (b) se não for, buscar o Primeiro Aditamento ao TS de 13/07/2020 com a Securitizadora/Agente Fiduciário.
6. **ICSD: correção de rota — TEM covenant formal (≥1,0x), não é só gerencial.** Achado na ata de 07/07/2020 (ver Histórico item 1): o ICSD (Geração de Caixa da Atividade / Serviço da Dívida) foi criado ali como covenant formal com mínimo de 1,0x a partir de 2022, não é uma métrica "sem mínimo exigido" como a versão anterior desta memória registrava (a partir só do material da Movecta 2024). Atual 1,16x é enquadrado, mas com menos folga do que a leitura anterior sugeria.
7. **Lista de 22 Eventos de Recompra Compulsória (vencimento antecipado) é bem mais ampla do que a ata de 2022 sugeria** — inclui, além da perda de fiador/garantias já conhecida, hipóteses como falência da Locatária, inadimplemento pecuniário da Cedente ≥R$1MM, protesto de títulos ≥R$1MM e mudança de controle societário sem novo fiador. Vale ter essa lista completa em mente ao avaliar risco de eventos gatilho, não só os itens (i)/(vii)/(xix) já mapeados por atas anteriores.
8. Estrutura de sale-leaseback com Cedente e Devedora sendo entidades jurídicas distintas do mesmo grupo — vale ter isso em mente ao avaliar risco de crédito consolidado do grupo Localfrio.
