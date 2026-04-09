function resolveShoppingHubApiBase() {
    const explicitBase = window.SHOPPINGHUB_API_BASE || '';
    if (explicitBase) {
        return explicitBase.replace(/\/$/, '');
    }

    const { origin, hostname, port } = window.location;
    const isLocalhost = hostname === 'localhost' || hostname === '127.0.0.1';

    if (isLocalhost && port && port !== '8000') {
        return 'http://127.0.0.1:8000/api';
    }

    return `${origin}/api`;
}

function resolveAssetUrl(explicitValue, fallbackValue) {
    if (!explicitValue) return fallbackValue;
    return String(explicitValue).trim() || fallbackValue;
}

window.SHOPPINGHUB_CONFIG = {
    API_BASE: resolveShoppingHubApiBase(),
    ASSETS: {
        BRAND_LOGO_URL: resolveAssetUrl(window.BOMCONTATO_BRAND_LOGO_URL, 'img/bomcontato-logo.png'),
        BRAND_LOGO_URL_ADMIN: resolveAssetUrl(window.BOMCONTATO_BRAND_LOGO_URL_ADMIN, '../img/bomcontato-logo.png'),
        PLACEHOLDER_IMAGE_URL: resolveAssetUrl(window.BOMCONTATO_PLACEHOLDER_IMAGE_URL, '/img/placeholder.jpg'),
        PLACEHOLDER_LOGO_URL: resolveAssetUrl(window.BOMCONTATO_PLACEHOLDER_LOGO_URL, '/img/logo-placeholder.jpg'),
        PLACEHOLDER_IMAGE_URL_MICROSITE: resolveAssetUrl(window.BOMCONTATO_PLACEHOLDER_IMAGE_URL_MICROSITE, '../img/placeholder.jpg'),
        PLACEHOLDER_LOGO_URL_MICROSITE: resolveAssetUrl(window.BOMCONTATO_PLACEHOLDER_LOGO_URL_MICROSITE, '../img/logo-placeholder.jpg')
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const brandLogo = document.getElementById('brandLogo');
    if (brandLogo) {
        brandLogo.src = window.SHOPPINGHUB_CONFIG.ASSETS.BRAND_LOGO_URL;
    }

    const adminBrandLogo = document.getElementById('adminBrandLogo');
    if (adminBrandLogo) {
        adminBrandLogo.src = window.SHOPPINGHUB_CONFIG.ASSETS.BRAND_LOGO_URL_ADMIN;
    }
});

window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch(`${window.SHOPPINGHUB_CONFIG.API_BASE}/site-config/branding`);
        if (!response.ok) return;

        const branding = await response.json();
        if (branding.brand_logo_url) {
            const brandLogo = document.getElementById('brandLogo');
            if (brandLogo) brandLogo.src = branding.brand_logo_url;
        }

        if (branding.admin_brand_logo_url) {
            const adminBrandLogo = document.getElementById('adminBrandLogo');
            if (adminBrandLogo) {
                adminBrandLogo.src = branding.admin_brand_logo_url;
            }
        } else if (branding.brand_logo_url) {
            const adminBrandLogo = document.getElementById('adminBrandLogo');
            if (adminBrandLogo) {
                adminBrandLogo.src = branding.brand_logo_url;
            }
        }
    } catch {
        // Keep static fallbacks when the site-config endpoint is unavailable.
    }
});
