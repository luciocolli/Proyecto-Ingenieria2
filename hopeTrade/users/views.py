from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.db import IntegrityError
from .forms import CreateNewUser, CreatelogIn #, EditProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required, admin_required
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
                rol = user.rol
                if int(rol) == 3:
                    return redirect('admin-posts')
                else:
                    return redirect('all-posts')
            else:
                form.add_error(
                    'dni', 'DNI y/o contraseña incorrectos'
                )
    return render(request, 'login.html',{'form': form} )

@login_required
def view_profile(request, id):  # puse el id=2 porque se supone que me tiene que llegar como parametro el que fue seleccionado, pero no hicimos el ver publiciones
    if request.method == 'GET':
        print(type(request.user.rol))
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

@admin_required
def asignar_colaborador(request):
        
    mensaje = None

    if request.method == 'POST':
        dni = request.POST.get('dni')
        try:
            usuario = User.objects.get(dni=dni)
        except User.DoesNotExist:
            mensaje = f"No se encuentra el usuario con el DNI {dni}"
        else:
            usuario.rol = 2
            usuario.save()
            mensaje = "Colaborador asignado correctamente"

    return render(request, 'asignar_colaborador.html', {'mensaje': mensaje})

@login_required
def editarPerfil(request):
    user = request.user

    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        date = request.POST.get('date')
        mail = request.POST.get('mail')
        password_actual = request.POST.get('password_actual')
        nueva_password = request.POST.get('nueva_password')


        
        if (password_actual and not nueva_password) or (nueva_password and not password_actual):
            messages.error(request, 'Debe proporcionar tanto la contraseña actual como la nueva contraseña para realizar cambios en la contraseña.')
            return redirect('editar-perfil')

        # Verificar si el usuario quiere cambiar la contraseña
        if password_actual and nueva_password:
            # Comprobar si la contraseña actual coincide con la del usuario
            if not user.password == password_actual:
                messages.error(request, 'La contraseña actual es incorrecta.')
                return redirect('editar-perfil')
            # Actualizar la contraseña
            user.password = nueva_password
        
        # Actualizar los otros campos del perfil
        user.name = name
        user.surname = surname
        user.date = date
        user.mail = mail
        user.save()

        messages.success(request, 'Perfil actualizado con éxito.')
        return redirect('editar-perfil')

    return render(request, 'editar-perfil.html', {'user': user})
