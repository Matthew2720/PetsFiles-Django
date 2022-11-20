from django.forms import ModelForm,TextInput,EmailInput,Select,PasswordInput
from django.forms import HiddenInput,DateInput,TimeInput,DateTimeInput
from .models import *

class VeterinaryForm(ModelForm):
    class Meta:
        model = Veterinary
        fields = '__all__'
        widgets = {
            'nameVeterinary': TextInput(attrs={'class':'form-control'}),
            'cityVeterinary': TextInput(attrs={'class':'form-control'}),
            'nit': TextInput(attrs={'class':'form-control'}) ,
            'email': TextInput(attrs={'class':'form-control'}),
            'direccion': TextInput(attrs={'class':'form-control'}),
            'password':PasswordInput(attrs={'class':'form-control'}),
        }
        labels = {
            'nameVeterinary': 'Veterinaria ',
            'cityVeterinary': 'Ciudad ',
            'nit': 'Nit ',
            'email':'Email ',
            'direccion':'Direccion',
            'password':'Contraseña '
        }

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ('username','first_name','last_name','password','direccion','email','groups')
        help_texts = {
            'username':None,'first_name':None,'last_name':None,'password':None,
            'direccion':None,'email':None,'groups':None
        }
        widgets = {
            'username': TextInput(attrs={'class':'form-control'}),
            'first_name': TextInput(attrs={'class':'form-control'}),
            'last_name': TextInput(attrs={'class':'form-control'}) ,
            'password': PasswordInput(attrs={'class':'form-control'}) ,
            'direccion': TextInput(attrs={'class':'form-control'}) ,
            'email': EmailInput(attrs={'class':'form-control'}),
            'groups': Select(attrs={'class':'form-control'}),
        }

class UserFormWithoutPassword(UserForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','direccion','email')
        help_texts = {
            'username':None,'first_name':None,'last_name':None,'password':None,
            'direccion':None,'email':None,'groups':None
        }
        widgets = {
            'username': TextInput(attrs={'class':'form-control'}),
            'first_name': TextInput(attrs={'class':'form-control'}),
            'last_name': TextInput(attrs={'class':'form-control'}) ,
            'password': PasswordInput(attrs={'class':'form-control'}) ,
            'direccion': TextInput(attrs={'class':'form-control'}) ,
            'email': EmailInput(attrs={'class':'form-control'}),
            'groups': Select(attrs={'class':'form-control'}),
        }


class ClientForm(ModelForm):

    class Meta:
        model = Client
        # exclude = ('veterinary',)
        fields = '__all__'
        widgets = {
            'veterinary': HiddenInput(attrs={'class':'form-control form-input'}),
            'name':TextInput(attrs={'class':'form-control form-input'}),
            'last_name':TextInput(attrs={'class':'form-control form-input'}),
            'identification':TextInput(attrs={'class':'form-control form-input'}),
            'email':EmailInput(attrs={'class':'form-control form-input'}),
            'phone':TextInput(attrs={'class':'form-control form-input'}),
        }
        labels = {
            'veterinary': 'Veterinaria',
            'name':'Nombres',
            'last_name':'Apellidos',
            'email':'Email',
            'phone':'Telefono',
            'identification':'Cedula'
        }

class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = '__all__'
        CHOICES = (('Macho', 'Macho'),('Hembra', 'Hembra'),)
        widgets = {
            'client': Select(attrs={'class':'form-control'}),
            'namePet':TextInput(attrs={'class':'form-control'}),
            'species':TextInput(attrs={'class':'form-control'}),
            'gender':Select(attrs={'class':'form-control'},choices= CHOICES ),
            'birthdate':DateInput(attrs={'class':'form-control','type':'date'}),
        }
        labels = {
            'client': 'Cliente',
            'namePet':'Nombre de la Mascota',
            'species':'Especie',
            'gender':'Genero',
            'birthdate':'Fecha de nacimiento'
        }

class DateForm(ModelForm):
    
    class Meta:
        model = Date
        exclude = ('is_active',)
        CHOICES = (('1', 'Consultorio 1'),('2', 'Consultorio 2'),)
        widgets = {
            'pet': Select(attrs={'class':'form-control'}),
            'client':Select(attrs={'class':'form-control'}),
            'doctor':Select(attrs={'class':'form-control'}),
            'room':Select(attrs={'class':'form-control'},choices= CHOICES ),
            'date':DateInput(attrs={'class':'form-control','type':'date'}),
            'hour':TimeInput(attrs={'class':'form-control','type':'time'})
        }
        labels = {
            'pet': 'Mascota',
            'client':'Cliente',
            'doctor':'Especialista',
            'room':'Consultorio',
            'date':'Fecha',
            'time':'Hora'
        }
