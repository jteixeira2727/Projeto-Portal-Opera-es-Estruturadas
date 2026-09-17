# Como usar esta pasta com o Claude Code

Este é o pipeline do Portal de Operações, pronto pra ser aberto com o
**Claude Code** (a versão do Claude que roda no terminal, direto nos seus
arquivos — diferente do chat do claude.ai). O `CLAUDE.md` nesta pasta já
documenta a arquitetura pro Claude Code ler sozinho assim que você abrir
uma sessão aqui.

## 1. Instalar o Claude Code (uma vez só)

No PowerShell, rode:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Não precisa instalar Node.js nem nada além disso. Recomendado (opcional):
instalar o [Git para Windows](https://git-scm.com/downloads/win), pra o
Claude Code poder usar Bash em vez de só PowerShell.

## 2. Entrar com sua conta

Na primeira vez que rodar `claude`, ele abre o navegador pra você logar —
usa a MESMA conta/assinatura do claude.ai (Pro, Max ou Team), sem
cobrança separada. Precisa ser plano pago (não funciona no gratuito).

## 3. Abrir esta pasta

```powershell
cd "C:\Users\joao.teixeira\OneDrive - JIVE INVESTMENTS CONSULTORIA LTDA\Área de Trabalho\Projeto Portal Operações Estruturadas\Pipeline"
claude
```

Ele já vai ler o `CLAUDE.md` automaticamente como contexto do projeto.

## 4. Rodar o build localmente

```powershell
python build_data.py        # regenera portfolio_data.json (demora ~3-5min)
python combine_build.py     # funde template + dados -> portal_publish.html
```

(Requer Python 3 com as bibliotecas que `build_data.py` importa —
peça pro próprio Claude Code checar/instalar o que faltar.)

## 5. Rodar os testes de regressão

```powershell
npm install
node test_dom2.js
node test_alianza.js
node test_alianza_topics.js
node test_msbaxis.js
```

Esperado: 0 erros/falhas em todos.

## Importante: publicar não é daqui

O Claude Code local edita arquivos nesta pasta, mas **não publica** a
nova versão do Portal (isso só é feito pela ferramenta de Artifact, que
só existe dentro de uma conversa no claude.ai/app desktop). Fluxo normal:
edite e teste aqui localmente até ficar certo do resultado, depois leve o
`portal_publish.html` final pra uma conversa no claude.ai pra publicar de
fato — ver detalhes no `CLAUDE.md`.
