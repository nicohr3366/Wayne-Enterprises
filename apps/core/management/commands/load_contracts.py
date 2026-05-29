import pandas as pd
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.core.management.base import BaseCommand
from apps.core.models import DefenseContract


class Command(BaseCommand):
    help = 'Carga contratos de defensa desde contratos.csv (pandas)'

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
            if pd.isna(val):
                return None
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
            if pd.isna(val):
                return False
            return str(val).strip().upper() in ('Y', 'TRUE', '1', 'YES', 'SI', 'SI')

        def safe_str(val):
            return str(val).strip() if pd.notna(val) else ''

        try:
            df = pd.read_csv(csv_file, sep=';', skiprows=2, encoding='utf-8-sig')
            self.stdout.write(f'  Archivo cargado: {len(df)} filas')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontro: {csv_file}'))
            return

        contratos = []
        errores = 0

        for i, row in df.iterrows():
            if not safe_str(row.get('CONTRACT ID', '')):
                continue
            try:
                c = DefenseContract(
                    contract_id=safe_str(row.get('CONTRACT ID', '')),
                    contract_number=safe_str(row.get('CONTRACT NUMBER', '')),
                    uei_number=safe_str(row.get('UEI NUMBER', '')),
                    cage_code=safe_str(row.get('CAGE CODE', '')),
                    fpds_transaction_id=safe_str(row.get('FPDS TRANSACTION ID', '')),
                    agency=safe_str(row.get('AGENCY', '')),
                    contractor_name=safe_str(row.get('CONTRACTOR NAME', '')),
                    obligated_amount_usd=money(row.get('OBLIGATED AMOUNT USD', 0)),
                    contract_ceiling_usd=money(row.get('CONTRACT CEILING USD', 0)),
                    modification_amount_usd=money(row.get('MODIFICATION AMOUNT USD', 0)),
                    etl_source_system=safe_str(row.get('ETL SOURCE SYSTEM', '')),
                    xml_schema_version=safe_str(row.get('XML SCHEMA VERSION', '')),
                    data_feed_format=safe_str(row.get('DATA FEED FORMAT', '')),
                    security_classification=safe_str(row.get('SECURITY CLASSIFICATION', '')),
                    naics_code=safe_str(row.get('NAICS CODE', '')),
                    naics_description=safe_str(row.get('NAICS DESCRIPTION', '')),
                    psc_code=safe_str(row.get('PSC CODE', '')),
                    cyber_compliance_level=safe_str(row.get('CYBER COMPLIANCE LEVEL', '')),
                    award_date=fecha(row.get('AWARD DATE')),
                    start_date=fecha(row.get('PERIOD OF PERFORMANCE START')),
                    end_date=fecha(row.get('PERIOD OF PERFORMANCE END')),
                    fiscal_year=int(row['FISCAL YEAR']) if pd.notna(row.get('FISCAL YEAR')) and str(row.get('FISCAL YEAR', '')).replace('.0', '').isdigit() else None,
                    performance_status=safe_str(row.get('PERFORMANCE STATUS', '')),
                    small_business=booleano(row.get('SMALL BUSINESS FLAG', 'N')),
                    veteran_owned=booleano(row.get('VETERAN OWNED FLAG', 'N')),
                    women_owned=booleano(row.get('WOMEN OWNED FLAG', 'N')),
                    hubzone=booleano(row.get('HUBZONE FLAG', 'N')),
                    place_of_performance_state=safe_str(row.get('PERFORMANCE STATE', '')),
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
            f'\nOK: {cargados} contratos cargados. {errores} filas con error.'
        ))
