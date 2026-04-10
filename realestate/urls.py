from django.urls import path
from . import views

app_name = 'realestate'

urlpatterns = [
    path('', views.home, name='home'),
]
