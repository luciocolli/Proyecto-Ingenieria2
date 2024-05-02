from django.db import models

# Create your models here.

class User(models.Model):
    dni = models.CharField(max_length=8, unique=True)    
    name = models.CharField(max_length=100)              
    surname = models.CharField(max_length=100)           
    mail = models.EmailField(unique=True)                
    date = models.DateField()                            
    password = models.CharField(max_length=100)     
    rol = models.CharField(max_length=1, default=1)
                
