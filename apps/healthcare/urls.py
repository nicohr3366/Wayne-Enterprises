from django.urls import path
from . import views

app_name = 'healthcare'

urlpatterns = [
    path('', views.home, name='home'),
]
