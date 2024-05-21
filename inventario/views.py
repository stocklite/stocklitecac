from django.shortcuts import render


def index(request):
    return render(request, 'inventario/index.html')

def alta_producto(request):
    return render(request, 'inventario/alta_producto.html')