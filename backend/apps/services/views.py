"""GET /api/services/ — lista servicios activos desde la BD."""
from rest_framework import generics
from .models import Service
from .serializers import ServiceSerializer


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
