from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Group, Permission


# Create your models here.
                
class User(AbstractBaseUser, PermissionsMixin):
    dni = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date = models.DateField()
    mail = models.EmailField(max_length=50,)
    password = models.CharField(max_length=128)
    rol = models.CharField(max_length=1, default=1)


    #Esto es para los many to many dijo chatgpt

    groups = models.ManyToManyField(Group, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions')


    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['name', 'surname', 'date']

    def save(self, *args, **kwargs):
        superuser = kwargs.pop('superuser', False)
        self.is_superuser = superuser
        super().save(*args, **kwargs)


class Card(models.Model):
    number = models.CharField(max_length= 18, unique= True)
    user = models.ForeignKey(User, on_delete= models.SET_NULL, related_name='cards', null= True)
    funds = models.IntegerField(default= 10000)