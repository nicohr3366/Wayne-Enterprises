import csv
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.core.management.base import BaseCommand
from apps.core.models import DefenseContract


class Command(BaseCommand):
    help = 'Carga contratos de defensa desde contratos.csv'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='apps/core/data/contratos.csv')
        parser.add_argument('--clear', action='store_true', help='Borra registros existentes antes de cargar')

    def handle(self, *args, **options):
        csv_file = options['file']

        if options['clear']:
            count = DefenseContract.objects.count()
            DefenseContract.objects.all().delete()
            self.stdout.write(f'  Borrados {count} registros existentes.')

        def money(val):
            try:
                return Decimal(str(val).replace('$', '').replace(',', '').strip() or '0')
            except InvalidOperation:
                return Decimal('0')

        def fecha(val):
            v = str(val).strip()
            if not v:
                return None
            for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'):
                try:
                    return datetime.strptime(v, fmt).date()
                except ValueError:
                    continue
            return None

        def booleano(val):
            return str(val).strip().upper() in ('Y', 'TRUE', '1', 'YES', 'SI', 'SÍ')

        contratos = []
        errores = 0

        with open(csv_file, encoding='utf-8-sig') as f:
            # Las primeras 2 filas son metadata, la fila 3 son los headers
            next(f)
            next(f)
            reader = csv.DictReader(f, delimiter=';')

            for i, row in enumerate(reader):
                # Ignorar filas vacías al final del archivo
                if not row.get('CONTRACT ID', '').strip():
                    continue
                try:
                    c = DefenseContract(
                        contract_id=row['CONTRACT ID'].strip(),
                        contract_number=row.get('CONTRACT NUMBER', '').strip(),
                        uei_number=row.get('UEI NUMBER', '').strip(),
                        cage_code=row.get('CAGE CODE', '').strip(),
                        fpds_transaction_id=row.get('FPDS TRANSACTION ID', '').strip(),
                        agency=row.get('AGENCY', '').strip(),
                        contractor_name=row.get('CONTRACTOR NAME', '').strip(),
                        obligated_amount_usd=money(row.get('OBLIGATED AMOUNT USD', 0)),
                        contract_ceiling_usd=money(row.get('CONTRACT CEILING USD', 0)),
                        modification_amount_usd=money(row.get('MODIFICATION AMOUNT USD', 0)),
                        etl_source_system=row.get('ETL SOURCE SYSTEM', '').strip(),
                        xml_schema_version=row.get('XML SCHEMA VERSION', '').strip(),
                        data_feed_format=row.get('DATA FEED FORMAT', '').strip(),
                        security_classification=row.get('SECURITY CLASSIFICATION', '').strip(),
                        naics_code=row.get('NAICS CODE', '').strip(),
                        naics_description=row.get('NAICS DESCRIPTION', '').strip(),
                        psc_code=row.get('PSC CODE', '').strip(),
                        cyber_compliance_level=row.get('CYBER COMPLIANCE LEVEL', '').strip(),
                        award_date=fecha(row.get('AWARD DATE')),
                        start_date=fecha(row.get('PERIOD OF PERFORMANCE START')),
                        end_date=fecha(row.get('PERIOD OF PERFORMANCE END')),
                        fiscal_year=int(row['FISCAL YEAR']) if str(row.get('FISCAL YEAR', '')).isdigit() else None,
                        performance_status=row.get('PERFORMANCE STATUS', '').strip(),
                        small_business=booleano(row.get('SMALL BUSINESS FLAG', 'N')),
                        veteran_owned=booleano(row.get('VETERAN OWNED FLAG', 'N')),
                        women_owned=booleano(row.get('WOMEN OWNED FLAG', 'N')),
                        hubzone=booleano(row.get('HUBZONE FLAG', 'N')),
                        place_of_performance_state=row.get('PERFORMANCE STATE', '').strip(),
                    )
                    contratos.append(c)
                except Exception as e:
                    errores += 1
                    if errores <= 5:
                        self.stdout.write(self.style.WARNING(f'  Fila {i + 4} ignorada: {e}'))

        total = len(contratos)
        batch_size = 500
        cargados = 0

        for i in range(0, total, batch_size):
            lote = contratos[i:i + batch_size]
            DefenseContract.objects.bulk_create(lote, ignore_conflicts=True)
            cargados += len(lote)
            self.stdout.write(f'  {cargados}/{total} registros...')

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ {cargados} contratos cargados. {errores} filas con error.'
        ))
