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

window.SHOPPINGHUB_CONFIG = {
    API_BASE: resolveShoppingHubApiBase()
};
