from django.db import models


class SatelliteErrorLog(models.Model):
	"""
	Dataset de Logs de Errores de Satélites WayneTech — Juliana
	Telemetría de errores y anomalías en satélites operacionales.
	"""
	# Log Identifiers
	log_id = models.CharField(max_length=50, unique=True, help_text='ID único del registro de error')
	timestamp = models.DateTimeField(help_text='Fecha y hora del evento')

	# Satellite Info
	satellite_id = models.CharField(max_length=50, help_text='ID del satélite')
	satellite_name = models.CharField(max_length=200, help_text='Nombre del satélite')
	orbit_type = models.CharField(
		max_length=20,
		choices=[
			('LEO', 'LEO - Órbita Baja'),
			('MEO', 'MEO - Órbita Media'),
			('GEO', 'GEO - Órbita Geoestacionaria'),
			('HEO', 'HEO - Órbita Elíptica Alta'),
		],
		help_text='Tipo de órbita'
	)
	satellite_type = models.CharField(
		max_length=50,
		choices=[
			('IoT', 'IoT'),
			('Relay', 'Relay'),
			('Observación', 'Observación'),
			('Seguridad', 'Seguridad'),
			('Datos', 'Datos'),
			('Investigación', 'Investigación'),
			('Navegación', 'Navegación'),
		],
		help_text='Tipo de satélite'
	)

	# Ground Station & Operator
	ground_station = models.CharField(max_length=100, help_text='Estación terrena')
	operator_id = models.CharField(max_length=100, blank=True, help_text='ID del operador')

	# Error Details
	error_code = models.CharField(max_length=20, help_text='Código de error (ej: ERR-RX-004)')
	error_description = models.CharField(max_length=500, help_text='Descripción del error')
	subsystem = models.CharField(
		max_length=100,
		help_text='Subsistema afectado (Receptor, Transmisor, OBC, ADCS, etc)'
	)
	severity = models.CharField(
		max_length=20,
		choices=[
			('LOW', 'Baja'),
			('MEDIUM', 'Media'),
			('HIGH', 'Alta'),
			('CRITICAL', 'Crítica'),
		],
		help_text='Nivel de severidad'
	)

	# Communications Parameters
	link_type = models.CharField(max_length=100, help_text='Tipo de enlace (Ka-Band, X-Band, etc)')
	protocol = models.CharField(max_length=100, help_text='Protocolo utilizado')
	frequency_mhz = models.FloatField(help_text='Frecuencia en MHz')

	# Signal Quality
	snr_db = models.FloatField(help_text='Relación Señal/Ruido en dB')
	bit_error_rate = models.CharField(max_length=50, help_text='Tasa de error de bits')
	elevation_angle_deg = models.FloatField(help_text='Ángulo de elevación en grados')

	# Event Metrics
	event_duration_ms = models.BigIntegerField(help_text='Duración del evento en ms')
	retry_count = models.IntegerField(help_text='Número de reintentos')
	weather_condition = models.CharField(
		max_length=100,
		choices=[
			('Clear', 'Despejado'),
			('Cloudy', 'Nublado'),
			('Fog', 'Niebla'),
			('Rain', 'Lluvia'),
			('Snow', 'Nieve'),
			('Stormy', 'Tormentoso'),
		],
		help_text='Condición meteorológica'
	)

	# Resolution Status
	requires_action = models.BooleanField(default=False, help_text='¿Requiere acción?')
	resolved = models.BooleanField(default=False, help_text='¿Ha sido resuelto?')
	resolution_action = models.CharField(max_length=500, blank=True, help_text='Acción de resolución tomada')
	resolution_time_min = models.IntegerField(null=True, blank=True, help_text='Tiempo de resolución en minutos')

	# Metadata
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-timestamp']
		verbose_name = 'Satellite Error Log'
		verbose_name_plural = 'Satellite Error Logs'
		indexes = [
			models.Index(fields=['satellite_id']),
			models.Index(fields=['timestamp']),
			models.Index(fields=['severity']),
		]

	def __str__(self):
		return f"{self.log_id} — {self.satellite_name} ({self.error_code})"

	@property
	def is_critical(self):
		return self.severity == 'CRITICAL' or self.requires_action


class NavItem(models.Model):
	label = models.CharField(max_length=100, help_text='Texto visible en el menú')
	url_name = models.CharField(max_length=100, help_text='Nombre de URL con namespace, por ejemplo ventures:home')
	order = models.IntegerField(default=0, help_text='Orden de aparición')
	is_active = models.BooleanField(default=True, help_text='Mostrar en el menú')
	open_in_new_tab = models.BooleanField(default=False)

	class Meta:
		ordering = ['order']
		verbose_name = 'Nav Item'
		verbose_name_plural = 'Nav Items'

	def __str__(self):
		return f'{self.order}. {self.label}'

	def get_url(self):
		from django.urls import reverse

		try:
			return reverse(self.url_name)
		except Exception:
			return '#'
