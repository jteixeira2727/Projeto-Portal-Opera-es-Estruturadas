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

  window.onerror = (msg, src, line, col, err) => {
    errors.push(`${msg} (line ${line})`);
  };
  window.scrollTo = () => {};
  window.HTMLElement.prototype.scrollTo = () => {};

  await new Promise(r => setTimeout(r, 1000));
  const doc = window.document;

  console.log('=== Initial load ===');
  console.log('errors so far:', errors.length, errors);
  console.log('sidebar items:', doc.querySelectorAll('.opitem').length);
  console.log('overview rows:', doc.querySelectorAll('#view-overview table tbody tr').length);

  // click every sidebar operation and check the detail view populates without new errors
  const names = [...doc.querySelectorAll('.opitem')].map(el => el.textContent.trim());
  console.log('\n=== Clicking through all', names.length, 'operations ===');
  let failures = [];
  for (const item of [...doc.querySelectorAll('.opitem')]) {
    const before = errors.length;
    item.dispatchEvent(new window.Event('click', { bubbles: true }));
    await new Promise(r => setTimeout(r, 20));
    const detailView = doc.getElementById('view-detail');
    const h2 = detailView.querySelector('#detail-head h2');
    const ok = detailView.className.includes('active') && h2 && detailView.innerHTML.length > 500;
    if (!ok || errors.length > before) {
      failures.push({name: item.textContent.trim(), ok, newErrors: errors.slice(before)});
    }
  }
  console.log('failures:', failures.length);
  if (failures.length) console.log(JSON.stringify(failures, null, 1));

  // spot check a few specific operations for expected content
  console.log('\n=== Spot checks ===');
  function checkOp(name, expectFundPositions) {
    const item = [...doc.querySelectorAll('.opitem')].find(el => el.textContent.trim() === name);
    if (!item) { console.log(name, '-> NOT FOUND IN SIDEBAR'); return; }
    item.dispatchEvent(new window.Event('click', { bubbles: true }));
    const dv = doc.getElementById('view-detail');
    const hasFP = dv.innerHTML.includes('Posição por Fundo');
    console.log(name, '-> fund positions panel present:', hasFP, '(expected', expectFundPositions, ')', hasFP===expectFundPositions ? 'OK' : 'MISMATCH');
    const hasAmortTable = dv.innerHTML.includes('Tabela de amortização mensal');
    console.log('   amortization table label present:', hasAmortTable);
  }
  checkOp('Habibs', true);
  checkOp('CVPAR', false);
  checkOp('Renda Residencial', true);
  checkOp('Calçada', true);
  checkOp('PKK', true);

  // acompanhamento view (48ª rodada: 1 aba só de novo, com sub-abas internas Obrigações/Ordinário)
  console.log('\n=== Acompanhamento view (sub-abas Obrigações / Ordinário) ===');
  const acompTab = [...doc.querySelectorAll('.navtab')].find(t => t.dataset.view === 'acomp');
  if (acompTab) {
    acompTab.dispatchEvent(new window.Event('click', { bubbles: true }));
    await new Promise(r => setTimeout(r, 50));
    for (const sub of ['obrig', 'ord']) {
      const subtab = doc.querySelector(`.acomp-subtab[data-sub="${sub}"]`);
      if (subtab) {
        subtab.dispatchEvent(new window.Event('click', { bubbles: true }));
        await new Promise(r => setTimeout(r, 50));
        console.log(`sub-aba ${sub} rows:`, doc.querySelectorAll('#acomp-subview table tbody tr').length);
      } else {
        console.log(sub, 'sub-aba not found');
      }
    }
  } else {
    console.log('acomp navtab not found');
  }

  console.log('\n=== TOTAL ERRORS ===', errors.length);
  errors.slice(0,10).forEach(e => console.log(' -', e));
})().catch(e => {
  console.log('SCRIPT THREW:', e);
});
