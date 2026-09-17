const { JSDOM } = require('jsdom');
const fs = require('fs');
const html = fs.readFileSync('./portal_publish.html', 'utf-8');

(async () => {
  const dom = new JSDOM(html, { runScripts: 'dangerously', resources: 'usable', pretendToBeVisual: true });
  const win = dom.window;
  win.scrollTo = () => {};
  win.HTMLElement.prototype.scrollTo = () => {};
  await new Promise(res => win.addEventListener('load', res));
  await new Promise(res => setTimeout(res, 300));
  const doc = win.document;

  let fails = 0;
  function check(label, cond) {
    console.log((cond ? 'OK  ' : 'FAIL') + ' - ' + label);
    if (!cond) fails++;
  }

  win.showDetail('MSB Axis');
  await new Promise(res => setTimeout(res, 250));
  const bodyTxt = doc.body.textContent || '';

  // 1. Highlights
  check('Highlight aporte SPE R$2,0MM / receita R$533.305', bodyTxt.includes('2,0MM') && bodyTxt.includes('533.305'));
  check('Highlight IC 1,30x / aportes MSB R$43,7MM', bodyTxt.includes('1,30x') && bodyTxt.includes('43,7MM'));

  // 2. Sobre a Operação
  check('Sobre a Operação: NC R$95,0MM / MSB Valência / Axis+Sync', bodyTxt.includes('95,0 MM') && bodyTxt.includes('MSB Valência') && bodyTxt.includes('Axis') && bodyTxt.includes('Sync'));
  check('Sobre a Operação: integralização R$48,4MM / Brio', bodyTxt.includes('48,4 MM') && bodyTxt.includes('Brio'));
  check('Sobre a Operação: prêmio R$1,9MM / 2,0%', bodyTxt.includes('1,9 MM') && bodyTxt.includes('2,0%'));
  check('Sobre a Operação: covenants IC>1,30x / estrutura de capital>20%', bodyTxt.includes('1,30x') && bodyTxt.includes('20%'));
  check('Sobre a Operação: aportes mensais R$2,0MM Nov/25-Out/26', bodyTxt.includes('Nov/25') && bodyTxt.includes('Out/26'));

  // 3. Informações do ativo comparativa AXIS/SYNC
  const ativoPanel = [...doc.querySelectorAll('.panel')].find(p => p.querySelector('h2') && p.querySelector('h2').textContent.trim() === 'Garantias');
  const ativoTxt = ativoPanel ? ativoPanel.textContent : '';
  check('Ativo: colunas AXIS e SYNC presentes', ativoTxt.includes('AXIS') && ativoTxt.includes('SYNC'));
  check('Ativo: Incorporadora MSB Sanchez', ativoTxt.includes('MSB Sanchez'));
  check('Ativo: Tipo de Ativo Residencial (compartilhado, igual nas 2 torres)', ativoTxt.includes('Residencial'));
  check('Ativo: Área Terreno 2.303', ativoTxt.includes('2.303'));
  check('Ativo: Área Privativa 8.083 / 3.838', ativoTxt.includes('8.083') && ativoTxt.includes('3.838'));
  check('Ativo: Nº Unidades (Área Média) 61 (133 m²) / 124 (31 m²)', ativoTxt.includes('61 unidades') && ativoTxt.includes('133 m²') && ativoTxt.includes('124 unidades') && ativoTxt.includes('31 m²'));
  check('Ativo: Tipologia com abertura de unidades por torre', ativoTxt.includes('131 m²') && ativoTxt.includes('136 m²') && ativoTxt.includes('studios'));
  check('Ativo: Previsão Habite-se Jul/27 (planilha viva, não Ago/27 do print)', ativoTxt.includes('Jul/27') && !ativoTxt.includes('Ago/27'));

  // 4/5. Itens de Acompanhamento: Estrutura de Capital card + bug do "Estoque" corrigido
  const covPanel = [...doc.querySelectorAll('.panel')].find(p => p.querySelector('h2') && p.querySelector('h2').textContent.trim() === 'Itens de Acompanhamento');
  const covTxt = covPanel ? covPanel.textContent : '';
  check('Covenants: card "Estrutura de Capital" presente', covTxt.includes('Estrutura de Capital'));
  check('Covenants: status mostra "Enquadrado" (não mais "Estoque"/"Vendido")', covTxt.includes('Enquadrado') && !covTxt.includes('>Estoque<') );
  check('Covenants: sem texto de obs excessivamente longo (nenhum obs > 220 chars)', ![...(covPanel?covPanel.querySelectorAll('.covitem-obs'):[])].some(el => el.textContent.length > 220));

  // 6. Card Acompanhamento da Carteira, Vendas e Estoque
  const cvePanel = [...doc.querySelectorAll('.panel')].find(p => p.querySelector('h2') && p.querySelector('h2').textContent.trim() === 'Acompanhamento da Carteira, Vendas e Estoque');
  check('Card Carteira/Vendas/Estoque presente', !!cvePanel);
  const cveTxt = cvePanel ? cvePanel.textContent : '';
  // (correção pt.4: estrutura mudou de linhas AXIS/SYNC/Consolidado p/ colunas AXIS/SYNC por ano, seguindo o exemplo)
  check('Card: colunas AXIS/SYNC (quantidade e preço médio) presentes', cveTxt.includes('AXIS') && cveTxt.includes('SYNC') && cveTxt.includes('Quantidade') && cveTxt.includes('Preço Médio'));
  check('Card: Carteira Recebida/a Receber (dado vivo da planilha)', cveTxt.includes('Carteira Recebida') && cveTxt.includes('Carteira a Receber'));
  check('Card: link "Ver abertura mês a mês"', !!cvePanel && !!cvePanel.querySelector('.carteira-link'));

  // 7. Sub-página detalhe mensal
  const carteiraLink = cvePanel ? cvePanel.querySelector('.carteira-link') : null;
  if (carteiraLink) carteiraLink.dispatchEvent(new win.Event('click', { bubbles: true, cancelable: true }));
  await new Promise(res => setTimeout(res, 200));
  const detView = doc.getElementById('view-carteiradetalhe');
  check('Sub-página de detalhe mensal ativa', detView && detView.classList.contains('active'));
  const detTxt = detView ? detView.textContent : '';
  // (correção pt.5: redesenhada p/ 9 colunas enxutas -- Vendas AXIS/SYNC + estoque/funding consolidado, sem repetir "Consolidado" como rótulo)
  check('Sub-página: colunas Vendas AXIS/SYNC + SD CRI (redesenhada)', detTxt.includes('AXIS') && detTxt.includes('SYNC') && detTxt.includes('SD CRI'));
  check('Sub-página: tabela com várias linhas mensais', detView ? detView.querySelectorAll('tbody tr').length >= 20 : false);
  const backBtn = doc.getElementById('carteiradetalhe-back');
  if (backBtn) backBtn.click();
  await new Promise(res => setTimeout(res, 200));

  // 8. Fluxo Mensal: IC em visão única (sem navegação por período)
  win.showDetail('MSB Axis');
  await new Promise(res => setTimeout(res, 250));
  const fluxoBody = doc.getElementById('fluxo-charts');
  const fluxoTxt = fluxoBody ? fluxoBody.textContent : '';
  check('Fluxo: título "Histórico + Projetado" presente', fluxoTxt.includes('Histórico + Projetado'));
  check('Fluxo: SEM navegação/dropdown de janela do IC (visão única)', !doc.getElementById('ic-end-select'));
  // (correção pós-publicação, 2ª rodada, ponto 3: nota de texto embaixo do gráfico virou
  // caixa de destaque + etiqueta DENTRO do gráfico, igual ao exemplo do usuário)
  // 45ª rodada: "Menor IC Proj." e a etiqueta "1,30x" do IC mínimo viraram texto desenhado
  // pelo ECharts (camada `graphic`, ver echartsLineOption/__computeValueLabels) -- não existem
  // mais como texto estático no HTML/SVG pra inspecionar sob JSDOM (mesma limitação do bloco
  // "Pt.6" mais abaixo). O valor 1,30x do covenant de IC mínimo já é verificado separadamente
  // (ver check "Sobre a Operação: covenants IC>1,30x" acima); a etiqueta e a caixa dentro do
  // gráfico em si foram conferidas visualmente via Playwright.

  // 9. Gráfico Evolução Física da Obra no lugar do LTV
  check('Fluxo: "Evolução Física da Obra" presente', fluxoTxt.includes('Evolução Física da Obra'));
  check('Fluxo: SEM chartbox de LTV', !fluxoTxt.includes('>LTV<') && !/<h3>LTV<\/h3>/.test(fluxoBody ? fluxoBody.innerHTML : ''));
  const legends = fluxoBody ? [...fluxoBody.querySelectorAll('.chart-legend')] : [];
  const obraLegendEl = legends.find(l => l.textContent.includes('Previsto Mês'));
  check('Fluxo: legenda do gráfico de obra (Previsto/Realizado), no topo do card', !!obraLegendEl && obraLegendEl.textContent.includes('Realizado Mês') && obraLegendEl.classList.contains('chart-legend-top'));

  // 10. Seção de Indicadores removida
  const indicPanel = [...doc.querySelectorAll('.panel')].find(p => p.querySelector('h2') && p.querySelector('h2').textContent.trim() === 'Indicadores');
  check('Seção "Indicadores" (dump bruto) ausente', !indicPanel);

  // ===== Rodada de correções (2ª) =====

  // Pt.2: quickstat "IC Atual" no lugar de "LTV Atual"
  const qstats = [...doc.querySelectorAll('.qstat')];
  const icAtualStat = qstats.find(q => (q.querySelector('.label')||{}).textContent === 'IC Atual');
  const ltvAtualStat = qstats.find(q => (q.querySelector('.label')||{}).textContent === 'LTV Atual');
  check('Quickstat: "IC Atual" presente (não mais "LTV Atual")', !!icAtualStat && !ltvAtualStat);

  // Pt.3: chip de status real (não "Sem covenants") -- escopo no detail-head da própria
  // operação, já que outras operações da carteira podem legitimamente ter "Sem covenants"
  const detHeadTxt = (doc.getElementById('detail-head')||{}).textContent || '';
  check('Chip de status do topo (MSB Axis) mostra "Enquadrada", não "Sem covenants"', detHeadTxt.includes('Enquadrada') && !detHeadTxt.includes('Sem covenants'));

  // Pt.1: card "Integralizações" + link + sub-página
  check('Item "Integralizações" presente em Itens de Acompanhamento', covTxt.includes('Integralizações'));
  const integralizacoesLink = covPanel ? covPanel.querySelector('.integralizacoes-link') : null;
  check('Link "Ver tabela de integralizações" presente', !!integralizacoesLink);
  if (integralizacoesLink) integralizacoesLink.dispatchEvent(new win.Event('click', { bubbles: true, cancelable: true }));
  await new Promise(res => setTimeout(res, 200));
  const integView = doc.getElementById('view-integralizacoes');
  check('Sub-página de Integralizações ativa', integView && integView.classList.contains('active'));
  const integTxt = integView ? integView.textContent : '';
  check('Sub-página Integralizações: resumo Emitido/Integralizado/A Integralizar', integTxt.includes('Emitido') && integTxt.includes('Integralizado') && integTxt.includes('A Integralizar'));
  check('Sub-página Integralizações: tabela com Data/Quantidade/PU/Valor', integTxt.includes('Quantidade') && integTxt.includes('PU de Integralização') && integTxt.includes('Valor Integralizado'));
  check('Sub-página Integralizações: várias linhas na tabela', integView ? integView.querySelectorAll('tbody tr').length >= 3 : false);
  const integBackBtn = doc.getElementById('integralizacoes-back');
  if (integBackBtn) integBackBtn.click();
  await new Promise(res => setTimeout(res, 200));
  win.showDetail('MSB Axis');
  await new Promise(res => setTimeout(res, 250));

  // Pt.4: tabela Vendas/Carteira/Estoque reestruturada (linhas por ano + banner de Carteira)
  const cvePanel2 = [...doc.querySelectorAll('.panel')].find(p => p.querySelector('h2') && p.querySelector('h2').textContent.trim() === 'Acompanhamento da Carteira, Vendas e Estoque');
  const cveTable = cvePanel2 ? cvePanel2.querySelector('table.cve-table') : null;
  check('Card Vendas/Carteira/Estoque: tabela única com cabeçalho agrupado', !!cveTable);
  const carteiraBanner = cvePanel2 ? cvePanel2.querySelector('tr.carteira-banner-row') : null;
  check('Card Vendas/Carteira/Estoque: linha-banner "Carteira Recebida/a Receber"', !!carteiraBanner);

  // Pt.4/rodada 4 pt.1: linha "Vendido" e "Estoque" com a MESMA classe .estoque-total
  // (revertido -- não mais cve-subtotal/cve-final), sem traço nos valores de quantidade/m²
  // que não são zero, e AXIS/SYNC separados (sem colspan) na linha Estoque
  const cveRows = cveTable ? [...cveTable.querySelectorAll('tbody tr')] : [];
  const vendidoTr = cveRows.find(r => r.textContent.includes('Vendido'));
  const estoqueTr = cveRows.find(r => r.querySelector('td') && r.querySelector('td').textContent.trim() === 'Estoque');
  check('Card Vendas/Carteira/Estoque: linhas Vendido/Estoque usam .estoque-total (revertido)', !!vendidoTr && vendidoTr.classList.contains('estoque-total') && !!estoqueTr && estoqueTr.classList.contains('estoque-total'));
  check('Card Vendas/Carteira/Estoque: linha Estoque com AXIS/SYNC separados (7 células, sem colspan)', estoqueTr ? estoqueTr.querySelectorAll('td').length === 7 : false);

  // Pt.5/rodada 4 pt.4: abertura mensal restaurada com colunas AXIS/SYNC completas
  // (Vendas, Área, Preço Médio, Área Estoque, Preço LTM Ponderado por torre) + 3 consolidadas,
  // em cabeçalho de 2 níveis (grupo + coluna)
  const carteiraLink2 = cvePanel2 ? cvePanel2.querySelector('.carteira-link') : null;
  if (carteiraLink2) carteiraLink2.dispatchEvent(new win.Event('click', { bubbles: true, cancelable: true }));
  await new Promise(res => setTimeout(res, 200));
  const detView2 = doc.getElementById('view-carteiradetalhe');
  const detTable2 = detView2 ? detView2.querySelector('table.amort-table') : null;
  check('Sub-página abertura mensal: usa estilo .amort-table (redesenhada)', !!detTable2);
  const groupHeadCells = detTable2 ? detTable2.querySelectorAll('thead tr.grouphead th') : [];
  const subHeadCells = detTable2 ? detTable2.querySelectorAll('thead tr.subhead th') : [];
  check('Sub-página abertura mensal: cabeçalho de grupo AXIS/SYNC/Consolidado', groupHeadCells.length === 4 && [...groupHeadCells].some(c=>c.textContent.trim()==='AXIS') && [...groupHeadCells].some(c=>c.textContent.trim()==='SYNC') && [...groupHeadCells].some(c=>c.textContent.trim()==='Consolidado'));
  check('Sub-página abertura mensal: 15 colunas de dado (6 AXIS + 6 SYNC + 3 consolidado -- revertido na 43ª rodada, ponto 4: usuário pediu de volta o dado completo sem empilhar células)', subHeadCells.length === 15);
  check('Sub-página abertura mensal: Área e Preço Médio por torre presentes (dado que estava faltando)', detTxt.includes('Área') && detTxt.includes('Preço Médio') && detTxt.includes('Preço LTM'));
  const backBtn2 = doc.getElementById('carteiradetalhe-back');
  if (backBtn2) backBtn2.click();
  await new Promise(res => setTimeout(res, 200));
  win.showDetail('MSB Axis');
  await new Promise(res => setTimeout(res, 250));

  // Pt.6: gráficos IC e Obra corrigidos
  // 45ª rodada: os 2 gráficos viraram ECharts (mount div + echarts.init em runtime de
  // navegador de verdade) -- sob JSDOM o `echarts` global nunca existe (script externo não
  // executa nesse harness), então mountEChart só devolve null sem desenhar nada, e não há
  // mais <text>/<path>/<line>/<rect> de SVG desenhado à mão pra inspecionar aqui (mesmo
  // padrão já usado em test_alianza.js pros gráficos de barra). O que dá pra verificar sob
  // JSDOM é a estrutura estática ao redor do gráfico (mount div presente, legenda/nota em
  // HTML) -- a renderização de fato (eixo, linha, cores, rótulos) já foi verificada
  // visualmente via Playwright (zfix_*/echarts_*.png).
  const fluxoBody2 = doc.getElementById('fluxo-charts');
  check('Gráfico IC: mount ECharts presente (#chart-icp)', !!fluxoBody2 && !!fluxoBody2.querySelector('#chart-icp.echart-mount'));
  const icpLegend = fluxoBody2 ? fluxoBody2.querySelector('.chart-legend') : null;
  const icpLegendTxt = icpLegend ? icpLegend.textContent : '';
  check('Gráfico IC: legenda "IC Histórico + Projetado" / "IC Mínimo" presente', icpLegendTxt.includes('IC Histórico + Projetado') && icpLegendTxt.includes('IC Mínimo'));
  const obraLegend = [...fluxoBody2.querySelectorAll('.chart-legend')].find(l=>l.textContent.includes('Previsto Mês'));
  check('Gráfico Obra: legenda com as 4 séries (Previsto/Realizado Mês/Acum.)', !!obraLegend && obraLegend.textContent.includes('Realizado Acum.'));
  check('Gráfico Obra: mount ECharts presente (#chart-obra)', !!fluxoBody2 && !!fluxoBody2.querySelector('#chart-obra.echart-mount'));

  console.log('\n=== TOTAL FAILURES ===', fails);
  win.close();
  process.exit(fails > 0 ? 1 : 0);
})();
