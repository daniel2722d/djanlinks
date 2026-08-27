/**
 * ANIMATIONS.JS — Efectos visuales extra
 *
 * Complementa animations.css aplicando clases dinámicamente.
 * Usado principalmente para Links AI (mascota flotante con glow).
 */
document.addEventListener('DOMContentLoaded', () => {
    // Elementos con data-glow-pulse → pulso de luz azul
    document.querySelectorAll('[data-glow-pulse]').forEach((el) => {
        el.style.animation = 'glowPulse 4s ease-in-out infinite';
    });

    // Elementos con data-links-float → flotación suave
    document.querySelectorAll('[data-links-float]').forEach((el) => {
        el.classList.add('links-float');
    });
});
