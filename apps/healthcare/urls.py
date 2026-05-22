from django.urls import path
from . import views

app_name = 'healthcare'

urlpatterns = [
    path('', views.home, name='home'),
    path('cybersecurity/', views.cybersecurity_dashboard, name='cybersecurity_dashboard'),
    path('cybersecurity/exportar/', views.export_csv, name='export_csv'),
]
