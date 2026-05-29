import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from apps.ventures.models import SatelliteErrorLog


class Command(BaseCommand):
	help = 'Carga logs de errores de satélites WayneTech desde CSV usando pandas'

	def add_arguments(self, parser):
		parser.add_argument('--file', type=str, default='apps/ventures/data/WayneTech_Satellite_ErrorLogs.csv')
		parser.add_argument('--clear', action='store_true', help='Borra registros existentes antes de cargar')

	def handle(self, *args, **options):
		csv_file = options['file']

		if options['clear']:
			count = SatelliteErrorLog.objects.count()
			SatelliteErrorLog.objects.all().delete()
			self.stdout.write(f'  OK: Borrados {count} registros existentes.')

		# Leer CSV con pandas
		try:
			df = pd.read_csv(csv_file, encoding='utf-8-sig')
			self.stdout.write(f'  OK: Archivo cargado: {len(df)} filas')
		except FileNotFoundError:
			self.stdout.write(self.style.ERROR(f'ERROR: No se encontro: {csv_file}'))
			return

		# Validar que existan las columnas requeridas
		required_cols = ['log_id', 'timestamp', 'satellite_id', 'satellite_name', 'error_code', 
		                  'error_description', 'severity', 'resolved']
		
		missing = [col for col in required_cols if col not in df.columns]
		if missing:
			self.stdout.write(self.style.ERROR(f'ERROR: Columnas faltantes: {", ".join(missing)}'))
			self.stdout.write(f'  Columnas disponibles: {", ".join(df.columns)}')
			return

		def parse_datetime(val):
			if pd.isna(val):
				return None
			v = str(val).strip()
			for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%m/%d/%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S'):
				try:
					return datetime.strptime(v, fmt)
				except ValueError:
					continue
			return None

		def safe_float(val):
			try:
				return float(val) if pd.notna(val) else None
			except (ValueError, TypeError):
				return None

		def safe_int(val):
			try:
				return int(float(val)) if pd.notna(val) else None
			except (ValueError, TypeError):
				return None

		def safe_str(val):
			return str(val).strip() if pd.notna(val) else ''

		def safe_bool(val):
			if pd.isna(val):
				return False
			v = str(val).strip().lower()
			return v in ('true', '1', 'yes', 'y', 'x')

		logs = []
		errores = 0
		duplicados = 0

		for idx, row in df.iterrows():
			log_id = safe_str(row['log_id'])
			if not log_id:
				continue

			# Verificar si ya existe
			if SatelliteErrorLog.objects.filter(log_id=log_id).exists():
				duplicados += 1
				continue

			try:
				error_log = SatelliteErrorLog(
					log_id=log_id,
					timestamp=parse_datetime(row['timestamp']),
					satellite_id=safe_str(row.get('satellite_id', '')),
					satellite_name=safe_str(row.get('satellite_name', '')),
					orbit_type=safe_str(row.get('orbit_type', '')),
					satellite_type=safe_str(row.get('satellite_type', '')),
					ground_station=safe_str(row.get('ground_station', '')),
					operator_id=safe_str(row.get('operator_id', '')),
					error_code=safe_str(row['error_code']),
					error_description=safe_str(row['error_description']),
					subsystem=safe_str(row.get('subsystem', '')),
					severity=safe_str(row.get('severity', 'MEDIUM')).upper()[:20],
					link_type=safe_str(row.get('link_type', '')),
					protocol=safe_str(row.get('protocol', '')),
					frequency_mhz=safe_float(row.get('frequency_mhz')),
					snr_db=safe_float(row.get('snr_db')),
					bit_error_rate=safe_float(row.get('bit_error_rate')),
					elevation_angle_deg=safe_float(row.get('elevation_angle_deg')),
					event_duration_ms=safe_int(row.get('event_duration_ms')),
					retry_count=safe_int(row.get('retry_count')),
					weather_condition=safe_str(row.get('weather_condition', '')),
					requires_action=safe_bool(row.get('requires_action', False)),
					resolved=safe_bool(row['resolved']),
					resolution_action=safe_str(row.get('resolution_action', '')),
					resolution_time_min=safe_int(row.get('resolution_time_min')),
				)
				logs.append(error_log)
			except Exception as e:
				errores += 1
				if errores <= 5:
					self.stdout.write(self.style.WARNING(f'  Fila {idx + 2} ignorada: {e}'))

		total = len(logs)
		batch_size = 500
		cargados = 0

		for i in range(0, total, batch_size):
			lote = logs[i:i + batch_size]
			SatelliteErrorLog.objects.bulk_create(lote, ignore_conflicts=True)
			cargados += len(lote)
			self.stdout.write(f'  {cargados}/{total} logs...')

		self.stdout.write(self.style.SUCCESS(
			f'\nOK: {cargados} logs cargados. {duplicados} duplicados. {errores} filas con error.'
		))
