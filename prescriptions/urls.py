from django.urls import path
from . import views

urlpatterns = [
    path('', views.prescription_list, name='prescription_list'),
    path('create/', views.prescription_create, name='prescription_create'),
    path('<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('<int:pk>/finalize/', views.prescription_finalize, name='prescription_finalize'),
    path('<int:pk>/dispense/', views.prescription_dispense, name='prescription_dispense'),
]
