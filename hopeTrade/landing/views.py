from django.shortcuts import render, redirect, get_object_or_404
from .models import Publication
from django.db import IntegrityError
from users.models import User
from .forms import CreateNewPublication, EditPublicationForm
from django.contrib.auth.decorators import login_required
from users.views import editarPerfil #Sin uso era para ver si se solucionaba
from django.contrib import messages

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
                    date=request.POST['date'],
                    user=request.user  # esto retorna al usuario que se encuentra navegando en el sistema
                )
                return redirect('all-posts')

@login_required
def editPublication(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)

    # Verifica si el usuario logueado es el creador de la publicación
    if publication.user != request.user:
        messages.error(request, "No tienes permiso para editar esta publicación.")
        return redirect('all-posts')

    if request.method == 'POST':
        form = EditPublicationForm(request.POST, instance=publication)
        if form.is_valid():
            form.save()
            messages.success(request, "La publicación ha sido editada correctamente.")
            return redirect('all-posts')
    else:
        form = EditPublicationForm(instance=publication)

    return render(request, 'editPublication.html', {'form': form})

@login_required
def show_all_posts(request):
    if request.method == 'GET':
        logged_user = request.user
        # Tomo las publicaciones de todos los usuarios menos del que se encuentra logueado
        posts = Publication.objects.exclude(user=logged_user.id)
        return render(request, 'show-all-posts.html', {
            'posts': posts
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
        return render(request, 'view-post.html', {
            'title': post.title,
            'description': post.description,
            'category': post.category,
            'state': post.state,
            'date': post.date,
            'user': post.user
        })
    

def show_my_posts(request): # Para ver listado de mis publicaciones
    if request.method == 'GET':
        logged_user = request.user
        myPosts = Publication.objects.filter(user=logged_user)
        return render(request, 'my-posts.html',{
            'myPosts' : myPosts
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
        })
    
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
        
def delete_post(request, id):
    if request.method == 'POST':
        publicacion = get_object_or_404(Publication, id=id)
        publicacion.delete()
        posts = Publication.objects.all()
        return render(request, 'admin-show-posts.html', {
            'posts': posts
        })