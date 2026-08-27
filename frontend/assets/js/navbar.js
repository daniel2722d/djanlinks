/**
 * NAVBAR.JS — Comportamiento del menú de navegación
 *
 * - Botón hamburguesa en móvil (data-nav-toggle)
 * - Dropdown de servicios en móvil
 * - Efecto visual al hacer scroll
 *
 * El HTML del navbar está en: components/navbar.html
 * Los estilos están en: assets/css/navbar.css
 */
document.addEventListener('DOMContentLoaded', () => {
    // Delegación de eventos: funciona aunque el navbar se cargue después vía fetch
    document.body.addEventListener('click', (e) => {
        const toggle = e.target.closest('[data-nav-toggle]');
        if (toggle) {
            const menu = document.querySelector('[data-nav-mobile]');
            toggle.classList.toggle('is-active');
            menu?.classList.toggle('is-open');
            return;
        }

        const dropdownBtn = e.target.closest('[data-nav-dropdown]');
        if (dropdownBtn && window.innerWidth < 768) {
            dropdownBtn.closest('.nav-dropdown')?.classList.toggle('is-open');
        }
    });

    // Añade clase al header cuando el usuario hace scroll
    window.addEventListener('scroll', () => {
        const header = document.querySelector('.site-header');
        if (!header) return;

        if (window.scrollY > 80) {
            header.classList.add('is-scrolled');
        } else {
            header.classList.remove('is-scrolled');
        }
    });
});
