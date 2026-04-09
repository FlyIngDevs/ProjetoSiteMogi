# 🏗️ Arquitetura e Boas Práticas do Bom Contato

## Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (HTML/CSS/JS)               │
│                                                         │
│  index.html ────► pages/microsite.html                │
│  css/style.css ──► css/microsite.css                  │
│  js/main.js ────► js/microsite.js                     │
└─────────────────┬──────────────────────────────────────┘
                  │ HTTP/REST (JSON)
                  │ CORS Enabled
                  ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Backend                        │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │ Routes (Endpoints)                              │   │
│  │ • auth.py    - Autenticação                    │   │
│  │ • annotators.py - Empresas                    │   │
│  │ • jobs.py    - Vagas                           │   │
│  │ • carousel.py - Carrossel                     │   │
│  │ • sponsors.py - Patrocínios                   │   │
│  └────────────────────────────────────────────────┘   │
│                       ▲                                │
│                       │ Logical Operations             │
│  ┌────────────────────────────────────────────────┐   │
│  │ Models (ORM - SQLAlchemy)                      │   │
│  │ • User - Usuários                              │   │
│  │ • Annotator - Empresas                         │   │
│  │ • Job - Vagas                                  │   │
│  │ • Carousel - Carrossel                         │   │
│  │ • Sponsorship - Patrocínios                    │   │
│  └────────────────────────────────────────────────┘   │
│                       ▼                                │
│  ┌────────────────────────────────────────────────┐   │
│  │ Schemas (Validação - Pydantic)                 │   │
│  │ • Validação de entrada                         │   │
│  │ • Serialização de saída                        │   │
│  │ • Type hints                                   │   │
│  └────────────────────────────────────────────────┘   │
└─────────────────┬──────────────────────────────────────┘
                  │ SQL Queries
                  ▼
┌─────────────────────────────────────────────────────────┐
│          Banco de Dados (SQLite ou PostgreSQL)         │
│                                                         │
│  • users                                               │
│  • annotators (empresas)                              │
│  • jobs (vagas)                                        │
│  • carousel_items                                      │
│  • sponsorships                                        │
└─────────────────────────────────────────────────────────┘
```

## Camadas da Aplicação

### 1. **Camada de Apresentação (Frontend)**
- HTML/CSS/JS puro
- Sem framework (vanilla JavaScript)
- Design responsivo
- Integração com API via fetch()

**Arquivos:**
- `index.html` - Interface principal
- `pages/microsite.html` - Template dinâmico
- `css/style.css` - Estilos globais
- `css/microsite.css` - Estilos specificos
- `js/main.js` - Lógica principal
- `js/microsite.js` - Lógica do micro site

### 2. **Camada de API (Backend)**

#### Routes (Roteamento)
```python
# Estrutura de arquivo
routes/
├── auth.py        # POST /api/auth/register, /login
├── annotators.py  # CRUD de empresas
├── jobs.py        # CRUD de vagas
├── carousel.py    # CRUD de carrossel
└── sponsors.py    # CRUD de patrocínios
```

**Características:**
- RESTful endpoints
- HTTP status codes corretos
- Error handling robusto
- Request/Response validation

#### Models (ORM)
```python
# SQLAlchemy Models
models/
├── user.py        # Tabela users
├── annotator.py   # Tabela annotators
├── job.py         # Tabela jobs
├── carousel.py    # Tabela carousel_items
└── sponsorship.py # Tabela sponsorships
```

**Boas Práticas:**
- Relationships definidas
- Timestamps (created_at, updated_at)
- Soft deletes onde apropriado
- Indexes em campos buscados

#### Schemas (Validação)
```python
# Pydantic Schemas
schemas/
├── user.py        # UserCreate, UserLogin, UserResponse
├── annotator.py   # AnnotatorCreate, AnnotatorUpdate, AnnotatorResponse
├── job.py         # JobCreate, JobUpdate, JobResponse
├── carousel.py    # CarouselCreate, CarouselUpdate, CarouselResponse
└── sponsorship.py # SponsorshipCreate, SponsorshipUpdate, SponsorshipResponse
```

**Padrão:**
- `Create` - Para criação (POST)
- `Update` - Para edição (PUT)
- `Response` - Para retorno (GET)
- `Mini` - Versão reduzida para listas

### 3. **Camada de Dados**

#### Database
```python
core/
├── config.py   # Configurações da app
└── security.py # JWT, hash de senhas

database/
└── database.py # Conexão, SessionLocal, get_db()
```

## Padrões de Design Implementados

### 1. **Dependency Injection**
```python
async def get_annotators(db: Session = Depends(get_db)):
    # get_db é injetado automaticamente
    return db.query(Annotator).all()
```

### 2. **Repository Pattern** (implícito)
Queries encapsuladas em rotas, facilita testes

### 3. **Schema Validation**
Entrada validada por Pydantic
Saída serializada por Pydantic

### 4. **Error Handling**
```python
if not resource:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Resource not found"
    )
```

### 5. **CORS Middleware**
Permite requisições cross-origin seguras

## Fluxo de Requisição Típico

```
1. Cliente (Frontend)
   ↓
   const response = await fetch('/api/annotators/');
   ↓
2. Navegador
   ↓
   OPTIONS /api/annotators/ (CORS preflight)
   GET /api/annotators/
   ↓
3. FastAPI
   ↓
   route: async def list_annotators()
   ↓
4. Database
   ↓
   SELECT * FROM annotators WHERE is_active = true;
   ↓
5. FastAPI
   ↓
   Serialize com AnnotatorMiniResponse
   ↓
6. Navegador
   ↓
   response.json()
   ↓
7. Frontend JavaScript
   ↓
   renderCompanies(companies)
```

## Boas Práticas Implementadas

### ✅ Backend

- **Separação de Responsabilidades**
  - Routes ≠ Models ≠ Schemas
  - Cada arquivo tem um propósito único

- **Type Hints**
  - Todo parâmetro tem tipo
  - Facilita IDE autocomplete

- **Validação em Camadas**
  - Pydantic schemas na entrada
  - SQLAlchemy models na persistência

- **Soft Deletes**
  - Campo `is_active` em vez de delete hard
  - Preserva integridade referencial

- **Error Handling**
  - HTTPException para erros esperados
  - Mensagens de erro úteis

- **Security**
  - Senhas com bcrypt
  - JWT para autenticação
  - CORS configurado

- **Database**
  - Index em campos buscados
  - Timestamps automáticos
  - Foreign keys onde apropriado

### ✅ Frontend

- **Vanilla JavaScript**
  - Sem dependências pesadas
  - Melhor performance

- **Responsive Design**
  - Mobile-first
  - Media queries bem estruturadas

- **Fetch API**
  - Reqs assíncronas
  - Try-catch para erros

- **Modular**
  - Funções pequenas e focadas
  - Fácil de manter

- **Acessibilidade**
  - Sem barreiras de cor
  - Ícones com alternativa de texto

## Estrutura de Pastas - Explicado

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py      # Pydantic Settings - tudo configurável
│   │   ├── security.py    # JWT + Password hashing
│   │   └── __init__.py
│   │
│   ├── database/
│   │   ├── database.py    # SQLAlchemy setup, SessionLocal
│   │   └── __init__.py
│   │
│   ├── models/            # SQLAlchemy ORM Models
│   │   ├── user.py
│   │   ├── annotator.py
│   │   ├── job.py
│   │   ├── carousel.py
│   │   ├── sponsorship.py
│   │   └── __init__.py
│   │
│   ├── schemas/           # Pydantic Schemas para validação
│   │   ├── user.py
│   │   ├── annotator.py
│   │   ├── job.py
│   │   ├── carousel.py
│   │   ├── sponsorship.py
│   │   └── __init__.py
│   │
│   ├── routes/            # FastAPI Routes (endpoints)
│   │   ├── auth.py        # Autenticação
│   │   ├── annotators.py  # CRUD empresas
│   │   ├── jobs.py        # CRUD vagas
│   │   ├── carousel.py    # CRUD carrossel
│   │   ├── sponsors.py    # CRUD patrocínios
│   │   └── __init__.py
│   │
│   ├── utils/
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── main.py               # FastAPI app + middleware
├── requirements.txt
├── .env.example
├── seed_data.py         # Populador de dados
├── Dockerfile
│
└── .gitignore
```

## Como Adicionar uma Nova Feature

### Exemplo: Adicionar modelo "Review"

1. **Criar Model** (`models/review.py`)
```python
class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("annotators.id"))
    rating = Column(Integer)  # 1-5
    text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
```

2. **Criar Schema** (`schemas/review.py`)
```python
class ReviewCreate(BaseModel):
    company_id: int
    rating: int
    text: str

class ReviewResponse(ReviewCreate):
    id: int
    created_at: datetime
```

3. **Criar Route** (`routes/reviews.py`)
```python
@router.get("/{company_id}/reviews")
async def get_company_reviews(company_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.company_id == company_id).all()
    return reviews
```

4. **Registrar Route** (`main.py`)
```python
from app.routes import reviews
app.include_router(reviews.router)
```

5. **Frontend** (adicionar JS para carregar reviews)

## Performance & Escalabilidade

### Melhorias Recomendadas

1. **Caching**
   - Redis para cache de empresas frequentes
   - Cache em cliente (browser localStorage)

2. **Paginação**
   - Já implementado com `skip` e `limit`
   - Reduz transferência de dados

3. **Indexação**
   - Índices em campos frequentemente buscados
   - `slug`, `city`, `company_name`

4. **Database Connection Pool**
   - SQLAlchemy já gerencia isso
   - Configurável em `.env`

5. **CDN para Assets**
   - Servir CSS/JS de CDN
   - Reduz latência

6. **Compression**
   - gzip para respostas JSON
   - Economia de banda

## Monitoramento & Debugging

### Logs
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Company created", extra={"company_id": company.id})
```

### Health Check
- GET /health
- GET / (root)

### Database Audit
- Timestamps em toda tabela
- Track de criação e modificação

## Deployment

### Desenvolvimento
```bash
uvicorn main:app --reload
```

### Produção
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
# ou gunicorn
gunicorn main:app -w 4 -b 0.0.0.0:8000
```

### Docker
```bash
docker build -t shopping-api .
docker run -p 8000:8000 shopping-api
```

## Testes (Recomendação)

```python
# tests/test_annotators.py
def test_create_annotator():
    client = TestClient(app)
    response = client.post("/api/annotators/", json={...})
    assert response.status_code == 200
    assert response.json()["company_name"] == "Test"
```

## Segurança em Produção

1. ✅ **HTTPS** - Use certificados SSL
2. ✅ **CORS** - Whitelist domínios
3. ✅ **Rate Limiting** - Previne abuso
4. ✅ **SQL Injection** - SQLAlchemy ORM protege
5. ✅ **XSS** - Não renderizamos HTML não-seguro
6. ✅ **CSRF** - Importante para formulários
7. ✅ **SECRET_KEY** - Mude em produção!

---

**Essa arquitetura é escalável, maintível e segue as melhores práticas de desenvolvimento web moderno! 🚀**
