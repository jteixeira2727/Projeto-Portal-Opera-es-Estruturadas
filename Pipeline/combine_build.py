import json

with open('portfolio_data_wrapped.json', 'r', encoding='utf-8') as f:
    wrapped_text = f.read()
# validate
json.loads(wrapped_text)

with open('portal_template.html', 'r', encoding='utf-8') as f:
    tpl = f.read()

out = tpl.replace('__PORTFOLIO_DATA_JSON__', wrapped_text)

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(out)

with open('portal_publish.html', 'w', encoding='utf-8') as f:
    f.write(out)

localtest = out.replace(
    'https://cdnjs.cloudflare.com/ajax/libs/echarts/6.1.0/echarts.min.js',
    '_test_echarts.min.js'
)
with open('portal_localtest.html', 'w', encoding='utf-8') as f:
    f.write(localtest)

print('bytes portal_publish.html:', len(out))
