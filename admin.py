from django.contrib import admin
from .models import Empleado, Departamento


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'cargo', 'departamento', 'estado', 'fecha_ingreso')
    list_filter = ('estado', 'departamento')
    search_fields = ('nombre', 'apellido', 'cargo')
