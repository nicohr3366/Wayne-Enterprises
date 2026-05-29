from django.urls import path
from . import views

app_name = 'capital'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('acciones/', views.stocks_list, name='stocks_list'),
    path('exportar/', views.export_csv, name='export_csv'),
]
