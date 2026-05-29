import pandas as pd
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.core.management.base import BaseCommand
from apps.capital.models import StockRecord


class Command(BaseCommand):
    help = 'Carga registros de bolsa WayneTech desde stocks.csv (pandas)'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='apps/capital/data/stocks.csv')
        parser.add_argument('--clear', action='store_true', help='Borra registros existentes antes de cargar')

    def handle(self, *args, **options):
        csv_file = options['file']

        if options['clear']:
            count = StockRecord.objects.count()
            StockRecord.objects.all().delete()
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

        def safe_decimal_null(val):
            if pd.isna(val):
                return None
            try:
                return Decimal(str(val).replace(',', '').strip())
            except InvalidOperation:
                return None

        def safe_bigint(val, default=0):
            if pd.isna(val):
                return default
            try:
                return int(float(val))
            except (ValueError, TypeError):
                return default

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
            df = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig')
            self.stdout.write(f'  Archivo cargado: {len(df)} filas')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontro: {csv_file}'))
            return

        registros = []
        errores = 0

        for i, row in df.iterrows():
            if not safe_str(row.get('TICKER', '')):
                continue
            try:
                rec = StockRecord(
                    ticker=safe_str(row.get('TICKER', '')),
                    company_name=safe_str(row.get('COMPANY', '')),
                    division=safe_str(row.get('DIVISION', '')),
                    date=safe_date(row.get('DATE')),
                    open_price=safe_decimal(row.get('OPEN', 0)),
                    high_price=safe_decimal(row.get('HIGH', 0)),
                    low_price=safe_decimal(row.get('LOW', 0)),
                    close_price=safe_decimal(row.get('CLOSE', 0)),
                    adj_close=safe_decimal(row.get('ADJ_CLOSE', 0)),
                    volume=safe_bigint(row.get('VOLUME', 0)),
                    market_cap_usd=safe_decimal(row.get('MARKET_CAP_USD', 0)),
                    pe_ratio=safe_decimal_null(row.get('PE_RATIO')),
                    dividend_yield=safe_decimal_null(row.get('DIVIDEND_YIELD')),
                    sector=safe_str(row.get('SECTOR', '')),
                    exchange=safe_str(row.get('EXCHANGE', '')),
                )
                registros.append(rec)
            except Exception as e:
                errores += 1
                if errores <= 5:
                    self.stdout.write(self.style.WARNING(f'  Fila {i + 2} ignorada: {e}'))

        total = len(registros)
        batch_size = 500
        cargados = 0

        for i in range(0, total, batch_size):
            lote = registros[i:i + batch_size]
            StockRecord.objects.bulk_create(lote, ignore_conflicts=True)
            cargados += len(lote)
            self.stdout.write(f'  {cargados}/{total} registros...')

        self.stdout.write(self.style.SUCCESS(
            f'\nOK: {cargados} registros de bolsa cargados. {errores} filas con error.'
        ))
