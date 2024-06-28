from django.shortcuts import render, redirect, get_object_or_404
from .forms import AltaProductoForm, SucursalesForm, PedidosForm, ItemPedidoFormset, BuscarTransferenciasForm, ItemPedidoForm
from django.contrib import messages
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from .models import Producto, Sucursales, ItemPedido, Pedidos
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from .forms import BusquedaForm, BuscarPedidosForm
from .forms import inlineformset_factory
from django.core.exceptions import ValidationError




@login_required
def index(request):
    username = request.user.username
    mensaje_de_bienvenida = f"Bienvenido, {username}"
    contexto = {
        'mensaje_bienvenida': mensaje_de_bienvenida
    }
    return render(request, 'inventario/index.html', contexto)


@login_required(login_url='login')
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


@login_required(login_url='login')
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

'''class PedidoCreateView(CreateView):
    model = Pedidos
    form_class = PedidosForm
    template_name = 'inventario/crear_pedido.html'
    success_url = reverse_lazy('listado_pedidos')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ItemPedidoFormset(self.request.POST, self.request.FILES)
        else:
            data['formset'] = ItemPedidoFormset()
        data['sucursales'] = Sucursales.objects.all()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        sucursal_id = self.request.POST.get('sucursal')
        tipo_de_operacion = form.cleaned_data['tipo_de_operacion']

        if formset.is_valid():
            if tipo_de_operacion == 'egresos':
                for item in formset:
                    if item.cleaned_data:
                        producto = item.cleaned_data.get('producto')
                        cantidad = item.cleaned_data.get('cantidad')
                        if producto and producto.cantidad < cantidad:
                            messages.error(self.request, f"No hay suficiente stock de {producto.nombre}")
                            return self.form_invalid(form)

            self.object = form.save(commit=False)
            if tipo_de_operacion == 'egresos' and not sucursal_id:
                messages.error(self.request, 'Debe seleccionar una sucursal para la operación de egresos.')
                return self.form_invalid(form)

            if tipo_de_operacion == 'egresos':
                self.object.sucursal = Sucursales.objects.get(id=sucursal_id)

            self.object.save()
            formset.instance = self.object
            formset.save()

            for item in formset:
                if item.cleaned_data:
                    producto = item.cleaned_data.get('producto')
                    cantidad = item.cleaned_data.get('cantidad')
                    if producto and cantidad:
                        if tipo_de_operacion == 'ingresos':
                            producto.cantidad += cantidad
                        elif tipo_de_operacion == 'egresos':
                            producto.cantidad -= cantidad
                        producto.save()

            messages.success(self.request, 'El pedido se registró correctamente')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)'''



@login_required(login_url='login')
def registro_pedido(request):
    if request.method == 'POST':
        pedido_form = PedidosForm(request.POST)
        formset = ItemPedidoFormset(request.POST, request.FILES)
        sucursal_id = request.POST.get('sucursal')

        if pedido_form.is_valid() and formset.is_valid():
            tipo_de_operacion = pedido_form.cleaned_data['tipo_de_operacion']

            # Validar existencia de stock para egresos antes de guardar el pedido
            if tipo_de_operacion == 'egresos':
                for item in formset:
                    if item.cleaned_data:  # Asegurarse de que el formulario no esté vacío
                        producto = item.cleaned_data.get('producto')
                        cantidad = item.cleaned_data.get('cantidad')
                        if producto and producto.cantidad < cantidad:
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

            for item in formset:
                if item.cleaned_data:  # Asegurarse de que el formulario no esté vacío
                    producto = item.cleaned_data.get('producto')
                    cantidad = item.cleaned_data.get('cantidad')
                    if producto and cantidad:
                        print(f"Producto: {producto.nombre}, Cantidad: {cantidad}")
                        if tipo_de_operacion == 'ingresos':
                            producto.cantidad += cantidad
                        elif tipo_de_operacion == 'egresos':
                            producto.cantidad -= cantidad
                        producto.save()
                        print(f"Nuevo stock de {producto.nombre}: {producto.cantidad}")

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

class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    context_object_name = 'productos'
    template_name = 'inventario/listado_productos.html'
    login_url = 'login' 
    
    def get_queryset(self):
        queryset = super().get_queryset()
        form = BusquedaForm(self.request.GET)
        if form.is_valid():
            termino_busqueda = form.cleaned_data['termino_busqueda']
            queryset = queryset.filter(nombre__icontains=termino_busqueda)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BusquedaForm(self.request.GET)
        return context
    

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

class SucursalListView(LoginRequiredMixin, ListView):
    model = Sucursales
    context_object_name = 'sucursales'
    template_name = 'inventario/listado_sucursales.html'
    login_url = 'login' 


class SucursalDeleteView(DeleteView):
    model = Sucursales
    template_name = 'inventario/borrar_sucursal.html'
    success_url = reverse_lazy('listado_sucursales')

class SucursalUpdateView(UpdateView):
    model = Sucursales
    template_name = 'inventario/editar_sucursal.html'
    fields = ['nombre_sucursal', 'direccion', 'telefono', 'email', 'encargado']
    success_url = reverse_lazy('listado_sucursales')

class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedidos
    context_object_name = 'pedidos'
    template_name = 'inventario/listado_pedidos.html'
    login_url = 'login'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        form = BuscarPedidosForm(self.request.GET)
        if form.is_valid():
            termino_busqueda = form.cleaned_data['termino_busqueda']
            if termino_busqueda:
                queryset = queryset.filter(sucursal__nombre_sucursal__icontains=termino_busqueda) | queryset.filter(tipo_de_operacion__icontains=termino_busqueda)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BuscarPedidosForm(self.request.GET)
        return context
    
class PedidoDeleteView(DeleteView):
    model = Pedidos
    template_name = 'inventario/borrar_pedido.html'
    success_url = reverse_lazy('inventario/listado_pedidos.html')


'''
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedidos, pk=pedido_id)
    if request.method == 'POST':
        form = PedidosForm(request.POST, instance=pedido)
        formset = ItemPedidoFormset(request.POST, instance=pedido)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('listado_pedidos')
    else:
        form = PedidosForm(instance=pedido)
        formset = ItemPedidoFormset(instance=pedido)
    
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'inventario/editar_pedido.html', context)'''

class PedidoUpdateView(UpdateView):
    model = Pedidos
    form_class = PedidosForm
    template_name = 'inventario/editar_pedido.html'
    success_url = reverse_lazy('listado_pedidos')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ItemPedidoFormset(self.request.POST, instance=self.object)
        else:
            data['formset'] = ItemPedidoFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
@login_required(login_url='login')
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