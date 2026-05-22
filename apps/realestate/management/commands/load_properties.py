import csv
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from apps.realestate.models import Property


class Command(BaseCommand):
    help = 'Carga propiedades de Gotham desde propiedades.csv'

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
            try:
                v = str(val).strip()
                return Decimal(v) if v else None
            except InvalidOperation:
                return None

        def entero(val):
            v = str(val).strip()
            return int(v) if v.isdigit() else None

        def booleano(val):
            return str(val).strip().upper() in ('Y', 'TRUE', '1', 'YES', 'SI', 'SÍ')

        propiedades = []
        errores = 0

        with open(csv_file, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for i, row in enumerate(reader):
                if not row.get('PROJECT_ID', '').strip():
                    continue
                try:
                    p = Property(
                        project_id=row['PROJECT_ID'].strip(),
                        name=row['NAME'].strip(),
                        developer=row.get('DEVELOPER', '').strip(),
                        property_type=row.get('PROPERTY_TYPE', '').strip(),
                        district=row.get('DISTRICT', '').strip(),
                        location=row.get('LOCATION', '').strip(),
                        area_sqft=decimal_val(row.get('AREA_SQFT', '')),
                        floors=entero(row.get('FLOORS', '')),
                        year_built=entero(row.get('YEAR_BUILT', '')),
                        price_usd=money(row.get('PRICE_USD', 0)),
                        market_value_usd=money(row.get('MARKET_VALUE_USD', 0)),
                        occupancy_rate=decimal_val(row.get('OCCUPANCY_RATE', '')),
                        project_status=row.get('PROJECT_STATUS', '').strip(),
                        green_certified=booleano(row.get('GREEN_CERTIFIED', 'N')),
                        smart_building=booleano(row.get('SMART_BUILDING', 'N')),
                        zoning_code=row.get('ZONING_CODE', '').strip(),
                        available=booleano(row.get('AVAILABLE', 'N')),
                        description=row.get('DESCRIPTION', '').strip(),
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
