from django.urls import path
from . import views

urlpatterns = [
    path('all-posts/', views.show_all_posts, name= 'all-posts'),
    path('view-post/<int:id>', views.show_post, name= 'post'),
    path('crear_publicacion/', views.createPublication, name= 'crearPublicaciones'),
    path('editPublication/<int:publication_id>/', views.editPublication, name='edit-publication'),
    path('about/', views.about, name= 'about'),
    path('miperfil/', views.show_my_profile, name='miperfil'),
    path('my-posts/', views.show_my_posts, name='my-posts'),
    path('my-post/<int:id>', views.show_my_post, name= 'view-my-post'),
    path('admin-show-posts', views.admin_posts, name= 'admin-posts'),
    path('delete_post<int:id>', views.delete_post, name= 'delete_post')
]