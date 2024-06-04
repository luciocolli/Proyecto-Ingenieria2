from django.db import models
from users.models import User  # me traigo la clase User desde la carpeta users

# Create your models here.

class Publication(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    date = models.DateField(null=True, blank= True)  # Vencimiento
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    file = models.CharField(max_length=100, default= 'Sin_foto.png', blank=True)
    isHide = models.BooleanField(default = False)
    

class Offer(models.Model):
    title = models.TextField(max_length = 100, null=True)
    description = models.TextField(max_length=500)
    date = models.DateField(null=True, blank = True)
    hour = models.TimeField(null= True, blank= True)
    sede = models.CharField(max_length=200, default='LA PLATA')
    user = models.ForeignKey(User, on_delete= models.DO_NOTHING)
    post = models.ForeignKey(Publication, on_delete= models.CASCADE)

class Intercambio(models.Model):
    post = models.ForeignKey(Publication, on_delete= models.CASCADE) # de aca sacamos el dueño
    offerOwner = models.ForeignKey(User, on_delete= models.DO_NOTHING)
    date = models.DateField(null=True, blank = True)
    isDone = models.BooleanField(default = False)

class CashDonation(models.Model):
    cash = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    name = models.CharField(max_length = 100, default='Sin Nombre')
    surname = models.CharField(max_length = 100, default='Sin apellido')
    dniDonor = models.CharField(max_length = 100)

class Coment(models.Model):
    parent_id = models.ForeignKey('self', on_delete = models.CASCADE, null = True, related_name='responses')
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete =  models.CASCADE)
    text = models.CharField(max_length = 255)

    