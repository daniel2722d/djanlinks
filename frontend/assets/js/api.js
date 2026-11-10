/**
 * API.JS — Cliente para conectar frontend con backend Django
 *
 * Cuando el backend esté corriendo (python manage.py runserver),
 * el frontend puede enviar/recibir datos por HTTP.
 *
 * URL base configurada en .env → DJANLINKS_API_URL
 * Por defecto: /api, usando el mismo servidor de Django
 *
 * Endpoints disponibles:
 * - POST /api/leads/        → enviar formulario de contacto
 * - GET  /api/services/     → listar servicios
 * - GET  /api/portfolio/    → listar proyectos
 * - POST /api/ai/chat/      → hablar con Links AI
 *
 * Uso: window.DJANLINKS_API.submitLead({ nombre: '...', mensaje: '...' })
 */
const API_BASE = window.DJANLINKS_API_URL || 'https://api.djanlinks.com/api';
const api = {
    async request(endpoint, options = {}) {
        const url = `${API_BASE}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        const response = await fetch(url, config);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return response.json();
    },

    /** Enviar lead desde formulario → backend/apps/leads/ */
    async submitLead(data) {
        return this.request('/leads/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    /** Obtener servicios → backend/apps/services/ */
    async getServices() {
        return this.request('/services/');
    },

    /** Obtener proyectos → backend/apps/portfolio/ */
    async getPortfolio() {
        return this.request('/portfolio/');
    },

    /** Chat con Links AI → backend/apps/ai/ */
    async chatWithLinks(message, history = [], meta = {}) {
        return this.request('/ai/chat/', {
            method: 'POST',
            body: JSON.stringify({ message, history, meta })
        });
    }
};

window.DJANLINKS_API = api;
