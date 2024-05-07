from django.shortcuts import render, redirect, get_object_or_404
from .models import Publication
from users.models import User
from .forms import CreateNewPublication
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def mostrarMiPerfil(request):
    return render(request, 'miperfil.html')

@login_required
def createPublication(request):
    if request.method == 'GET':
        return render(request, 'createPublication.html', {
            'form': CreateNewPublication()
        })
    else:
        #publication = Publication.objects.get(id=1)
        #publication.delete()
        Publication.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            category = request.POST['category'],
            state = request.POST['state'],
            date = request.POST['date'],
            user = request.user # esto retorna al usuario que se encuentra navegando en el sistema
        )
        return redirect('show-all-posts.html')
    
@login_required
def show_all_posts(request):
    if request.method == 'GET':
        logged_user = request.user
        # Tomo las publicaciones de todos los usuarios menos del que se encuentra logueado
        posts = Publication.objects.exclude(user= logged_user.id)
        return render(request, 'show-all-posts.html',{
            'posts' : posts
        })
    

@login_required
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