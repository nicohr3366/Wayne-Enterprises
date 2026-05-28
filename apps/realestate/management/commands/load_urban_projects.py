import pandas as pd

from django.core.management.base import BaseCommand

from apps.realestate.models import UrbanProject


class Command(BaseCommand):

    help = 'Carga proyectos urbanos desde CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='apps/realestate/data/gotham_urban_projects.csv'
        )

    def handle(self, *args, **options):

        df = pd.read_csv(options['file'])
        print(df.columns)

        registros = []

        for _, row in df.iterrows():

            registros.append(
                UrbanProject(
                    project_id=row['ID_Proyecto'],
                    project_name=row['Nombre_Proyecto'],
                    district=row['Distrito'],
                    project_type=row['Tipo_Proyecto'],
                    status=row['Estado'],
                    priority=row['Prioridad'],
                    total_budget_musd=row['Presupuesto_Total_MUSD'],
                    executed_cost_musd=row['Costo_Ejecutado_MUSD'],
                    physical_progress_pct=row['Avance_Fisico_Pct'],
                    financial_progress_pct=row['Avance_Financiero_Pct'],
                    security_incidents=row['Incidentes_Seguridad'],
                    contractor=row['Contratista'],
                )
            )

        UrbanProject.objects.bulk_create(
            registros,
            ignore_conflicts=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'✓ {len(registros)} registros cargados.'
            )
        )