"""Rutas de leads — montadas en core/urls.py como /api/leads/"""
from django.urls import path
from .views import LeadCreateView

urlpatterns = [
    path('', LeadCreateView.as_view(), name='lead-create'),
]
