from django.db import models

# Create your models here.

class User(models.Model):
    dni = models.IntegerField(unique=True)    
    name = models.CharField(max_length=100)              
    surname = models.CharField(max_length=100)           
    mail = models.EmailField(max_length=100,unique=True)                
    date = models.DateField()                            
    password = models.CharField(max_length=100)     
    rol = models.CharField(max_length=1, default=1)
                
