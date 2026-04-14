// Generate placeholder SVG images for missing assets

const PLACEHOLDER_SVG_CAROUSEL = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100%" height="400"%3E%3Crect fill="%23e0e0e0" width="100%" height="100%"/%3E%3Ctext x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial" font-size="32" fill="%23999"%3ECarousel Placeholder%3C/text%3E%3C/svg%3E';

const PLACEHOLDER_SVG_LOGO = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="60"%3E%3Crect fill="%23f5f5f5" width="100%" height="100%"/%3E%3Ctext x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial" font-size="14" fill="%23666"%3EBom Contato%3C/text%3E%3C/svg%3E';

const PLACEHOLDER_SVG_GENERIC = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="200"%3E%3Crect fill="%23f0f0f0" width="100%" height="100%"/%3E%3Ctext x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial" font-size="16" fill="%23aaa"%3EImagem não disponível%3C/text%3E%3C/svg%3E';

// Fix missing carousel images
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('img[src*="placeholder"]').forEach(img => {
        img.onerror = function() {
            this.src = PLACEHOLDER_SVG_CAROUSEL;
            this.onerror = null;
        };
    });

    // Fix missing logos
    const brandLogo = document.getElementById('brandLogo');
    if (brandLogo) {
        brandLogo.onerror = function() {
            this.src = PLACEHOLDER_SVG_LOGO;
            this.onerror = null;
        };
    }
});
