import csv

from django.core.management.base import BaseCommand
from apps.healthcare.models import CyberSecurityRecord


class Command(BaseCommand):
    help = 'Carga datos de ciberseguridad desde CSV'

    def handle(self, *args, **kwargs):

        registros = []

        with open(
            'apps/healthcare/data/cybersecurity.csv',
            encoding='utf-8-sig'
        ) as f:

            reader = csv.DictReader(f)

            for row in reader:

                registros.append(
                    CyberSecurityRecord(
                        incident_id=row['ID_Evento'],
                        threat_type=row['Tipo_Evento'],
                        severity=row['Severidad'],
                        affected_system=row['Sistema_Afectado'],
                        status=row['Estado'],
                    )
                )

        CyberSecurityRecord.objects.bulk_create(
            registros,
            ignore_conflicts=True
            
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'✓ {len(registros)} registros cargados'
            )
        )