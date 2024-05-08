from django.urls import path
from . import views
from landing import views as langin_views

urlpatterns = [
    path('', views.index, name= 'home'),
    path('login/', views.login_view, name= 'login'),
    path('register/', views.register, name= 'register'),
    path('asignar-colaborador/', views.asignar_colaborador, name='asignar_colaborador'),
    #path('all-posts/', langin_views.show_all_posts, name= 'all-posts'),
    path('view-profile/<int:id>', views.view_profile, name= 'profile'),
    path('user-posts/', views.view_posts, name= 'user-posts'),
    path('user-exchages/', views.view_exchanges, name= 'user-exchanges'),
    path('user-ratings/', views.view_ratings, name= 'user-ratings'),
    path('logout/', views.user_logout, name='logout'),
] 

