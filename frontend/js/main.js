// ==================== API Configuration ====================
const API_BASE = window.SHOPPINGHUB_CONFIG?.API_BASE || 'http://127.0.0.1:8000/api';

// ==================== CAROUSEL ====================
let currentSlide = 0;
let slides = [];
let allJobs = [];
let currentJobsPage = 1;
const JOBS_PER_PAGE = 6;
let selectedJob = null;
let sponsorSlides = [];
let currentSponsorPage = 0;
const SPONSORS_PER_PAGE = 4;
let featuredCompanies = [];
let currentCompaniesPage = 0;
const COMPANIES_PER_PAGE = 4;
const GROUP_FADE_DURATION_MS = 500;

async function initCarousel() {
    try {
        const response = await fetch(`${API_BASE}/carousel/`);
        const data = await response.json();
        slides = data;

        if (slides.length > 0) {
            renderCarousel();
            createCarouselDots();
            autoRotateCarousel();
        }
    } catch (error) {
        console.error('Error loading carousel:', error);
    }
}

function renderCarousel() {
    const carousel = document.getElementById('mainCarousel');
    if (!carousel) return;

    carousel.innerHTML = '';

    slides.forEach((slide, index) => {
        const item = document.createElement('div');
        item.className = `carousel-item ${index === 0 ? 'active' : ''}`;
        item.innerHTML = `
            <img src="${normalizeAssetPath(slide.image_url, '/img/placeholder.jpg')}" alt="${slide.title}">
            <div class="carousel-caption">
                <h2>${slide.title}</h2>
                <p>${slide.description || 'Bem-vindo ao Bom Contato'}</p>
            </div>
        `;
        carousel.appendChild(item);
    });
}

function createCarouselDots() {
    const dotsContainer = document.getElementById('carouselDots');
    if (!dotsContainer) return;

    dotsContainer.innerHTML = '';

    slides.forEach((_, index) => {
        const dot = document.createElement('span');
        dot.className = `dot ${index === 0 ? 'active' : ''}`;
        dot.onclick = () => goToSlide(index);
        dotsContainer.appendChild(dot);
    });
}

function nextSlide() {
    if (slides.length === 0) return;
    currentSlide = (currentSlide + 1) % slides.length;
    updateCarousel();
}

function prevSlide() {
    if (slides.length === 0) return;
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    updateCarousel();
}

function goToSlide(index) {
    currentSlide = index;
    updateCarousel();
}

function updateCarousel() {
    const items = document.querySelectorAll('.carousel-item');
    const dots = document.querySelectorAll('.dot');

    if (!items.length || !dots.length) return;

    items.forEach(item => item.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));

    items[currentSlide]?.classList.add('active');
    dots[currentSlide]?.classList.add('active');
}

function autoRotateCarousel() {
    setInterval(() => {
        nextSlide();
    }, 11000);
}

function getSponsorClickUrl(sponsor) {
    const rawValue = sponsor.website_url ? String(sponsor.website_url).trim() : '';
    if (!rawValue) return '';

    if (/^https?:\/\//i.test(rawValue)) {
        return rawValue;
    }

    const digits = rawValue.replace(/\D/g, '');
    return digits ? `https://wa.me/${digits}` : '';
}

// ==================== HELPERS ====================
function truncateText(value, maxLength) {
    if (!value) return '';
    return value.length > maxLength ? `${value.slice(0, maxLength)}...` : value;
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

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

    return `/${withoutFrontendPrefix}`;
}

function swapContainerWithFade(containerId, renderCallback) {
    const container = document.getElementById(containerId);
    if (!container) {
        renderCallback();
        return;
    }

    container.classList.remove('fade-swap-in');
    container.classList.add('fade-swap-out');

    window.setTimeout(() => {
        renderCallback();
        container.classList.remove('fade-swap-out');
        container.classList.add('fade-swap-in');

        window.setTimeout(() => {
            container.classList.remove('fade-swap-in');
        }, GROUP_FADE_DURATION_MS);
    }, GROUP_FADE_DURATION_MS);
}

async function getErrorMessage(response, fallbackMessage) {
    try {
        const error = await response.json();
        if (Array.isArray(error.detail)) {
            return error.detail.map(item => item.msg).join(', ');
        }
        return error.detail || fallbackMessage;
    } catch {
        return fallbackMessage;
    }
}

function getConnectionHelpMessage() {
    if (window.location.protocol === 'file:') {
        return 'Erro ao conectar com o servidor. Abra o frontend por http://localhost:3000 e mantenha a API em http://127.0.0.1:8000.';
    }

    return 'Erro ao conectar com o servidor. Verifique se a API FastAPI esta rodando em http://127.0.0.1:8000.';
}

// ==================== COMPANIES ====================
async function loadCompanies() {
    try {
        const response = await fetch(`${API_BASE}/annotators/?limit=12`);
        featuredCompanies = await response.json();
        currentCompaniesPage = 0;
        renderCompanies(featuredCompanies);
        createCompaniesDots();
        autoRotateCompanies();
    } catch (error) {
        console.error('Error loading companies:', error);
    }
}

function renderCompanies(companies) {
    const grid = document.getElementById('companiesGrid');
    if (!grid) return;

    grid.innerHTML = '';

    if (companies.length === 0) {
        grid.innerHTML = '<p style="text-align:center;color:var(--text-light)">Nenhuma empresa encontrada</p>';
        return;
    }

    const start = currentCompaniesPage * COMPANIES_PER_PAGE;
    const visibleCompanies = companies.slice(start, start + COMPANIES_PER_PAGE);

    visibleCompanies.forEach(company => {
        grid.appendChild(createCompanyCard(company));
    });
}

function createCompaniesDots() {
    const dotsContainer = document.getElementById('companiesDots');
    if (!dotsContainer) return;

    dotsContainer.innerHTML = '';

    const totalPages = Math.ceil(featuredCompanies.length / COMPANIES_PER_PAGE);
    if (totalPages <= 1) return;

    for (let index = 0; index < totalPages; index += 1) {
        const dot = document.createElement('span');
        dot.className = `dot ${index === currentCompaniesPage ? 'active' : ''}`;
        dot.onclick = () => goToCompaniesPage(index);
        dotsContainer.appendChild(dot);
    }
}

function updateCompaniesSlider() {
    swapContainerWithFade('companiesGrid', () => {
        renderCompanies(featuredCompanies);
    });

    const dots = document.querySelectorAll('#companiesDots .dot');
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentCompaniesPage);
    });
}

function goToCompaniesPage(index) {
    currentCompaniesPage = index;
    updateCompaniesSlider();
}

function nextCompaniesPage() {
    const totalPages = Math.ceil(featuredCompanies.length / COMPANIES_PER_PAGE);
    if (totalPages <= 1) return;

    currentCompaniesPage = (currentCompaniesPage + 1) % totalPages;
    updateCompaniesSlider();
}

function autoRotateCompanies() {
    const totalPages = Math.ceil(featuredCompanies.length / COMPANIES_PER_PAGE);
    if (totalPages <= 1) return;

    setInterval(() => {
        nextCompaniesPage();
    }, 12000);
}

function createCompanyCard(company) {
    const card = document.createElement('div');
    const description = company.description || 'Conheca esta empresa na plataforma.';
    const city = company.city || 'Cidade nao informada';
    const state = company.state || '';

    card.className = 'company-card';
    card.onclick = () => goToMicroSite(company.slug);

    const socialLinks = [];
    if (company.instagram_url) {
        socialLinks.push(`<a href="${company.instagram_url}" target="_blank" class="social-icon"><i class="fab fa-instagram"></i></a>`);
    }
    if (company.facebook_url) {
        socialLinks.push(`<a href="${company.facebook_url}" target="_blank" class="social-icon"><i class="fab fa-facebook"></i></a>`);
    }
    if (company.whatsapp_number) {
        socialLinks.push(`<a href="https://wa.me/${company.whatsapp_number}" target="_blank" class="social-icon"><i class="fab fa-whatsapp"></i></a>`);
    }

    card.innerHTML = `
        <div class="company-header">
            <img src="${normalizeAssetPath(company.banner_url, '/img/placeholder.jpg')}" alt="${company.company_name}" class="company-banner">
            <div class="company-logo">
                <img src="${normalizeAssetPath(company.logo_url, '/img/logo-placeholder.jpg')}" alt="Logo">
            </div>
        </div>
        <div class="company-body">
            <div class="company-name">${company.company_name}</div>
            <div class="company-location">
                <i class="fas fa-map-marker-alt"></i> ${city}${state ? `, ${state}` : ''}
            </div>
            <div class="company-description">${truncateText(description, 80)}</div>
            <div class="company-social">
                ${socialLinks.join('')}
            </div>
            <button class="company-btn">Visitar Loja</button>
        </div>
    `;

    return card;
}

function goToMicroSite(slug) {
    window.location.href = `pages/microsite.html?company=${slug}`;
}

// ==================== JOBS ====================
async function loadJobs(filters = {}) {
    try {
        let url = `${API_BASE}/jobs/?limit=100`;

        if (filters.search) url += `&search=${encodeURIComponent(filters.search)}`;
        if (filters.category) url += `&category=${encodeURIComponent(filters.category)}`;
        if (filters.city) url += `&city=${encodeURIComponent(filters.city)}`;
        if (filters.featured) url += '&featured_only=true';

        const response = await fetch(url);
        allJobs = await response.json();
        currentJobsPage = 1;
        renderJobsPage();
    } catch (error) {
        console.error('Error loading jobs:', error);
    }
}

function renderJobsPage() {
    const totalPages = Math.max(1, Math.ceil(allJobs.length / JOBS_PER_PAGE));
    const safePage = Math.min(currentJobsPage, totalPages);
    currentJobsPage = safePage;
    const start = (safePage - 1) * JOBS_PER_PAGE;
    const paginatedJobs = allJobs.slice(start, start + JOBS_PER_PAGE);
    renderJobs(paginatedJobs);
    renderJobsPagination(totalPages);
}

function renderJobs(jobs) {
    const grid = document.getElementById('jobsGrid');
    if (!grid) return;

    grid.innerHTML = '';

    if (jobs.length === 0) {
        grid.innerHTML = '<p style="text-align:center;color:var(--text-light)">Nenhuma vaga disponivel</p>';
        return;
    }

    jobs.forEach(job => {
        grid.appendChild(createJobCard(job));
    });
}

function renderJobsPagination(totalPages) {
    const wrapper = document.getElementById('jobsPagination');
    const prevBtn = document.getElementById('jobsPrevBtn');
    const nextBtn = document.getElementById('jobsNextBtn');
    const pageInfo = document.getElementById('jobsPageInfo');
    const pageNumbers = document.getElementById('jobsPageNumbers');

    if (!wrapper || !prevBtn || !nextBtn || !pageInfo || !pageNumbers) return;

    if (allJobs.length <= JOBS_PER_PAGE) {
        wrapper.style.display = 'none';
        pageNumbers.innerHTML = '';
        return;
    }

    wrapper.style.display = 'flex';
    prevBtn.disabled = currentJobsPage === 1;
    nextBtn.disabled = currentJobsPage === totalPages;
    pageInfo.textContent = `Pagina ${currentJobsPage} de ${totalPages}`;
    pageNumbers.innerHTML = buildPageNumbers(totalPages);

    pageNumbers.querySelectorAll('.pagination-number').forEach(button => {
        button.addEventListener('click', () => {
            currentJobsPage = Number(button.dataset.page);
            renderJobsPage();
        });
    });
}

function buildPageNumbers(totalPages) {
    let pages = [];

    for (let page = 1; page <= totalPages; page += 1) {
        pages.push(`
            <button
                type="button"
                class="pagination-number${page === currentJobsPage ? ' active' : ''}"
                data-page="${page}"
            >
                ${page}
            </button>
        `);
    }

    return pages.join('');
}

function createJobCard(job) {
    const card = document.createElement('div');
    const description = job.description || 'Confira os detalhes completos desta oportunidade.';
    const salaryRange = job.salary_min && job.salary_max
        ? `${formatCurrency(job.salary_min)} - ${formatCurrency(job.salary_max)}`
        : 'Salario a discutir';

    card.className = 'job-card';
    card.innerHTML = `
        <div class="job-title">${job.title}</div>
        <div class="job-company">${job.company_name}</div>
        <div class="job-info">
            <span class="job-badge"><i class="fas fa-map-marker-alt"></i> ${job.city}</span>
            <span class="job-badge"><i class="fas fa-briefcase"></i> ${job.category}</span>
        </div>
        <div class="job-description" id="jobDescription-${job.id}">${truncateText(description, 100)}</div>
        <div class="job-salary">${salaryRange}</div>
        <div class="job-actions">
            <button type="button" class="job-btn job-btn-secondary" id="jobToggle-${job.id}" onclick="toggleJobDescription(${job.id})" aria-expanded="false">Mais informacoes</button>
            <button type="button" class="job-btn" onclick="contactJob(${job.id})">Candidatar-se</button>
        </div>
    `;

    return card;
}

function toggleJobDescription(jobId) {
    const descriptionElement = document.getElementById(`jobDescription-${jobId}`);
    const toggleButton = document.getElementById(`jobToggle-${jobId}`);
    const cardElement = toggleButton?.closest('.job-card');
    const job = allJobs.find(currentJob => currentJob.id === jobId);

    if (!descriptionElement || !toggleButton || !cardElement || !job) return;

    const fullDescription = job.description || 'Confira os detalhes completos desta oportunidade.';
    const isExpanded = cardElement.classList.toggle('expanded');

    toggleButton.textContent = isExpanded ? 'Menos informacoes' : 'Mais informacoes';
    toggleButton.setAttribute('aria-expanded', String(isExpanded));

    descriptionElement.textContent = isExpanded
        ? fullDescription
        : truncateText(fullDescription, 100);
}

function contactJob(jobId) {
    selectedJob = allJobs.find(job => job.id === jobId) || null;
    const modal = document.getElementById('applyJobModal');
    const title = document.getElementById('applyJobTitle');
    const hiddenId = document.getElementById('applyJobId');

    if (!modal || !title || !hiddenId) return;

    title.textContent = selectedJob
        ? `${selectedJob.title} - ${selectedJob.company_name}`
        : `Vaga #${jobId}`;
    hiddenId.value = String(jobId);
    modal.style.display = 'block';
}

// ==================== SPONSORS ====================
async function loadSponsors() {
    try {
        const response = await fetch(`${API_BASE}/sponsorships/?position=banner`);
        sponsorSlides = await response.json();
        currentSponsorPage = 0;
        renderSponsors(sponsorSlides);
        createSponsorDots();
        autoRotateSponsors();
    } catch (error) {
        console.error('Error loading sponsors:', error);
    }
}

function renderSponsors(sponsors) {
    const container = document.getElementById('sponsorsContainer');
    if (!container) return;

    container.innerHTML = '';

    if (!sponsors.length) return;

    const start = currentSponsorPage * SPONSORS_PER_PAGE;
    const visibleSponsors = sponsors.slice(start, start + SPONSORS_PER_PAGE);

    visibleSponsors.forEach((sponsor) => {
        const card = document.createElement('div');
        card.className = 'sponsor-card active';
        const sponsorImage = sponsor.logo_url || sponsor.banner_url;
        const imageClass = 'sponsor-logo-image';
        const clickUrl = getSponsorClickUrl(sponsor);
        if (clickUrl) {
            card.onclick = () => window.open(clickUrl, '_blank');
        }
        card.innerHTML = `
            <img src="${normalizeAssetPath(sponsorImage, '/img/logo-placeholder.jpg')}" alt="${sponsor.company_name}" class="${imageClass}">
            <h3>${sponsor.company_name}</h3>
            <p>${sponsor.description || 'Patrocinador oficial'}</p>
        `;
        container.appendChild(card);
    });
}

function createSponsorDots() {
    const dotsContainer = document.getElementById('sponsorsDots');
    if (!dotsContainer) return;

    dotsContainer.innerHTML = '';

    const totalPages = Math.ceil(sponsorSlides.length / SPONSORS_PER_PAGE);
    if (totalPages <= 1) return;

    for (let index = 0; index < totalPages; index += 1) {
        const dot = document.createElement('span');
        dot.className = `dot ${index === currentSponsorPage ? 'active' : ''}`;
        dot.onclick = () => goToSponsorSlide(index);
        dotsContainer.appendChild(dot);
    }
}

function updateSponsorsCarousel() {
    const dots = document.querySelectorAll('#sponsorsDots .dot');
    swapContainerWithFade('sponsorsContainer', () => {
        renderSponsors(sponsorSlides);
    });

    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentSponsorPage);
    });
}

function goToSponsorSlide(index) {
    currentSponsorPage = index;
    updateSponsorsCarousel();
}

function nextSponsorSlide() {
    const totalPages = Math.ceil(sponsorSlides.length / SPONSORS_PER_PAGE);
    if (totalPages <= 1) return;
    currentSponsorPage = (currentSponsorPage + 1) % totalPages;
    updateSponsorsCarousel();
}

function autoRotateSponsors() {
    const totalPages = Math.ceil(sponsorSlides.length / SPONSORS_PER_PAGE);
    if (totalPages <= 1) return;

    setInterval(() => {
        nextSponsorSlide();
    }, 12000);
}

// ==================== SEARCH ====================
document.getElementById('searchForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const searchTerm = document.getElementById('searchInput')?.value?.trim();
    if (!searchTerm) return;

    try {
        const [companies, jobs] = await Promise.all([
            fetch(`${API_BASE}/annotators/?search=${encodeURIComponent(searchTerm)}`).then(r => r.json()),
            fetch(`${API_BASE}/jobs/?search=${encodeURIComponent(searchTerm)}`).then(r => r.json())
        ]);

        showSearchResults(companies, jobs);
    } catch (error) {
        console.error('Search error:', error);
    }
});

function showSearchResults(companies, jobs) {
    const carouselContainer = document.getElementById('mainCarousel')?.parentElement;
    const resultsSection = document.getElementById('searchResults');
    const container = document.getElementById('searchResultsContainer');

    if (!resultsSection || !container) return;
    if (carouselContainer) carouselContainer.style.display = 'none';

    resultsSection.style.display = 'block';
    container.innerHTML = '';

    const companiesTitle = document.createElement('h3');
    companiesTitle.textContent = `Empresas (${companies.length})`;
    container.appendChild(companiesTitle);

    const companiesGrid = document.createElement('div');
    companiesGrid.style.display = 'grid';
    companiesGrid.style.gridTemplateColumns = 'repeat(auto-fill,minmax(250px,1fr))';
    companiesGrid.style.gap = '2rem';
    companiesGrid.style.marginBottom = '3rem';
    companies.forEach(company => companiesGrid.appendChild(createCompanyCard(company)));
    container.appendChild(companiesGrid);

    const jobsTitle = document.createElement('h3');
    jobsTitle.textContent = `Vagas de Trabalho (${jobs.length})`;
    container.appendChild(jobsTitle);

    const jobsGrid = document.createElement('div');
    jobsGrid.style.display = 'grid';
    jobsGrid.style.gridTemplateColumns = 'repeat(auto-fill,minmax(300px,1fr))';
    jobsGrid.style.gap = '2rem';
    jobs.forEach(job => jobsGrid.appendChild(createJobCard(job)));
    container.appendChild(jobsGrid);

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ==================== FILTERS ====================
document.getElementById('jobSearch')?.addEventListener('input', () => {
    applyJobFilters();
});

document.getElementById('categoryFilter')?.addEventListener('change', () => {
    applyJobFilters();
});

document.getElementById('cityFilter')?.addEventListener('change', () => {
    applyJobFilters();
});

function applyJobFilters() {
    const filters = {
        search: document.getElementById('jobSearch')?.value || '',
        category: document.getElementById('categoryFilter')?.value || '',
        city: document.getElementById('cityFilter')?.value || ''
    };

    loadJobs(filters);
}

// ==================== MODALS ====================
document.getElementById('postJobBtn')?.addEventListener('click', () => {
    document.getElementById('postJobModal').style.display = 'block';
});

document.getElementById('loginBtn')?.addEventListener('click', () => {
    document.getElementById('loginModal').style.display = 'block';
});

document.getElementById('jobsPrevBtn')?.addEventListener('click', () => {
    if (currentJobsPage > 1) {
        currentJobsPage -= 1;
        renderJobsPage();
    }
});

document.getElementById('jobsNextBtn')?.addEventListener('click', () => {
    const totalPages = Math.ceil(allJobs.length / JOBS_PER_PAGE);
    if (currentJobsPage < totalPages) {
        currentJobsPage += 1;
        renderJobsPage();
    }
});

function closeModal() {
    document.getElementById('postJobModal').style.display = 'none';
}

function closeLoginModal() {
    document.getElementById('loginModal').style.display = 'none';
}

function closeApplyModal() {
    document.getElementById('applyJobModal').style.display = 'none';
}

window.onclick = (event) => {
    const postJobModal = document.getElementById('postJobModal');
    const loginModal = document.getElementById('loginModal');
    const applyJobModal = document.getElementById('applyJobModal');

    if (event.target === postJobModal) {
        postJobModal.style.display = 'none';
    }
    if (event.target === loginModal) {
        loginModal.style.display = 'none';
    }
    if (event.target === applyJobModal) {
        applyJobModal.style.display = 'none';
    }
};

document.getElementById('jobForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(document.getElementById('jobForm'));
    const jobData = {
        title: formData.get('title'),
        description: formData.get('description'),
        category: formData.get('category'),
        employment_type: formData.get('employment_type'),
        salary_min: formData.get('salary_min') ? parseInt(formData.get('salary_min'), 10) : null,
        salary_max: formData.get('salary_max') ? parseInt(formData.get('salary_max'), 10) : null,
        city: formData.get('city'),
        state: formData.get('state'),
        company_name: formData.get('company_name'),
        company_email: formData.get('company_email'),
        company_phone: formData.get('company_phone'),
        requirements: formData.get('requirements'),
        contact_email: formData.get('contact_email'),
        contact_phone: formData.get('contact_phone') || null
    };

    try {
        const response = await fetch(`${API_BASE}/jobs/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jobData)
        });

        if (response.ok) {
            alert('Vaga postada com sucesso!');
            closeModal();
            document.getElementById('jobForm').reset();
            loadJobs();
        } else {
            const error = await response.json();
            alert(`Erro ao postar vaga: ${error.detail || 'Tente novamente'}`);
            console.error('Job posting error:', error);
        }
    } catch (error) {
        alert('Erro ao conectar com o servidor');
        console.error('Job submission error:', error);
    }
});

document.getElementById('applyJobForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const jobId = document.getElementById('applyJobId')?.value;
    const form = document.getElementById('applyJobForm');
    if (!jobId || !form) return;

    const formData = new FormData(form);

    try {
        const response = await fetch(`${API_BASE}/jobs/${jobId}/apply`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.message || 'Candidatura enviada com sucesso!');
            closeApplyModal();
            form.reset();
        } else {
            const message = await getErrorMessage(response, 'Nao foi possivel enviar a candidatura');
            alert(`Erro: ${message}`);
        }
    } catch (error) {
        alert(getConnectionHelpMessage());
        console.error('Application error:', error);
    }
});

// ==================== AUTH ====================
function switchAuthTab(tab) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const loginTabBtn = document.getElementById('loginTabBtn');
    const registerTabBtn = document.getElementById('registerTabBtn');

    if (!loginForm || !registerForm || !loginTabBtn || !registerTabBtn) return;

    if (tab === 'login') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        loginTabBtn.classList.add('active');
        registerTabBtn.classList.remove('active');
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        loginTabBtn.classList.remove('active');
        registerTabBtn.classList.add('active');
    }
}

document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('accessToken', data.access_token);
            localStorage.setItem('userEmail', email);
            alert('Login realizado com sucesso!');
            closeLoginModal();
            updateAuthUI();
            document.getElementById('loginForm').reset();
        } else {
            const message = await getErrorMessage(response, 'Credenciais invalidas');
            alert(`Erro: ${message}`);
        }
    } catch (error) {
        alert(getConnectionHelpMessage());
        console.error('Login error:', error);
    }
});

document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const fullName = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const password2 = document.getElementById('registerPassword2').value;

    if (password !== password2) {
        alert('As senhas nao correspondem!');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                full_name: fullName,
                password
            })
        });

        if (response.ok) {
            alert('Cadastro realizado com sucesso! Faca login para continuar.');
            switchAuthTab('login');
            document.getElementById('loginEmail').value = email;
            document.getElementById('registerForm').reset();
        } else {
            const message = await getErrorMessage(response, 'Nao foi possivel cadastrar');
            alert(`Erro: ${message}`);
        }
    } catch (error) {
        alert(getConnectionHelpMessage());
        console.error('Register error:', error);
    }
});

function updateAuthUI() {
    const token = localStorage.getItem('accessToken');
    const userEmail = localStorage.getItem('userEmail');
    const loginBtn = document.getElementById('loginBtn');

    if (!loginBtn) return;

    if (token && userEmail) {
        loginBtn.innerHTML = `<i class="fas fa-user"></i> ${userEmail} <span id="logoutBtn" style="cursor:pointer; margin-left: 10px;">(Sair)</span>`;
        loginBtn.style.cursor = 'pointer';
        loginBtn.onclick = null;

        document.getElementById('logoutBtn')?.addEventListener('click', (e) => {
            e.stopPropagation();
            logout();
        });
    } else {
        loginBtn.innerHTML = '<i class="fas fa-user"></i> Conectar';
        loginBtn.onclick = () => {
            document.getElementById('loginModal').style.display = 'block';
        };
    }
}

function logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('userEmail');
    alert('Desconectado com sucesso!');
    updateAuthUI();
}

// ==================== INITIALIZE ====================
document.addEventListener('DOMContentLoaded', () => {
    initCarousel();
    loadCompanies();
    loadJobs();
    loadSponsors();
    updateAuthUI();
});
