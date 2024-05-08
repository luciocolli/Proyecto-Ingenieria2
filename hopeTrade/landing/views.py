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
        return redirect('all-posts')
    
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
def show_my_profile(request):
    
    if request.method == 'GET':
        logged_user = request.user
        #logged_user = get_object_or_404(User.objects.filter(id=2))
        dni = logged_user.dni
        return render(request, 'miperfil.html', {
            'dni' : dni,
            'name' : logged_user.name,
            'surname' : logged_user.surname,
            'mail' : logged_user.mail,
            'date' : logged_user.date,
            'user': logged_user
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
    
def show_my_posts(request):
    if request.method == 'GET':
        logged_user = request.user
        myPosts = Publication.objects.filter(user=logged_user)
        return render(request, 'my-posts.html',{
            'myPosts' : myPosts
        })
    
@login_required
def show_my_post(request, id):
    if request.method == 'GET':
        post = get_object_or_404(Publication, id=id)
        return render(request, 'view-my-post.html', {
            'title': post.title,
            'description': post.description,
            'category': post.category,
            'state': post.state,
            'date': post.date,
        })