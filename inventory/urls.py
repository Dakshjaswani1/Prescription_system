from django.urls import path
from . import views

urlpatterns = [
    path('', views.medicine_list, name='medicine_list'),
    path('add/', views.medicine_create, name='medicine_create'),
    path('<int:pk>/', views.medicine_detail, name='medicine_detail'),
]
