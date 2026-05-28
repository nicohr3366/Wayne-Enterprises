from django.urls import path
from . import views

app_name = 'ventures'

urlpatterns = [
    path('', views.home, name='home'),
    path('satellites/dashboard/', views.satellites_dashboard, name='dashboard'),
    path('satellites/', views.satellites_list, name='satellites_list'),
    path('satellites/<str:log_id>/', views.satellite_detail, name='satellite_detail'),
    path('satellites/export/csv/', views.export_csv, name='export_csv'),
]
