const API_BASE = window.SHOPPINGHUB_CONFIG?.API_BASE || 'http://127.0.0.1:8000/api';

const state = {
    token: localStorage.getItem('adminAccessToken') || '',
    user: null,
    hasAdmin: true,
    annotators: [],
    jobs: [],
    carousel: [],
    sponsors: [],
    branding: {
        brand_logo_url: '',
        admin_brand_logo_url: ''
    },
    editing: {
        annotatorId: null,
        jobId: null,
        carouselId: null,
        sponsorId: null
    }
};

function authHeaders(json = true) {
    const headers = {
        Authorization: `Bearer ${state.token}`
    };
    if (json) headers['Content-Type'] = 'application/json';
    return headers;
}

async function fetchJson(url, options = {}) {
    const response = await fetch(url, options);
    let payload = null;

    try {
        payload = await response.json();
    } catch {
        payload = null;
    }

    if (!response.ok) {
        throw new Error(payload?.detail || 'Falha na requisicao');
    }

    return payload;
}

function setMessage(id, message, isError = false) {
    const node = document.getElementById(id);
    if (!node) return;
    node.textContent = message;
    node.style.color = isError ? '#b63f2b' : '#2a7f4f';
}

function normalizeAssetInput(value) {
    if (!value) return null;

    const normalizedValue = String(value).trim().replace(/\\/g, '/');
    if (!normalizedValue) return null;

    if (/^https?:\/\//i.test(normalizedValue) || normalizedValue.startsWith('data:')) {
        return normalizedValue;
    }

    const withoutFrontendPrefix = normalizedValue.replace(/^\.?\/?frontend\//i, '');
    return withoutFrontendPrefix.startsWith('/') ? withoutFrontendPrefix : `/${withoutFrontendPrefix}`;
}

function slugify(value) {
    return String(value || '')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()
        .trim()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '');
}

async function uploadAdminImage(file, folder, targetInputId, messageId) {
    if (!state.token) {
        setMessage(messageId, 'Faca login como administrador antes de enviar imagens.', true);
        return;
    }

    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    setMessage(messageId, 'Enviando imagem...');

    try {
        const response = await fetch(`${API_BASE}/admin/upload-image?folder=${encodeURIComponent(folder)}`, {
            method: 'POST',
            headers: authHeaders(false),
            body: formData
        });

        let payload = null;
        try {
            payload = await response.json();
        } catch {
            payload = null;
        }

        if (!response.ok) {
            throw new Error(payload?.detail || 'Falha ao enviar imagem');
        }

        const targetInput = document.getElementById(targetInputId);
        if (targetInput) {
            targetInput.value = payload.url;
        }

        setMessage(messageId, 'Imagem enviada com sucesso.');
        return payload;
    } catch (error) {
        setMessage(messageId, error.message, true);
        return null;
    }
}

function wireImageUpload(fileInputId, folder, targetInputId, messageId, onUploaded = null) {
    const fileInput = document.getElementById(fileInputId);
    if (!fileInput) return;

    fileInput.addEventListener('change', async (event) => {
        const selectedFile = event.target.files?.[0];
        const payload = await uploadAdminImage(selectedFile, folder, targetInputId, messageId);
        if (payload && onUploaded) {
            await onUploaded(payload);
        }
        fileInput.value = '';
    });
}

async function loadAdminStatus() {
    const data = await fetchJson(`${API_BASE}/auth/admin-status`);
    state.hasAdmin = data.has_admin;
    document.getElementById('bootstrapHint').style.display = data.has_admin ? 'none' : 'block';
}

async function tryRestoreSession() {
    if (!state.token) return;

    try {
        const me = await fetchJson(`${API_BASE}/auth/me`, {
            headers: authHeaders(false)
        });
        state.user = me;

        if (!me.is_superuser) {
            renderAuthState(false);
            return;
        }

        renderAuthState(true);
        await loadAdminData();
    } catch {
        logout();
    }
}

function renderAuthState(isAdmin) {
    document.getElementById('authCard').style.display = isAdmin ? 'none' : 'grid';
    document.getElementById('adminApp').style.display = isAdmin ? 'block' : 'none';
    document.getElementById('logoutBtn').style.display = state.token ? 'inline-flex' : 'none';

    if (state.user && !isAdmin) {
        setMessage(
            'authMessage',
            state.hasAdmin
                ? 'Sua conta existe, mas nao possui permissao de administrador.'
                : 'Nao existe administrador ainda. Use o botao abaixo para promover esta conta.',
            true
        );
    }
}

async function handleAdminLogin(event) {
    event.preventDefault();
    setMessage('authMessage', '');

    const email = document.getElementById('adminEmail').value;
    const password = document.getElementById('adminPassword').value;

    try {
        const tokenData = await fetchJson(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        state.token = tokenData.access_token;
        localStorage.setItem('adminAccessToken', state.token);

        const me = await fetchJson(`${API_BASE}/auth/me`, {
            headers: authHeaders(false)
        });
        state.user = me;

        if (!me.is_superuser) {
            renderAuthState(false);
            return;
        }

        renderAuthState(true);
        await loadAdminData();
    } catch (error) {
        setMessage('authMessage', error.message, true);
    }
}

async function bootstrapAdmin() {
    try {
        const me = await fetchJson(`${API_BASE}/auth/bootstrap-admin`, {
            method: 'POST',
            headers: authHeaders(false)
        });
        state.user = me;
        state.hasAdmin = true;
        renderAuthState(true);
        await loadAdminData();
    } catch (error) {
        setMessage('authMessage', error.message, true);
    }
}

function logout() {
    state.token = '';
    state.user = null;
    localStorage.removeItem('adminAccessToken');
    renderAuthState(false);
}

async function loadAdminData() {
    const results = await Promise.allSettled([
        fetchJson(`${API_BASE}/admin/dashboard`, { headers: authHeaders(false) }),
        fetchJson(`${API_BASE}/admin/annotators`, { headers: authHeaders(false) }),
        fetchJson(`${API_BASE}/admin/jobs`, { headers: authHeaders(false) }),
        fetchJson(`${API_BASE}/admin/carousel`, { headers: authHeaders(false) }),
        fetchJson(`${API_BASE}/admin/sponsorships`, { headers: authHeaders(false) }),
        fetchJson(`${API_BASE}/admin/branding`, { headers: authHeaders(false) })
    ]);

    const [dashboardResult, annotatorsResult, jobsResult, carouselResult, sponsorsResult, brandingResult] = results;
    const failures = results.filter(result => result.status === 'rejected');

    document.getElementById('adminWelcome').textContent = `Bem-vindo, ${state.user.full_name}`;
    setMessage(
        'adminDataMessage',
        failures.length ? 'Alguns dados do painel nao puderam ser carregados. Recarregue a pagina apos reiniciar o backend.' : ''
    );

    renderDashboard(dashboardResult.status === 'fulfilled' ? dashboardResult.value : null);
    state.annotators = annotatorsResult.status === 'fulfilled' ? annotatorsResult.value : [];
    state.jobs = jobsResult.status === 'fulfilled' ? jobsResult.value : [];
    state.carousel = carouselResult.status === 'fulfilled' ? carouselResult.value : [];
    state.sponsors = sponsorsResult.status === 'fulfilled' ? sponsorsResult.value : [];
    state.branding = brandingResult.status === 'fulfilled'
        ? brandingResult.value
        : { brand_logo_url: '', admin_brand_logo_url: '' };

    renderAnnotators();
    renderJobs();
    renderCarousel();
    renderSponsors();
    renderBranding();
    fillAnnotatorSelect();
}

function renderDashboard(data) {
    const statsGrid = document.getElementById('statsGrid');
    if (!data) {
        statsGrid.innerHTML = '';
        return;
    }

    const cards = [
        ['Empresas ativas', data.annotators_active, `${data.annotators_total} cadastradas`],
        ['Vagas ativas', data.jobs_active, `${data.jobs_total} cadastradas`],
        ['Carousel ativo', data.carousel_active, `${data.carousel_total} itens`],
        ['Patrocinios ativos', data.sponsorships_active, `${data.sponsorships_total} itens`]
    ];

    statsGrid.innerHTML = cards.map(([label, value, hint]) => `
        <div class="stat-card">
            <span class="muted">${label}</span>
            <strong>${value}</strong>
            <span class="muted">${hint}</span>
        </div>
    `).join('');
}

function renderAnnotators() {
    document.getElementById('annotatorsTable').innerHTML = state.annotators.length ? state.annotators.map(item => `
        <tr>
            <td><strong>${item.company_name}</strong><br><span class="muted">${item.slug}</span></td>
            <td>${item.city}, ${item.state}</td>
            <td>${item.is_active ? 'Ativa' : 'Inativa'}${item.is_verified ? ' / Verificada' : ''}</td>
            <td><div class="row-actions"><button class="mini-btn" onclick="editAnnotator(${item.id})">Editar</button><button class="mini-btn danger" onclick="deleteAnnotator(${item.id})">Desativar</button></div></td>
        </tr>
    `).join('') : '<tr><td colspan="4" class="muted">Nenhuma empresa carregada.</td></tr>';
}

function renderJobs() {
    document.getElementById('jobsTable').innerHTML = state.jobs.length ? state.jobs.map(item => `
        <tr>
            <td><strong>${item.title}</strong><br><span class="muted">${item.category}</span></td>
            <td>${item.company_name}</td>
            <td>${item.is_active ? 'Ativa' : 'Inativa'}${item.is_featured ? ' / Destaque' : ''}</td>
            <td><div class="row-actions"><button class="mini-btn" onclick="editJob(${item.id})">Editar</button><button class="mini-btn danger" onclick="deleteJob(${item.id})">Desativar</button></div></td>
        </tr>
    `).join('') : '<tr><td colspan="4" class="muted">Nenhuma vaga carregada.</td></tr>';
}

function renderCarousel() {
    document.getElementById('carouselTable').innerHTML = state.carousel.length ? state.carousel.map(item => `
        <tr>
            <td><strong>${item.title}</strong><br><span class="muted">${item.image_url}</span></td>
            <td>${item.order}</td>
            <td>${item.is_active ? 'Ativo' : 'Inativo'}</td>
            <td><div class="row-actions"><button class="mini-btn" onclick="editCarousel(${item.id})">Editar</button><button class="mini-btn danger" onclick="deleteCarousel(${item.id})">Desativar</button></div></td>
        </tr>
    `).join('') : '<tr><td colspan="4" class="muted">Nenhum item de carousel carregado.</td></tr>';
}

function renderSponsors() {
    document.getElementById('sponsorsTable').innerHTML = state.sponsors.length ? state.sponsors.map(item => `
        <tr>
            <td><strong>${item.company_name}</strong><br><span class="muted">${item.website_url || '-'}</span></td>
            <td>${item.position}</td>
            <td>${item.is_active ? 'Ativo' : 'Inativo'}</td>
            <td><div class="row-actions"><button class="mini-btn" onclick="editSponsor(${item.id})">Editar</button><button class="mini-btn danger" onclick="deleteSponsor(${item.id})">Desativar</button></div></td>
        </tr>
    `).join('') : '<tr><td colspan="4" class="muted">Nenhum patrocinio carregado.</td></tr>';
}

function fillAnnotatorSelect() {
    document.getElementById('carouselAnnotatorId').innerHTML =
        '<option value="">Sem empresa vinculada</option>' +
        state.annotators.map(item => `<option value="${item.id}">${item.company_name}</option>`).join('');
}

function toDateTimeLocal(value) {
    if (!value) return '';
    return new Date(value).toISOString().slice(0, 16);
}

function resetAnnotatorForm() {
    state.editing.annotatorId = null;
    document.getElementById('annotatorFormTitle').textContent = 'Nova empresa';
    document.getElementById('annotatorForm').reset();
    document.getElementById('annotatorId').value = '';
    document.getElementById('annotatorIsActive').checked = true;
    document.getElementById('annotatorIsVerified').checked = false;
    setMessage('annotatorMessage', '');
}

function resetJobForm() {
    state.editing.jobId = null;
    document.getElementById('jobFormTitle').textContent = 'Nova vaga';
    document.getElementById('jobAdminForm').reset();
    document.getElementById('jobId').value = '';
    document.getElementById('jobIsActive').checked = true;
    document.getElementById('jobIsFeatured').checked = false;
    setMessage('jobMessage', '');
}

function resetCarouselForm() {
    state.editing.carouselId = null;
    document.getElementById('carouselFormTitle').textContent = 'Novo item';
    document.getElementById('carouselForm').reset();
    document.getElementById('carouselId').value = '';
    document.getElementById('carouselOrder').value = '0';
    document.getElementById('carouselRotationSpeed').value = '5000';
    document.getElementById('carouselIsActive').checked = true;
    setMessage('carouselMessage', '');
}

function resetSponsorForm() {
    state.editing.sponsorId = null;
    document.getElementById('sponsorFormTitle').textContent = 'Novo patrocinio';
    document.getElementById('sponsorForm').reset();
    document.getElementById('sponsorId').value = '';
    document.getElementById('sponsorOrder').value = '0';
    document.getElementById('sponsorIsActive').checked = true;
    setMessage('sponsorMessage', '');
}

function renderBranding() {
    document.getElementById('brandLogoUrl').value = state.branding.brand_logo_url || '';
    document.getElementById('adminBrandLogoUrl').value = state.branding.admin_brand_logo_url || '';

    const adminBrandLogo = document.getElementById('adminBrandLogo');
    if (adminBrandLogo && (state.branding.admin_brand_logo_url || state.branding.brand_logo_url)) {
        adminBrandLogo.src = state.branding.admin_brand_logo_url || state.branding.brand_logo_url;
    }
}

function editAnnotator(id) {
    const item = state.annotators.find(entry => entry.id === id);
    if (!item) return;
    state.editing.annotatorId = id;
    document.getElementById('annotatorFormTitle').textContent = `Editar empresa #${id}`;
    document.getElementById('annotatorId').value = item.id;
    document.getElementById('annotatorCompanyName').value = item.company_name || '';
    document.getElementById('annotatorSlug').value = item.slug || '';
    document.getElementById('annotatorDescription').value = item.description || '';
    document.getElementById('annotatorEmail').value = item.email || '';
    document.getElementById('annotatorPhone').value = item.phone || '';
    document.getElementById('annotatorWebsite').value = item.website || '';
    document.getElementById('annotatorCity').value = item.city || '';
    document.getElementById('annotatorState').value = item.state || '';
    document.getElementById('annotatorAddress').value = item.address || '';
    document.getElementById('annotatorLogoUrl').value = item.logo_url || '';
    document.getElementById('annotatorBannerUrl').value = item.banner_url || '';
    document.getElementById('annotatorPhoto1Url').value = item.photo_1_url || '';
    document.getElementById('annotatorPhoto2Url').value = item.photo_2_url || '';
    document.getElementById('annotatorPhoto3Url').value = item.photo_3_url || '';
    document.getElementById('annotatorPhoto4Url').value = item.photo_4_url || '';
    document.getElementById('annotatorFacebookUrl').value = item.facebook_url || '';
    document.getElementById('annotatorInstagramUrl').value = item.instagram_url || '';
    document.getElementById('annotatorWhatsapp').value = item.whatsapp_number || '';
    document.getElementById('annotatorTwitterUrl').value = item.twitter_url || '';
    document.getElementById('annotatorLinkedinUrl').value = item.linkedin_url || '';
    document.getElementById('annotatorIsActive').checked = !!item.is_active;
    document.getElementById('annotatorIsVerified').checked = !!item.is_verified;
}

function editJob(id) {
    const item = state.jobs.find(entry => entry.id === id);
    if (!item) return;
    state.editing.jobId = id;
    document.getElementById('jobFormTitle').textContent = `Editar vaga #${id}`;
    document.getElementById('jobId').value = item.id;
    document.getElementById('jobTitle').value = item.title || '';
    document.getElementById('jobCategory').value = item.category || '';
    document.getElementById('jobDescription').value = item.description || '';
    document.getElementById('jobEmploymentType').value = item.employment_type || '';
    document.getElementById('jobCompanyId').value = item.company_id || '';
    document.getElementById('jobCompanyName').value = item.company_name || '';
    document.getElementById('jobCompanyEmail').value = item.company_email || '';
    document.getElementById('jobCompanyPhone').value = item.company_phone || '';
    document.getElementById('jobSalaryMin').value = item.salary_min || '';
    document.getElementById('jobSalaryMax').value = item.salary_max || '';
    document.getElementById('jobCity').value = item.city || '';
    document.getElementById('jobState').value = item.state || '';
    document.getElementById('jobRequirements').value = item.requirements || '';
    document.getElementById('jobContactEmail').value = item.contact_email || '';
    document.getElementById('jobContactPhone').value = item.contact_phone || '';
    document.getElementById('jobIsFeatured').checked = !!item.is_featured;
    document.getElementById('jobIsActive').checked = !!item.is_active;
}

function editCarousel(id) {
    const item = state.carousel.find(entry => entry.id === id);
    if (!item) return;
    state.editing.carouselId = id;
    document.getElementById('carouselFormTitle').textContent = `Editar item #${id}`;
    document.getElementById('carouselId').value = item.id;
    document.getElementById('carouselTitle').value = item.title || '';
    document.getElementById('carouselAnnotatorId').value = item.annotator_id || '';
    document.getElementById('carouselDescription').value = item.description || '';
    document.getElementById('carouselImageUrl').value = item.image_url || '';
    document.getElementById('carouselLinkUrl').value = item.link_url || '';
    document.getElementById('carouselOrder').value = item.order ?? 0;
    document.getElementById('carouselRotationSpeed').value = item.rotation_speed ?? 5000;
    document.getElementById('carouselIsActive').checked = !!item.is_active;
}

function editSponsor(id) {
    const item = state.sponsors.find(entry => entry.id === id);
    if (!item) return;
    state.editing.sponsorId = id;
    document.getElementById('sponsorFormTitle').textContent = `Editar patrocinio #${id}`;
    document.getElementById('sponsorId').value = item.id;
    document.getElementById('sponsorCompanyName').value = item.company_name || '';
    document.getElementById('sponsorPosition').value = item.position || 'banner';
    document.getElementById('sponsorLogoUrl').value = item.logo_url || '';
    document.getElementById('sponsorBannerUrl').value = item.banner_url || '';
    document.getElementById('sponsorWebsiteUrl').value = item.website_url || '';
    document.getElementById('sponsorOrder').value = item.order ?? 0;
    document.getElementById('sponsorStartDate').value = toDateTimeLocal(item.start_date);
    document.getElementById('sponsorEndDate').value = toDateTimeLocal(item.end_date);
    document.getElementById('sponsorDescription').value = item.description || '';
    document.getElementById('sponsorIsActive').checked = !!item.is_active;
}

async function deleteAnnotator(id) {
    if (!confirm('Deseja desativar esta empresa?')) return;
    await fetchJson(`${API_BASE}/annotators/${id}`, { method: 'DELETE', headers: authHeaders(false) });
    await loadAdminData();
}

async function deleteJob(id) {
    if (!confirm('Deseja desativar esta vaga?')) return;
    await fetchJson(`${API_BASE}/jobs/${id}`, { method: 'DELETE', headers: authHeaders(false) });
    await loadAdminData();
}

async function deleteCarousel(id) {
    if (!confirm('Deseja desativar este item do carousel?')) return;
    await fetchJson(`${API_BASE}/carousel/${id}`, { method: 'DELETE', headers: authHeaders(false) });
    await loadAdminData();
}

async function deleteSponsor(id) {
    if (!confirm('Deseja desativar este patrocinio?')) return;
    await fetchJson(`${API_BASE}/sponsorships/${id}`, { method: 'DELETE', headers: authHeaders(false) });
    await loadAdminData();
}

async function saveAnnotator(event) {
    event.preventDefault();
    const id = state.editing.annotatorId;
    const companyName = document.getElementById('annotatorCompanyName').value;
    const slugInput = document.getElementById('annotatorSlug');
    const generatedSlug = slugify(slugInput.value || companyName);

    if (!generatedSlug) {
        setMessage('annotatorMessage', 'Informe um nome de empresa valido para gerar o slug.', true);
        return;
    }

    slugInput.value = generatedSlug;

    const payload = {
        company_name: companyName,
        slug: generatedSlug,
        description: document.getElementById('annotatorDescription').value,
        email: document.getElementById('annotatorEmail').value,
        phone: document.getElementById('annotatorPhone').value,
        website: document.getElementById('annotatorWebsite').value || null,
        logo_url: normalizeAssetInput(document.getElementById('annotatorLogoUrl').value),
        banner_url: normalizeAssetInput(document.getElementById('annotatorBannerUrl').value),
        photo_1_url: normalizeAssetInput(document.getElementById('annotatorPhoto1Url').value),
        photo_2_url: normalizeAssetInput(document.getElementById('annotatorPhoto2Url').value),
        photo_3_url: normalizeAssetInput(document.getElementById('annotatorPhoto3Url').value),
        photo_4_url: normalizeAssetInput(document.getElementById('annotatorPhoto4Url').value),
        city: document.getElementById('annotatorCity').value,
        state: document.getElementById('annotatorState').value,
        address: document.getElementById('annotatorAddress').value || null,
        facebook_url: document.getElementById('annotatorFacebookUrl').value || null,
        instagram_url: document.getElementById('annotatorInstagramUrl').value || null,
        whatsapp_number: document.getElementById('annotatorWhatsapp').value || null,
        twitter_url: document.getElementById('annotatorTwitterUrl').value || null,
        linkedin_url: document.getElementById('annotatorLinkedinUrl').value || null,
        is_active: document.getElementById('annotatorIsActive').checked,
        is_verified: document.getElementById('annotatorIsVerified').checked
    };

    const url = id ? `${API_BASE}/annotators/${id}` : `${API_BASE}/annotators/`;
    const method = id ? 'PUT' : 'POST';
    const body = payload;

    try {
        await fetchJson(url, { method, headers: authHeaders(), body: JSON.stringify(body) });
        resetAnnotatorForm();
        setMessage('annotatorMessage', 'Empresa salva com sucesso.');
        await loadAdminData();
    } catch (error) {
        setMessage('annotatorMessage', error.message, true);
    }
}

async function saveJob(event) {
    event.preventDefault();
    const id = state.editing.jobId;
    const payload = {
        title: document.getElementById('jobTitle').value,
        description: document.getElementById('jobDescription').value,
        category: document.getElementById('jobCategory').value,
        employment_type: document.getElementById('jobEmploymentType').value,
        salary_min: document.getElementById('jobSalaryMin').value ? Number(document.getElementById('jobSalaryMin').value) : null,
        salary_max: document.getElementById('jobSalaryMax').value ? Number(document.getElementById('jobSalaryMax').value) : null,
        city: document.getElementById('jobCity').value,
        state: document.getElementById('jobState').value,
        company_id: document.getElementById('jobCompanyId').value ? Number(document.getElementById('jobCompanyId').value) : null,
        company_name: document.getElementById('jobCompanyName').value,
        company_email: document.getElementById('jobCompanyEmail').value,
        company_phone: document.getElementById('jobCompanyPhone').value,
        requirements: document.getElementById('jobRequirements').value,
        contact_email: document.getElementById('jobContactEmail').value,
        contact_phone: document.getElementById('jobContactPhone').value || null,
        is_active: document.getElementById('jobIsActive').checked,
        is_featured: document.getElementById('jobIsFeatured').checked
    };

    const url = id ? `${API_BASE}/jobs/${id}` : `${API_BASE}/jobs/`;
    const method = id ? 'PUT' : 'POST';
    const body = payload;

    try {
        await fetchJson(url, { method, headers: authHeaders(), body: JSON.stringify(body) });
        resetJobForm();
        setMessage('jobMessage', 'Vaga salva com sucesso.');
        await loadAdminData();
    } catch (error) {
        setMessage('jobMessage', error.message, true);
    }
}

async function saveCarousel(event) {
    event.preventDefault();
    const id = state.editing.carouselId;
    const payload = {
        title: document.getElementById('carouselTitle').value,
        description: document.getElementById('carouselDescription').value || null,
        image_url: normalizeAssetInput(document.getElementById('carouselImageUrl').value),
        link_url: document.getElementById('carouselLinkUrl').value || null,
        annotator_id: document.getElementById('carouselAnnotatorId').value ? Number(document.getElementById('carouselAnnotatorId').value) : null,
        order: Number(document.getElementById('carouselOrder').value || 0),
        rotation_speed: Number(document.getElementById('carouselRotationSpeed').value || 5000),
        is_active: document.getElementById('carouselIsActive').checked
    };

    const url = id ? `${API_BASE}/carousel/${id}` : `${API_BASE}/carousel/`;
    const method = id ? 'PUT' : 'POST';
    const body = payload;

    try {
        await fetchJson(url, { method, headers: authHeaders(), body: JSON.stringify(body) });
        resetCarouselForm();
        setMessage('carouselMessage', 'Item salvo com sucesso.');
        await loadAdminData();
    } catch (error) {
        setMessage('carouselMessage', error.message, true);
    }
}

async function saveSponsor(event) {
    event.preventDefault();
    const id = state.editing.sponsorId;
    const payload = {
        company_name: document.getElementById('sponsorCompanyName').value,
        logo_url: normalizeAssetInput(document.getElementById('sponsorLogoUrl').value),
        banner_url: normalizeAssetInput(document.getElementById('sponsorBannerUrl').value),
        description: document.getElementById('sponsorDescription').value || null,
        website_url: document.getElementById('sponsorWebsiteUrl').value || null,
        position: document.getElementById('sponsorPosition').value,
        order: Number(document.getElementById('sponsorOrder').value || 0),
        start_date: new Date(document.getElementById('sponsorStartDate').value).toISOString(),
        end_date: document.getElementById('sponsorEndDate').value ? new Date(document.getElementById('sponsorEndDate').value).toISOString() : null,
        is_active: document.getElementById('sponsorIsActive').checked
    };

    const url = id ? `${API_BASE}/sponsorships/${id}` : `${API_BASE}/sponsorships/`;
    const method = id ? 'PUT' : 'POST';
    const body = payload;

    try {
        await fetchJson(url, { method, headers: authHeaders(), body: JSON.stringify(body) });
        resetSponsorForm();
        setMessage('sponsorMessage', 'Patrocinio salvo com sucesso.');
        await loadAdminData();
    } catch (error) {
        setMessage('sponsorMessage', error.message, true);
    }
}

async function saveBranding(event) {
    if (event) event.preventDefault();

    const payload = {
        brand_logo_url: normalizeAssetInput(document.getElementById('brandLogoUrl').value),
        admin_brand_logo_url: normalizeAssetInput(document.getElementById('adminBrandLogoUrl').value)
    };

    try {
        state.branding = await fetchJson(`${API_BASE}/admin/branding`, {
            method: 'PUT',
            headers: authHeaders(),
            body: JSON.stringify(payload)
        });
        renderBranding();
        setMessage('brandingMessage', 'Branding salvo com sucesso.');
    } catch (error) {
        setMessage('brandingMessage', error.message, true);
    }
}

function activateTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    document.querySelectorAll('.tab-panel').forEach(panel => {
        panel.classList.toggle('active', panel.id === `tab-${tabName}`);
    });
}

document.getElementById('adminLoginForm').addEventListener('submit', handleAdminLogin);
document.getElementById('bootstrapBtn').addEventListener('click', bootstrapAdmin);
document.getElementById('logoutBtn').addEventListener('click', logout);
document.getElementById('annotatorForm').addEventListener('submit', saveAnnotator);
document.getElementById('jobAdminForm').addEventListener('submit', saveJob);
document.getElementById('carouselForm').addEventListener('submit', saveCarousel);
document.getElementById('sponsorForm').addEventListener('submit', saveSponsor);
document.getElementById('brandingForm').addEventListener('submit', saveBranding);
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => activateTab(btn.dataset.tab));
});

window.editAnnotator = editAnnotator;
window.deleteAnnotator = deleteAnnotator;
window.resetAnnotatorForm = resetAnnotatorForm;
window.editJob = editJob;
window.deleteJob = deleteJob;
window.resetJobForm = resetJobForm;
window.editCarousel = editCarousel;
window.deleteCarousel = deleteCarousel;
window.resetCarouselForm = resetCarouselForm;
window.editSponsor = editSponsor;
window.deleteSponsor = deleteSponsor;
window.resetSponsorForm = resetSponsorForm;

document.addEventListener('DOMContentLoaded', async () => {
    resetAnnotatorForm();
    resetJobForm();
    resetCarouselForm();
    resetSponsorForm();
    wireImageUpload('annotatorLogoFile', 'annotators', 'annotatorLogoUrl', 'annotatorMessage');
    wireImageUpload('annotatorBannerFile', 'annotators', 'annotatorBannerUrl', 'annotatorMessage');
    wireImageUpload('annotatorPhoto1File', 'annotators', 'annotatorPhoto1Url', 'annotatorMessage');
    wireImageUpload('annotatorPhoto2File', 'annotators', 'annotatorPhoto2Url', 'annotatorMessage');
    wireImageUpload('annotatorPhoto3File', 'annotators', 'annotatorPhoto3Url', 'annotatorMessage');
    wireImageUpload('annotatorPhoto4File', 'annotators', 'annotatorPhoto4Url', 'annotatorMessage');
    wireImageUpload('carouselImageFile', 'carousel', 'carouselImageUrl', 'carouselMessage');
    wireImageUpload('sponsorLogoFile', 'sponsors', 'sponsorLogoUrl', 'sponsorMessage');
    wireImageUpload('sponsorBannerFile', 'sponsors', 'sponsorBannerUrl', 'sponsorMessage');
    wireImageUpload('brandLogoFile', 'branding', 'brandLogoUrl', 'brandingMessage', async () => saveBranding());
    wireImageUpload('adminBrandLogoFile', 'branding', 'adminBrandLogoUrl', 'brandingMessage', async () => saveBranding());
    await loadAdminStatus();
    await tryRestoreSession();
});
