from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Card
from landing.models import TransferDonation as transfer
from landing.models import Publication, Calification, Intercambio
from django.db import IntegrityError
from .forms import CreateNewUser, CreatelogIn, AddCard, TransferDonation #, EditProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from datetime import datetime
from datetime import date
from django.contrib.auth.decorators import login_required, admin_required
from . import backend as back
from django.db.models import Avg, Q
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
def view_ratings(request, id):
    if request.method == 'GET':

        #Agarro usuario del GET, y sus Calificaciones
        user = get_object_or_404(User, id=id)
        user_calificaciones = Calification.objects.filter(Q(intercambio__post__user=user) | Q(intercambio__offerOwner=user)).exclude(user=user)
        promedio = user_calificaciones.aggregate(Avg('calification'))['calification__avg']
        message = None
        if not user_calificaciones:
            message = "No posees calificaciones registradas."

        # Procesar cada calificación para convertirla en estrellas
        for calificacion in user_calificaciones:
            calificacion.calification = calificacion_con_estrellas(calificacion.calification)

        return render(request, 'user-ratings.html',{
            'msg': message,
            'user_calificaciones': user_calificaciones,
            'promedio': promedio,
            'user': user,
        })

def calificacion_con_estrellas(calificacion):
    # Mapea el número de calificación a emojis de estrellas
    estrellas = '⭐️' * int(calificacion)
    return estrellas

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

#@admin_required
def view_asignar_colaborador(request):
  
    if request.method == 'GET':
        logged_user = request.user
        users = User.objects.exclude(id=logged_user.id)

        if not users:
            message = 'No hay usuarios registrados.'
        else:
            message = None

        return render(request, 'asignar_colaborador.html',{
            'users': users,
            'msg': message
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

def add_card(request):
    
    if request.method == 'GET':
        return render(request, 'add_card.html', {
            'form': AddCard()
        })
    else:

        form = AddCard(request.POST)
        message = None

        if form.is_valid():

            card_number = form.cleaned_data['number']

            try:
                Card.objects.create(
                    number = card_number,
                    user = request.user
                )
            except IntegrityError:
                form.add_error(
                    'number', 'La tarjeta ingresada ya se encuentra en el sistema'
                )
            else:
                message = 'Tarjeta agregada con éxito'
    return render(request, 'add_card.html', {'form': form,
                                             'msg' : message})


def make_transfer_donation(request):

    def has_founds(card, form):
        if card.has_funds:
            transfer.objects.create(
                amount = form.cleaned_data['amount'],
                date = date.today(),
                card = card,
                name = request.user.name,
                surname = request.user.surname,
                dniDonor = request.user.dni
            )
            return 'Se ha realizado la transferencia correctamente'
        return 'La tarjeta ingresada no posee fondos'

    
    if request.method == 'GET':
        return render(request, 'make_transfer_donation.html', {
            'form' : TransferDonation()
        })
    else:
        form = TransferDonation(request.POST)
        message = None

        if form.is_valid():

            try:
                card_number = form.cleaned_data['number']
                card = Card.objects.filter(number= card_number, user = request.user).first()
                message = has_founds(card, form)
            except Exception as e:
                message = 'La tarjeta no se encuentra registrada en el sistema'

        return render(request, 'make_transfer_donation.html', {
                'form' : TransferDonation(),
                'msg' : message
            })


