from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from landing.models import Publication
from django.db import IntegrityError
from .forms import CreateNewUser, CreatelogIn #, EditProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from datetime import datetime
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
            # ACORDARME DE SACAR ESTO
            #---------------------------------------------------------------------------------------
            if back.enviarMail(user.mail, 'Sesión iniciada', f'Hola {user.name}, se detectó un inicio de sesión.'):
                print('Mail se envio bien') 
            else:
                print("Mail sale mal")
            #---------------------------------------------------------------------------------------
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
def view_profile(request, id):
    if request.method == 'GET':
        print(type(request.user.rol))
        user = get_object_or_404(User, id=id)
        print(type(user.id))
        return render(request, 'view_profile.html', {
            'name': user.name,
            'surname': user.surname,
            'email': user.mail,
            'calification': back.calculate_califications(),
            'id': user.id
        })

@login_required
def view_posts(request, id):
    if request.method == 'GET':
        posts = Publication.objects.filter(user = id) # user en Publication es el campo que contiene solo el id del dueño de la publicacion
        owner = User.objects.get(id = id)  # busco al dueño
        
        if not posts:
            msg = 'El usuario no tiene publicaciones disponibles'
        else:
            msg = None

        return render(request, 'user-posts.html',{
            'name': owner.name,
            'posts' : posts,
            'msg': msg
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
def view_asignar_colaborador(request):
  
    if request.method == 'GET':
        logged_user = request.user
        users = User.objects.exclude(id=logged_user.id)

        return render(request, 'asignar_colaborador.html',{
            'users': users
        })

@login_required
def asignar_colaborador(request):
    
    if request.method == 'POST':
        dni = request.POST.get('dni')
        user = get_object_or_404(User, dni=dni)
        user.rol = 2  # Cambia al rol deseado
        user.save()
    return redirect('view_asignar_colaborador')

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

        edad = back.get_years(datetime.strptime(date, '%Y-%m-%d').date())
        if edad < 18:
            messages.error(request, 'Debes ser mayor de 18 años para modificar tu perfil.')
            return redirect('editar-perfil')
        
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
