from django.shortcuts import render, redirect
from .forms import AltaProductoForm, SucursalesForm, PedidosForm, ItemPedidoFormset
from django.contrib import messages
from django.views.generic import ListView
from .models import Producto

def index(request):
    return render(request, 'inventario/index.html')

def alta_producto(request):
    if request.method == 'POST':
        form = AltaProductoForm(request.POST)
        if form.is_valid():
            form.save()
            print('los datos del form son:', request.POST)# este print nos muestra los datos ingresados en el formulario 
            messages.success(request, 'El producto se agrego correctamente')
            return redirect('index')  # aca dirigimos a index si los datos del form son validos u otra pagina
    else:
        form = AltaProductoForm()

    contexto = {
        'alta_producto_form': form
    }
    
    return render(request, "inventario/alta_producto.html", contexto)# redirige a la misma pagina si hay algun error

def alta_sucursales(request):
    if request.method == 'POST':
        suc_form = SucursalesForm(request.POST)
        if suc_form.is_valid():
            suc_form.save()
            messages.success(request, 'El pedido se agrego correctamente')
            return redirect('index')  # aca dirigimos a index si los datos del form son validos u otra pagina
    else:
        form = SucursalesForm()

    contexto = {
        'sucursal_form': form
    }

    return render(request, 'inventario/alta_sucursales.html', contexto)

def registro_pedido(request):
    if request.method == 'POST':
        pedido_form = PedidosForm(request.POST)
        formset = ItemPedidoFormset(request.POST, request.FILES)

        if pedido_form.is_valid() and formset.is_valid():
            pedido = pedido_form.save()
            formset.instance = pedido
            formset.save()

            tipo_de_operacion = pedido.tipo_de_operacion
            for item in formset.cleaned_data:
                producto = item['producto']
                cantidad = item['cantidad']
                if tipo_de_operacion == 'ingreso':
                    producto.cantidad += cantidad
                elif tipo_de_operacion == 'egreso':
                    producto.cantidad -= cantidad
                producto.save()

        messages.success(request, 'El pedido se registro correctamente')
        return redirect('index')
        
    else: 
        pedido_form = PedidosForm()
        formset = ItemPedidoFormset()

    contexto = {
        'pedido_form': pedido_form,
        'formset': formset,
    }
    return render(request, 'inventario/pedidos_cliente.html', contexto)


class ProductoListView(ListView):
    model = Producto
    context_object_name = 'productos'
    template_name = 'inventario/listado_productos.html'
    ordering = ['codigo']

def listado_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/listado_productos.html', {'productos': productos})