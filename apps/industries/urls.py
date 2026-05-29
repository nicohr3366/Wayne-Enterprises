from django.urls import path
from . import views

app_name = 'industries'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('grid/', views.grid_list, name='grid_list'),
    path('exportar/', views.export_csv, name='export_csv'),
]
