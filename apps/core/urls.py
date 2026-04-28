from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contratos/', views.contracts_dashboard, name='contracts_dashboard'),
    path('contratos/lista/', views.contracts_list, name='contracts_list'),
    path('contratos/<int:pk>/', views.contract_detail, name='contract_detail'),
    path('contratos/exportar/', views.export_csv, name='contracts_export'),
]
