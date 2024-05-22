from django.shortcuts import render, redirect, get_object_or_404
from .models import Publication, Offer
from django.db import IntegrityError
from users.models import User
from .forms import CreateNewPublication, EditPublicationForm
from django.contrib.auth.decorators import login_required, admin_required
from users.views import editarPerfil #Sin uso era para ver si se solucionaba
from django.contrib import messages
from users import backend as back
# Create your views here.


def index(request):
    return render(request, 'base.html')


def about(request):
    return render(request, 'about.html')


@login_required
def createPublication(request):
    if request.method == 'GET':
        return render(request, 'createPublication.html', {
            'form': CreateNewPublication()
        })
    else:
        # publication = Publication.objects.get(id=1)
        # publication.delete()

        form = CreateNewPublication(request.POST)

        if form.is_valid():

            new_title = request.POST['title']
            post_owner = request.user
            exists_title = Publication.objects.filter(user= post_owner, title= new_title).exists()
            cleaned_date = form.cleaned_data['date'] # The date is cleaned in case it's empty
            # This conditional checks if the user that is creating the post already has one with the same title
            if exists_title:
                # In this case, the user is notified
                form.add_error(
                        'title', 'Ya posees una publicación con este título'
                        )
                return render(request, 'createPublication.html', {'form': form})
            else:
                Publication.objects.create(
                    title=request.POST['title'],
                    description=request.POST['description'],
                    category=request.POST['category'],
                    state=request.POST['state'],
                    date=cleaned_date,
                    user=request.user,  # esto retorna al usuario que se encuentra navegando en el sistema
                    file= request.POST['file']
                )
                return redirect('all-posts')
        else:
            return render(request, 'createPublication.html', {'form': form})

@login_required
def editPublication(request, publication_id):

    def hasOffers(user):
        return Offer.objects.exists(user)
    
    publication = get_object_or_404(Publication, id=publication_id)
    mensaje = None
    
    # Verifica si el usuario logueado es el creador de la publicación
    if publication.user != request.user and not hasOffers(publication.user):
        mensaje = "No tienes permiso para editar esta publicación."

    if request.method == 'POST':
        form = EditPublicationForm(request.POST, instance=publication)
        if form.is_valid():
            new_title = form.cleaned_data['title'] 
            encontre = Publication.objects.filter(user = publication.user, title = new_title).exclude(id=publication.id).exists()
            if not encontre:
                form.save()
                mensaje = "Se han guardado los cambios."
            else:
                mensaje = "Ya posees una publicacion con este titulo"
    else:
        form = EditPublicationForm(instance=publication)
    return render(request, 'editPublication.html', {
        'form': form,
        'mensaje': mensaje
    })



@login_required
def show_all_posts(request):
    if request.method == 'GET':
        logged_user = request.user
        # Tomo las publicaciones de todos los usuarios menos del que se encuentra logueado
        posts = Publication.objects.exclude(user=logged_user.id)
        
        if not posts:
            message = 'No hay publicaciones disponibles'
        else:
            message = None

        return render(request, 'show-all-posts.html', {
            'nombre_usuario' : logged_user.name,
            'posts': posts,
            'msg': message
        })


@login_required
def show_my_profile(request):

    if request.method == 'GET':
        logged_user = request.user
        # logged_user = get_object_or_404(User.objects.filter(id=2))
        dni = logged_user.dni
        return render(request, 'miperfil.html', {
            'dni' : dni,
            'name' : logged_user.name,
            'surname' : logged_user.surname,
            'mail' : logged_user.mail,
            'date' : logged_user.date
        })

@login_required  #Para ver Publicacion en la pagina principal
def show_post(request, id):
    if request.method == 'GET':
        post = get_object_or_404(Publication, id=id)
        print(post.file)
        return render(request, 'view-post.html', {
            'title': post.title,
            'description': post.description,
            'category': post.category,
            'state': post.state,
            'date': post.date,
            'user': post.user,
            'file' : post.file
        })
    

def show_my_posts(request): # Para ver listado de mis publicaciones
    if request.method == 'GET':
        logged_user = request.user
        myPosts = Publication.objects.filter(user=logged_user)

        if not myPosts:
            message = 'No hay publicaciones disponibles'
        else:
            message = None

        return render(request, 'my-posts.html',{
            'myPosts' : myPosts,
            'msg': message
        })

@login_required
def show_my_post(request, id):  # Para ver una publicacion propia
    if request.method == 'GET':
        post = get_object_or_404(Publication, id=id)
        return render(request, 'view-my-post.html', {
            'title': post.title,
            'description': post.description,
            'category': post.category,
            'state': post.state,
            'date': post.date,
            'file': post.file
        })
    
@admin_required
def admin_posts(request):   
    if request.method == 'GET':
        posts = Publication.objects.all()
        return render(request, 'admin-show-posts.html', {
            'posts': posts
        })
    else:
        posts = Publication.objects.all()
        return render(request, 'admin-show-posts.html', {
            'posts': posts
        })

@admin_required
def delete_post(request, id):
    if request.method == 'POST':
        publicacion = get_object_or_404(Publication, id=id)
        back.enviarMail(publicacion.user.mail,'Publicación eliminada', f'Hola {publicacion.user.name}, tu publicación a sido eliminada porque era indebida')
        publicacion.delete()
        posts = Publication.objects.all()
        return render(request, 'admin-show-posts.html', {
            'posts': posts
        })