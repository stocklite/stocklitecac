from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar_producto/', views.alta_producto, name='alta_producto'),
    path('agregar_pedido/', views.alta_pedido, name='alta_pedido' ),
    path('hacer_pedido/', views.pedidos_cliente, name='pedidos_cliente' )
]