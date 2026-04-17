from django.urls import path
from . import views

app_name = 'industries'

urlpatterns = [
    path('', views.home, name='home'),
]
