# Railway Deployment Guide

## Setup Rápido (5 minutos)

### 1. Criar Conta Train (se não tiver)
- Vá para https://railway.app
- Clique "Login with GitHub"
- Autorize Railway

### 2. Nova Aplicação
1. Clique "Create New Project"
2. Selecione "Deploy from GitHub repo"
3. Autorize Railway no GitHub
4. Selecione repositório "ProjetoSiteMogi"
5. Clique "Deploy"

### 3. Configurar Variáveis de Ambiente
No Railway Dashboard:

1. Vá em "Variables" (ao lado de "Deployments")
2. Adicione TODAS estas variáveis:

```
DATABASE_URL=               # ← Deixe vazio (Railway cria automaticamente se adicionar PostgreSQL)
SECRET_KEY=                 # ← Railway gera automaticamente
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
DEBUG=false
API_TITLE=Bom Contato API
API_VERSION=1.0.0

# S3 / Object Storage (use seus valores atuais)
STORAGE_ENDPOINT_URL=https://seu-bucket.region.linodestorage.com
STORAGE_BUCKET_NAME=seu-bucket-name
STORAGE_ACCESS_KEY_ID=sua-chave
STORAGE_SECRET_ACCESS_KEY=sua-chave-secreta
STORAGE_REGION=auto
STORAGE_PUBLIC_BASE_URL=https://seu-bucket.region.linodestorage.com

# SMTP (se configurado)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu-email@gmail.com
SMTP_PASSWORD=sua-senha
SMTP_FROM_EMAIL=seu-email@gmail.com
SMTP_FROM_NAME=Bom Contato
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

### 4. Adicionar PostgreSQL (Se não tiver)
1. No Railway Dashboard
2. Clique "Marketplace" (ícone de pacotes)
3. Procure "PostgreSQL"
4. Clique "+ Add"
5. Railway conecta automaticamente (variável DATABASE_URL)

### 5. Deploy
1. Clique "Deploy Now"
2. Vá em "Deployments" e acompanhe o log
3. Quando aparecer ✓ verde = sucesso!

## Variáveis de Ambiente Necessárias

Railway fornece automaticamente:
- ✅ `DATABASE_URL` (se adicionar PostgreSQL)
- ✅ `PORT` (seu app escuta nesta porta)

Você adiciona manualmente:
- ✅ `STORAGE_*` (seu S3 externo)
- ✅ `SMTP_*` (seu email)
- ✅ `SECRET_KEY` (Rails gera, mas pode customizar)

## Se Der Erro no Deploy

1. Vá em "Deployments"
2. Clique no deployment que falhou
3. Veja os logs completos
4. Procure por primeira mensagem de erro
5. Compartilhe aqui se precisar help

## Diferenças Render → Railway

| Aspecto | Render | Railway |
|--------|--------|---------|
| Deploy | render.yaml | railway.json (simples) |
| Banco | Integrado | Marketplace |
| Logs | Separados | Integrados |
| Variáveis | Dashboard | Dashboard + railway.json |
| URL | Nome customizado | Automática primeiro, depois custom |

## Após Deploy Bem-Sucedido

1. Sua app estará em `https://seu-projeto.railway.app`
2. Vá em "Deployment" → "Domain" para customizar URL
3. API Docs estarão em `https://seu-projeto.railway.app/docs`

## Rollback (se precisar de emergência)

Railway mantém histórico de deploys:
1. Vá em "Deployments"
2. Clique no deploy anterior
3. Clique "Redeploy"

## Chat Support Railway

Se tiver dúvida:
1. Railway tem Discord muito ativo
2. Ou vá em "Help" na Dashboard

## Troubleshooting S3

Se o bucket ainda der problema:

### Teste 1: Credenciais
```python
cd backend
python -c "
import os
os.environ['STORAGE_ENDPOINT_URL'] = 'seu-endpoint'
os.environ['STORAGE_BUCKET_NAME'] = 'seu-bucket'
os.environ['STORAGE_ACCESS_KEY_ID'] = 'sua-chave'
os.environ['STORAGE_SECRET_ACCESS_KEY'] = 'sua-secreta'

from app.services.storage import is_storage_configured
print('Storage configured:', is_storage_configured())
"
```

### Teste 2: Upload File
```python
from app.services.storage import upload_bytes
result = upload_bytes(b'teste', 'test.txt', 'test')
print(result)
```

Se ainda der `AccessDenied`:
- Vá em seu provedor S3 (Linode/DigitalOcean)
- Regenere a chave de acesso
- Adicione permissões: `s3:GetObject`, `s3:PutObject`

## URLs Customizadas

Após deploy:

1. Railway gera URL automática: `seu-projeto-xxxx.railway.app`
2. Para customizar, vá em projeto → Settings → Networking
3. Adicione domínio customizado (requer DNS)

---

**Próximo passo:** Faça commit, crie conta Railway, e faça push!
