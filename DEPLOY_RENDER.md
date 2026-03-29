# Deploy para Render - Guia Rápido

## Situação Atual
Você está recebendo:
```
ERRO: Erro carregando o app ASGI. Não foi possível importar o módulo "main".
```

## Solução Implementada

Adicionei debug detalhado ao código para identificar exatamente onde falha a importação. Agora você vai ver mensagens como:

```
✓ FastAPI imports successful
✓ Config imported
✓ Database imported
✓ Routes imported
✓✓✓ MAIN.PY INITIALIZATION COMPLETE ✓✓✓
```

## Como Fazer Deploy Correto

### Passo 1: Teste Local (Obrigatório)
```bash
cd backend

# Primeiro verifique tudo
python preflight.py

# Se passou, execute a aplicação
python run.py
```

Se `preflight.py` falhar,corrija os erros ANTES de fazer push.

### Passo 2: Commit e Push
```bash
git add -A
git commit -m "Fix: Add detailed ASGI debugging and improved startup"
git push origin main
```

### Passo 3: Deploy no Render

**Opção A - Se Render usar Auto-Deploy:**
- Espere o deploy começar automaticamente
- Monitoré em Logs (veja abaixo)

**Opção B - Deploy Manual (Recomendado):**
1. Va para https://dashboard.render.com
2. Clique em "shoppinghub"
3. Clique em "Settings" no topo
4. Role para baixo até "Build" section
5. Clique "Clear Cache"
6. Clique em "Manual Deploy" → "Deploy latest commit"
7. Aguarde e monitore

### Passo 4: Monitore os Logs
1. Na dashboard: clique "Logs"
2. Procure pelas mensagens `✓` para confirmar cada etapa
3. A primeira mensagem `✗` indica onde está o problema

## Você Deve Vêr Esta Sequência

```
Build started...
pip install -r requirements.txt
...
Build with success 🎉

Deploying...
[1/4] Loading environment...
  ✓ Loading .env or using environment variables
[2/4] Initializing FastAPI application...
  ✓ Application created: Shopping Platform API
[3/4] Setting up database...
  ✓ Database engine initialized
  ✓ Database tables created
  ✓ Database connection working
[4/4] Verifying application...
  ✓ App verified (X routes)

✓✓✓ STARTUP SEQUENCE COMPLETE - STARTING SERVER ✓✓✓

Server starting on http://0.0.0.0:8000
API Documentation: http://localhost:8000/docs

INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Se Continuar Dando Erro

### Verificação 1: Logs Detalhados
1. Vá em Logs
2. Procure por primeira linha com`✗`
3. Leia a mensagem de erro completa
4. Procure em `RENDER_TROUBLESHOOTING.md` por solução

### Verificação 2: Git Push bem-sucedido?
```bash
# Confirm que todos os arquivos foram enviados
git log --oneline -5
git status  # Deve estar clean
```

### Verificação 3: Render detectou mudança?
1. Va em "Settings" do seu serviço
2. Clique "Clear Cache"
3. Faça "Manual Deploy"

## Arquivos-Chave Adicionados/Modificados

### Novos Arquivos
- `preflight.py` - Testa tudo localmente antes de deploy
- `run.py` - Runner aperfeiçoado com logging detalhado
- `wsgi.py` - Fallback WSGI (em último caso)
- `RENDER_TROUBLESHOOTING.md` - Guia completo

### Arquivos Modificados
- `main.py` - Adicionado debugging em cada etapa
- `render.yaml` - Configuração atualizada

## Próximos 15 Minutos

1. **Agora** (2 min):
   ```bash
   cd backend
   python preflight.py
   ```

2. **Se passou** (1 min):
   ```bash
   git add -A
   git commit -m "Fix: Render ASGI module import with detailed debugging"
   git push
   ```

3. **Na dashboard Render** (10 min):
   - Vá em Settings → Clear Cache
   - Manual Deploy
   - Monitore Logs
   - Procure por `✓✓✓ STARTUP SEQUENCE COMPLETE`

4. **Teste** (2 min):
   - Visite https://seu-app.render.com/health
   - Deve retornar `{"status":"healthy"}`

## SOS - Se Tudo Falhar

1. Leia os logs COMPLETAMENTE
2. Procure pela primeira mensagem `✗`
3. Verifique `RENDER_TROUBLESHOOTING.md`
4. Se for erro de import, está em main.py
5. Se for erro de database, está em docker/conexão
6. Se for error of rota, está em algum arquivo app/

## Teste Sem Deploy

Para testar sem fazer deploy real no Render:

```bash
cd backend

# Simula exatamente o que Render fará
pip install -r requirements.txt
python run.py
```

Se funcionar localmente com `python run.py`, vai funcionar no Render.

---

**TL;DR:**
1. `cd backend && python preflight.py`
2. `git add -A && git commit -m 'Fix' && git push`
3. Render dashboard → Clear Cache + Manual Deploy
4. Monitor Logs
5. Procure por `✓✓✓ STARTUP SEQUENCE COMPLETE`
