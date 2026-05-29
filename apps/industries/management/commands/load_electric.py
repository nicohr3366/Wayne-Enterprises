import pandas as pd
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.core.management.base import BaseCommand
from apps.industries.models import ElectricRecord


class Command(BaseCommand):
    help = 'Carga datos red electrica Gotham desde electric_grid.csv (pandas)'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='apps/industries/data/electric_grid.csv')
        parser.add_argument('--clear', action='store_true', help='Borra registros existentes antes de cargar')

    def handle(self, *args, **options):
        csv_file = options['file']

        if options['clear']:
            count = ElectricRecord.objects.count()
            ElectricRecord.objects.all().delete()
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

        def safe_int(val):
            if pd.isna(val):
                return None
            try:
                return int(float(val))
            except (ValueError, TypeError):
                return None

        def safe_date(val):
            if pd.isna(val):
                return None
            v = str(val).strip()
            for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'):
                try:
                    return datetime.strptime(v, fmt).date()
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
                rec = ElectricRecord(
                    record_id=safe_str(row.get('RECORD_ID', '')),
                    date=safe_date(row.get('DATE')),
                    station_id=safe_str(row.get('STATION_ID', '')),
                    station_name=safe_str(row.get('STATION_NAME', '')),
                    gotham_district=safe_str(row.get('GOTHAM_DISTRICT', '')),
                    station_type=safe_str(row.get('STATION_TYPE', '')),
                    energy_generated_mwh=safe_decimal(row.get('ENERGY_GENERATED_MWH')),
                    energy_consumed_mwh=safe_decimal(row.get('ENERGY_CONSUMED_MWH')),
                    peak_demand_mw=safe_decimal(row.get('PEAK_DEMAND_MW')),
                    avg_demand_mw=safe_decimal(row.get('AVG_DEMAND_MW')),
                    renewable_pct=safe_decimal(row.get('RENEWABLE_PCT')),
                    outage_hours=safe_decimal(row.get('OUTAGE_HOURS')),
                    fuel_type=safe_str(row.get('FUEL_TYPE', '')),
                    grid_frequency_hz=safe_decimal(row.get('GRID_FREQUENCY_HZ')),
                    transmission_loss_pct=safe_decimal(row.get('TRANSMISSION_LOSS_PCT')),
                    fiscal_year=safe_int(row.get('FISCAL_YEAR')),
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
            ElectricRecord.objects.bulk_create(lote, ignore_conflicts=True)
            cargados += len(lote)
            self.stdout.write(f'  {cargados}/{total} registros...')

        self.stdout.write(self.style.SUCCESS(
            f'\nOK: {cargados} registros red electrica cargados. {errores} filas con error.'
        ))
