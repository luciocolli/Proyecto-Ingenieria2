from django.db import models
from users.models import User  # me traigo la clase User desde la carpeta users

# Create your models here.

class Publication(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    date = models.DateField()  # Vencimiento
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    file = models.CharField(max_length=100, default= 'Sin_foto.png')
    