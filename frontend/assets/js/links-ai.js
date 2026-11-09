/**
 * LINKS-AI.JS - Asistente IA de DJANLINKS.
 *
 * Crea un widget flotante para conversar con Links, consultar servicios,
 * capturar leads basicos y pasar a WhatsApp cuando el usuario quiera hablar
 * con un asesor.
 */
const LinksAI = {
    storageKey: 'djanlinks.linksAI.v1',
    history: [],
    messagesState: [],
    leadCapture: { active: false, step: null, data: {} },
    isSending: false,
    whatsappUrl: 'https://wa.me/573052707206?text=Hola%2C%20vengo%20desde%20la%20web%20de%20DJANLINKS.%20Quiero%20hablar%20con%20un%20asesor.',

    init() {
        this.loadState();
        this.enhanceVisuals();
        this.ensureWidget();
        this.initChatWidget();
        window.addEventListener('djanlinks:cookie-consent', (event) => {
            if (event.detail?.functional) {
                this.saveState();
                return;
            }

            try {
                window.sessionStorage.removeItem(this.storageKey);
            } catch {
                // The chat remains available in memory when storage is unavailable.
            }
        });
    },

    enhanceVisuals() {
        document.querySelectorAll('.links-wrapper').forEach((wrapper) => {
            if (!wrapper.querySelector('.links-glow')) {
                const glow = document.createElement('div');
                glow.className = 'links-glow';
                glow.setAttribute('data-glow-pulse', '');
                wrapper.prepend(glow);
            }
        });
    },

    ensureWidget() {
        if (document.getElementById('links-ai-widget')) return;

        const widget = document.createElement('aside');
        widget.id = 'links-ai-widget';
        widget.className = 'links-ai-widget';
        widget.innerHTML = `
            <button id="links-ai-toggle" class="links-ai-toggle" type="button" aria-label="Abrir chat con Links">
                <span class="links-ai-toggle__glow"></span>
                <img src="assets/images/links.png" alt="Links" class="links-ai-toggle__avatar">
                <span class="links-ai-toggle__dot"></span>
            </button>

            <section id="links-ai-panel" class="links-ai-panel" aria-label="Chat con Links">
                <header class="links-ai-header">
                    <div class="links-ai-brand">
                        <img src="assets/images/links.png" alt="Links" class="links-ai-avatar">
                        <div>
                            <p class="links-ai-kicker">Links AI</p>
                            <h2>Asistente DJANLINKS</h2>
                        </div>
                    </div>
                    <button class="links-ai-close" type="button" data-links-close aria-label="Cerrar chat">x</button>
                </header>

                <div id="links-ai-messages" class="links-ai-messages"></div>

                <div class="links-ai-quick-actions">
                    <button type="button" data-links-prompt="Quiero cotizar un proyecto web">Cotizar web</button>
                    <button type="button" data-links-prompt="Necesito automatizar un proceso con IA">Automatizar</button>
                    <button type="button" data-links-prompt="Quiero hablar con un asesor">Asesor</button>
                </div>

                <form id="links-ai-form" class="links-ai-form">
                    <input id="links-ai-input" type="text" autocomplete="off" maxlength="500"
                        placeholder="Preguntale a Links..." aria-label="Mensaje para Links">
                    <button type="submit">Enviar</button>
                </form>
            </section>
        `;

        document.body.appendChild(widget);
    },

    initChatWidget() {
        const toggle = document.getElementById('links-ai-toggle');
        const panel = document.getElementById('links-ai-panel');
        const form = document.getElementById('links-ai-form');
        const input = document.getElementById('links-ai-input');
        const messages = document.getElementById('links-ai-messages');

        if (!toggle || !panel || !form || !input || !messages) return;

        this.restoreMessages(messages);

        toggle.addEventListener('click', () => {
            panel.classList.toggle('is-open');
            if (panel.classList.contains('is-open')) input.focus();
        });

        document.querySelector('[data-links-close]')?.addEventListener('click', () => {
            panel.classList.remove('is-open');
        });

        document.querySelectorAll('[data-links-prompt]').forEach((button) => {
            button.addEventListener('click', () => {
                const prompt = button.getAttribute('data-links-prompt');
                this.sendMessage(prompt, { input, messages, panel });
            });
        });

        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            const text = input.value.trim();
            if (!text) return;
            await this.sendMessage(text, { input, messages, panel });
        });
    },

    restoreMessages(messages) {
        messages.innerHTML = '';

        if (this.messagesState.length) {
            this.messagesState.forEach((message) => {
                this.appendMessage(
                    messages,
                    message.text,
                    message.role,
                    message.actions || [],
                    false,
                    false
                );
            });
            return;
        }

        this.appendMessage(
            messages,
            'Hola, soy Links. Puedo ayudarte a elegir servicios, resolver dudas y conectarte con un asesor por WhatsApp.',
            'bot',
            [
                { label: 'Hablar con un asesor', url: this.whatsappUrl },
                { label: 'Ver planes', url: 'nuestros_planes.html' }
            ]
        );
    },

    async sendMessage(text, elements) {
        if (this.isSending) return;

        const { input, messages, panel } = elements;
        panel.classList.add('is-open');

        this.appendMessage(messages, text, 'user');
        input.value = '';

        if (this.leadCapture.active) {
            this.isSending = true;
            this.setInputState(input, true);
            try {
                await this.handleLeadCapture(text, messages);
            } finally {
                this.isSending = false;
                this.setInputState(input, false);
            }
            return;
        }

        this.isSending = true;
        this.setInputState(input, true);

        const requestHistory = this.history.slice(-8);
        this.history.push({ role: 'user', content: text });
        this.history = this.history.slice(-8);
        this.saveState();

        const typing = this.appendMessage(messages, 'Links esta pensando...', 'bot', [], true, false);
        const slowTimer = window.setTimeout(() => {
            const bubble = typing.querySelector('.links-ai-bubble');
            if (bubble) bubble.textContent = 'Sigo revisando para responderte mejor...';
        }, 8000);

        try {
            if (!window.DJANLINKS_API?.chatWithLinks) {
                throw new Error('Links API is not available.');
            }

            const reply = await window.DJANLINKS_API?.chatWithLinks(text, requestHistory, {
                page: window.location.pathname
            });

            window.clearTimeout(slowTimer);
            typing.remove();

            const responseText = reply?.response || 'Gracias por tu mensaje. Te puedo conectar con un asesor por WhatsApp.';
            const actions = this.normalizeActions(reply?.actions);

            if (reply?.whatsapp_url) this.whatsappUrl = reply.whatsapp_url;
            if (reply?.should_redirect && !actions.some((action) => action.url?.includes('wa.me'))) {
                actions.unshift({ label: 'Hablar con un asesor', url: this.whatsappUrl });
            }

            this.appendMessage(messages, responseText, 'bot', actions);
            this.history.push({ role: 'assistant', content: responseText });
            this.history = this.history.slice(-8);

            if (reply?.lead_capture?.start) {
                this.startLeadCapture(messages, {
                    serviceHint: reply.lead_capture.service_hint,
                    initialMessage: text
                });
            }
        } catch {
            window.clearTimeout(slowTimer);
            typing.remove();
            this.appendMessage(
                messages,
                'Ahora mismo no puedo conectar con el backend, pero puedes hablar con un asesor por WhatsApp.',
                'bot',
                [
                    { label: 'Abrir WhatsApp', url: this.whatsappUrl },
                    { label: 'Reintentar', prompt: text }
                ]
            );
        } finally {
            this.isSending = false;
            this.setInputState(input, false);
            this.saveState();
        }
    },

    startLeadCapture(messages, options = {}) {
        if (this.leadCapture.active) return;

        this.leadCapture = {
            active: true,
            step: 'nombre',
            data: {
                servicio: options.serviceHint || '',
                mensajeInicial: options.initialMessage || '',
                pagina: window.location.pathname
            }
        };

        this.appendMessage(
            messages,
            'Para avanzar con la cotizacion, dime tu nombre. Si prefieres no dejar datos, escribe cancelar.',
            'bot'
        );
        this.saveState();
    },

    async handleLeadCapture(text, messages) {
        const normalized = text.trim().toLowerCase();
        if (['cancelar', 'cancela', 'salir', 'no'].includes(normalized)) {
            this.leadCapture = { active: false, step: null, data: {} };
            this.appendMessage(
                messages,
                'Listo, no guardo tus datos. Puedes seguir preguntandome o abrir WhatsApp cuando quieras.',
                'bot',
                [{ label: 'Abrir WhatsApp', url: this.whatsappUrl }]
            );
            this.saveState();
            return;
        }

        if (this.leadCapture.step === 'nombre') {
            this.leadCapture.data.nombre = text.trim();
            this.leadCapture.step = 'telefono';
            this.appendMessage(messages, 'Gracias. Ahora dime tu numero de WhatsApp o telefono.', 'bot');
            this.saveState();
            return;
        }

        if (this.leadCapture.step === 'telefono') {
            this.leadCapture.data.telefono = text.trim();

            if (!this.leadCapture.data.servicio) {
                this.leadCapture.step = 'servicio';
                this.appendMessage(messages, 'Que tipo de proyecto necesitas: web, software, IA, diseno, marketing o contenido?', 'bot');
                this.saveState();
                return;
            }

            this.leadCapture.step = 'mensaje';
            this.appendMessage(messages, 'Perfecto. Cuentame en una frase que necesitas construir o mejorar.', 'bot');
            this.saveState();
            return;
        }

        if (this.leadCapture.step === 'servicio') {
            this.leadCapture.data.servicio = text.trim();
            this.leadCapture.step = 'mensaje';
            this.appendMessage(messages, 'Genial. Cuentame en una frase que necesitas construir o mejorar.', 'bot');
            this.saveState();
            return;
        }

        if (this.leadCapture.step === 'mensaje') {
            this.leadCapture.data.detalle = text.trim();
            await this.submitLeadCapture(messages);
        }
    },

    async submitLeadCapture(messages) {
        const data = this.leadCapture.data;
        const mensaje = [
            data.mensajeInicial ? `Consulta inicial: ${data.mensajeInicial}` : '',
            data.detalle ? `Detalle: ${data.detalle}` : '',
            data.pagina ? `Pagina: ${data.pagina}` : ''
        ].filter(Boolean).join('\n');

        try {
            if (!window.DJANLINKS_API?.submitLead) {
                throw new Error('Lead API is not available.');
            }

            await window.DJANLINKS_API?.submitLead({
                nombre: data.nombre || 'Lead desde Links AI',
                telefono: data.telefono || '',
                correo: '',
                empresa: '',
                servicio: data.servicio || 'Consulta desde Links AI',
                mensaje: mensaje || 'Consulta creada desde Links AI'
            });

            this.leadCapture = { active: false, step: null, data: {} };
            this.appendMessage(
                messages,
                'Listo, deje tus datos registrados para que el equipo de DJANLINKS te contacte. Tambien puedes abrir WhatsApp si quieres acelerar la conversacion.',
                'bot',
                [{ label: 'Abrir WhatsApp', url: this.whatsappUrl }]
            );
        } catch {
            this.appendMessage(
                messages,
                'No pude guardar tus datos en este momento. Para no hacerte esperar, te recomiendo escribirnos directo por WhatsApp.',
                'bot',
                [{ label: 'Abrir WhatsApp', url: this.whatsappUrl }]
            );
        } finally {
            this.leadCapture = { active: false, step: null, data: {} };
            this.saveState();
        }
    },

    setInputState(input, isDisabled) {
        input.disabled = isDisabled;
        const submit = document.querySelector('#links-ai-form button[type="submit"]');
        if (submit) submit.disabled = isDisabled;
    },

    normalizeActions(actions = []) {
        return actions
            .filter((action) => action && action.label && (action.url || action.prompt))
            .slice(0, 3);
    },

    appendMessage(container, text, role, actions = [], isTyping = false, persist = true) {
        const msg = document.createElement('div');
        msg.className = `links-ai-msg links-ai-msg--${role}`;
        if (isTyping) msg.classList.add('is-typing');

        const bubble = document.createElement('div');
        bubble.className = 'links-ai-bubble';
        bubble.textContent = text;
        msg.appendChild(bubble);

        if (actions.length) {
            const actionWrap = document.createElement('div');
            actionWrap.className = 'links-ai-actions';

            actions.forEach((action) => {
                if (action.prompt) {
                    const button = document.createElement('button');
                    button.type = 'button';
                    button.textContent = action.label;
                    button.addEventListener('click', () => {
                        const input = document.getElementById('links-ai-input');
                        const panel = document.getElementById('links-ai-panel');
                        this.sendMessage(action.prompt, { input, messages: container, panel });
                    });
                    actionWrap.appendChild(button);
                    return;
                }

                const link = document.createElement('a');
                link.href = action.url;
                link.textContent = action.label;
                if (action.url.startsWith('http')) {
                    link.target = '_blank';
                    link.rel = 'noopener noreferrer';
                }
                actionWrap.appendChild(link);
            });

            msg.appendChild(actionWrap);
        }

        container.appendChild(msg);
        container.scrollTop = container.scrollHeight;

        if (persist) {
            this.messagesState.push({ text, role, actions: this.normalizeActions(actions) });
            this.messagesState = this.messagesState.slice(-20);
            this.saveState();
        }

        return msg;
    },

    loadState() {
        if (!this.canPersistSession()) return;

        try {
            const saved = window.sessionStorage.getItem(this.storageKey);
            if (!saved) return;

            const state = JSON.parse(saved);
            this.history = Array.isArray(state.history) ? state.history.slice(-8) : [];
            this.messagesState = Array.isArray(state.messagesState) ? state.messagesState.slice(-20) : [];
            this.whatsappUrl = state.whatsappUrl || this.whatsappUrl;
            this.leadCapture = state.leadCapture?.active
                ? state.leadCapture
                : { active: false, step: null, data: {} };
        } catch {
            this.history = [];
            this.messagesState = [];
            this.leadCapture = { active: false, step: null, data: {} };
        }
    },

    saveState() {
        if (!this.canPersistSession()) return;

        try {
            window.sessionStorage.setItem(this.storageKey, JSON.stringify({
                history: this.history,
                messagesState: this.messagesState,
                whatsappUrl: this.whatsappUrl,
                leadCapture: this.leadCapture
            }));
        } catch {
            // sessionStorage can fail in private browsing; Links still works in memory.
        }
    },

    canPersistSession() {
        try {
            const consent = JSON.parse(window.localStorage.getItem('djanlinks.cookie-consent.v1'));
            return consent?.functional === true;
        } catch {
            return false;
        }
    }
};

document.addEventListener('DOMContentLoaded', () => LinksAI.init());
