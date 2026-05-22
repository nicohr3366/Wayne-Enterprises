from django.urls import path
from . import views

app_name = 'realestate'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('propiedades/', views.properties_list, name='list'),
    path('propiedades/<int:pk>/', views.property_detail, name='detail'),
    path('exportar/', views.export_csv, name='export'),
]
