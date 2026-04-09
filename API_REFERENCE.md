# 📦 API Reference - Bom Contato

## Base URL
```
http://localhost:8000/api
```

## Status Codes
- `200` OK - Sucesso
- `201` Created - Recurso criado
- `400` Bad Request - Dados inválidos
- `401` Unauthorized - Não autenticado
- `404` Not Found - Recurso não existe
- `500` Server Error - Erro do servidor

---

## 🔐 Autenticação

### Register (Registre um novo usuário)
```
POST /auth/register

{
    "email": "usuario@example.com",
    "full_name": "Seu Nome",
    "password": "senha123"
}

Response (200):
{
    "id": 1,
    "email": "usuario@example.com",
    "full_name": "Seu Nome",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00"
}
```

### Login (Obter token de acesso)
```
POST /auth/login

{
    "email": "usuario@example.com",
    "password": "senha123"
}

Response (200):
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### Get Current User
```
GET /auth/me
Headers: Authorization: Bearer {access_token}

Response (200):
{
    "user_id": "1"
}
```

---

## 🏢 Annotators (Empresas)

### List Companies
```
GET /annotators/?skip=0&limit=20&search=tech

Query Parameters:
- skip: int (padrão: 0)
- limit: int (padrão: 20, máx: 100)
- search: str (busca na empresa)

Response (200):
[
    {
        "id": 1,
        "company_name": "TechStore Brasil",
        "slug": "techstore-brasil",
        "logo_url": "https://..."
    }
]
```

### Create Company
```
POST /annotators/

{
    "company_name": "Tech Store",
    "slug": "tech-store",
    "description": "Loja de tecnologia",
    "email": "contato@techstore.com",
    "phone": "(11) 3000-1000",
    "website": "https://techstore.com",
    "city": "São Paulo",
    "state": "SP",
    "address": "Rua X, 100",
    "facebook_url": "https://facebook.com/techstore",
    "instagram_url": "https://instagram.com/techstore",
    "whatsapp_number": "5511999999999",
    "twitter_url": "https://twitter.com/techstore",
    "linkedin_url": "https://linkedin.com/company/techstore"
}

Response (200): [Completo AnnotatorResponse]
```

### Get Company by ID
```
GET /annotators/{id}

Response (200): [Completo AnnotatorResponse]
```

### Get Company by Slug (Micro Site)
```
GET /annotators/slug/{slug}

Response (200): [Completo AnnotatorResponse]
```

### Update Company
```
PUT /annotators/{id}

{
    "company_name": "Tech Store Updated",
    "description": "Nova descrição",
    ...campos opcionais
}

Response (200): [AnnotatorResponse atualizado]
```

### Delete Company (Soft Delete)
```
DELETE /annotators/{id}

Response (200):
{
    "message": "Annotator deleted"
}
```

---

## 💼 Jobs (Vagas de Emprego)

### List Jobs with Filters
```
GET /jobs/?skip=0&limit=20&search=python&category=it&city=São Paulo&featured_only=false

Query Parameters:
- skip: int
- limit: int
- search: str
- category: str (sales, it, marketing, hr, admin)
- city: str
- featured_only: bool

Response (200):
[
    {
        "id": 1,
        "title": "Desenvolvedor Python",
        "company_name": "TechStore",
        "city": "São Paulo",
        "category": "it",
        "salary_min": 8000,
        "salary_max": 12000
    }
]
```

### Create Job
```
POST /jobs/

{
    "title": "Desenvolvedor Python Senior",
    "description": "Procuramos um dev experiente...",
    "category": "it",
    "employment_type": "full-time",
    "salary_min": 8000,
    "salary_max": 12000,
    "city": "São Paulo",
    "state": "SP",
    "company_id": 1,
    "company_name": "TechStore Brasil",
    "company_email": "rh@techstore.com",
    "company_phone": "(11) 3000-1000",
    "requirements": "5+ anos experiência",
    "contact_email": "rh@techstore.com",
    "contact_phone": "(11) 99999-0000"
}

Response (200): [JobResponse completo]
```

### Get Job Details
```
GET /jobs/{id}

Response (200): [JobResponse completo]
```

### Update Job
```
PUT /jobs/{id}

{
    "title": "Novo título",
    "salary_min": 9000,
    ...campos opcionais
}

Response (200): [JobResponse atualizado]
```

### Delete Job
```
DELETE /jobs/{id}

Response (200):
{
    "message": "Job deleted"
}
```

### Get Company Jobs
```
GET /jobs/company/{company_id}?skip=0&limit=20

Response (200): [Array de JobMiniResponse]
```

---

## 🎠 Carousel (Carrossel)

### List Carousel Items
```
GET /carousel/?skip=0&limit=10

Response (200):
[
    {
        "id": 1,
        "title": "TechStore - Oferta do Mês",
        "description": "Confira nossas ofertas...",
        "image_url": "https://...",
        "link_url": "/annotators/slug/techstore-brasil",
        "annotator_id": 1,
        "order": 1,
        "is_active": true,
        "auto_rotate": true,
        "created_at": "2024-01-15T10:30:00"
    }
]
```

### Create Carousel Item
```
POST /carousel/

{
    "title": "Meu Negócio",
    "description": "Descrição da oferta",
    "image_url": "https://exemplo.com/imagem.jpg",
    "link_url": "https://meusite.com",
    "annotator_id": 1,
    "order": 1,
    "rotation_speed": 5000
}

Response (200): [CarouselResponse]
```

### Get Carousel Item
```
GET /carousel/{id}

Response (200): [CarouselResponse]
```

### Update Carousel Item
```
PUT /carousel/{id}

{
    "title": "Novo título",
    "order": 2,
    ...campos opcionais
}

Response (200): [CarouselResponse atualizado]
```

### Delete Carousel Item
```
DELETE /carousel/{id}

Response (200):
{
    "message": "Carousel item deleted"
}
```

---

## 📢 Sponsorships (Patrocínios)

### List Sponsorships
```
GET /sponsorships/?position=banner&skip=0&limit=10

Query Parameters:
- position: str (banner, sidebar, footer)
- skip: int
- limit: int

Response (200):
[
    {
        "id": 1,
        "company_name": "Banco XYZ",
        "logo_url": "https://...",
        "banner_url": "https://...",
        "description": "Soluções bancárias",
        "website_url": "https://bancoXYZ.com",
        "position": "banner",
        "order": 1,
        "is_active": true,
        "start_date": "2024-01-15",
        "end_date": "2025-01-15"
    }
]
```

### Create Sponsorship
```
POST /sponsorships/

{
    "company_name": "Seguros ABC",
    "logo_url": "https://...",
    "banner_url": "https://...",
    "description": "Os melhores seguros",
    "website_url": "https://segurosABC.com",
    "position": "sidebar",
    "order": 1,
    "start_date": "2024-01-15T00:00:00",
    "end_date": "2025-01-15T00:00:00"
}

Response (200): [SponsorshipResponse]
```

### Get Sponsorship
```
GET /sponsorships/{id}

Response (200): [SponsorshipResponse]
```

### Update Sponsorship
```
PUT /sponsorships/{id}

{
    "company_name": "Novo Nome",
    "position": "footer",
    ...campos opcionais
}

Response (200): [SponsorshipResponse atualizado]
```

### Delete Sponsorship
```
DELETE /sponsorships/{id}

Response (200):
{
    "message": "Sponsorship deleted"
}
```

---

## 🏥 Health Check

### API Status
```
GET /

Response (200):
{
    "message": "Shopping Platform API",
    "version": "1.0.0",
    "docs": "/docs"
}
```

### Health Check
```
GET /health

Response (200):
{
    "status": "healthy"
}
```

---

## 📋 Error Responses

### 400 Bad Request
```json
{
    "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
    "detail": "Could not validate credentials",
    "headers": {
        "WWW-Authenticate": "Bearer"
    }
}
```

### 404 Not Found
```json
{
    "detail": "Company not found"
}
```

### 422 Unprocessable Entity (Validation Error)
```json
{
    "detail": [
        {
            "loc": ["body", "email"],
            "msg": "invalid email format",
            "type": "value_error.email"
        }
    ]
}
```

---

## 🧪 Exemplo de Fluxo Completo

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "full_name": "Admin",
    "password": "admin123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

### 3. Create Company
```bash
curl -X POST http://localhost:8000/api/annotators/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Minha Loja",
    "slug": "minha-loja",
    "description": "Descrição da loja",
    "email": "contato@minhaloja.com",
    "phone": "11999999999",
    "city": "São Paulo",
    "state": "SP"
  }'
```

### 4. Create Job Posting
```bash
curl -X POST http://localhost:8000/api/jobs/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Dev Web",
    "description": "Procuramos dev web",
    "category": "it",
    "employment_type": "full-time",
    "salary_min": 5000,
    "salary_max": 8000,
    "city": "São Paulo",
    "state": "SP",
    "company_name": "Minha Loja",
    "company_email": "rh@minhaloja.com",
    "company_phone": "11999999999",
    "requirements": "3+ anos",
    "contact_email": "rh@minhaloja.com"
  }'
```

### 5. Search Companies
```bash
curl "http://localhost:8000/api/annotators/?search=Minha&limit=10"
```

### 6. Get Company by Slug (Micro Site)
```bash
curl "http://localhost:8000/api/annotators/slug/minha-loja"
```

---

## 📚 Documentação Interativa

Acesse **http://localhost:8000/docs** para Swagger UI completo com:
- ✅ Testes de endpoint
- ✅ Esquemas visuais
- ✅ Exemplos de requisição/resposta
- ✅ Modelos e tipos

---

## 🔄 Paginação

Todos os endpoints de listagem suportam paginação:

```bash
GET /api/annotators/?skip=0&limit=20
# Retorna items 0-20

GET /api/annotators/?skip=20&limit=20
# Retorna items 20-40
```

### Cálculo de páginas em JavaScript:
```javascript
const pageSize = 20;
const currentPage = 1;
const skip = (currentPage - 1) * pageSize;

fetch(`/api/annotators/?skip=${skip}&limit=${pageSize}`)
```

---

## 🔍 Busca e Filtros

### Busca Full-Text
```bash
# Busca em múltiplos campos
GET /api/annotators/?search=tech

# Busca de vagas
GET /api/jobs/?search=python
```

### Filtros Específicos
```bash
# Vagas por categoria
GET /api/jobs/?category=it

# Vagas por cidade
GET /api/jobs/?city=São Paulo

# Vagas em destaque
GET /api/jobs/?featured_only=true

# Combinado
GET /api/jobs/?search=dev&category=it&city=São Paulo
```

---

**🎉 Pronto para integrar? Use a documentação Swagger em `/docs`!**
