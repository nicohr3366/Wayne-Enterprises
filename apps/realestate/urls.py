from django.urls import path
from . import views

app_name = 'realestate'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('projects/', views.projects_list, name='projects_list'),
    path(
        'projects/<int:project_id>/',
        views.project_detail,
        name='project_detail'
    ),
]