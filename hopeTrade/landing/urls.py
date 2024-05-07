from django.urls import path
from . import views

urlpatterns = [
    path('all-posts/', views.show_all_posts, name= 'all-posts'),
    path('view-post/<int:id>', views.show_post, name= 'post'),
    path('crear_publicacion/', views.createPublication, name= 'crearPublicaciones'),
    path('about/', views.about, name= 'about'),
    path('miperfil/', views.show_my_profile, name='miperfil'),
]