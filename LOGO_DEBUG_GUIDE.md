# 🔍 Guia Completo: Como o Logo Deveria Funcionar

## O Fluxo Esperado (Upload → Banco → Renderização)

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. VOCÊ FAZ UPLOAD NO PAINEL ADMIN                              │
│    - Vai em: Painel Admin → Branding → Escolher arquivo        │
│    - Seleciona uma imagem PNG                                   │
│    - Sistema envia (POST): /api/admin/upload-image?folder=brand │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. UPLOAD PARA O BUCKET S3                                      │
│    - Backend recebe arquivo                                     │
│    - Envia para Linode Spaces (ou AWS S3)                       │
│    - Recebe de volta URL ASSINADA (com token de acesso)         │
│    - Exemplo: https://ts.storageapi.dev/.../logo.png?X-Amz...  │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. VOCÊ CLICA "SALVAR BRANDING"                                 │
│    - Sistema envia (PUT): /api/site-config/branding             │
│    - Payload: { "brand_logo_url": "https://..." }               │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. BANCO DE DADOS (PostgreSQL)                                  │
│    - Tabela: site_settings                                      │
│    - Insere/Atualiza:                                           │
│      key: "brand_logo_url"                                      │
│      value: "https://ts.storageapi.dev/.../logo.png?X-Amz..."  │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. VISITANTE ABRE O SITE (index.html)                           │
│    - HTML carrega com: <img id="brandLogo" src="...default..."> │
│    - JavaScript executa: loadBranding()                         │
│    - Fetch GET: /api/site-config/branding (público, sem auth)   │
│    - Recebe: { "brand_logo_url": "https://..." }                │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. ATUALIZAR IMG NO CABEÇALHO                                   │
│    - JavaScript encontra: document.getElementById('brandLogo')  │
│    - Muda o src para a URL do banco                             │
│    - Imagem aparece no cabeçalho! ✅                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Checklist: Como Debugar Se Não Está Funcionando

### ✅ Passo 1: Verificar se Upload Funcionou

**O que fazer:**
1. Abra o painel admin → Branding
2. Selecione uma imagemsua
3. **Abra o Console (F12 → Network)**
4. Procure por: **POST /api/admin/upload-image?folder=branding**

**O que você deve ver:**
```
✅ Status: 200 OK
Resposta:
{
  "url": "https://ts.storageapi.dev/..../logo.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&...",
  "filename": "logo.png",
  "key": "branding/logo-xxxxx.png"
}
```

**Se você vê erro:**
- `401 Unauthorized` → Você não é admin (faça login novamente)
- `500 Internal Server Error` → Problema no backend (arquivo não salvou)
- `413 Payload Too Large` → Imagem muito grande

---

### ✅ Passo 2: Verificar se Salvou no Banco

**O que fazer:**
1. Depois que fez upload, clique **"Salvar branding"**
2. No Console (F12 → Network), procure por: **PUT /api/site-config/branding**

**O que você deve ver:**
```
✅ Status: 200 OK
Resposta:
{
  "brand_logo_url": "https://ts.storageapi.dev/..../logo.png?X-Amz-...",
  "admin_brand_logo_url": null
}
```

**Se você vê erro:**
- `401 Unauthorized` → Você não é admin
- `404 Not Found` → Endpoint não existe (problema no backend)
- `400 Bad Request` → Dados inválidos

---

### ✅ Passo 3: Verificar se a API Retorna a URL

**O que fazer:**
1. Abra o Console (F12 → Console)
2. Execute:
```javascript
fetch('http://127.0.0.1:8000/api/site-config/branding')
  .then(r => r.json())
  .then(d => console.log(d))
```

**O que você deve ver:**
```
{
  "brand_logo_url": "https://ts.storageapi.dev/.../logo.png?X-Amz-...",
  "admin_brand_logo_url": null
}
```

**Se você vê `null` ou `{ }`:**
- O banco está vazio (você não salvou nada ainda)
- Ou o endpoint não existe

---

### ✅ Passo 4: Verificar se Renderiza no Cabeçalho

**O que fazer:**
1. Abra o site (index.html)
2. Abra o Console (F12 → Console)
3. Execute:
```javascript
console.log('Logo element:', document.getElementById('brandLogo'));
console.log('Logo src:', document.getElementById('brandLogo').src);
console.log('Logo loaded:', document.getElementById('brandLogo').complete);
```

**O que você deve ver:**
```
Logo element: <img id="brandLogo" ...>  ← elemento encontrado
Logo src: https://ts.storageapi.dev/.../logo.png?X-Amz-...  ← URL correta
Logo loaded: true  ← imagem carregou
```

**Se você vê:**
- `Logo element: null` → Elemento #brandLogo não existe no HTML
- `Logo src: img/bomcontato-logo.png` → Logo ainda é a padrão (não atualizou)
- `Logo loaded: false` → Imagem não conseguiu carregar (erro CORS ou URL inválida)

---

## 🔧 Soluções Rápidas

### Problema: Logo não atualiza no cabeçalho

**Solução 1: Recarregue a página com Ctrl+F5**
- Força atualizar o CSS e JavaScript

**Solução 2: Limpe o cache do navegador**
- Ctrl+Shift+Delete → Limpar dados de navegação → Todo o tempo

**Solução 3: Abra no Dev Tools e force atualizar**
- F12 → Network → Marque "Disable cache" → Recarregue

---

### Problema: Erro "Imagem não pode ser carregada"

**Possível causa:** URL com problema de CORS
**Solução:**
1. Copie a URL do logo (do banco)
2. Abra em uma aba do navegador
3. Se aparecer erro de CORS, o problema é no S3/Linode

---

### Problema: Painel Admin não salva nada

**Verificar:**
1. Console → Network → PUT /api/site-config/branding
2. Está retornando erro?

**Se sim:**
- Verifique se o endpoint existe em `backend/app/routes/site_config.py`
- Verifique se você é admin (logout e login novamente)

---

## 🧪 Usar Arquivo de Teste

Abra este arquivo no navegador:
```
test_logo_full.html
```

Ele vai:
1. ✅ Testar se a API retorna a URL
2. ✅ Verificar se o elemento HTML existe
3. ✅ Simular o carregamento do logo
4. ✅ Diagnosticar exatamente onde está o problema

---

## 📞 Resumo do Que Preciso Saber

Se o logo ainda não está funcionando, me mostre a saída do **arquivo test_logo_full.html** aberto no navegador. Ele vai dizer exatamente:

- ✅ Upload funcionando?
- ✅ Banco de dados salvando?
- ✅ API retornando?
- ✅ HTML renderizando?

Com essas informações, consigo encontrar o problema em 2 minutos! 🚀
