from django.shortcuts import render
from .models import Empleado, Departamento


def home(request):
    total_empleados = Empleado.objects.filter(estado='activo').count()
    total_departamentos = Departamento.objects.count()
    empleados_recientes = Empleado.objects.select_related('departamento').order_by('-fecha_ingreso')[:6]
    departamentos = Departamento.objects.all()

    context = {
        'total_empleados': total_empleados,
        'total_departamentos': total_departamentos,
        'empleados_recientes': empleados_recientes,
        'departamentos': departamentos,
    }
    return render(request, 'manor/home.html', context)
