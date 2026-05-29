import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from apps.manor.models import Empleado


class Command(BaseCommand):
    help = 'Carga empleados de Wayne Manor RRHH desde empleados.csv'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='apps/manor/data/empleados.csv')
        parser.add_argument('--clear', action='store_true', help='Borra registros existentes antes de cargar')

    def handle(self, *args, **options):
        if options['clear']:
            count = Empleado.objects.count()
            Empleado.objects.all().delete()
            self.stdout.write(f'  Borrados {count} registros existentes.')

        def fecha(val):
            v = str(val).strip()
            if not v:
                return None
            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y'):
                try:
                    return datetime.strptime(v, fmt).date()
                except ValueError:
                    continue
            return None

        def dinero(val):
            try:
                return Decimal(str(val).replace('$', '').replace(',', '').strip() or '0')
            except InvalidOperation:
                return Decimal('0')

        registros = []
        errores = 0

        with open(options['file'], encoding='utf-8-sig') as f:
            next(f)  # fila metadata
            reader = csv.DictReader(f, delimiter=';')
            for i, row in enumerate(reader):
                if not row.get('EMPLOYEE_ID', '').strip():
                    continue
                try:
                    registros.append(Empleado(
                        employee_id      = row['EMPLOYEE_ID'].strip(),
                        nombre           = row.get('NOMBRE', '').strip(),
                        apellido         = row.get('APELLIDO', '').strip(),
                        cargo            = row.get('CARGO', '').strip(),
                        nivel_rbac       = row.get('NIVEL_RBAC', 'usuario').strip(),
                        division         = row.get('DIVISION', 'manor').strip(),
                        departamento     = row.get('DEPARTAMENTO', '').strip(),
                        email            = row.get('EMAIL', '').strip(),
                        fecha_ingreso    = fecha(row.get('FECHA_INGRESO')),
                        fecha_nacimiento = fecha(row.get('FECHA_NACIMIENTO')),
                        salario_anual    = dinero(row.get('SALARIO_ANUAL', 0)),
                        estado           = row.get('ESTADO', 'activo').strip(),
                        tipo_contrato    = row.get('TIPO_CONTRATO', 'full_time').strip(),
                        ubicacion        = row.get('UBICACION', '').strip(),
                        formacion        = row.get('FORMACION', '').strip(),
                        anos_experiencia = int(row.get('ANOS_EXPERIENCIA', 0) or 0),
                        genero           = row.get('GENERO', 'N').strip(),
                    ))
                except Exception as e:
                    errores += 1
                    if errores <= 5:
                        self.stdout.write(self.style.WARNING(f'  Fila {i + 3} ignorada: {e}'))

        total = len(registros)
        Empleado.objects.bulk_create(registros, ignore_conflicts=True)
        self.stdout.write(f'  {total}/{total} registros...')
        self.stdout.write(self.style.SUCCESS(
            f'\nOK: {total} empleados cargados. {errores} filas con error.'
        ))
