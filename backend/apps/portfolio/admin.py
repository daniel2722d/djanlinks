from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_featured', 'is_active', 'order']
    prepopulated_fields = {'slug': ('title',)}
