from django.urls import path
from . import views

app_name = 'manor'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('empleados/', views.empleados_list, name='list'),
    path('exportar/', views.export_csv, name='export'),
]
