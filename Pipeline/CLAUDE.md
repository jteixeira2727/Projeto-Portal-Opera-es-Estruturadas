# Portal de Operações — pipeline de dados e template

Este projeto gera o **Portal de Operações** da Mauá Capital (JiveMauá): um
dashboard interno (HTML único, ~12MB) publicado como Artifact em
https://claude.ai/artifact/GtYDGjFBk2jqQZRXUfMG2n, usado pelo time de
Real Estate para acompanhar o portfólio de crédito estruturado (CRI/FIDC).

Existe também um artifact "vault" só de armazenamento de arquivos, usado
para sincronizar este pipeline entre sessões (não é uma página pra
visualizar): https://claude.ai/artifact/HhrgT2u4sSZfW8C2D539fp

## Como o build funciona

1. `build_data.py` lê a planilha financeira do João (`ativos.xlsx`, não
   incluída aqui — vem da pasta `Operações`/anexos do projeto),
   `documents_meta.json` e `obligations_data.json`, e escreve
   `portfolio_data.json`.
2. Um passo de "wrap" (histórico manual, ver Notas abaixo) combina
   `portfolio_data.json` de vários meses num único
   `portfolio_data_wrapped.json`, com a chave `months["AAAA-MM"]` por mês
   (ex.: `months["2026-07"]`). **Este é o arquivo que o template consome.**
3. `combine_build.py` funde `portal_template.html` (CSS/JS/estrutura) com
   `portfolio_data_wrapped.json` (substituindo o placeholder
   `__PORTFOLIO_DATA_JSON__`), gerando `portal.html` / `portal_publish.html`
   / `portal_localtest.html` (idênticos, exceto que o `_localtest` troca o
   CDN do ECharts por um arquivo local `_test_echarts.min.js`, que não foi
   trazido pra este pacote — só é necessário rodando dentro da sessão de
   nuvem original).
4. `extract_documents.py` faz a extração de texto (com OCR quando preciso)
   dos PDFs/DOCX de cada operação, escrevendo `documents_data.json` — um
   cache caro de gerar (rodar de novo só se novos documentos entrarem).

## Arquivos de dados

- `documents_meta.json` — schema:
  `{instrumentos: [{tipo, nome, nome_curto, data_original,
  original_presente_na_pasta, aditamentos_conhecidos:[{numero, data,
  presente_na_pasta}], presente_na_pasta, completo,
  versao_mais_recente_na_pasta, gap, nota}], metodologia_nota}` por operação
  — construído por `build_doc_instrumentos()` em `build_data.py`.
- `obligations_data.json` — schema:
  `{<nome_operacao>: {reviewed, latest_ata_data, latest_ata_arquivo, items:
  [...], observacao_reviewer}}`. `observacao_reviewer` (o "aviso" do
  revisor) fica no dado mas **não é renderizado** no portal (pedido
  explícito do usuário).
- `documents_data.json` — texto extraído de todos os documentos já lidos
  (cache de `extract_documents.py`).
- `portfolio_data_wrapped.json` — snapshot mensal completo, já publicado.

## Publicar uma nova versão

**Importante**: o Claude Code local (rodando neste computador) só edita
arquivos — ele **não publica Artifacts**. Publicar o `portal_publish.html`
atualizado como nova versão do Portal (e sincronizar o vault) só é
possível de dentro de uma conversa no claude.ai/desktop app que tenha a
ferramenta Artifact — não pelo Claude Code CLI.

Fluxo recomendado: edite/teste localmente aqui com o Claude Code até o
`portal_publish.html` (gerado por `combine_build.py`) ficar do jeito
esperado (rode os testes, veja um screenshot local), depois leve esse
`portal_publish.html` final pra uma conversa no claude.ai (anexando o
arquivo ou pedindo pra sincronizar a partir desta pasta) pra de fato
publicar.

## Testes de regressão

`test_dom2.js`, `test_alianza.js`, `test_alianza_topics.js`,
`test_msbaxis.js` — todos leem `./portal_publish.html` via JSDOM e
verificam presença/estrutura de elementos-chave (sem servidor, sem
browser real). Rodar com `node <arquivo>.js`; esperado: 0 erros/falhas em
todos. Precisam de `npm install` primeiro (dependência: `jsdom`).

Não incluídos neste pacote (ficaram só na sessão de nuvem original, por
serem descartáveis/específicos daquele ambiente): dezenas de scripts de
diagnóstico visual pontuais (`check_*.js`, `shot_*.js`, `screenshot_*.py`,
capturas de tela `.png` de rodadas anteriores) e variantes antigas de
`portfolio_data*.json` (backups intermediários de rodadas passadas).

## Notas / decisões não óbvias (evite redescobrir isso)

- **Alinhamento de gráficos ECharts** (`echartsBarOption` vs
  `echartsGroupedBarOption`): grids com `labelBars`/rótulos por barra
  reservam `grid.top` diferente internamente (34px vs 18px) — uma
  diferença invisível comparando só a altura do `<div>` container por
  fora. Pra medir de verdade, use a API interna do ECharts:
  `echarts.getInstanceByDom(el).getModel().getComponent('grid',0)
  .coordinateSystem.getRect()` — dá a posição exata da área de plotagem.
  Já foi a causa de 2 correções "confirmadas" que na prática não
  resolveram o problema — sempre medir assim antes de declarar resolvido.
- **`build_data.py` demora ~3-5 min** — rode em background
  (`nohup python3 build_data.py > log.txt 2>&1 &` no Linux; no Windows,
  `Start-Process` ou deixe rodando numa aba separada) se o terminal tiver
  timeout curto.
- Emojis foram removidos de toda a UI (pedido explícito do usuário).
- O painel "Consultar Documentos" (chat de IA dentro do portal) só
  funciona dentro do Artifact publicado no claude.ai (usa a capability
  `sample`, que pede consentimento de cada usuário) — abrir
  `portal_publish.html` localmente no navegador não ativa esse chat.
