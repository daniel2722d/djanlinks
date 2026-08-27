from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'correo', 'servicio', 'is_contacted', 'created_at']
    list_filter = ['is_contacted', 'created_at']
    search_fields = ['nombre', 'correo', 'empresa']
