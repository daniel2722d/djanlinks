import json
import unicodedata
import urllib.error
import urllib.request
from urllib.parse import quote

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

INTENT_KEYWORDS = {
    "contact": (
        "asesor", "contacto", "contactar", "whatsapp", "reunion", "llamar",
        "hablar", "contratar", "comprar", "agendar",
    ),
    "pricing": (
        "precio", "precios", "plan", "planes", "cotiza", "cotizacion",
        "presupuesto", "costo", "cuanto vale", "cuanto cuesta",
    ),
    "ai": (
        "ia", "inteligencia artificial", "chatbot", "automatizacion",
        "automatizar", "asistente", "bot", "gemini",
    ),
    "web": (
        "web", "pagina", "landing", "sitio", "ecommerce", "tienda",
        "seo tecnico",
    ),
    "software": (
        "software", "app", "aplicacion", "sistema", "dashboard", "crm",
        "plataforma", "inventario", "facturacion",
    ),
    "design": (
        "diseno", "ui", "ux", "branding", "marca", "logo", "identidad",
        "interfaz",
    ),
    "marketing": (
        "marketing", "seo", "redes", "publicidad", "campana", "anuncios",
        "posicionamiento",
    ),
    "content": (
        "contenido", "video", "audiovisual", "reels", "fotografia",
        "motion", "edicion",
    ),
    "portfolio": (
        "portafolio", "proyectos", "casos", "arq722", "azul celeste",
        "ruta verde",
    ),
}

SERVICE_HINTS = {
    "ai": "Inteligencia Artificial",
    "web": "Desarrollo Web",
    "software": "Software & Apps",
    "design": "Diseno UI/UX",
    "marketing": "Marketing Digital",
    "content": "Contenido Audiovisual",
}

LINKS_SYSTEM_PROMPT = """
Eres Links, el asistente de IA oficial de DJANLINKS Creative Tech Studio.

Identidad:
- DJANLINKS es un estudio premium de desarrollo de software, IA, automatizacion,
  diseno web, UX/UI, branding digital y soluciones tecnologicas.
- Links representa creatividad, tecnologia, automatizacion y experiencias
  digitales inteligentes.
- Tu tono es profesional, cercano, innovador y confiable.

Objetivos:
- Ayudar al visitante a entender servicios, planes, portafolio y formas de
  iniciar un proyecto.
- Recomendar el servicio adecuado segun la necesidad del usuario.
- Hacer preguntas breves para calificar el proyecto cuando falte informacion.
- Facilitar el contacto con un asesor por WhatsApp cuando el usuario muestre
  interes comercial, pida precio, cotizacion, reunion o asesoria humana.

Servicios:
- Desarrollo web premium y landing pages.
- Software a medida, sistemas internos, dashboards y CRM.
- Inteligencia artificial, chatbots y automatizaciones.
- UX/UI y branding digital.
- Marketing digital y contenido audiovisual.

Reglas:
- Responde siempre en espanol.
- Se claro y breve: 2 a 4 frases, salvo que el usuario pida detalle.
- No inventes precios cerrados si no estan confirmados; invita a cotizar.
- Si recomiendas hablar con un asesor, dilo naturalmente.
- Nunca pidas datos sensibles. Para contacto, sugiere WhatsApp o captura
  nombre y telefono si el usuario quiere cotizar.
""".strip()


def build_whatsapp_url(message=""):
    base = f"https://wa.me/{settings.LINKS_WHATSAPP_NUMBER}"
    text = message or (
        "Hola, vengo desde la web de DJANLINKS. Quiero hablar con un asesor "
        "sobre mi proyecto."
    )
    return f"{base}?text={quote(text)}"


def normalize_text(value):
    value = unicodedata.normalize("NFKD", str(value).lower())
    return "".join(char for char in value if not unicodedata.combining(char))


def classify_intent(message):
    normalized = normalize_text(message)
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return intent
    return "general"


def should_capture_lead(intent):
    return intent in {"contact", "pricing"}


def sanitize_history(history, message):
    if not isinstance(history, list):
        return []

    clean = []
    for item in history[-8:]:
        role = item.get("role")
        content = str(item.get("content", "")).strip()
        if role in {"user", "assistant"} and content:
            clean.append({"role": role, "content": content[:1000]})

    if clean:
        last = clean[-1]
        same_message = normalize_text(last["content"]) == normalize_text(message)
        if last["role"] == "user" and same_message:
            clean = clean[:-1]

    return clean[-6:]


def call_gemini(message, history):
    contents = []

    for item in history:
        contents.append({
            "role": "user" if item["role"] == "user" else "model",
            "parts": [{"text": item["content"]}],
        })

    contents.append({
        "role": "user",
        "parts": [{"text": message}],
    })

    body = {
        "systemInstruction": {
            "parts": [{"text": LINKS_SYSTEM_PROMPT}],
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.65,
            "maxOutputTokens": 350,
        },
    }

    model = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
    request = urllib.request.Request(
        f"{GEMINI_API_BASE}/{model}:generateContent?key={settings.GEMINI_API_KEY}",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=25) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def fallback_reply(message, intent):
    if intent == "pricing":
        return (
            "Puedo orientarte. El valor depende del alcance: landing, sitio "
            "multipagina, software, IA o automatizacion. Si quieres, te tomo "
            "unos datos basicos para que un asesor prepare una cotizacion real."
        )

    if intent == "contact":
        return (
            "Claro. Puedo conectarte con un asesor por WhatsApp o tomar tus "
            "datos aqui mismo para que el equipo te contacte."
        )

    if intent == "ai":
        return (
            "Para IA y automatizacion podemos crear chatbots, asistentes, flujos "
            "de atencion, integraciones y procesos internos. Lo ideal es mapear "
            "que tarea quieres automatizar y que resultado esperas."
        )

    if intent == "web":
        return (
            "Para web podemos ayudarte con landing pages, sitios premium, "
            "portafolios, paginas corporativas y experiencias con animaciones. "
            "La mejor opcion depende de si quieres vender, captar leads o "
            "posicionar marca."
        )

    if intent == "software":
        return (
            "Para software podemos construir sistemas internos, dashboards, CRM, "
            "apps y plataformas conectadas a bases de datos. Primero conviene "
            "definir usuarios, procesos y reportes clave."
        )

    if intent == "design":
        return (
            "En diseno trabajamos interfaces, experiencia de usuario, branding e "
            "identidad visual. Podemos ayudarte a que la marca se vea premium y "
            "sea facil de usar."
        )

    if intent == "marketing":
        return (
            "En marketing podemos apoyar con estrategia digital, SEO, publicidad "
            "y contenido orientado a conversion. La ruta depende del canal donde "
            "quieres crecer."
        )

    if intent == "content":
        return (
            "En contenido audiovisual podemos crear piezas para marca, redes, "
            "campanas y presentaciones. Lo importante es definir objetivo, formato "
            "y estilo visual."
        )

    if intent == "portfolio":
        return (
            "Puedes revisar el portafolio para ver proyectos como ARQ722, Azul "
            "Celeste y Ruta Verde. Tambien puedo recomendarte el caso mas cercano "
            "a lo que quieres construir."
        )

    return (
        "Soy Links, el asistente IA de DJANLINKS. Puedo ayudarte a elegir "
        "servicios, entender planes, revisar ideas de software o conectarte con "
        "un asesor por WhatsApp."
    )


def actions_for_intent(intent, whatsapp_url):
    common_contact = {"label": "Hablar con un asesor", "url": whatsapp_url}

    if intent in {"contact", "pricing"}:
        return [
            common_contact,
            {"label": "Ver planes", "url": "nuestros_planes.html"},
            {"label": "Ver portafolio", "url": "portafolio.html"},
        ]

    if intent == "web":
        return [
            {"label": "Ver desarrollo web", "url": "desarrollo.html"},
            {"label": "Ver planes", "url": "nuestros_planes.html"},
            common_contact,
        ]

    if intent == "ai":
        return [
            {"label": "Ver IA", "url": "ia.html"},
            {"label": "Ver software", "url": "software.html"},
            common_contact,
        ]

    if intent == "software":
        return [
            {"label": "Ver software", "url": "software.html"},
            {"label": "Ver portafolio", "url": "portafolio.html"},
            common_contact,
        ]

    if intent == "design":
        return [
            {"label": "Ver diseno", "url": "diseno.html"},
            {"label": "Ver portafolio", "url": "portafolio.html"},
            common_contact,
        ]

    if intent == "marketing":
        return [
            {"label": "Ver marketing", "url": "marketing.html"},
            {"label": "Ver planes", "url": "nuestros_planes.html"},
            common_contact,
        ]

    if intent == "content":
        return [
            {"label": "Ver contenido", "url": "contenido.html"},
            {"label": "Ver portafolio", "url": "portafolio.html"},
            common_contact,
        ]

    if intent == "portfolio":
        return [
            {"label": "Ver portafolio", "url": "portafolio.html"},
            {"label": "Ver planes", "url": "nuestros_planes.html"},
            common_contact,
        ]

    return [
        {"label": "Ver planes", "url": "nuestros_planes.html"},
        {"label": "Ver portafolio", "url": "portafolio.html"},
        common_contact,
    ]


class ChatView(APIView):
    def post(self, request):
        message = str(request.data.get("message", "")).strip()
        raw_history = request.data.get("history", [])

        if not message:
            return Response(
                {"error": "El mensaje es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(message) > 1500:
            return Response(
                {"error": "El mensaje es demasiado largo"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        intent = classify_intent(message)
        history = sanitize_history(raw_history, message)
        source = "fallback"

        try:
            if settings.GEMINI_API_KEY:
                response_text = call_gemini(message, history)
                source = "gemini"
            else:
                response_text = fallback_reply(message, intent)

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            ValueError,
            json.JSONDecodeError,
            KeyError,
            IndexError,
        ):
            response_text = fallback_reply(message, intent)

        whatsapp_text = (
            "Hola, vengo desde la web de DJANLINKS. Links me recomendo hablar "
            f"con un asesor. Mi consulta es: {message[:300]}"
        )
        whatsapp_url = build_whatsapp_url(whatsapp_text)

        return Response({
            "response": response_text,
            "source": source,
            "intent": intent,
            "should_redirect": intent == "contact",
            "whatsapp_url": whatsapp_url,
            "actions": actions_for_intent(intent, whatsapp_url),
            "lead_capture": {
                "start": should_capture_lead(intent),
                "service_hint": SERVICE_HINTS.get(intent, ""),
            },
        })
