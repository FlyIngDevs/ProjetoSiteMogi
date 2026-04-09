# MIGRAÇÃO RENDER → RAILWAY
# Passo a Passo Detalhado

## ANTES DE COMEÇAR

Você vai precisar:
- [ ] Conta GitHub (já tem)
- [ ] Conta Railway (crie em https://railway.app)
- [ ] Credenciais S3 funcionando
- [ ] URL do banco de dados (se tiver no Render)

---

## ETAPA 1: Preparar Código Local (10 min)

### 1.1 Verificar que tudo funciona
```bash
cd backend
python diagnose.py          # ✓ Deve passar
python run.py               # ✓ Deve iniciar
```

### 1.2 Commit final para Render (clean up)
```bash
git add -A
git commit -m "chore: Ready for Railway migration"
git push
```

### 1.3 Testar Dockerfile localmente (opcional)
```bash
docker build -t bom-contato:latest .
docker run -p 8000:8000 bom-contato:latest
# Visite http://localhost:8000/docs
```

---

## ETAPA 2: Setup Railway (5 min)

### 2.1 Criar Conta
1. Vá para https://railway.app
2. Clique "Login with GitHub"
3. Autorize com suas credenciais GitHub

### 2.2 Criar Novo Projeto
1. Dashboard inicio → "Create New Project"
2. Clique "+ New Project"
3. Selecione "Deploy from GitHub repo"
4. Autorize Railway a acessar GitHub
5. Procure "ProjetoSiteMogi"
6. Clique para selecionar

Railway vai:
- ✓ Detectar Dockerfile
- ✓ Criar container automaticamente
- ✓ Começar deploy (vai dar erro por enquanto - esperado)

### 2.3 Esperar Build Falhar (normal)
A primeira tentativa vai falhar porque faltam variáveis de ambiente.

---

## ETAPA 3: Adicionar PostgreSQL (3 min)

Railway pode criar banco automaticamente OU usar o existente.

### Opção A: Novo banco PostgreSQL (recomendado)
1. No dashboard do projeto, clique "Marketplace" (ícone de pacotes)
2. Procure "PostgreSQL"
3. Clique "+ Add to Project"
4. Aceitar defaults
5. Railway automaticamente:
   - ✓ Cria banco
   - ✓ Gera `DATABASE_URL`
   - ✓ Conecta ao seu app

### Opção B: Usar banco existente (Render)
1. Vá em "Variables" do seu app
2. Adicione manualmente:
```
DATABASE_URL=postgresql://user:pass@render-host:5432/database
```

---

## ETAPA 4: Configurar Variáveis de Ambiente (5 min)

No dashboard do seu projeto:

1. Clique no serviço (seu app, não PostgreSQL)
2. Vá em "Variables"
3. Adicione CADA uma dessas (copie/cole):

**Básicas:**
```
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
DEBUG=false
API_TITLE=Bom Contato API
API_VERSION=1.0.0
```

**S3/Storage (COPIE SEUS VALORES ATUAIS):**
```
STORAGE_ENDPOINT_URL=https://seu-bucket.region.linodestorage.com
STORAGE_BUCKET_NAME=seu-bucket-name
STORAGE_ACCESS_KEY_ID=sua-chave-aqui
STORAGE_SECRET_ACCESS_KEY=sua-chave-secreta-aqui
STORAGE_REGION=auto
STORAGE_PUBLIC_BASE_URL=https://seu-bucket.region.linodestorage.com
```

**SMTP (se configurado):**
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-aqui
SMTP_FROM_EMAIL=seu-email@gmail.com
SMTP_FROM_NAME=Bom Contato
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

⚠️ **IMPORTANTE:** Clique "Save" após CADA variável!

---

## ETAPA 5: Trigger Deploy (2 min)

Railway detecta automaticamente:
- ✓ Se você fez push (conecta a GitHub)
- ✓ Se você adicionou variáveis
- ✓ E refaz o deploy

Ou force manualmente:
1. Vá em "Deployments"
2. Clique "Trigger Deploy" ou espere auto-deploy

---

## ETAPA 6: Monitorar Deploy (5 min)

### Logs em Tempo Real
1. Clique em "Deployments"
2. Selecione o deploy que está rodando
3. Veja logs ao vivo

**Você deve ver:**
```
[1/4] Loading environment...
  ✓ Loading environment variables
[2/4] Initializing FastAPI application...
  ✓ Config imported
  ✓ Database imported
[3/4] Setting up database...
  ✓ Database tables created
[4/4] Verifying application...
  ✓ App verified

✓✓✓ STARTUP SEQUENCE COMPLETE ✓✓✓
```

### Se der erro:
1. Procure primeira linha com `✗`
2. Leia mensagem de erro completa
3. Compartilhe comigo

---

## ETAPA 7: Testar URL (2 min)

1. No dashboard, procure "Deployment"
2. Clique no serviço (vai mostrar URL)
3. URL padrão: `https://seu-projeto-xxxx.railway.app`

**Testes:**
```
✓ https://seu-projeto-xxxx.railway.app/health
  → Deve retornar {"status":"healthy"}

✓ https://seu-projeto-xxxx.railway.app/docs
  → Deve abrir Swagger UI

✓ POST https://seu-projeto-xxxx.railway.app/api/auth/register
  → Testa integração com banco
```

---

## ETAPA 8: Custom Domain (opcional, 2 min)

Se quiser URL customizada:

1. Vá em "Settings" do seu serviço
2. Procure "Custom Domain" ou "Networking"
3. Adicione seu domínio (ex: `api.bomcontato.com`)
4. Configure DNS no seu provedor de domínio

---

## ETAPA 9: Remover Render (when ready)

Agora que tudo está em Railway:

1. Vá em https://dashboard.render.com
2. Clique em seu serviço "shoppinghub"
3. Settings → Scroll down
4. Clique "Delete Service"
5. Confirme

---

## TROUBLESHOOTING S3

Se bucket continuar com `AccessDenied`:

### Check 1: Credenciais
Em Railway Variables, copie exatos seus valores:
- [ ] STORAGE_ENDPOINT_URL - correto?
- [ ] STORAGE_BUCKET_NAME - correto?
- [ ] STORAGE_ACCESS_KEY_ID - recém gerado?
- [ ] STORAGE_SECRET_ACCESS_KEY - correto?

### Check 2: Permissões S3
Seu provedor (Linode/DigitalOcean/AWS):
1. Regenere credenciais (às vezes ajuda)
2. Certifique que tem permissões:
   - `s3:PutObject` ← para upload
   - `s3:GetObject` ← para leitura
   - `s3:DeleteObject` ← para delete

### Check 3: CORS S3 (se público)
Se uploads públicos, S3 pode pedir CORS configurado.

---

## COMPARAÇÃO: Render vs Railway

| Feature | Render | Railway |
|---------|--------|---------|
| Auto-redeploy | ✓ | ✓ |
| PostgreSQL | ✓ Integrado | ✓ Marketplace |
| Logs | Bons | Melhores |
| Performance | Bom | Excelente |
| Preço | ~$15/mo | ~$5/mo (grátis com limites) |
| Suporte | Discord | Discord (muito ativo) |

---

## FASE FINAL

Após tudo funcionar:

1. [ ] URL Railway funciona
2. [ ] Banco funciona
3. [ ] Uploads S3 funcionam
4. [ ] API /docs funciona
5. [ ] Deletar de Render

**Pronto!** 🎉 Você está em Railway!

---

**Tempo total estimado:** ~20-30 minutos
**Problemas?** Compartilhe logs e ajudamos!
