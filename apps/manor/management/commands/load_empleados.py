import pandas as pd
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from apps.manor.models import Empleado


class Command(BaseCommand):
    help = 'Carga empleados de Wayne Manor RRHH desde empleados.csv (pandas)'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='apps/manor/data/empleados.csv')
        parser.add_argument('--clear', action='store_true', help='Borra registros existentes antes de cargar')

    def handle(self, *args, **options):
        csv_file = options['file']

        if options['clear']:
            count = Empleado.objects.count()
            Empleado.objects.all().delete()
            self.stdout.write(f'  Borrados {count} registros existentes.')

        def fecha(val):
            if pd.isna(val):
                return None
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
            if pd.isna(val):
                return Decimal('0')
            try:
                return Decimal(str(val).replace('$', '').replace(',', '').strip() or '0')
            except InvalidOperation:
                return Decimal('0')

        def safe_str(val, default=''):
            return str(val).strip() if pd.notna(val) else default

        def safe_int(val, default=0):
            if pd.isna(val):
                return default
            try:
                return int(float(val))
            except (ValueError, TypeError):
                return default

        try:
            df = pd.read_csv(csv_file, sep=';', skiprows=1, encoding='utf-8-sig')
            self.stdout.write(f'  Archivo cargado: {len(df)} filas')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontro: {csv_file}'))
            return

        registros = []
        errores = 0

        for i, row in df.iterrows():
            if not safe_str(row.get('EMPLOYEE_ID', '')):
                continue
            try:
                registros.append(Empleado(
                    employee_id=safe_str(row.get('EMPLOYEE_ID', '')),
                    nombre=safe_str(row.get('NOMBRE', '')),
                    apellido=safe_str(row.get('APELLIDO', '')),
                    cargo=safe_str(row.get('CARGO', '')),
                    nivel_rbac=safe_str(row.get('NIVEL_RBAC', 'usuario')),
                    division=safe_str(row.get('DIVISION', 'manor')),
                    departamento=safe_str(row.get('DEPARTAMENTO', '')),
                    email=safe_str(row.get('EMAIL', '')),
                    fecha_ingreso=fecha(row.get('FECHA_INGRESO')),
                    fecha_nacimiento=fecha(row.get('FECHA_NACIMIENTO')),
                    salario_anual=dinero(row.get('SALARIO_ANUAL', 0)),
                    estado=safe_str(row.get('ESTADO', 'activo')),
                    tipo_contrato=safe_str(row.get('TIPO_CONTRATO', 'full_time')),
                    ubicacion=safe_str(row.get('UBICACION', '')),
                    formacion=safe_str(row.get('FORMACION', '')),
                    anos_experiencia=safe_int(row.get('ANOS_EXPERIENCIA', 0)),
                    genero=safe_str(row.get('GENERO', 'N')),
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
