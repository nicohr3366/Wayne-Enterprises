import pandas as pd
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.core.management.base import BaseCommand
from apps.foundation.models import Donacion


class Command(BaseCommand):
    help = 'Carga donaciones de Wayne Foundation desde donaciones.csv (pandas)'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='apps/foundation/data/donaciones.csv')
        parser.add_argument('--clear', action='store_true', help='Borra registros existentes antes de cargar')

    def handle(self, *args, **options):
        csv_file = options['file']

        if options['clear']:
            count = Donacion.objects.count()
            Donacion.objects.all().delete()
            self.stdout.write(f'  Borrados {count} registros existentes.')

        def safe_str(val, default=''):
            return str(val).strip() if pd.notna(val) else default

        def safe_decimal(val, default='0'):
            if pd.isna(val):
                return Decimal(default)
            try:
                return Decimal(str(val).replace(',', '').strip())
            except InvalidOperation:
                return Decimal(default)

        def safe_int(val):
            if pd.isna(val):
                return None
            try:
                return int(float(val))
            except (ValueError, TypeError):
                return None

        def safe_bool(val):
            if pd.isna(val):
                return False
            v = str(val).strip().upper()
            return v in ('TRUE', '1', 'YES', 'Y', 'SI')

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
            if not safe_str(row.get('DONATION_ID', '')):
                continue
            try:
                rec = Donacion(
                    donation_id=safe_str(row.get('DONATION_ID', '')),
                    donor_name=safe_str(row.get('DONOR_NAME', '')),
                    donor_type=safe_str(row.get('DONOR_TYPE', '')),
                    amount_usd=safe_decimal(row.get('AMOUNT_USD', 0)),
                    donation_date=safe_date(row.get('DONATION_DATE')),
                    project_name=safe_str(row.get('PROJECT_NAME', '')),
                    project_category=safe_str(row.get('PROJECT_CATEGORY', '')),
                    gotham_district=safe_str(row.get('GOTHAM_DISTRICT', '')),
                    purpose=safe_str(row.get('PURPOSE', '')),
                    fiscal_year=safe_int(row.get('FISCAL_YEAR')),
                    tax_deductible=safe_bool(row.get('TAX_DEDUCTIBLE', True)),
                    matched=safe_bool(row.get('MATCHED', False)),
                    recurring=safe_bool(row.get('RECURRING', False)),
                    status=safe_str(row.get('STATUS', 'completed')),
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
            Donacion.objects.bulk_create(lote, ignore_conflicts=True)
            cargados += len(lote)
            self.stdout.write(f'  {cargados}/{total} registros...')

        self.stdout.write(self.style.SUCCESS(
            f'\nOK: {cargados} donaciones cargadas. {errores} filas con error.'
        ))
