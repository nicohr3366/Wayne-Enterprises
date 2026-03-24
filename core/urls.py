from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('api/division/<int:pk>/', views.division_detail, name='division_detail'),
    path('api/executive/<int:pk>/', views.executive_detail, name='executive_detail'),
    path('api/gadget/<int:pk>/', views.gadget_detail, name='gadget_detail'),
    path('api/villain/<int:pk>/', views.villain_detail, name='villain_detail'),
]
