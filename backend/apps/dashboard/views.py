"""
DASHBOARD — Estadísticas para panel administrativo
===================================================
GET /api/dashboard/stats/

Devuelve conteos de leads, proyectos y servicios.
Útil para un futuro panel de control interno.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.leads.models import Lead
from apps.portfolio.models import Project
from apps.services.models import Service


class DashboardStatsView(APIView):

    def get(self, request):
        return Response({
            'leads_total': Lead.objects.count(),
            'leads_pending': Lead.objects.filter(is_contacted=False).count(),
            'projects_active': Project.objects.filter(is_active=True).count(),
            'services_active': Service.objects.filter(is_active=True).count(),
        })
