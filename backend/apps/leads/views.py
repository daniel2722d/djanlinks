"""
LEADS — Vista API para recibir contactos
=========================================
POST /api/leads/ con JSON: { nombre, correo, mensaje, ... }
Conecta con: frontend/assets/js/api.js → submitLead()
"""
from rest_framework import generics
from .models import Lead
from .serializers import LeadSerializer


class LeadCreateView(generics.CreateAPIView):
    """Crea un nuevo lead en la base de datos."""

    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
