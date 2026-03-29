# Solucionando Erro ASGI no Render

## Problema
```
ERRO: Erro carregando o app ASGI. Não foi possível importar o módulo "main".
```

Este erro ocorre quando o Render não consegue importar o módulo `main.py` durante o startup da aplicação.

## Solução Rápida

### Opção 1: Forçar Reimplantação (Recomendado)
1. Vue para a dashboard do Render
2. Acesse sua aplicação "shoppinghub"
3. Clique em "Clear build cache" seguido de "Redeploy" ou "Manual Deploy"
4. Aguarde o build completar

### Opção 2: Verificar Logs
1. Vá para "Logs" na dashboard do Render
2. Procure por mensagens que começam com `✓` ou `✗`
3. Procure a primeira linha que começa com `✗` para ver onde falha

Exemplo de log esperado:
```
✓ FastAPI imports successful
✓ Config imported
✓ Database imported
✓ Routes imported
✓ FastAPI app created
✓ CORS middleware added
✓ Uploads mount added
✓ All routes included
✓✓✓ MAIN.PY INITIALIZATION COMPLETE ✓✓✓
```

## Arquivos de Diagnóstico

### Debug Automático
O arquivo `main.py` agora imprime estágios de inicialização:
- Print no início da importação
- Print após cada import de módulo
- Print de erros com traceback completo
- Status final "INITIALIZATION COMPLETE"

Estes logs ajudam a identificar **exatamente** onde o erro ocorre.

### Scripts de Teste
- **`test_import.py`** - Testa cada componente individualmente
- **`check_structure.py`** - Verifica estrutura dos arquivos
- **`run.py`** - Executa com diagnósticos integrados (usado no startCommand)
- **`wsgi.py`** - Fallback WSGI se uvicorn falhar

## Soluções Alternativas (Se Rápida Não Funcionar)

### Alternativa 1: Usar WSGI
Se continuar a dar erro, modifique `render.yaml`:
```yaml
startCommand: gunicorn wsgi:app --bind 0.0.0.0:$PORT
```

E adicione ao `requirements.txt`:
```
gunicorn>=21.0.0
```

Então faça:
```bash
git add -A
git commit -m "Fix: Use gunicorn instead of uvicorn"
git push
```

### Alternativa 2: Python Direto
```yaml
startCommand: python -c "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))"
```

### Alternativa 3: Entrypoint Shell (RequersPermissão)
Se shell scripts são permitidos:
```yaml
startCommand: ./entrypoint.sh
```

E certifique-se que o arquivo tem permissão:
```bash
chmod +x backend/entrypoint.sh
```

## Checklist de Verificação

- [ ] `main.py` existe em `backend/`
- [ ] `app/` pasta existe com todos os `__init__.py`
- [ ] `requirements.txt` tem todas as dependências
- [ ] Arquivo `.env` está no `.gitignore`
- [ ] `render.yaml` está atualizado
- [ ] Nenhum arquivo `.pyc` está sendo commitado
- [ ] Git push foi bem-sucedido (`git push` retorna exit 0)

## Troubleshooting Passo a Passo

### Se o erro aparecer imediatamente após "Rodando"
1. Procure em Logs por antes da mensagem de erro
2. A primeira linha `✗` mostra onde exatamente falha
3. Geralmente é:
   - Falta de importação (modulo faltando)
   - Variable de ambiente não definida
   - Permissão de arquivo
   - Banco de dados não acessível

### Se o buildCommand falhar
O erro está durante `pip install`:
1. Procure por `ERROR:` ou `error:` nos logs
2. Geralmente falta de compilação (ex: bcrypt precisa de build tools)
3. Solução: Procure em GitHub Issues do pacote problemático

### Se tudo passar mas app não responder
1. Verifique `/health` - se retornar erro 500, há bug
2. Verifique `/docs` - se retornar HTML, app está rodando
3. Procure por erros de conexão de banco de dados

## Variáveis de Ambiente Críticas

Estadas devem estar definidas no Render Dashboard ou render.yaml:
- `DATABASE_URL` - Deve estar configurada (From Database)
- `SECRET_KEY` - Deve estar gerada aleatoriamente
- `PYTHONUNBUFFERED=1` - Mostra output em tempo real
- `PYTHONDONTWRITEBYTECODE=1` - Não cria .pyc files

## Como Deployar com Sucesso

1. Teste localmente:
   ```bash
   cd backend
   python test_import.py
   python run.py
   ```

2. Se passar, faça commit:
   ```bash
   git add -A
   git commit -m "Add: Render deployment diagnostics"
   git push
   ```

3. No Render Dashboard:
   - Vá em shoppinghub → Settings → Branches
   - Desative "Auto-Deploy" temporariamente
   - Que "Clear build cache"
   - Clique "Deploy latest commit"
   - Monit ore "Logs" em tempo real

4. Se passar:
   - Re-ative "Auto-Deploy"

## Referências

- [Render Python Deployment](https://render.com/docs/deploy-python)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Gunicorn Documentation](https://gunicorn.org/)

## Pergunta Frequentes

**P: Por que diz "python run.py" mas o erro diz "uvicorn main:app"?**
R: Você pode ter uma implantação em cache. Vá em Render Dashboard e clique "Clear build cache" e depois "Redeploy".

**P: Onde vejo os logs do meu código?**
R: Na dashboard do Render, clique em sua aplicação → "Logs" → Procure por mensagens que começam com `✓` ou `✗`.

**P: Como faço para debug sem reimplantar?**
R: Teste localmente com `python run.py`. Se funcionar localmente, o problema é na configuração do Render.

**P: Qual é a diferença entre build e deploy?**
R: Build instala dependências. Deploy executa o startCommand. Se build falhar, não chega a deploy.

