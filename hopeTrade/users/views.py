from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.db import IntegrityError
from .forms import CreateNewUser, CreatelogIn
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required
from . import backend as back

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):

    if request.method == 'GET':
        return render(request, 'register.html', {
            'form': CreateNewUser()
        })
    else:
        # usuario = User.objects.get(id=1)
        # usuario.delete()

        form = CreateNewUser(request.POST)

        if form.is_valid():
            # Calculate the years of the user
            date = form.cleaned_data['date']
            edad = back.get_years(date)

            # If he´s 18 or older
            if edad >= 18:
                try:
                    User.objects.create(
                        dni=request.POST['dni'],
                        surname=request.POST['surname'],
                        name=request.POST['name'],
                        mail=request.POST['mail'],
                        date=request.POST['date'],
                        password=request.POST['password']
                    )
                    return redirect('login')
                except IntegrityError:
                    form.add_error(
                        'dni', 'El dni ingresado ya se encuentra cargado en el sistema')
            else:
                form.add_error(
                    'date', 'Debes ser mayor de 18 años para poder registrarte')
        return render(request, 'register.html', {'form': form})


def login_view(request):

    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': CreatelogIn()
        })
    else:

        form = CreatelogIn(request.POST)
        if form.is_valid():
            dni = request.POST['dni']
            password = request.POST['password']
            user = back.authenticate(request, dni=dni, password=password)
            if user is not None:
                login(request, user)
                return redirect('all-posts')
            else:
                form.add_error(
                    'dni', 'DNI y/o contraseña incorrectos'
                )
        return render(request, 'login.html',{'form': form} )

@login_required
def view_profile(request, id):  # puse el id=2 porque se supone que me tiene que llegar como parametro el que fue seleccionado, pero no hicimos el ver publiciones
    if request.method == 'GET':
        user = get_object_or_404(User, id=id)
        return render(request, 'view_profile.html', {
            'name': user.name,
            'surname': user.surname,
            'email': user.mail,
            'calification': back.calculate_califications()
        })

@login_required
def view_posts(request):
    if request.method == 'GET':
        return render(request, 'user-posts.html',{
            'auth' : request.user.is_authenticated
        })

@login_required
def view_exchanges(request):
    if request.method == 'GET':
        return render(request, 'user-exchanges.html')

@login_required
def view_ratings(request):
    if request.method == 'GET':
        return render(request, 'user-ratings.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')