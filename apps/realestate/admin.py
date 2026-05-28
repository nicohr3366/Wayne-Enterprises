from django.contrib import admin
from .models import Property, UrbanProject

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_type', 'location', 'available', 'created_at')
    list_filter = ('property_type', 'available')
    search_fields = ('name', 'location')

@admin.register(UrbanProject)
class UrbanProjectAdmin(admin.ModelAdmin):
    list_display = (
        'project_id',
        'project_name',
        'district',
        'status',
        'priority'
    )

    list_filter = (
        'status',
        'priority',
        'district'
    )

    search_fields = (
        'project_name',
        'district'
    )