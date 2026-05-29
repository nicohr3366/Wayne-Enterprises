import pandas as pd
from decimal import Decimal, InvalidOperation
from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from apps.tech.models import TumblerTelemetry


class Command(BaseCommand):
    help = 'Carga telemetria Tumbler desde telemetry.csv (pandas)'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='apps/tech/data/telemetry.csv')
        parser.add_argument('--clear', action='store_true', help='Borra registros existentes antes de cargar')

    def handle(self, *args, **options):
        csv_file = options['file']

        if options['clear']:
            count = TumblerTelemetry.objects.count()
            TumblerTelemetry.objects.all().delete()
            self.stdout.write(f'  Borrados {count} registros existentes.')

        def safe_str(val, default=''):
            return str(val).strip() if pd.notna(val) else default

        def safe_decimal(val):
            if pd.isna(val):
                return None
            try:
                return Decimal(str(val).replace(',', '').strip())
            except InvalidOperation:
                return None

        def safe_datetime(val):
            if pd.isna(val):
                return None
            v = str(val).strip()
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%m/%d/%Y %H:%M:%S'):
                try:
                    dt = datetime.strptime(v, fmt)
                    return dt.replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
            return None

        try:
            df = pd.read_csv(csv_file, sep=';', skiprows=1, encoding='utf-8-sig')
            self.stdout.write(f'  Archivo cargado: {len(df)} filas')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontro: {csv_file}'))
            return

        registros = []
        errores = 0

        for i, row in df.iterrows():
            if not safe_str(row.get('RECORD_ID', '')):
                continue
            try:
                rec = TumblerTelemetry(
                    record_id=safe_str(row.get('RECORD_ID', '')),
                    timestamp=safe_datetime(row.get('TIMESTAMP')),
                    vehicle_id=safe_str(row.get('VEHICLE_ID', '')),
                    vehicle_model=safe_str(row.get('VEHICLE_MODEL', '')),
                    mission_id=safe_str(row.get('MISSION_ID', '')),
                    mission_type=safe_str(row.get('MISSION_TYPE', '')),
                    speed_kmh=safe_decimal(row.get('SPEED_KMH')),
                    fuel_level_pct=safe_decimal(row.get('FUEL_LEVEL_PCT')),
                    engine_temp_c=safe_decimal(row.get('ENGINE_TEMP_C')),
                    battery_level_pct=safe_decimal(row.get('BATTERY_LEVEL_PCT')),
                    latitude=safe_decimal(row.get('LATITUDE')),
                    longitude=safe_decimal(row.get('LONGITUDE')),
                    gotham_zone=safe_str(row.get('GOTHAM_ZONE', '')),
                    alert_type=safe_str(row.get('ALERT_TYPE', '')),
                    system_status=safe_str(row.get('SYSTEM_STATUS', 'operational')),
                    distance_km=safe_decimal(row.get('DISTANCE_KM')),
                )
                registros.append(rec)
            except Exception as e:
                errores += 1
                if errores <= 5:
                    self.stdout.write(self.style.WARNING(f'  Fila {i + 3} ignorada: {e}'))

        total = len(registros)
        batch_size = 500
        cargados = 0

        for i in range(0, total, batch_size):
            lote = registros[i:i + batch_size]
            TumblerTelemetry.objects.bulk_create(lote, ignore_conflicts=True)
            cargados += len(lote)
            self.stdout.write(f'  {cargados}/{total} registros...')

        self.stdout.write(self.style.SUCCESS(
            f'\nOK: {cargados} registros de telemetria cargados. {errores} filas con error.'
        ))
