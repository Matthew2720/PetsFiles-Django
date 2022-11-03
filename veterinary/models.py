from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelos MER.
class Veterinary(models.Model):
    nameVeterinary = models.CharField(max_length=50,blank=False,null=False)
    cityVeterinary = models.CharField(max_length=50,blank=True,null=True)
    nit = models.CharField(max_length=50,blank=False,null=False)
    email = models.EmailField()
    password = models.CharField(max_length=50, default='admin')

    def __str__(self):
        return self.nameVeterinary
    
#UserModel
class User(AbstractUser):
    direccion = models.CharField(max_length=50,blank=False, null= False)
    veterinary = models.ForeignKey(Veterinary, on_delete=models.PROTECT,null=True,blank=True)
    
    def set_veterinary(self,id):
        self.veterinary = id

#EndUserModel
    
class Client(models.Model):
    veterinary = models.ForeignKey(Veterinary, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=False,null=False)
    last_name = models.CharField(max_length=50,blank=False,null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=15,blank=True,null=True)
    mobil = models.CharField(max_length=15,blank=False,null=False)
    
    def __str__(self):
        return self.name
    
class Pet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    namePet = models.CharField(max_length=30,blank=False,null=False)
    species = models.CharField(max_length=30,blank=True,null=True)
    age = models.CharField(max_length=3 , blank=False, null = False)
    
    def __str__(self):
        return self.namePet

