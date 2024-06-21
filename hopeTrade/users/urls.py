from django.urls import path
from . import views
from landing import views as langin_views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name= 'home'),
    path('login/', views.login_view, name= 'login'),
    path('register/', views.register, name= 'register'),
    path('asignar-colaborador/', views.view_asignar_colaborador, name='view_asignar_colaborador'), # Esta ruta solo muestra los usuarios y su info
    path('cambiar-rol/', views.asignar_colaborador, name='change-rol'), # ejecuta la accion de cambiar el rol en la bd y redirige a la url de arriba, los datos ya van a estar modificados
    path('editar-perfil/', views.editarPerfil, name='editar-perfil'),
    #path('all-posts/', langin_views.show_all_posts, name= 'all-posts'),
    path('all-posts/', langin_views.show_all_posts, name= 'all-posts'),
    path('view-profile/<int:id>', views.view_profile, name= 'profile'),
    path('user-posts/<int:id>', views.view_posts, name= 'user-posts'),
    path('user-exchages/', views.view_exchanges, name= 'user-exchanges'),
    path('user-ratings/', views.view_ratings, name= 'user-ratings'),
    path('logout/', views.user_logout, name='logout'),
    path('add-card/', views.add_card, name='add-card'),
    path('delete-card/', views.delete_card, name='delete-card'),
] 

