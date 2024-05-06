from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'home'),
    path('login/', views.login_view, name= 'login'),
    path('register/', views.register, name= 'register'),
    path('holanda/', views.login_view, name='holanda')
    
    ]