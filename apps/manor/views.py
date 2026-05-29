import json
import csv
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count, Avg, Sum, Q
from django.core.paginator import Paginator
from .models import Empleado


@login_required
def home(request):
    return render(request, 'manor/home.html')


@login_required
def dashboard(request):
    total = Empleado.objects.count()

    if total == 0:
        return render(request, 'manor/dashboard.html', {'sin_datos': True})

    activos    = Empleado.objects.filter(estado='activo').count()
    avg_sal    = Empleado.objects.aggregate(avg=Avg('salario_anual'))['avg'] or 0
    avg_exp    = Empleado.objects.aggregate(avg=Avg('anos_experiencia'))['avg'] or 0

    def qs_to_json(qs, label_key, value_key):
        return json.dumps([
            {label_key: str(r[label_key] or ''), value_key: float(r[value_key] or 0)}
            for r in qs
        ])

    by_division   = Empleado.objects.values('division').annotate(count=Count('id')).order_by('-count')
    by_rol        = Empleado.objects.values('nivel_rbac').annotate(count=Count('id')).order_by('-count')
    by_depto      = Empleado.objects.values('departamento').annotate(count=Count('id')).order_by('-count')[:12]
    by_estado     = Empleado.objects.values('estado').annotate(count=Count('id')).order_by('-count')
    by_contrato   = Empleado.objects.values('tipo_contrato').annotate(count=Count('id')).order_by('-count')
    by_genero     = Empleado.objects.values('genero').annotate(count=Count('id')).order_by('-count')
    sal_por_rol   = Empleado.objects.values('nivel_rbac').annotate(avg=Avg('salario_anual')).order_by('-avg')
    by_formacion  = Empleado.objects.values('formacion').annotate(count=Count('id')).order_by('-count')[:8]

    context = {
        'total':         total,
        'activos':       activos,
        'avg_sal_k':     round(float(avg_sal) / 1000, 1),
        'avg_exp':       round(float(avg_exp), 1),

        'by_division_json':  qs_to_json(by_division,  'division',     'count'),
        'by_rol_json':       qs_to_json(by_rol,        'nivel_rbac',   'count'),
        'by_depto_json':     qs_to_json(by_depto,      'departamento', 'count'),
        'by_estado_json':    qs_to_json(by_estado,     'estado',       'count'),
        'by_contrato_json':  qs_to_json(by_contrato,   'tipo_contrato','count'),
        'by_genero_json':    qs_to_json(by_genero,     'genero',       'count'),
        'sal_por_rol_json':  qs_to_json(sal_por_rol,   'nivel_rbac',   'avg'),
        'by_formacion_json': qs_to_json(by_formacion,  'formacion',    'count'),
    }
    return render(request, 'manor/dashboard.html', context)


@login_required
def empleados_list(request):
    qs = Empleado.objects.all()

    division  = request.GET.get('division', '')
    rol       = request.GET.get('rol', '')
    depto     = request.GET.get('depto', '')
    estado    = request.GET.get('estado', '')
    search    = request.GET.get('search', '')

    if division:
        qs = qs.filter(division=division)
    if rol:
        qs = qs.filter(nivel_rbac=rol)
    if depto:
        qs = qs.filter(departamento=depto)
    if estado:
        qs = qs.filter(estado=estado)
    if search:
        qs = qs.filter(
            Q(nombre__icontains=search) |
            Q(apellido__icontains=search) |
            Q(cargo__icontains=search) |
            Q(email__icontains=search)
        )

    total_filtrado = qs.count()
    paginator = Paginator(qs, 25)
    page_obj  = paginator.get_page(request.GET.get('page', 1))

    divisiones   = Empleado.objects.values_list('division',     flat=True).distinct().order_by('division')
    roles        = Empleado.objects.values_list('nivel_rbac',   flat=True).distinct().order_by('nivel_rbac')
    deptos       = Empleado.objects.values_list('departamento', flat=True).distinct().order_by('departamento')
    estados      = Empleado.objects.values_list('estado',       flat=True).distinct().order_by('estado')

    context = {
        'page_obj':         page_obj,
        'total_filtrado':   total_filtrado,
        'divisiones':       divisiones,
        'roles':            roles,
        'deptos':           deptos,
        'estados':          estados,
        'current_division': division,
        'current_rol':      rol,
        'current_depto':    depto,
        'current_estado':   estado,
        'current_search':   search,
    }
    return render(request, 'manor/list.html', context)


@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="rrhh_wayne_manor.csv"'
    response.write('﻿')

    qs = Empleado.objects.all()
    if request.GET.get('division'):
        qs = qs.filter(division=request.GET['division'])
    if request.GET.get('rol'):
        qs = qs.filter(nivel_rbac=request.GET['rol'])
    if request.GET.get('estado'):
        qs = qs.filter(estado=request.GET['estado'])

    writer = csv.writer(response)
    writer.writerow([
        'EMPLOYEE_ID', 'NOMBRE', 'APELLIDO', 'CARGO', 'NIVEL_RBAC',
        'DIVISION', 'DEPARTAMENTO', 'EMAIL', 'FECHA_INGRESO',
        'SALARIO_ANUAL', 'ESTADO', 'TIPO_CONTRATO', 'UBICACION',
        'FORMACION', 'ANOS_EXPERIENCIA', 'GENERO',
    ])
    for e in qs:
        writer.writerow([
            e.employee_id, e.nombre, e.apellido, e.cargo, e.nivel_rbac,
            e.division, e.departamento, e.email, e.fecha_ingreso,
            e.salario_anual, e.estado, e.tipo_contrato, e.ubicacion,
            e.formacion, e.anos_experiencia, e.genero,
        ])
    return response
