# Solucionando Erro ASGI no Render

## Problema
```
ERRO: Erro carregando o app ASGI. Não foi possível importar o módulo "main".
```

Este erro ocorre quando o Render não consegue importar o módulo `main.py` durante o startup da aplicação.

## Soluções Implementadas

### 1. **Testes e Diagnósticos**

Antes de fazer deploy no Render, teste localmente:

```bash
cd backend

# Teste 1: Verificar estrutura
python check_structure.py

# Teste 2: Testar importações
python test_import.py

# Teste 3: Testar execução direta
python run.py
```

### 2. **Alternativas de Deploy**

#### Opção A: Usar entrypoint.sh (r

eccommended)
- Mantém o arquivo `render.yaml` existente
- O buildCommand executa testes antes de instalar
- Garante que tudo funciona antes do deploy

#### Opção B: Usar render-alternative.yaml
Se a Opção A falhar:
1. Renomeie `render.yaml` para `render-backup.yaml`
2. Renomeie `render-alternative.yaml` para `render.yaml`
3. Considere mudar `startCommand` para:
   - `python run.py` (Python direto)
   - `uvicorn main:app --host 0.0.0.0 --port $PORT` (Uvicorn direto)

### 3. **Verificação de Permissões**

Se usar entrypoint.sh, certifique-se que tem permissão de execução:

```bash
chmod +x backend/entrypoint.sh
git add backend/entrypoint.sh
git commit -m "Fix: Add execute permission to entrypoint.sh"
git push
```

### 4. **Debug no Render**

Se o erro persistir após o deploy:

1. Clique em "Logs" na dashboard do Render
2. Procure por mensagens de erro durante o "Build"
3. Se o Build passar mas o app falhar, procure erros durante "Deploy"

Você deve ver sequência:
```
==> Build with success 🎉
==> Deploying...
==> Running 'uvicorn main:app --host 0.0.0.0 --port $PORT'
```

Se falhar na primeira mensagem, o problema é nas dependências.
Se falhar na segunda, é problema de importação do módulo.

### 5. **Arquivo de Configuração Crítico**

O arquivo de deploy **deve** incluir:

```yaml
envVars:
  - key: PYTHONUNBUFFERED
    value: '1'
  - key: PYTHONDONTWRITEBYTECODE
    value: '1'
```

Esta configuração garante que erros sejam mostrados imediatamente.

### 6. **Checklist de Deploy**

- [ ] `main.py` existe no diretório `backend/`
- [ ] Pasta `app/` existe com `__init__.py`
- [ ] Arquivo `.env` está no `.gitignore` (não fazer commit)
- [ ] `entrypoint.sh` tem permissão de execução (`chmod +x`)
- [ ] `requirements.txt` tem todas as dependências
- [ ] `render.yaml` está configurado corretamente
- [ ] Fazer commit de todos os arquivos Python novos
- [ ] Fazer push para o repositório

### 7. **Arquivos Adicionados/Modificados**

Novos arquivos para diagnóstico:
- `backend/test_import.py` - Testa se módulos importam corretamente
- `backend/check_structure.py` - Verifica estrutura dos arquivos
- `backend/run.py` - Alternative runner (Python puro)
- `backend/entrypoint.sh` - Script de inicialização (bash)
- `render-alternative.yaml` - Configuração alternativa
- `backend/__init__.py` - Package marker

Arquivos modificados:
- `backend/main.py` - Adicionado tratamento de erros
- `backend/app/core/config.py` - Adicionado carregamento de .env
- `backend/Dockerfile` - Atualizado para Python 3.12
- `backend/requirements.txt` - Verificado e validado
- `render.yaml` - Adicionado buildCommand com testes

## Próximos Passos

1. Teste localmente:
   ```bash
   cd backend
   python test_import.py
   ```

2. Se passar, faça commit:
   ```bash
   git add -A
   git commit -m "Feat: Add ASGI import diagnostics and Render config improvements"
   git push
   ```

3. Reimplanta no Render
4. Monitore os logs

## Contato / Referências

- [Render Deploying Python Apps](https://render.com/docs/deploy-python)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Uvicorn Configuration](https://www.uvicorn.org/)
