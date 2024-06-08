from django.urls import path
from . import views
from .views import ProductoListView, listado_productos

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar_producto/', views.alta_producto, name='alta_producto'),
    path('agregar_sucursal/', views.alta_sucursales, name='alta_sucursales'),
    path('hacer_pedido/', views.registro_pedido, name='registro_pedido'),
    path('listado_productos/', listado_productos, name='listado_productos')
]