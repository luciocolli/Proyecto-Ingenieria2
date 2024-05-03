from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

from .forms import CreateNewUser

def register(request):
    
    if request.method == 'GET':
        return render(request, 'register.html', {
            'form': CreateNewUser()
        })
    else:
        #usuario = User.objects.get(id=1)
        #usuario.delete()
        User.objects.create(
            dni = request.POST['dni'],
            surname = request.POST['surname'],
            name = request.POST['name'],
            mail = request.POST['mail'],
            date = request.POST['date'],
            password = request.POST['password']
        )
        return redirect('login')
