from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime

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
    is_doctor = models.BooleanField(default=False)
    
    def set_veterinary(self,id):
        self.veterinary = id

#EndUserModel
    
class Client(models.Model):
    veterinary = models.ForeignKey(Veterinary, on_delete= models.PROTECT ,blank=True,null=True)
    name = models.CharField(max_length=50,blank=False,null=False)
    last_name = models.CharField(max_length=50,blank=False,null=False)
    identification = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    
    def __str__(self):
        return self.name
    
class Pet(models.Model):
    client = models.ForeignKey(Client, on_delete= models.PROTECT)
    namePet = models.CharField(max_length=30,blank=False,null=False)
    species = models.CharField(max_length=30,blank=True,null=True)
    birthdate = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=6 , blank=False, null = False, default='Desconocido')
    # veterinary = models.CharField(max_length=50, default="None")
    
    def __str__(self):
        return self.namePet

class Events(models.Model):
    pet = models.ForeignKey(Pet,on_delete= models.PROTECT)
    client = models.ForeignKey(Client,on_delete= models.PROTECT)
    doctor = models.ForeignKey(User,on_delete= models.PROTECT,limit_choices_to={'is_doctor': True})
    name = models.CharField(max_length=255,null=True,blank=True, default= "Consulta")
    end = models.DateTimeField(null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True, default = end)
    room = models.CharField(max_length=15,null=False)
    is_active = models.BooleanField(default = True)

    # def clean(self):
    #     if self.start < datetime.now():
    #         raise ValidationError ('No puede ser menor a la fecha actual')
    #     return super().clean()

    def __str__(self):
        return self.name