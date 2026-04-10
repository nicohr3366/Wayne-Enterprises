from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_type', 'location', 'available', 'created_at')
    list_filter = ('property_type', 'available')
    search_fields = ('name', 'location')
