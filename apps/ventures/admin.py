from django.contrib import admin

from .models import NavItem, SatelliteErrorLog


@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
	list_display = ('order', 'label', 'url_name', 'is_active', 'open_in_new_tab')
	list_editable = ('label', 'url_name', 'is_active', 'open_in_new_tab')
	list_filter = ('is_active', 'open_in_new_tab')
	search_fields = ('label', 'url_name')
	ordering = ('order',)


@admin.register(SatelliteErrorLog)
class SatelliteErrorLogAdmin(admin.ModelAdmin):
	list_display = ('log_id', 'timestamp', 'satellite_name', 'error_code', 'severity', 'resolved', 'requires_action')
	list_filter = ('severity', 'resolved', 'requires_action', 'timestamp', 'satellite_type')
	search_fields = ('log_id', 'satellite_name', 'satellite_id', 'error_code', 'error_description')
	readonly_fields = ('log_id', 'timestamp')
	fieldsets = (
		('Identificación', {
			'fields': ('log_id', 'timestamp', 'satellite_id', 'satellite_name')
		}),
		('Error', {
			'fields': ('error_code', 'error_description', 'severity', 'subsystem')
		}),
		('Satélite', {
			'fields': ('orbit_type', 'satellite_type', 'ground_station', 'operator_id')
		}),
		('Comunicación', {
			'fields': ('link_type', 'protocol', 'frequency_mhz', 'snr_db', 'bit_error_rate', 'elevation_angle_deg')
		}),
		('Evento', {
			'fields': ('event_duration_ms', 'retry_count', 'weather_condition')
		}),
		('Resolución', {
			'fields': ('requires_action', 'resolved', 'resolution_action', 'resolution_time_min')
		}),
	)
	date_hierarchy = 'timestamp'
	ordering = ('-timestamp',)
