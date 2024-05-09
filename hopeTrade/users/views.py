from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.db import IntegrityError
from .forms import CreateNewUser, CreatelogIn, EditProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

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


@login_required
def editarPerfil(request):
    user = request.user
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            # Si se ha proporcionado una nueva contraseña
            password_actual = form.cleaned_data.get('password_actual')
            nueva_password = form.cleaned_data.get('nueva_password')

            if password_actual and nueva_password:
                if not user.password == password_actual:
                    messages.error(request, 'La contraseña actual es incorrecta.')
                    return redirect('editar-perfil')
                user.password = nueva_password

            # Mover el guardado del formulario aquí para asegurar que la verificación de la contraseña actual se realiza antes de guardar
            form.save()
            messages.success(request, 'Perfil actualizado con éxito.')
            return redirect('editar-perfil')
    else:
        form = EditProfileForm(instance=user)
    
    return render(request, 'editar-perfil.html', {'form': form})
