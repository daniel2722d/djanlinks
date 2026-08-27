# Estructura del proyecto DJANLINKS creative tech

## Frontend (`frontend/`)

Sitio estático modular con componentes reutilizables.

| Página | Descripción |
|--------|-------------|
| `index.html` | Inicio con hero, preview de portafolio, servicios y planes |
| `about.html` | Conócenos — filosofía, Links AI, tecnologías |
| `desarrollo.html`, `diseno.html`, `marketing.html`, `contenido.html`, `software.html`, `ia.html` | Servicios individuales |
| `nuestros_planes.html` | Planes premium |
| `portafolio.html` | Proyectos destacados (ARQ722, Azul Celeste, Ruta Verde) |
| `contact.html` | Formulario y canales de contacto |

### Componentes (`components/`)

Cargados dinámicamente vía `app.js` (requiere servidor local):

- `navbar.html` — Navegación y WhatsApp flotante
- `footer.html` — Pie de página
- `hero.html` — Video hero + presentación (solo index)
- `loader.html` — Pantalla de carga

### Tipografía

- **Cuerpo:** Inter (300–800)
- **Títulos:** Space Grotesk (400–700)
- **Acento:** Azul `#3b82f6`

## Backend (`backend/`)

API REST Django con apps:

- `users` — Autenticación (pendiente)
- `services` — Catálogo de servicios
- `portfolio` — Proyectos
- `leads` — Formularios de contacto
- `ai` — Links AI chat
- `dashboard` — Estadísticas admin

## Assets

Copiar imágenes y videos del sitio anterior a:

```
frontend/assets/images/
frontend/assets/videos/
```

Archivos requeridos: `logo.png`, `hero.png`, `hero.mp4`, `arq722.png`, `azul celeste.png`, `ruta_verde.png`, `links.png`, `links_conocenos.png`, `links_contacto.png`, `sobre_nosotros.png`, `fondo_*.png`, `ia.png`, `software.png`, `contacto.png`.
