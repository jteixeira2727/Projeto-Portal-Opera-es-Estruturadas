const { JSDOM } = require('jsdom');
const fs = require('fs');

const html = fs.readFileSync('./portal_publish.html', 'utf-8');
let errors = [];

(async () => {
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', resources: 'usable',
    url: 'https://example.com/portal.html', pretendToBeVisual: true,
  });
  const { window } = dom;
  window.onerror = (msg, src, line) => { errors.push(`${msg} (line ${line})`); };
  window.scrollTo = () => {};
  window.HTMLElement.prototype.scrollTo = () => {};
  await new Promise(r => setTimeout(r, 1000));
  const doc = window.document;

  const items = [...doc.querySelectorAll('.opitem')];
  const target = items.find(el => el.textContent.includes('Alianza GRU e Mauá'));
  target.dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
  await new Promise(r => setTimeout(r, 300));

  const links = [...doc.querySelectorAll('.topics-link')];
  console.log('topics links found:', links.map(a => a.textContent.trim()));

  for (const linkText of ['Ver obrigações', 'Ver regras de quórum']) {
    const link = links.find(a => a.textContent.includes(linkText));
    console.log('\n=== clicking:', linkText, '===');
    link.dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
    await new Promise(r => setTimeout(r, 200));
    const view = doc.getElementById('view-topics');
    console.log('h2:', view.querySelector('#detail-head h2')?.textContent);
    console.log('fonte:', view.querySelector('.topics-fonte')?.textContent);
    console.log('sections:', view.querySelectorAll('.topicsec').length);
    console.log('topiclist items:', view.querySelectorAll('.topicitem').length);
    console.log('compare cards:', view.querySelectorAll('.topiccompare-card').length);
    console.log('ordered list items:', view.querySelectorAll('.topiclist-ordered li').length);
    console.log('highlight sections:', view.querySelectorAll('.topicsec-highlight').length);
    // back button
    const back = doc.getElementById('topics-back');
    back.dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
    await new Promise(r => setTimeout(r, 200));
  }

  console.log('\n=== TOTAL ERRORS ===', errors.length, errors);
})();
