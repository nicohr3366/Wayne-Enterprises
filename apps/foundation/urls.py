from django.urls import path
from . import views

app_name = 'foundation'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('donaciones/', views.donaciones_list, name='donaciones_list'),
    path('exportar/', views.export_csv, name='export_csv'),
]
