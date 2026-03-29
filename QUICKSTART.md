# Quick Start - ShoppingHub

## Inicio rapido

### Backend

```bash
cd backend
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

Se quiser sobrescrever as configuracoes padrao, copie `backend/.env.example` para `backend/.env`.

Para popular o banco com dados de exemplo:

```bash
python seed_data.py
```

Para subir a API:

```bash
uvicorn main:app --reload
```

API: `http://localhost:8000`
Docs: `http://localhost:8000/docs`

### Frontend

Em outro terminal:

```bash
cd frontend
python -m http.server 8080
```

Frontend: `http://localhost:8080`

### Painel admin

- URL: `http://localhost:3000/pages/admin.html` ou `http://localhost:8080/pages/admin.html`
- se ainda nao existir admin, faca login com uma conta comum e use o botao para promover esta conta

### Candidatura com curriculo

- o botao `Candidatar-se` envia nome, contato, mensagem e curriculo para o e-mail da vaga
- configure SMTP em `backend/.env` usando o arquivo `backend/.env.example`
- formatos aceitos para curriculo: `PDF`, `DOC` e `DOCX`

## Testes rapidos

```bash
curl http://localhost:8000/api/annotators/
curl http://localhost:8000/api/jobs/
curl http://localhost:8000/api/carousel/
curl http://localhost:8000/api/sponsorships/
```

## Docker

```bash
docker-compose up -d
docker-compose down
```

## Solucao de problemas

### CORS
- confirme que o backend esta em `http://localhost:8000`
- confirme que o frontend esta em `http://localhost:8080` ou `http://127.0.0.1:8080`

### Banco local
- o SQLite de desenvolvimento fica em `backend/shopping.db`
- para recriar do zero, remova o arquivo e suba a API novamente

### Porta ocupada no Windows

```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## Deploy no Render

- o projeto inclui `render.yaml`
- o backend passa a servir o frontend no mesmo dominio
- em producao, use PostgreSQL e disco persistente para `uploads`
- configure no Render, se necessario:
  - `SMTP_HOST`
  - `SMTP_PORT`
  - `SMTP_USERNAME`
  - `SMTP_PASSWORD`
  - `SMTP_FROM_EMAIL`
