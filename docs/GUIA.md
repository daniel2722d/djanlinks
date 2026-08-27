# Guia rapida - DJANLINKS creative tech studio

Si te sientes perdido, empieza por aqui.

## Que es cada carpeta

```
djlnx-studio/
├── frontend/     Sitio web estatico que ve el visitante
├── backend/      API Django, formularios y Links AI
├── assets/       Carpeta antigua; usa frontend/assets si ya migraste
├── database/     Scripts SQL para PostgreSQL
├── docs/         Documentacion y Dockerfile
├── .env          Variables secretas
└── docker-compose.yml
```

## Como levantar todo en tu PC

Ejecuta estos comandos desde la raiz del proyecto:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

- Sitio web: http://localhost:8000
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

No abras los HTML con doble clic: los componentes se cargan con `fetch` y necesitan servidor local.

## Flujo del sitio web

1. El visitante abre `http://localhost:8000`.
2. Django sirve los archivos reales de `frontend/`.
3. `frontend/assets/js/app.js` carga los componentes:
   - `frontend/components/loader.html`
   - `frontend/components/navbar.html`
   - `frontend/components/footer.html`
   - `frontend/components/hero.html` solo en el inicio
4. CSS, JS, imagenes y videos viven en `frontend/assets/`.

## Flujo del backend

1. `manage.py` en la raiz prepara el path hacia `backend/`.
2. `backend/core/settings.py` carga la configuracion.
3. `backend/core/urls.py` separa las rutas:
   - `/api/...` para la API
   - `/admin/` para Django admin
   - `/`, `/*.html`, `/assets/...` y `/components/...` para el frontend

## Apps principales

| App | Que hace |
|-----|----------|
| `leads` | Guarda contactos del formulario |
| `services` | Catalogo de servicios |
| `portfolio` | Proyectos del portafolio |
| `ai` | Chat de Links AI |
| `dashboard` | Estadisticas para admin |
| `users` | Usuarios |

## Orden recomendado para aprender el codigo

1. `frontend/index.html`
2. `frontend/assets/js/app.js`
3. `frontend/components/navbar.html`
4. `frontend/assets/css/variables.css`
5. `backend/core/urls.py`
6. `backend/apps/leads/`

## Donde cambio algo

| Quiero cambiar | Archivo |
|----------------|---------|
| Menu de navegacion | `frontend/components/navbar.html` |
| Pie de pagina | `frontend/components/footer.html` |
| Colores / fuentes | `frontend/assets/css/variables.css` |
| Texto de inicio | `frontend/index.html` |
| Planes y precios | `frontend/nuestros_planes.html` |
| Servicio especifico | `frontend/desarrollo.html`, `frontend/diseno.html`, etc. |
| Proyectos | `frontend/portafolio.html` |
| Formulario contacto | `frontend/contact.html` |
| WhatsApp | Busca `573052707206` en el proyecto |
| Base de datos | `.env` y `backend/core/settings.py` |
