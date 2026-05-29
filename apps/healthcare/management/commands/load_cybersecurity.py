import pandas as pd
from django.core.management.base import BaseCommand
from apps.healthcare.models import CyberSecurityRecord


class Command(BaseCommand):
    help = 'Carga datos de ciberseguridad desde CSV (pandas)'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='apps/healthcare/data/cybersecurity.csv')
        parser.add_argument('--clear', action='store_true', help='Borra registros existentes antes de cargar')

    def handle(self, *args, **options):
        csv_file = options['file']

        if options['clear']:
            count = CyberSecurityRecord.objects.count()
            CyberSecurityRecord.objects.all().delete()
            self.stdout.write(f'  Borrados {count} registros existentes.')

        def safe_str(val):
            return str(val).strip() if pd.notna(val) else ''

        try:
            df = pd.read_csv(csv_file, encoding='utf-8-sig')
            self.stdout.write(f'  Archivo cargado: {len(df)} filas')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontro: {csv_file}'))
            return

        registros = []
        errores = 0

        for i, row in df.iterrows():
            try:
                registros.append(
                    CyberSecurityRecord(
                        incident_id=safe_str(row.get('ID_Evento', '')),
                        threat_type=safe_str(row.get('Tipo_Evento', '')),
                        severity=safe_str(row.get('Severidad', '')),
                        affected_system=safe_str(row.get('Sistema_Afectado', '')),
                        status=safe_str(row.get('Estado', '')),
                    )
                )
            except Exception as e:
                errores += 1
                if errores <= 5:
                    self.stdout.write(self.style.WARNING(f'  Fila {i + 2} ignorada: {e}'))

        CyberSecurityRecord.objects.bulk_create(
            registros,
            ignore_conflicts=True
        )

        self.stdout.write(self.style.SUCCESS(
            f'OK: {len(registros)} registros cargados. {errores} filas con error.'
        ))
