# 📋 Pedidos EBD 2026 — App Web

## Como colocar no ar (Render grátis)

### Passo 1 — Sobe no GitHub
1. Cria um repositório no GitHub (ex: `ebd-pedidos-2026`)
2. Faz upload de TODOS os arquivos desta pasta:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - pasta `templates/` com o `index.html`

### Passo 2 — Conecta no Render
1. Acessa https://render.com e cria conta grátis
2. Clica em **New > Web Service**
3. Conecta com seu GitHub e seleciona o repositório `ebd-pedidos-2026`
4. Configura:
   - **Name:** ebd-pedidos-2026
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Clica em **Create Web Service**

### Passo 3 — Pronto!
- O Render vai gerar um link tipo: `https://ebd-pedidos-2026.onrender.com`
- Manda o link pra outra secretária — as duas editam ao mesmo tempo!

## Observação importante
O Render grátis "dorme" após 15 min sem acesso.
Na primeira vez que abrir depois de um tempo, demora ~30 segundos pra acordar.
