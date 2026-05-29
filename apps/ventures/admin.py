from django.contrib import admin

from .models import NavItem


@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
	list_display = ('order', 'label', 'url_name', 'is_active', 'open_in_new_tab')
	list_editable = ('label', 'url_name', 'is_active', 'open_in_new_tab')
	list_filter = ('is_active', 'open_in_new_tab')
	search_fields = ('label', 'url_name')
	ordering = ('order',)
