from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelos MER.
class Veterinary(models.Model):
    nameVeterinary = models.CharField(max_length=50,blank=False,null=False,unique=True)
    cityVeterinary = models.CharField(max_length=50,blank=True,null=True)
    nit = models.CharField(max_length=50,blank=False,null=False,unique=True)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=60,blank=True, null= True)
    password = models.CharField(max_length=50, default='admin')

    def __str__(self):
        return self.nameVeterinary
    
#UserModel
class User(AbstractUser):
    direccion = models.CharField(max_length=50,blank=True, null= True)
    veterinary = models.ForeignKey(Veterinary, on_delete=models.PROTECT,null=True,blank=True)
    
    def set_veterinary(self,id):
        self.veterinary = id

#EndUserModel
    
class Client(models.Model):
    veterinary = models.ForeignKey(Veterinary, on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=50,blank=False,null=False)
    last_name = models.CharField(max_length=50,blank=False,null=False)
    identification = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    
    def __str__(self):
        return self.name
    
class Pet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    namePet = models.CharField(max_length=30,blank=False,null=False)
    species = models.CharField(max_length=30,blank=True,null=True)
    age = models.CharField(max_length=3 , blank=False, null = False)
    
    def __str__(self):
        return self.namePet

