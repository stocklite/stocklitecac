from django import forms
from django.core.exceptions import ValidationError

class AltaProductoForms(forms.Form):
    codigo = forms.IntegerField(label='Codigo de Producto', required=True)
    nombre = forms.CharField(label='Nombre de Producto', required=True)
    costo = forms.DecimalField(label='Precio de Costo', required=True)
    venta = forms.DecimalField(label='Precio de venta', required=True)
    cantidad = forms.IntegerField(label='Cantidad', required=True)
    proveedor = forms.CharField(label='Proveedor', required=True)

   
    def clean_nombre(self):
        if not self.cleaned_data["nombre"].isalpha():#el tema es ke aca con el atributo isalpha no se puede poner espacios.. a revisar! ke otra opcion podemos ponerle
            raise ValidationError('El nombre del Producto solo debe contener letras')
        return self.cleaned_data['nombre']
    

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        proveedor = cleaned_data.get('proveedor')
        if nombre == 'fideos' and proveedor == 'molinos':# cuando tengamos la base de datos esto cambiara por valores reales de la tabla de la DB.
            raise ValidationError('EL producto ya esta registrado')
        
        if self.cleaned_data["codigo"] < 10000000000:
            raise ValidationError('EL campo del codigo de producto debe contener al menos 10 numeros, si el codigo no tiene los 10 numeros completar con "0" al inicio del codigo' )