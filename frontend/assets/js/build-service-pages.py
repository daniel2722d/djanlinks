# Script auxiliar — genera páginas de servicio (ejecutar una vez si necesitas regenerar)
# python frontend/assets/js/build-service-pages.py

SERVICES = [
    {
        "file": "desarrollo.html",
        "title": "Desarrollo Web",
        "breadcrumb": "Desarrollo Web",
        "image": "fondo_desarrollo.png",
        "hero": "Sitios web modernos, rápidos y optimizados para marcas que buscan presencia digital premium.",
        "desc": "Desarrollamos sitios web con enfoque en rendimiento, experiencia de usuario y conversión. Cada proyecto combina código limpio, diseño cinematográfico y optimización SEO.",
        "features": [
            ("Landing pages premium", "Páginas de alto impacto visual diseñadas para convertir visitantes en clientes."),
            ("Sitios multipágina", "Estructuras escalables con navegación intuitiva y contenido organizado."),
            ("Optimización SEO", "Configuración técnica y de contenido para posicionamiento en buscadores."),
        ],
        "items": ["Diseño responsive", "Integración WhatsApp", "Animaciones AOS", "Hosting y dominio", "Velocidad optimizada", "Formularios de contacto"],
        "wa": "Desarrollo%20Web",
    },
    {
        "file": "diseno.html",
        "title": "Diseño UI/UX",
        "breadcrumb": "Diseño UI/UX",
        "image": "fondo_diseno.png",
        "hero": "Interfaces cinematográficas, elegantes y memorables que conectan con tu audiencia.",
        "desc": "Diseñamos experiencias visuales premium enfocadas en elegancia, interacción y conexión emocional con el usuario. Cada interfaz refleja la identidad única de tu marca.",
        "features": [
            ("UI cinematográfica", "Interfaces con glassmorphism, glow effects y tipografía premium."),
            ("Experiencia de usuario", "Flujos intuitivos que guían al usuario hacia la conversión."),
            ("Design systems", "Sistemas de diseño coherentes para marcas escalables."),
        ],
        "items": ["Wireframes y prototipos", "Figma premium", "Paleta de marca", "Componentes reutilizables", "Mobile first", "Microinteracciones"],
        "wa": "Dise%C3%B1o%20UI%2FUX",
    },
    {
        "file": "marketing.html",
        "title": "Marketing Digital",
        "breadcrumb": "Marketing Digital",
        "image": "fondo_marketing.png",
        "hero": "Estrategias digitales para aumentar visibilidad, posicionamiento y conversiones.",
        "desc": "Combinamos creatividad y datos para construir estrategias de marketing que potencian el crecimiento de marcas modernas en el entorno digital.",
        "features": [
            ("Redes sociales", "Contenido estratégico para Instagram, TikTok y más."),
            ("SEO y posicionamiento", "Visibilidad orgánica sostenible en buscadores."),
            ("Campañas digitales", "Publicidad orientada a resultados y conversiones."),
        ],
        "items": ["Estrategia de contenido", "Branding digital", "Analytics", "Email marketing", "Meta Ads", "Google Ads"],
        "wa": "Marketing%20Digital",
    },
    {
        "file": "contenido.html",
        "title": "Contenido Audiovisual",
        "breadcrumb": "Contenido Audiovisual",
        "image": "fondo_contenido.png",
        "hero": "Producción audiovisual cinematográfica para marcas con identidad visual fuerte.",
        "desc": "Creamos contenido audiovisual de alto impacto: videos promocionales, reels, motion graphics y piezas visuales que elevan la percepción de tu marca.",
        "features": [
            ("Video corporativo", "Producciones profesionales que transmiten confianza y valor."),
            ("Reels y short-form", "Contenido optimizado para redes sociales y engagement."),
            ("Motion graphics", "Animaciones y efectos visuales que capturan la atención."),
        ],
        "items": ["Guión y storyboard", "Edición premium", "Color grading", "Motion design", "Fotografía", "Branding visual"],
        "wa": "Contenido%20Audiovisual",
    },
    {
        "file": "software.html",
        "title": "Software & Apps",
        "breadcrumb": "Software & Apps",
        "image": "software.png",
        "hero": "Plataformas, sistemas y aplicaciones modernas enfocadas en automatización y escalabilidad.",
        "desc": "Desarrollamos software empresarial, paneles administrativos y aplicaciones móviles con arquitectura moderna, bases de datos seguras y experiencias premium.",
        "features": [
            ("Software empresarial", "Sistemas internos para gestión, inventarios y reportes."),
            ("Apps móviles", "Android e iOS con UI/UX premium y notificaciones push."),
            ("APIs e integraciones", "Conexión con servicios externos y automatización."),
        ],
        "items": ["Panel administrativo", "Base de datos segura", "Gestión de usuarios", "Reportes en tiempo real", "API REST", "Escalabilidad"],
        "wa": "Software%20%26%20Apps",
    },
    {
        "file": "ia.html",
        "title": "Inteligencia Artificial",
        "breadcrumb": "Inteligencia Artificial",
        "image": "ia.png",
        "hero": "Asistentes inteligentes, automatización y soluciones IA para optimizar tu negocio.",
        "desc": "Integramos inteligencia artificial en experiencias digitales: chatbots, automatización de WhatsApp, atención al cliente y procesos empresariales inteligentes con Links AI.",
        "features": [
            ("Chatbots inteligentes", "Asistentes virtuales que atienden y califican leads 24/7."),
            ("Automatización", "Flujos automáticos para ventas, soporte y tareas repetitivas."),
            ("Links AI", "Nuestra mascota IA que representa la esencia futurista del estudio."),
        ],
        "items": ["Chatbots WhatsApp", "IA conversacional", "Automatización de tareas", "Integraciones CRM", "Análisis de datos", "Soluciones a medida"],
        "wa": "Inteligencia%20Artificial",
    },
]

TEMPLATE = '''<!DOCTYPE html>
<!--
  {title_upper} — Página de servicio individual
  Enlazada desde el menú Servicios → {breadcrumb}
-->
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | DJANLINKS creative tech studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://unpkg.com/aos@2.3.4/dist/aos.css" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/variables.css">
    <link rel="stylesheet" href="assets/css/global.css">
    <link rel="stylesheet" href="assets/css/animations.css">
    <link rel="stylesheet" href="assets/css/navbar.css">
    <link rel="stylesheet" href="assets/css/hero.css">
    <link rel="stylesheet" href="assets/css/footer.css">
    <link rel="stylesheet" href="assets/css/responsive.css">
</head>
<body class="bg-black text-white">

    <div id="loader-component"></div>
    <div id="navbar-component"></div>

    <section class="hero-page overflow-hidden">
        <div class="absolute top-1/3 left-1/2 -translate-x-1/2 w-[700px] h-[700px] bg-blue-500/10 blur-[160px] rounded-full"></div>
        <div class="relative z-10 max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center">
            <div>
                <div class="hero-breadcrumb">
                    <a href="index.html" class="hover:text-blue-400 transition">Inicio</a>
                    <span>/</span>
                    <span class="is-current">{breadcrumb}</span>
                </div>
                <p data-aos="fade-up" class="hero-eyebrow">DJANLINKS creative tech studio</p>
                <h1 data-aos="fade-up" class="text-5xl lg:text-7xl font-black leading-tight mb-8">{title}</h1>
                <p data-aos="fade-up" data-aos-delay="150" class="text-gray-400 text-xl leading-relaxed mb-10">{hero}</p>
                <a href="https://wa.me/573052707206?text=Hola%2C%20me%20interesa%20{wa}"
                   class="inline-flex bg-blue-500 hover:bg-blue-600 px-8 py-4 rounded-full text-white font-medium transition duration-300 hover:scale-105">
                    Cotizar proyecto
                </a>
            </div>
            <div data-aos="fade-left" class="relative group">
                <div class="absolute -inset-2 bg-blue-500/20 blur-3xl rounded-3xl opacity-40 group-hover:opacity-70 transition duration-700"></div>
                <img src="assets/images/{image}" alt="{title}" class="relative rounded-3xl border border-white/10 shadow-2xl w-full object-cover max-h-[480px]">
            </div>
        </div>
    </section>

    <section class="py-24 px-6">
        <div class="max-w-4xl mx-auto text-center mb-20">
            <p data-aos="fade-up" class="text-gray-400 text-xl leading-relaxed">{desc}</p>
        </div>
        <div class="max-w-7xl mx-auto grid md:grid-cols-3 gap-8">
{features_html}
        </div>
    </section>

    <section class="py-20 px-6">
        <div class="max-w-5xl mx-auto glass-card rounded-3xl p-10 lg:p-16">
            <h2 data-aos="fade-up" class="text-4xl font-bold mb-10 text-center">¿Qué incluye?</h2>
            <ul class="grid md:grid-cols-2 gap-6 text-gray-300 text-lg">
{items_html}
            </ul>
        </div>
    </section>

    <section class="py-24 px-6 pb-32">
        <div class="max-w-5xl mx-auto glass-card rounded-[40px] p-16 text-center relative overflow-hidden">
            <div class="absolute inset-0 bg-blue-500/10 blur-[120px]"></div>
            <div class="relative z-10">
                <h2 class="text-5xl font-black mb-8">¿Listo para empezar?</h2>
                <p class="text-gray-400 text-xl mb-10 max-w-2xl mx-auto">Llevemos tu proyecto de {title_lower} al siguiente nivel con diseño premium y tecnología moderna.</p>
                <a href="https://wa.me/573052707206?text=Hola%2C%20me%20interesa%20{wa}"
                   class="inline-flex px-10 py-5 rounded-full bg-blue-500 text-white font-semibold text-lg hover:scale-105 transition duration-300">
                    Hablemos por WhatsApp
                </a>
            </div>
        </div>
    </section>

    <div id="footer-component"></div>

    <script src="https://unpkg.com/aos@2.3.4/dist/aos.js"></script>
    <script src="assets/js/app.js"></script>
    <script src="assets/js/navbar.js"></script>
    <script src="assets/js/animations.js"></script>
    <script src="assets/js/scroll.js"></script>
    <script src="assets/js/api.js"></script>
    <script src="assets/js/links-ai.js"></script>
</body>
</html>
'''

import pathlib

root = pathlib.Path(__file__).resolve().parents[2]

for s in SERVICES:
    features_html = ""
    for i, (ft, fd) in enumerate(s["features"]):
        delay = f' data-aos-delay="{i * 100}"' if i else ""
        features_html += f'''
            <div data-aos="fade-up"{delay} class="glass-card rounded-3xl p-10">
                <h3 class="text-2xl font-bold mb-4">{ft}</h3>
                <p class="text-gray-400 leading-relaxed">{fd}</p>
            </div>'''
    items_html = "\n".join(f'                <li class="flex items-center gap-3"><span class="text-blue-400">✓</span> {item}</li>' for item in s["items"])
    html = TEMPLATE.format(
        title=s["title"],
        title_upper=s["title"].upper(),
        title_lower=s["title"].lower(),
        breadcrumb=s["breadcrumb"],
        image=s["image"],
        hero=s["hero"],
        desc=s["desc"],
        features_html=features_html,
        items_html=items_html,
        wa=s["wa"],
    )
    (root / s["file"]).write_text(html, encoding="utf-8")
    print("OK", s["file"])
