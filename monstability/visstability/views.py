from django.shortcuts import render
from .models import Nodes

def index(request):
    context = {}    #словарь для передачи контента в шаблон HTML
    return render(request, 'index.html', context)

def diagram(request):
    context = {}
    return render(request, 'diagram.html', context)

def model(request):
    context = {}
    return render(request, 'model.html', context)

def tablestead(request):
    nodes = Nodes.objects.all()
    context = {'nodes': nodes}
    return render(request, 'tablestead.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)