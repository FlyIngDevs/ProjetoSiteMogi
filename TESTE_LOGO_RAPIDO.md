# 🚀 INSTRUÇÕES RÁPIDAS: Como Testar o Logo

## 1️⃣ Primeira Coisa: Abra Este Arquivo

Abra no navegador:
```
test_logo_full.html
```

Este arquivo vai executar 5 testes automaticamente e dizer EXATAMENTE qual é o problema.

---

## 2️⃣ Clique em "Executar Diagnóstico Completo"

Ele vai:
- ✅ Testar se a API funciona
- ✅ Testar se o logo foi salvo no banco
- ✅ Testar se a imagem pode ser carregada
- ✅ Testar se o elemento HTML existe
- ✅ Dizer EXATAMENTE o que está errado

---

## 3️⃣ Me Mostre a Saída

Copie o resultado do diagnóstico e me mostretodo ele. Com essas informações vou saber:
- Se o upload funcionou? ✅
- Se salvou no banco? ✅
- Se a API retorna? ✅
- Se renderiza no cabeçalho? ✅
- Qual é o erro exato? 🔴

---

## Por Enquanto: Passos Para Você Testar Manualmente

### Se você quer ver o Console (F12):

1. **Abra o painel admin:**
   - URL: `frontend/pages/admin.html`

2. **Vá em: Branding**

3. **Teste o upload:**
   - Selecione uma imagem PNG
   - No Console (F12 → Network), você deve ver:
     ```
     POST /api/admin/upload-image?folder=branding → 200 OK
     ```
   - Se vir erro 401, faça login novamente

4. **Clique "Salvar branding":**
   - No Console (F12 → Network), você deve ver:
     ```
     PUT /api/site-config/branding → 200 OK
     ```
   - Se vir erro 404, o endpoint não existe

5. **Abra o site público:**
   - URL: `index.html`
   - Abra Console (F12 → Console)
   - Execute:
     ```javascript
     console.log(document.getElementById('brandLogo').src)
     ```
   - Deve mostrar a URL do logo que você salvou (não mais `img/bomcontato-logo.png`)

---

## 🎯 Teste Rápido em 30 Segundos

1. Abra `test_logo_full.html` no navegador
2. Clique em **"Executar Diagnóstico Completo"**
3. Leia a saída
4. Me mande a mensagem exata que aparece

Pronto! Com isso vou saber exatamente o que consertar! 🚀
