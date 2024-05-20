from django.shortcuts import render
from django.http import HttpResponse
import datetime

def index(request):
    context = {
        'nombre' : 'Walter',
        'fecha_hora' : datetime.datetime.now()
    }


    return render(request, "inventario/index.html", context)

def create(request):
    return HttpResponse("Ingrese un producto")

def update(request):
    return HttpResponse("Actualice el producto")

def delete(request):
    return HttpResponse("Quiere eliminar este producto?")
