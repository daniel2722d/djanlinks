"""
LEADS — Modelo de datos para formularios de contacto
=====================================================

Cuando alguien llena el formulario en contact.html, los datos
pueden guardarse aquí vía POST /api/leads/

Flujo típico de una app Django:
  models.py → define tablas | views.py → lógica | urls.py → rutas | admin.py → panel
"""
from django.db import models


class Lead(models.Model):
    """Un lead = una persona que dejó sus datos de contacto."""

    nombre = models.CharField(max_length=200)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    empresa = models.CharField(max_length=200, blank=True)
    servicio = models.CharField(max_length=200, blank=True)  # Tipo de proyecto
    mensaje = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)  # ¿Ya le respondimos?

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.nombre} — {self.created_at:%Y-%m-%d}'
