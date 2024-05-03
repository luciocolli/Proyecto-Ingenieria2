from django.shortcuts import render, redirect
from .models import Publication
from .forms import CreateNewPublication

# Create your views here.

def index(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def mostrarMiPerfil(request):
    return render(request, 'miperfil.html')

def createPublication(request):
    if request.method == 'GET':
        return render(request, 'createPublication.html', {
            'form': CreateNewPublication()
        })
    else:
        #publication = Publication.objects.get(id=1)
        #publication.delete()
        Publication.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            category = request.POST['category'],
            state = request.POST['state'],
            date = request.POST['date'],
        )
        return redirect('principal')