from django.shortcuts import render, redirect
from .forms import AltaProductoForm, SucursalesForm, PedidosForm, ItemPedidoFormset, BuscarTransferenciasForm
from django.contrib import messages
from django.views.generic import ListView, UpdateView, DeleteView
from .models import Producto, Sucursales, ItemPedido, Pedidos
from django.urls import reverse_lazy
from django.db.models import Sum

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
            messages.success(request, 'La sucursal se agrego correctamente')
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
        sucursal_id = request.POST.get('sucursal')

        if pedido_form.is_valid() and formset.is_valid():
            tipo_de_operacion = pedido_form.cleaned_data['tipo_de_operacion']
            
            # Validar existencia de stock para egresos antes de guardar el pedido
            if tipo_de_operacion == 'egresos':
                for item in formset.cleaned_data:
                    producto = item['producto']
                    cantidad = item['cantidad']
                    if producto.cantidad < cantidad:
                        messages.error(request, f"No hay suficiente stock de {producto.nombre}")
                        return redirect('registro_pedido')
            
            # Guardar el pedido y actualizar la cantidad de productos
            pedido = pedido_form.save(commit=False)
            if tipo_de_operacion == 'egresos' and not sucursal_id:
                messages.error(request, 'Debe seleccionar una sucursal para la operación de egresos.')
                return redirect('registro_pedido')

            if tipo_de_operacion == 'egresos':
                pedido.sucursal = Sucursales.objects.get(id=sucursal_id)

            pedido.save()
            formset.instance = pedido
            formset.save()

            for item in formset.cleaned_data:
                producto = item['producto']
                cantidad = item['cantidad']
                if tipo_de_operacion == 'ingresos':
                    producto.cantidad += cantidad
                elif tipo_de_operacion == 'egresos':
                    producto.cantidad -= cantidad
                producto.save()

            messages.success(request, 'El pedido se registró correctamente')
            return redirect('index')
    else:
        pedido_form = PedidosForm()
        formset = ItemPedidoFormset()

    contexto = {
        'pedido_form': pedido_form,
        'formset': formset,
        'sucursales': Sucursales.objects.all()
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

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'inventario/borrar_producto.html'
    success_url = reverse_lazy('listado_productos')

class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'inventario/editar_producto.html'
    fields = ['codigo', 'nombre', 'costo', 'venta', 'cantidad', 'proveedor']
    success_url = reverse_lazy('listado_productos')

class SucursalListView(ListView):
    model = Sucursales
    context_object_name = 'sucursales'
    template_name = 'inventario/listado_sucursales.html'
    ordering = ['nombre_sucursal']

class SucursalDeleteView(DeleteView):
    model = Sucursales
    template_name = 'inventario/borrar_sucursal.html'
    success_url = reverse_lazy('listado_sucursales')

class SucursalUpdateView(UpdateView):
    model = Sucursales
    template_name = 'inventario/editar_sucursal.html'
    fields = ['nombre_sucursal', 'direccion', 'telefono', 'email', 'encargado']
    success_url = reverse_lazy('listado_sucursales')


def buscar_transferencias(request):
    form = BuscarTransferenciasForm(request.GET or None)
    transferencias = None

    if form.is_valid():
        sucursal = form.cleaned_data['sucursal']
        transferencias = (
            ItemPedido.objects
            .filter(pedido__sucursal=sucursal, pedido__tipo_de_operacion='egresos')
            .values('producto__nombre')
            .annotate(total_cantidad=Sum('cantidad'))
            .order_by('producto__nombre')
        )
    contexto = {
        'form': form,
        'transferencias': transferencias,
    }
    return render(request, 'inventario/buscar_transferencias.html', contexto)