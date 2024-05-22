from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar_producto/', views.alta_producto, name='alta_producto'),
    path('agregar_proveedor/', views.alta_proveedores, name='alta_proveedores' )
]