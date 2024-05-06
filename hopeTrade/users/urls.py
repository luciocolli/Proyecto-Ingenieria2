from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'home'),
    path('login/', views.login, name= 'login'),
    path('register/', views.register, name= 'register'),
    path('asignar-colaborador/', views.asignar_colaborador, name='asignar_colaborador')
]