# DJANLINKS creative tech studio

Estudio creativo especializado en experiencias digitales futuristas — diseño, desarrollo web, software, IA y contenido audiovisual cinematográfico.

> **¿Perdido?** Lee primero **[docs/GUIA.md](docs/GUIA.md)** — mapa del proyecto, qué hace cada carpeta y por dónde empezar.

## Estructura

```
djanlinks-creative-tech/
├── frontend/          # Sitio web estático modular
├── backend/           # API Django REST
├── database/          # Scripts y volúmenes PostgreSQL
├── docs/              # Documentación y Docker
├── .env
├── requirements.txt
└── docker-compose.yml
```

## Inicio rápido

### Desarrollo local

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abre [http://localhost:8000](http://localhost:8000). El mismo comando sirve el frontend y la API:

- Sitio web: [http://localhost:8000](http://localhost:8000)
- API: [http://localhost:8000/api/](http://localhost:8000/api/)

### Links AI

Links funciona como asistente flotante del sitio. Para conectarlo con Gemini,
configura estas variables en `.env`:

```env
GEMINI_API_KEY=tu_api_key
GEMINI_MODEL=gemini-2.5-flash
LINKS_WHATSAPP_NUMBER=573052707206
```

Si `GEMINI_API_KEY` no existe, Links usa respuestas locales de respaldo y
mantiene activo el acceso a WhatsApp.

### Docker (todo el stack)

```bash
docker compose up --build
```

- Frontend: [http://localhost:8080](http://localhost:8080)
- Backend: [http://localhost:8000](http://localhost:8000)
- PostgreSQL: `localhost:5432`

## Assets

Copia tus imágenes y videos a `frontend/assets/images/` y `frontend/assets/videos/`. Ver lista completa en [docs/ESTRUCTURA.md](docs/ESTRUCTURA.md).

## Tipografía y diseño

- **Inter** — texto general
- **Space Grotesk** — títulos
- Paleta oscura con acentos azul `#3b82f6`, glassmorphism y animaciones AOS

## Contacto

- WhatsApp: [+57 305 270 7206](https://wa.me/573052707206)
- Email: contacto@djlnxstudio.com
