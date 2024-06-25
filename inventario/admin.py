from django.contrib import admin
from .models import Pedidos, Sucursales, Producto, ItemPedido

admin.site.register(Producto)
admin.site.register(Pedidos)
admin.site.register(Sucursales)
admin.site.register(ItemPedido)

# Register your models here.
