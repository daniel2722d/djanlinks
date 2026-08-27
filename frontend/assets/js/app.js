/**
 * =============================================================================
 * APP.JS — Cerebro del frontend
 * =============================================================================
 *
 * Este archivo se ejecuta en TODAS las páginas HTML.
 * Su trabajo principal: cargar los componentes reutilizables (navbar, footer, etc.)
 *
 * ¿Cómo funciona?
 * 1. Cada página HTML tiene divs vacíos como: <div id="navbar-component"></div>
 * 2. app.js hace fetch() al archivo .html del componente
 * 3. Inserta el HTML dentro del div
 *
 * REQUIERE servidor local (`python manage.py runserver`) - no funciona con file://
 *
 * Archivos relacionados:
 * - components/*.html  → piezas de UI
 * - navbar.js          → menú móvil
 * - animations.js      → efectos visuales
 * - scroll.js          → scroll suave a anclas (#proyectos)
 * =============================================================================
 */
const DJANLINKS = {
    basePath: '',
    assetVersion: '20260619-portafolio-menu-fix',

    /** Punto de entrada — se llama al cargar cada página */
    async init() {
        this.basePath = this.resolveBasePath();
        await this.loadComponents();  // 1º: navbar, footer, loader, hero
        this.normalizePortfolioLinks();
        this.hideLoader();              // 2º: quita pantalla de carga
        this.initAOS();                 // 3º: activa animaciones al scroll
        this.markActiveNav();           // 4º: resalta link activo en menú
        this.guardPortfolioNavigation();
    },

    resolveBasePath() {
        const path = window.location.pathname;
        if (path.includes('/frontend/')) return '';
        return '';
    },

    /**
     * Lista de componentes a inyectar en cada página.
     * Para agregar uno nuevo: crea el .html en components/ y añádelo aquí.
     */
    async loadComponents() {
        const components = [
            { id: 'loader-component', file: 'components/loader.html' },   // Pantalla de carga
            { id: 'navbar-component', file: 'components/navbar.html' },   // Menú superior
            { id: 'footer-component', file: 'components/footer.html' }    // Pie de página
        ];

        // Hero solo existe en index.html (tiene div#hero-component)
        const heroEl = document.getElementById('hero-component');
        if (heroEl) {
            components.push({ id: 'hero-component', file: 'components/hero.html' });
        }

        await Promise.all(
            components.map(({ id, file }) => this.injectComponent(id, file))
        );
    },

    /** Descarga un componente HTML y lo inserta en el div correspondiente */
    async injectComponent(elementId, filePath) {
        const target = document.getElementById(elementId);
        if (!target) return;

        try {
            const separator = filePath.includes('?') ? '&' : '?';
            const response = await fetch(
                `${filePath}${separator}v=${this.assetVersion}`,
                { cache: 'no-store' }
            );
            if (!response.ok) throw new Error(`No se pudo cargar ${filePath}`);
            target.innerHTML = await response.text();
        } catch (error) {
            console.warn(`Componente ${filePath}:`, error.message);
        }
    },

    /** Oculta el loader cuando la página terminó de cargar */
    hideLoader() {
        const loader = document.querySelector('.page-loader');
        if (!loader) return;

        window.addEventListener('load', () => {
            setTimeout(() => loader.classList.add('is-hidden'), 400);
        });

        // Fallback: ocultar después de 2s aunque algo falle
        setTimeout(() => loader.classList.add('is-hidden'), 2000);
    },

    /** Inicializa AOS (Animate On Scroll) — librería externa en el <head> */
    initAOS() {
        if (typeof AOS !== 'undefined') {
            AOS.init({ duration: 1000, once: true });
        }
    },

    /**
     * Marca el enlace del menú que coincide con la página actual.
     * data-nav solo está en links principales (proyectos, planes, about, contact).
     */
    markActiveNav() {
        const current = window.location.pathname.split('/').pop() || 'index.html';
        document.querySelectorAll('[data-nav]').forEach((link) => {
            const href = link.getAttribute('href');
            if (href === current || (current === '' && href === 'index.html')) {
                link.classList.add('is-active');
            }
        });
    },

    normalizePortfolioLinks() {
        document.querySelectorAll('a[href*="portfolio.html"]').forEach((link) => {
            link.setAttribute('href', link.getAttribute('href').replaceAll('portfolio.html', 'portafolio.html'));
        });
    },

    guardPortfolioNavigation() {
        document.body.addEventListener('click', (event) => {
            const link = event.target.closest('a[href*="portfolio.html"]');
            if (!link) return;

            event.preventDefault();
            window.location.href = link.href.replaceAll('portfolio.html', 'portafolio.html');
        });
    }
};

document.addEventListener('DOMContentLoaded', () => DJANLINKS.init());
