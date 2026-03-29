"""
Script para popular o banco de dados com dados de exemplo
Execute: python seed_data.py
"""

from app.database.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.annotator import Annotator
from app.models.job import Job
from app.models.carousel import Carousel
from app.models.sponsorship import Sponsorship
from app.core.security import get_password_hash
from datetime import datetime, timedelta

# Create tables
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    try:
        # Clear existing data (optional)
        db.query(User).delete()
        db.query(Annotator).delete()
        db.query(Job).delete()
        db.query(Carousel).delete()
        db.query(Sponsorship).delete()
        
        # Create admin user
        admin_user = User(
            email="admin@shopping.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            is_superuser=True,
            is_active=True
        )
        db.add(admin_user)
        
        # Create sample companies
        companies = [
            Annotator(
                company_name="TechStore Brasil",
                slug="techstore-brasil",
                description="Loja especializada em produtos tecnológicos de qualidade. Oferecemos as melhores marcas com preços competitivos.",
                email="contato@techstore.com",
                phone="(11) 3000-1000",
                website="https://techstore.com",
                city="São Paulo",
                state="SP",
                address="Rua Paulista, 1000",
                instagram_url="https://instagram.com/techstore",
                facebook_url="https://facebook.com/techstore",
                whatsapp_number="5511999990000",
                is_active=True,
                is_verified=True
            ),
            Annotator(
                company_name="Fashion Trends",
                slug="fashion-trends",
                description="Moda contemporânea com as últimas tendências. Roupas, acessórios e sapatos para homem, mulher e criança.",
                email="contato@fashiontrends.com",
                phone="(21) 2000-1000",
                website="https://fashiontrends.com",
                city="Rio de Janeiro",
                state="RJ",
                instagram_url="https://instagram.com/fashiontrends",
                facebook_url="https://facebook.com/fashiontrends",
                linkedin_url="https://linkedin.com/company/fashiontrends",
                is_active=True,
                is_verified=True
            ),
            Annotator(
                company_name="Gourmet Foods",
                slug="gourmet-foods",
                description="Alimentos premium importados e produtos gourmet. Especialistas em qualidade desde 2010.",
                email="vendas@gourmetfoods.com",
                phone="(31) 3000-5000",
                city="Belo Horizonte",
                state="MG",
                instagram_url="https://instagram.com/gourmetfoods",
                whatsapp_number="5531999995555",
                is_active=True,
                is_verified=True
            ),
        ]
        
        for company in companies:
            db.add(company)
        
        db.commit()
        
        # Create carousel items
        carousel_items = [
            Carousel(
                title="Bem-vindo ao TechStore",
                description="Confira nossos produtos de tecnologia em destaque",
                image_url="https://via.placeholder.com/800x400/FF6B6B/FFFFFF?text=TechStore",
                annotator_id=1,
                order=1,
                is_active=True
            ),
            Carousel(
                title="Fashion Trends - Novas Coleções",
                description="Veja as últimas tendências de moda",
                image_url="https://via.placeholder.com/800x400/4ECDC4/FFFFFF?text=Fashion",
                annotator_id=2,
                order=2,
                is_active=True
            ),
            Carousel(
                title="Gourmet Foods Premium",
                description="Produtos importados de qualidade",
                image_url="https://via.placeholder.com/800x400/FFE66D/FFFFFF?text=Gourmet",
                annotator_id=3,
                order=3,
                is_active=True
            ),
        ]
        
        for item in carousel_items:
            db.add(item)
        
        db.commit()
        
        # Create jobs
        jobs = [
            Job(
                title="Desenvolvedor Python Senior",
                description="Procuramos um desenvolvedor Python experiente com conhecimento em FastAPI para integrar nosso time de desenvolvimento.",
                category="it",
                employment_type="full-time",
                salary_min=8000,
                salary_max=12000,
                city="São Paulo",
                state="SP",
                company_id=1,
                company_name="TechStore Brasil",
                company_email="rh@techstore.com",
                company_phone="(11) 3000-1000",
                requirements="5+ anos experiência, FastAPI, PostgreSQL, Git, Docker",
                contact_email="rh@techstore.com",
                contact_phone="(11) 99999-0000",
                is_active=True,
                is_featured=True,
                expires_at=datetime.utcnow() + timedelta(days=30)
            ),
            Job(
                title="Assistente de Vendas",
                description="Procuramos um assistente de vendas entusiasmado para trabalhar em nossa loja física de RJ.",
                category="sales",
                employment_type="full-time",
                salary_min=2000,
                salary_max=3000,
                city="Rio de Janeiro",
                state="RJ",
                company_id=2,
                company_name="Fashion Trends",
                company_email="rh@fashiontrends.com",
                company_phone="(21) 2000-1000",
                requirements="Experiência em vendas, excelente comunicação, disponibilidade",
                contact_email="rh@fashiontrends.com",
                is_active=True,
                is_featured=False,
                expires_at=datetime.utcnow() + timedelta(days=30)
            ),
            Job(
                title="Gerente de Operações",
                description="Gerenciamento completo de operações logísticas e estoque de nossa empresa.",
                category="admin",
                employment_type="full-time",
                salary_min=5000,
                salary_max=7000,
                city="Belo Horizonte",
                state="MG",
                company_id=3,
                company_name="Gourmet Foods",
                company_email="rh@gourmetfoods.com",
                company_phone="(31) 3000-5000",
                requirements="5+ anos em gestão, Excel avançado, inglês",
                contact_email="rh@gourmetfoods.com",
                is_active=True,
                is_featured=False,
                expires_at=datetime.utcnow() + timedelta(days=30)
            ),
        ]
        
        for job in jobs:
            db.add(job)
        
        db.commit()
        
        # Create sponsorships
        sponsorships = [
            Sponsorship(
                company_name="Banco XYZ",
                logo_url="https://via.placeholder.com/200x100/1877F2/FFFFFF?text=Banco+XYZ",
                description="Soluções bancárias para você",
                position="banner",
                order=1,
                is_active=True,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=365)
            ),
            Sponsorship(
                company_name="Seguros ABC",
                logo_url="https://via.placeholder.com/200x100/25D366/FFFFFF?text=Seguros+ABC",
                description="Os melhores seguros do mercado",
                position="sidebar",
                order=1,
                is_active=True,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=365)
            ),
        ]
        
        for sponsorship in sponsorships:
            db.add(sponsorship)
        
        db.commit()
        
        print("✓ Database seeded successfully!")
        print("  - 1 Admin user created")
        print("  - 3 Companies created")
        print("  - 3 Carousel items created")
        print("  - 3 Jobs created")
        print("  - 2 Sponsorships created")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
