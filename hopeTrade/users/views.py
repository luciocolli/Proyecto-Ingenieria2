from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User
from django.db import  IntegrityError
from django.contrib import messages
from datetime import datetime

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

def asignar_colaborador(request):
    mensaje = None

    if request.method == 'POST':
        dni = request.POST.get('dni')
        try:
            usuario = User.objects.get(dni=dni)
        except User.DoesNotExist:
            mensaje = f"No se encuentra el usuario con el DNI {dni}"
        else:
            if request.user.is_authenticated:  # Verificar si el usuario está autenticado
                if request.user.rol == '3':
                    usuario.rol = '2'
                    usuario.save()
                    mensaje = "Colaborador asignado correctamente"
                else:
                    mensaje = "No tienes los permisos para realizar esta acción"
            else:
                mensaje = "Debes iniciar sesión para realizar esta acción"

    return render(request, 'asignar_colaborador.html', {'mensaje': mensaje})