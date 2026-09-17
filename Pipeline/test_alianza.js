const { JSDOM } = require('jsdom');
const fs = require('fs');

const html = fs.readFileSync('./portal_publish.html', 'utf-8');
let errors = [];

(async () => {
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    resources: 'usable',
    url: 'https://example.com/portal.html',
    pretendToBeVisual: true,
  });
  const { window } = dom;
  window.onerror = (msg, src, line, col, err) => { errors.push(`${msg} (line ${line})`); };
  window.scrollTo = () => {};
  window.HTMLElement.prototype.scrollTo = () => {};

  await new Promise(r => setTimeout(r, 1000));
  const doc = window.document;

  const items = [...doc.querySelectorAll('.opitem')];
  const target = items.find(el => el.textContent.includes('Alianza GRU e Mauá'));
  console.log('found sidebar item:', !!target);
  target.dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
  await new Promise(r => setTimeout(r, 300));

  console.log('errors after click:', errors.length, errors);

  const view = doc.getElementById('view-detail');
  const qstats = [...view.querySelectorAll('#quickstats .qstat')].map(el => el.textContent.trim().replace(/\s+/g,' '));
  console.log('=== quickstats ===');
  qstats.forEach(q => console.log(' ', q));

  console.log('=== fund positions rows ===');
  console.log(view.querySelectorAll('.fundpos-table tbody tr').length);

  console.log('=== caracteristicas (ativo-compare-table count) ===');
  console.log(view.querySelectorAll('.ativo-compare-table').length, '(expect 2: caracteristicas + garantias)');

  console.log('=== garantias meta ===');
  const garantiasMeta = [...view.querySelectorAll('.panel-head .meta')].map(e=>e.textContent);
  console.log(garantiasMeta);

  console.log('=== locacoes galpao rows ===');
  const locTable = view.querySelector('.loc-table');
  console.log('loc-table found:', !!locTable);
  if (locTable) {
    console.log('rows:', locTable.querySelectorAll('tbody tr').length);
    console.log('total rows (locrow-total):', locTable.querySelectorAll('tbody tr.locrow-total').length);
  }

  console.log('=== highlights ===');
  console.log([...view.querySelectorAll('.highlights-list li')].map(e=>e.textContent.trim().slice(0,80)));

  console.log('=== sobre operacao ===');
  console.log(view.querySelectorAll('.sobre-bullets li').length, 'bullets');

  console.log('=== covenants items ===');
  console.log([...view.querySelectorAll('.covitem .item')].map(e=>e.textContent));

  console.log('=== fluxo charts (after render) ===');
  await new Promise(r => setTimeout(r, 300));
  const chartboxes = [...view.querySelectorAll('.chartbox h3')].map(e=>e.textContent);
  console.log(chartboxes);
  const svgs = view.querySelectorAll('#fluxo-charts svg');
  console.log('svg count:', svgs.length);
  const ltvCallouts = [...view.querySelectorAll('.chart-callout')].map(e=>e.textContent);
  console.log('ltv callouts:', ltvCallouts);
  const icLegend = [...view.querySelectorAll('.chart-legend span')].map(e=>e.textContent);
  console.log('ic legend:', icLegend);

  console.log('=== TOTAL ERRORS ===', errors.length);
})();
