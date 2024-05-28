from django.shortcuts import render, redirect
from .forms import AltaProductoForms, AltaPedidoForms, PedidosClienteForms
from django.contrib import messages


def index(request):
    return render(request, 'inventario/index.html')

def alta_producto(request):
    if request.method == 'POST':
        form = AltaProductoForms(request.POST)
        if form.is_valid():
            print('los datos del form son:', request.POST)# este print nos muestra los datos ingresados en el formulario 
            messages.success(request, 'El producto se agrego correctamente')
            return redirect('index')  # aca dirigimos a index si los datos del form son validos u otra pagina
    else:
        form = AltaProductoForms()

    contexto = {
        'alta_producto_form': form
    }
    
    return render(request, "inventario/alta_producto.html", contexto)# redirige a la misma pagina si hay algun error

def alta_pedido(request):
    if request.method == 'POST':
        form = AltaPedidoForms(request.POST)
        if form.is_valid():
            print('los datos del form son:', request.POST)# este print nos muestra los datos ingresados en el formulario 
            messages.success(request, 'El pedido se agrego correctamente')
            return redirect('index')  # aca dirigimos a index si los datos del form son validos u otra pagina
    else:
        form = AltaPedidoForms()

    contexto = {
        'alta_pedido_form': form
    }
    return render(request, 'inventario/alta_pedido.html', contexto)

def pedidos_cliente(request):
    if request.method == 'POST':
        form = PedidosClienteForms(request.POST)
        if form.is_valid():
            print('los datos del form son:', request.POST)# este print nos muestra los datos ingresados en el formulario 
            messages.success(request, 'El pedido se realizo correctamente')
            return redirect('index')  # aca dirigimos a index si los datos del form son validos u otra pagina
    else:
        form = PedidosClienteForms()

    contexto = {
        'pedidos_cliente_form': form
    }
    return render(request, 'inventario/pedidos_cliente.html', contexto)
