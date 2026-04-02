# 📑 ShoppingHub - Índice de Documentação e Arquivos

## 🗂️ Estrutura Completa do Projeto

```
shoping/
├── 📋 README.md                 ← COMECE AQUI - Documentação completa
├── 🚀 QUICKSTART.md             ← Guia de início rápido
├── 🏗️  ARCHITECTURE.md           ← Explicação da arquitetura
├── 📚 API_REFERENCE.md          ← Referência de endpoints
├── 📝 INDEX.md                  ← Este arquivo
│
├── backend/
│   ├── 📌 main.py               - Aplicação FastAPI principal
│   ├── 📝 requirements.txt       - Dependências Python
│   ├── 🔑 .env.example          - Variáveis de ambiente
│   ├── 📂 .gitignore            - Arquivos ignorados
│   ├── 🐳 Dockerfile            - Docker config
│   ├── 🌱 seed_data.py          - Script para popular dados
│   │
│   └── app/
│       ├── 🔐 core/
│       │   ├── config.py         - Configurações (Pydantic Settings)
│       │   ├── security.py       - Autenticação JWT e hashing
│       │   └── __init__.py
│       │
│       ├── 🗄️  database/
│       │   ├── database.py       - SQLAlchemy setup, SessionLocal
│       │   └── __init__.py
│       │
│       ├── 📊 models/            - Modelos SQLAlchemy ORM
│       │   ├── user.py           - Usuários
│       │   ├── annotator.py      - Empresas
│       │   ├── job.py            - Vagas
│       │   ├── carousel.py       - Carrossel
│       │   ├── sponsorship.py    - Patrocínios
│       │   └── __init__.py
│       │
│       ├── ✅ schemas/           - Schemas Pydantic (validação)
│       │   ├── user.py           - UserCreate, UserLogin, UserResponse
│       │   ├── annotator.py      - AnnotatorCreate, AnnotatorUpdate, AnnotatorResponse
│       │   ├── job.py            - JobCreate, JobUpdate, JobResponse
│       │   ├── carousel.py       - CarouselCreate, CarouselUpdate, CarouselResponse
│       │   ├── sponsorship.py    - SponsorshipCreate, SponsorshipUpdate, SponsorshipResponse
│       │   └── __init__.py
│       │
│       ├── 🛣️  routes/            - FastAPI Endpoints
│       │   ├── auth.py           - /api/auth/* (Register, Login, Me)
│       │   ├── annotators.py     - /api/annotators/* (CRUD empresas)
│       │   ├── jobs.py           - /api/jobs/* (CRUD vagas)
│       │   ├── carousel.py       - /api/carousel/* (CRUD carrossel)
│       │   ├── sponsors.py       - /api/sponsorships/* (CRUD patrocínios)
│       │   └── __init__.py
│       │
│       ├── 🛠️  utils/
│       │   └── __init__.py
│       │
│       └── __init__.py
│
├── frontend/
│   ├── 📄 index.html             - Página principal dinâmica
│   ├── 🎨 css/
│   │   ├── style.css             - Estilos globais (moderno e responsivo)
│   │   └── microsite.css         - Estilos específicos do micro site
│   ├── ⚙️  js/
│   │   ├── main.js               - Lógica principal (load data, carousel, busca)
│   │   └── microsite.js          - Lógica do micro site
│   ├── 📄 pages/
│   │   └── microsite.html        - Template dinâmico do micro site
│   └── 🖼️  img/
│       └── (placeholder images aqui)
│
└── 🐳 docker-compose.yml         - Docker compose (backend + frontend + postgres)
    ⚙️  setup.sh                  - Script setup para Linux/Mac
    🪟 setup.bat                 - Script setup para Windows
```

---

## 📖 Como Usar Esta Documentação

### 1️⃣ **Para Começar Rápido** 
   → Leia [QUICKSTART.md](QUICKSTART.md)

### 2️⃣ **Para Entender a Arquitetura**
   → Leia [ARCHITECTURE.md](ARCHITECTURE.md)

### 3️⃣ **Para Usar a API**
   → Consulte [API_REFERENCE.md](API_REFERENCE.md)

### 4️⃣ **Para Detalhes Completos**
   → Leia [README.md](README.md)

### 5️⃣ **Documentação Interativa**
   → Acesse `http://localhost:8000/docs` (após iniciar o backend)

---

## 🚀 Início Rápido (3 Passos)

### Passo 1: Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac: ou venv\Scripts\activate (Windows)
pip install -r requirements.txt
python seed_data.py  # Opcional: popula dados de exemplo
uvicorn main:app --reload
```

### Passo 2: Setup Frontend
```bash
# Em outro terminal
cd frontend
python -m http.server 8080
```

### Passo 3: Acesse
- 🏠 Frontend: http://localhost:8080
- 📚 API Docs: http://localhost:8000/docs
- 🌐 API Base: http://localhost:8000

---

## 📁 Arquivos Importantes Explicados

### Backend

| Arquivo | Propósito | Tipo |
|---------|-----------|------|
| `main.py` | Inicializa FastAPI + middleware + rotas | Core |
| `seed_data.py` | Popula banco com dados de exemplo | Utilidade |
| .env.example | Template de variáveis de ambiente | Config |
| requirements.txt | Dependências Python pip | Dependência |
| Dockerfile | Imagem Docker do backend | DevOps |

### Frontend

| Arquivo | Propósito | Tipo |
|---------|-----------|------|
| index.html | Página principal com carrossel e vagas | Frontend |
| pages/microsite.html | Template para micro sites das empresas | Frontend |
| css/style.css | Estilos globais (gradientes, animações) | Estilos |
| css/microsite.css | Estilos de micro sites | Estilos |
| js/main.js | Fetch de dados API e renderização | Lógica |
| js/microsite.js | Carregamento de empresa por slug | Lógica |

---

## 🎯 Funcionalidades Implementadas

### ✅ Autenticação
- [x] Registro de usuário
- [x] Login com JWT
- [x] Hash seguro de senhas (bcrypt)

### ✅ Empresas (Annotators)
- [x] CRUD completo
- [x] Busca por texto
- [x] Slug customizável para URLs
- [x] Redes sociais integradas
- [x] Soft delete

### ✅ Vagas (Jobs)
- [x] CRUD completo
- [x] Filtros por categoria, cidade, empresa
- [x] Busca full-text
- [x] Vagas em destaque
- [x] Data de expiração

### ✅ Carrossel
- [x] Auto-rotativo
- [x] Clicável para empresas
- [x] Customização de velocidade
- [x] Ordenação

### ✅ Patrocínios
- [x] CRUD completo
- [x] Diferentes posições (banner, sidebar, footer)
- [x] Datas de validade
- [x] Ordenação

### ✅ Frontend
- [x] Design moderno e responsivo
- [x] Gradientes vibrantes
- [x] Animações suaves
- [x] Mobile-first
- [x] Micro sites dinâmicos

### ✅ API
- [x] RESTful endpoints
- [x] Validação Pydantic
- [x] Type hints completos
- [x] CORS habilitado
- [x] Documentação Swagger

---

## 🔄 Fluxo de Dados

```
Usuário (Frontend)
    ↓
[fetch() JavaScript]
    ↓
FastAPI Backend
    ↓
Validação Pydantic
    ↓
SQLAlchemy ORM
    ↓
Banco de Dados (SQLite/PostgreSQL)
    ↓
Resposta JSON
    ↓
Renderização no Frontend
```

---

## 💾 Banco de Dados

### Tabelas Criadas
1. **users** - Usuários registrados
2. **annotators** - Empresas/anunciantes
3. **jobs** - Vagas de emprego
4. **carousel_items** - Items do carrossel
5. **sponsorships** - Patrocinadores

### Tipos Suportados
- SQLite (desenvolvimento - padrão)
- PostgreSQL (produção - recomendado)

### Como Mudar para PostgreSQL
1. Instale PostgreSQL
2. Crie banco: `CREATE DATABASE shopping_db;`
3. Edite `.env`: `DATABASE_URL=postgresql://user:pass@localhost/shopping_db`
4. Reinicie backend

---

## 🔐 Segurança Implementada

- ✅ Senhas com bcrypt (nunca salva em plain text)
- ✅ JWT para autenticação stateless
- ✅ CORS configurado (whitelist de origins)
- ✅ Type hints em tudo (evita tipo errado)
- ✅ Validação Pydantic (entrada segura)
- ✅ SQLAlchemy ORM (previne SQL injection)
- ✅ Soft deletes (não perde dados críticos)

---

## 📊 Exemplos de Uso

### Criar Empresa
```bash
curl -X POST http://localhost:8000/api/annotators/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Tech Store",
    "slug": "tech-store",
    "description": "Loja tech",
    "email": "contato@tech.com",
    "phone": "11999999999",
    "city": "São Paulo",
    "state": "SP"
  }'
```

### Buscar Empresas
```bash
curl "http://localhost:8000/api/annotators/?search=tech&limit=10"
```


---

## 🎨 Design Highlights

- 🎨 **Cores Modernas**: RGB primário (#FF6B6B), secundário (#4ECDC4), destaque (#FFE66D)
- 📱 **Responsivo**: Mobile-first, testes em 480px, 768px, 1024px
- ✨ **Animações**: Transições suaves, hover effects, fade-in
- 🎠 **Carrossel**: Auto-rotativo com controls manuais
- 🌐 **Acessibilidade**: Ícones Font Awesome, sem barreiras de cor
- 📊 **Grid Layout**: CSS Grid para cards responsivos

---
**teste**
## 🚀 Próximas Melhorias Recomendadas

1. **Painel Administrativo**
   - Dashboard com estatísticas
   - Gerenciamento de empresas/vagas

2. **Sistema de Ratings**
   - Avaliações de empresas
   - Comentários

3. **Chat em Tempo Real**
   - WebSockets para mensagens
   - Notificações em tempo real

4. **Pagamentos**
   - Stripe integration
   - Patrocínios pagos

5. **Email**
   - Notificações por email
   - Recuperação de senha

6. **Testes**
   - Unit tests (pytest)
   - Integration tests

7. **Performance**
   - Redis cache
   - CDN para assets

8. **Analytics**
   - Google Analytics
   - Relatórios customizados

---

## 📱 Endpoints da API

### Autenticação
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

### Empresas
- `GET /api/annotators/`
- `POST /api/annotators/`
- `GET /api/annotators/{id}`
- `GET /api/annotators/slug/{slug}`
- `PUT /api/annotators/{id}`
- `DELETE /api/annotators/{id}`

### Vagas
- `GET /api/jobs/`
- `POST /api/jobs/`
- `GET /api/jobs/{id}`
- `POST /api/jobs/`
- `PUT /api/jobs/{id}`
- `DELETE /api/jobs/{id}`
- `GET /api/jobs/company/{company_id}`

### Carrossel
- `GET /api/carousel/`
- `POST /api/carousel/`
- `GET /api/carousel/{id}`
- `PUT /api/carousel/{id}`
- `DELETE /api/carousel/{id}`

### Patrocínios
- `GET /api/sponsorships/`
- `POST /api/sponsorships/`
- `GET /api/sponsorships/{id}`
- `PUT /api/sponsorships/{id}`
- `DELETE /api/sponsorships/{id}`

---

## 🐳 Docker

### Build & Run
```bash
docker-compose up -d

# Acesse:
# - Frontend: http://localhost:8080
# - Backend: http://localhost:8000
# - Database: localhost:5432
```

### Parar
```bash
docker-compose down
```

---

## 📞 Suporte

Para dúvidas, consulte:
1. **Documentação**: Este arquivo + README.md
2. **API Docs**: http://localhost:8000/docs
3. **Código**: Comentários inline em toda aplicação
4. **Exemplos**: seed_data.py

---

## 📝 Licença

Projeto open-source. Sinta-se livre para usar e modificar!

---

## 🎉 Pronto para Começar?

1. ✅ Leia [QUICKSTART.md](QUICKSTART.md)
2. ✅ Execute `setup.bat` ou `setup.sh`
3. ✅ Acesse http://localhost:8080
4. ✅ Explore a API em http://localhost:8000/docs

**Boa sorte! 🚀**
