from django.urls import path
from . import views

app_name = 'tech'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('telemetria/', views.telemetry_list, name='telemetry_list'),
    path('exportar/', views.export_csv, name='export_csv'),
]
