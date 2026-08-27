/**
 * SCROLL.JS — Navegación suave por anclas
 *
 * Cuando haces clic en un link como href="#proyectos",
 * hace scroll animado en lugar de salto brusco.
 * Compensa la altura del navbar fijo (96px).
 */
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', (e) => {
            const targetId = anchor.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (!target) return;

            e.preventDefault();
            const headerOffset = 96; // Altura del navbar sticky
            const top = target.getBoundingClientRect().top + window.scrollY - headerOffset;
            window.scrollTo({ top, behavior: 'smooth' });
        });
    });
});
