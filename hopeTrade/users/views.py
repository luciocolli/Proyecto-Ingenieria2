from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User
from django.db import  IntegrityError
from django.contrib import messages
from datetime import datetime
from .forms import CreateNewUser, CreatelogIn
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model

# Create your views here.

def index(request):
    return render(request, 'index.html')



def login_view(request):

    if request.method == 'GET':
        return render(request, 'login.html', {
            'form' : CreatelogIn()
        })
    else:
        if request.method == 'POST':
            dni = request.POST['dni']
            password = request.POST['password']
            user = authenticate(request,dni = dni , password = password)
            if user is not None:
                login(request, user)
                return redirect('holanda')
            else:
                return redirect('register')
        else:
            return render(request, 'login.html')



def register(request):
    
    if request.method == 'GET':
        return render(request, 'register.html', {
            'form': CreateNewUser()
        })
    else:
        #usuario = User.objects.get(id=1)
        #usuario.delete()

        form = CreateNewUser(request.POST)
        
        if form.is_valid():
            # Calculate the years of the user
            date = form.cleaned_data['date']
            edad = get_years(date)
            
            # If he´s 18 or older 
            if edad >= 18:
                try: 
                    User.objects.create(
                        dni = request.POST['dni'],
                        surname = request.POST['surname'],
                        name = request.POST['name'],
                        mail = request.POST['mail'],
                        date = request.POST['date'],
                        password = request.POST['password']
                    )
                    return redirect('login')
                except IntegrityError:
                    form.add_error('dni', 'El dni ingresado ya se encuentra cargado en el sistema')
            else:
                form.add_error('date', 'Debes ser mayor de 18 años para poder registrarte')
        return render(request, 'register.html', {'form': form})
    

def get_years(date):
    actual_date = datetime.now().date()
    edad = actual_date.year - date.year - ((actual_date.month, actual_date.day) < (date.month, date.day))
    return edad

def authenticate(request, dni=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            usuario = User.objects.get(dni=dni)
            if usuario.password == password:
                return usuario
        except User.DoesNotExist:
            return None
