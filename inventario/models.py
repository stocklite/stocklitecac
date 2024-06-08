from django.db import models

class Producto(models.Model):# este es el modelo para alta producto
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    venta = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    proveedor = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
class Sucursales(models.Model):#este es el modelo para las sucursales
    nombre_sucursal =models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.IntegerField()
    email= models.EmailField()
    encargado = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_sucursal
    
class Pedidos(models.Model):
    TIPO_OPERACION_CHOICES = [
        ('ingresos', 'Ingresos'),
        ('egresos', 'Egresos')
    ]
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_de_operacion = models.CharField(max_length=8, choices=TIPO_OPERACION_CHOICES, default='ingresos')

    def __str__(self):
        return f"{self.sucursal} - {self.fecha} - {self.tipo_de_operacion}"
    


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto} - {self.cantidad}"
