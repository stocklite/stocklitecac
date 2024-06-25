from django.urls import path, include
from . import views
from .views import ProductoListView, ProductoDeleteView, ProductoUpdateView, SucursalListView, SucursalDeleteView, SucursalUpdateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='inventario/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('index', views.index, name='index'),    
    path('agregar_producto/', views.alta_producto, name='alta_producto'),
    path('listado_productos/', ProductoListView.as_view(), name='listado_productos'),
    path('producto/<int:pk>/edit/', ProductoUpdateView.as_view(), name='producto-edit'),
    path('producto/<int:pk>/delete/', ProductoDeleteView.as_view(), name='producto-delete'),
    path('agregar_sucursal/', views.alta_sucursales, name='alta_sucursales'),
    path('listado_sucursales/', SucursalListView.as_view(), name='listado_sucursales'),
    path('sucursal/<int:pk>/edit/', SucursalUpdateView.as_view(), name='sucursal-edit'),
    path('sucursal/<int:pk>/delete/', SucursalDeleteView.as_view(), name='sucursal-delete'),
    path('hacer_pedido/', views.registro_pedido, name='registro_pedido'),
    path('buscar_transferencias/', views.buscar_transferencias, name='buscar_transferencias'),
    
    
]