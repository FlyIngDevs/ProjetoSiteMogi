# 🔧 Corrigido: Problema de URLs de Imagens no S3

## ✅ O Problema Foi Resolvido

O erro `404 (Not Found)` ao tentar carregar imagens do S3 foi corrigido com uma solução em cascata.

## 📋 Alterações Realizadas

### 1. **Arquivo: `backend/app/services/storage.py`**
   - ❌ **Removido**: Função `upload_bytes()` duplicada
   - ✅ **Melhorado**: `get_image_url()` agora tenta:
     - URL pública direta (se `STORAGE_PUBLIC_BASE_URL` configurado)
     - Signed URL do S3 (com expiração de 24h)
     - Endpoint proxy do backend como fallback (mais confiável)

### 2. **Novo Arquivo: `backend/app/routes/images.py`**
   - ✅ **Criado** endpoint público: `/api/image-proxy/{object_key}`
   - Servidor proxy que sirve imagens do S3 através do backend
   - Inclui validações de segurança (anti-traversal)
   - Cache de 1 hora para melhor performance
   - **Sem autenticação** (público para todos)

### 3. **Arquivo: `backend/app/routes/site_config.py`**
   - ✅ **Modificado**: Endpoint GET `/api/site-config/branding`
   - Agora **regenera URLs** ao retornar (em vez de usar direto do banco)
   - Extrai o `object_key` da URL armazenada
   - Gera URL funcional através de `get_image_url()`

### 4. **Arquivo: `backend/main.py`**
   - ✅ **Registrado**: Novo router de imagens

### 5. **Arquivo: `backend/app/routes/__init__.py`**
   - ✅ **Importado**: Novo módulo `images`

## 🔄 Como Funciona Agora

```
User acessa site → Frontend carrega branding
                ↓
GET /api/site-config/branding
                ↓
Backend regenera URL usando get_image_url()
                ↓
Retorna uma de: URL pública | Signed URL | Proxy URL
                ↓
Se for Proxy URL → /api/image-proxy/{object_key}
                ↓
Backend faz proxy para S3 (com suas credenciais)
                ↓
Imagem é servida ao navegador ✅
```

## 🚀 Como Usar

### Opção 1: URL Pública Direta (Mais Rápido)
Se seu bucket S3 permite acesso público, configure:

```bash
export STORAGE_PUBLIC_BASE_URL="https://t3.storageapi.dev/embedded-toolbox-tlbg8use"
```

Sem isso, o sistema **usa proxy automaticamente**.

### Opção 2: Proxy Automático (Padrão - Mais Seguro)
Nenhuma configuração necessária! O sistema automáticamente:
- Tenta signed URL primeiro
- Se falhar, usa proxy do backend

## ✔️ Teste Rápido

### No Console do Browser (F12):
```javascript
// Teste 1: Verificar se branding carrega
fetch('/api/site-config/branding')
  .then(r => r.json())
  .then(d => console.log('Logo URL:', d.brand_logo_url))

// Teste 2: Verificar se a imagem carrega
const img = new Image()
img.onload = () => console.log('✅ Imagem carregou!')
img.onerror = () => console.log('❌ Erro ao carregar')
fetch('/api/site-config/branding')
  .then(r => r.json())
  .then(d => { img.src = d.brand_logo_url })
```

### Via cURL:
```bash
# Teste o endpoint
curl -s http://localhost:8000/api/site-config/branding | jq .

# Teste a imagem diretamente
curl -v "http://localhost:8000/api/image-proxy/branding/uuid.png"
```

## 🔐 Segurança

- ✅ Validação de paths (anti-directory-traversal)
- ✅ Apenas pastas autorizadas: `branding`, `annotators`, `carousel`, `sponsors`
- ✅ Uso de credenciais do backend (não expõe credenciais ao cliente)
- ✅ Cache com expiração apropriada

## 📝 Notas

- **Duplicação Removida**: Função `upload_bytes()` que estava definida 2x foi unificada
- **URL Regenerada**: URLs são geradas fresh a cada request, evitando URLs expiradas
- **Compatibilidade**: Mantém compatibilidade com URLs já armazenadas no banco

---

**Se ainda houver problemas**, verifique:
1. ✅ Variáveis de ambiente do S3 estão corretas
2. ✅ Credenciais do S3 têm permissão de GET
3. ✅ Backend está rodando (deve ter novo endpoint)
4. ✅ Arquivo foi salvo corretamente (check `logs` para detalhes)
