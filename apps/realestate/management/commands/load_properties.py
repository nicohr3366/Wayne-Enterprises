import pandas as pd
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from apps.realestate.models import Property


class Command(BaseCommand):
    help = 'Carga propiedades de Gotham desde propiedades.csv (pandas)'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='apps/realestate/data/propiedades.csv')
        parser.add_argument('--clear', action='store_true', help='Borra registros existentes antes de cargar')

    def handle(self, *args, **options):
        csv_file = options['file']

        if options['clear']:
            count = Property.objects.count()
            Property.objects.all().delete()
            self.stdout.write(f'  Borrados {count} registros existentes.')

        def money(val):
            try:
                return Decimal(str(val).replace('$', '').replace(',', '').strip() or '0')
            except InvalidOperation:
                return Decimal('0')

        def decimal_val(val):
            if pd.isna(val):
                return None
            try:
                v = str(val).strip()
                return Decimal(v) if v else None
            except InvalidOperation:
                return None

        def entero(val):
            if pd.isna(val):
                return None
            v = str(val).strip().replace('.0', '')
            return int(v) if v.isdigit() else None

        def booleano(val):
            if pd.isna(val):
                return False
            return str(val).strip().upper() in ('Y', 'TRUE', '1', 'YES', 'SI', 'SI')

        def safe_str(val):
            return str(val).strip() if pd.notna(val) else ''

        try:
            df = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig')
            self.stdout.write(f'  Archivo cargado: {len(df)} filas')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontro: {csv_file}'))
            return

        propiedades = []
        errores = 0

        for i, row in df.iterrows():
            if not safe_str(row.get('PROJECT_ID', '')):
                continue
            try:
                p = Property(
                    project_id=safe_str(row.get('PROJECT_ID', '')),
                    name=safe_str(row.get('NAME', '')),
                    developer=safe_str(row.get('DEVELOPER', '')),
                    property_type=safe_str(row.get('PROPERTY_TYPE', '')),
                    district=safe_str(row.get('DISTRICT', '')),
                    location=safe_str(row.get('LOCATION', '')),
                    area_sqft=decimal_val(row.get('AREA_SQFT')),
                    floors=entero(row.get('FLOORS')),
                    year_built=entero(row.get('YEAR_BUILT')),
                    price_usd=money(row.get('PRICE_USD', 0)),
                    market_value_usd=money(row.get('MARKET_VALUE_USD', 0)),
                    occupancy_rate=decimal_val(row.get('OCCUPANCY_RATE')),
                    project_status=safe_str(row.get('PROJECT_STATUS', '')),
                    green_certified=booleano(row.get('GREEN_CERTIFIED', 'N')),
                    smart_building=booleano(row.get('SMART_BUILDING', 'N')),
                    zoning_code=safe_str(row.get('ZONING_CODE', '')),
                    available=booleano(row.get('AVAILABLE', 'N')),
                    description=safe_str(row.get('DESCRIPTION', '')),
                )
                propiedades.append(p)
            except Exception as e:
                errores += 1
                if errores <= 5:
                    self.stdout.write(self.style.WARNING(f'  Fila {i + 2} ignorada: {e}'))

        total = len(propiedades)
        batch_size = 100
        cargados = 0

        for i in range(0, total, batch_size):
            lote = propiedades[i:i + batch_size]
            Property.objects.bulk_create(lote, ignore_conflicts=True)
            cargados += len(lote)
            self.stdout.write(f'  {cargados}/{total} registros...')

        self.stdout.write(self.style.SUCCESS(
            f'\nOK: {cargados} propiedades cargadas. {errores} filas con error.'
        ))
