from django.urls import path
from . import views

urlpatterns = [
    path('all-posts/', views.show_all_posts, name= 'all-posts'),
    path('view-post/<int:id>/', views.show_post, name= 'post'),
    path('crear_publicacion/', views.createPublication, name= 'crearPublicaciones'),
    path('editPublication/<int:publication_id>', views.editPublication, name='edit-publication'),
    path('about/', views.about, name= 'about'),
    path('miperfil/', views.show_my_profile, name='miperfil'),
    path('my-posts/', views.show_my_posts, name='my-posts'),
    path('my-post/<int:id>', views.show_my_post, name= 'view-my-post'),
    path('admin-show-posts', views.admin_posts, name= 'admin-posts'),
    path('delete_post/<int:id>', views.delete_post, name= 'delete_post'),
    path('make_offer/<int:post_id>/', views.offer_post, name= 'make_offer'),
    path('delete_publication/<int:id>', views.user_delete_post, name='user_delete_post'),
    path('my-offers/<int:id>', views.show_my_offers, name='show_my_offers'), # las ofertas que recibo
    path('offers/',views.show_offers, name = 'offers'), # mis ofertas
    path('decline-offer<int:id>', views.decline_offer, name='decline_offer'),
    path('accept-offer<int:id>', views.accept_offer, name='accept_offer'),
    path('cancel-offer<int:id>', views.cancel_offer, name='cancel_offer'),
    path('delete-users/', views.delete_all_users, name='delete-users'),
    path('donation', views.donation, name='donation'),
    path('cash_register', views.cashRegister, name='cash_register'),
    path('article_register', views.article_register, name='article_register'),
    path('show_articles', views.show_articles, name='show_articles'),
    path('make_coment/', views.makeComent, name='make_coment'),
    path('view_coments/', views.viewComents, name='view_coments'),
    path('make_response/<int:id>', views.makeResponse, name='make_response'),
    path('show_intercambios_dia', views.show_intercambios_today, name='intercambios_today'),
    path('confirm_intercambio/<int:id>/', views.confirm_intercambio, name='confirm_intercambio'),
    path('decline_intercambio/<int:id>', views.decline_intercambio, name='decline_intercambio'),
    path('calificar-intercambio/<int:id>', views.calificar_intercambio, name='calificar-intercambio'),
]