// ==================== API Configuration ====================
const API_BASE = window.SHOPPINGHUB_CONFIG?.API_BASE || 'http://127.0.0.1:8000/api';

const params = new URLSearchParams(window.location.search);
const companySlug = params.get('company');

function normalizeAssetPath(value, fallback) {
    if (!value) return fallback;

    const normalizedValue = String(value).trim().replace(/\\/g, '/');
    if (!normalizedValue) return fallback;

    if (/^https?:\/\//i.test(normalizedValue) || normalizedValue.startsWith('data:')) {
        return normalizedValue;
    }

    const withoutFrontendPrefix = normalizedValue.replace(/^\.?\/?frontend\//i, '');
    if (withoutFrontendPrefix.startsWith('/')) {
        return withoutFrontendPrefix;
    }

    return withoutFrontendPrefix.startsWith('img/')
        ? `../${withoutFrontendPrefix}`
        : `../${withoutFrontendPrefix}`;
}

// ==================== Load Company Data ====================
async function loadCompanyData() {
    try {
        if (!companySlug) {
            window.location.href = '../index.html';
            return;
        }

        const response = await fetch(`${API_BASE}/annotators/slug/${companySlug}`);

        if (!response.ok) {
            throw new Error('Company not found');
        }

        const company = await response.json();
        renderCompanyPage(company);
    } catch (error) {
        console.error('Error loading company:', error);
        document.body.innerHTML = '<div class="container" style="text-align:center;margin-top:5rem"><h2>Empresa nao encontrada</h2></div>';
    }
}

function renderCompanyPage(company) {
    document.getElementById('companyNameNav').textContent = company.company_name;
    document.getElementById('companyLogo').src = normalizeAssetPath(company.logo_url, '../img/logo-placeholder.jpg');
    document.getElementById('companyName').textContent = company.company_name;
    document.getElementById('companyLocation').innerHTML =
        `<i class="fas fa-map-marker-alt"></i> ${company.city}, ${company.state}`;
    document.getElementById('companyDesc').textContent = company.description;
    document.getElementById('aboutText').textContent = company.description;
    renderGallery(company);

    document.getElementById('phone').textContent = company.phone || '-';
    document.getElementById('email').textContent = company.email || '-';

    if (company.website) {
        document.getElementById('website').href = company.website;
        document.getElementById('website').textContent = 'Visitar';
    } else {
        document.getElementById('website').parentElement.style.display = 'none';
    }

    setupSocialLinks(company);
}

function renderGallery(company) {
    const gallery = document.getElementById('galleryContainer');
    if (!gallery) return;

    const photos = [
        company.photo_1_url,
        company.photo_2_url,
        company.photo_3_url,
        company.photo_4_url
    ].filter(Boolean);

    if (!photos.length) {
        gallery.innerHTML = `
            <div class="gallery-empty">
                <p>Nenhuma foto cadastrada para esta empresa ainda.</p>
            </div>
        `;
        return;
    }

    gallery.innerHTML = photos.map((photo, index) => `
        <div class="gallery-item">
            <img src="${normalizeAssetPath(photo, '../img/placeholder.jpg')}" alt="Galeria ${index + 1}">
        </div>
    `).join('');
}

function setupSocialLinks(company) {
    const socials = [
        { element: 'socialFacebook', url: company.facebook_url },
        { element: 'socialInstagram', url: company.instagram_url },
        { element: 'socialTwitter', url: company.twitter_url },
        { element: 'socialLinkedin', url: company.linkedin_url }
    ];

    socials.forEach(social => {
        const elem = document.getElementById(social.element);
        if (!elem) return;

        if (social.url) {
            elem.href = social.url;
            elem.style.display = 'flex';
        } else {
            elem.style.display = 'none';
        }
    });

    const whatsapp = document.getElementById('socialWhatsapp');
    if (!whatsapp) return;

    if (company.whatsapp_number) {
        whatsapp.href = `https://wa.me/${company.whatsapp_number}`;
        whatsapp.style.display = 'flex';
    } else {
        whatsapp.style.display = 'none';
    }
}

// ==================== Contact Buttons ====================
document.querySelectorAll('.btn-contact').forEach(btn => {
    btn.addEventListener('click', (e) => {
        if (e.target.closest('.btn-contact').classList.contains('secondary')) {
            const phone = document.getElementById('phone').textContent;
            if (phone && phone !== '-') {
                window.location.href = `tel:${phone}`;
            }
        } else {
            alert('Sistema de mensagens em desenvolvimento');
        }
    });
});

// ==================== Initialize ====================
document.addEventListener('DOMContentLoaded', () => {
    loadCompanyData();
});
