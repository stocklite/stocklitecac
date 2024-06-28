from django import forms
from django.core.exceptions import ValidationError
from .models import Producto, Sucursales, Pedidos, ItemPedido
from django.forms import inlineformset_factory

class AltaProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'costo', 'venta', 'cantidad', 'proveedor']

    def clean_nombre(self):# estos es para validacion de campo individual del nombre
        nombre = self.cleaned_data['nombre']
        if not all(char.isalpha() or char.isspace() for char in nombre):
            raise ValidationError('El nombre del Producto solo debe contener letras')
        return nombre
    def clean_codigo(self):# estos es para validacion de campo individual del codigo
        codigo = self.cleaned_data.get('codigo')
        if codigo and Producto.objects.filter(codigo=codigo).exists():
            raise ValidationError('EL codigo ya se encuentra registrado')
        return codigo


    def clean(self):# esto es para una validacion general del formulario Alta Producto
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        proveedor = cleaned_data.get('proveedor')
        codigo = cleaned_data.get('codigo')

        if Producto.objects.filter(nombre=nombre, proveedor=proveedor).exists():
            raise ValidationError('El producto con este nombre y proveedor ya se encuentran registrados')
        if Producto.objects.filter(codigo=codigo).exists():
            raise ValidationError('EL codigo ya se encuentra registrado')
        if cleaned_data.get('codigo') and cleaned_data['codigo'] < 1000000000:
            raise ValidationError('EL campo del codigo de producto debe contener al menos 10 numeros, si el codigo no tiene los 10 numeros completar con "0" al inicio del codigo')
        return cleaned_data
        

class SucursalesForm(forms.ModelForm):
    class Meta:
        model = Sucursales
        fields = ['nombre_sucursal', 'direccion', 'telefono', 'email', 'encargado']
   



class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = '__all__'

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ('producto', 'cantidad', 'precio', 'total')

ItemPedidoFormset = inlineformset_factory(
    Pedidos,
    ItemPedido,
    form=ItemPedidoForm,
    extra=1,
    can_delete=True
)

class BuscarTransferenciasForm(forms.Form):
    sucursal = forms.ModelChoiceField(queryset=Sucursales.objects.all(), required=True, label="Sucursal")


class BusquedaForm(forms.Form):
    termino_busqueda = forms.CharField(label='Buscar')

class BuscarPedidosForm(forms.Form):
    termino_busqueda = forms.CharField(label='Buscar pedidos', max_length=100, required=False)