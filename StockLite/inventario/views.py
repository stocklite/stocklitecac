from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "index.html")

def create(request):
    return HttpResponse("Ingrese un producto")

def update(request):
    return HttpResponse("Actualice el producto")

def delete(request):
    return HttpResponse("Quiere eliminar este producto?")
