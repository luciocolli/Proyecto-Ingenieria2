from django.urls import path
from . import views

urlpatterns = [
    path('principal/', views.index, name= 'principal'),
    path('crear_publicacion/', views.createPublication, name= 'crearPublicaciones'),
    path('about/', views.about, name= 'about'),
    path('miperfil/', views.show_my_profile, name='miperfil')
]