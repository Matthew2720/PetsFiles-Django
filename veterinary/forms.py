from django.forms import ModelForm,TextInput,EmailInput,Select,PasswordInput
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
        }
        labels = {
            'nameVeterinary': 'Veterinaria',
            'cityVeterinary': 'Ciudad',
            'nit': 'Ingresa el documento',
            'email':'Email'
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
            'direccion': PasswordInput(attrs={'class':'form-control'}) ,
            'email': TextInput(attrs={'class':'form-control'}),
            'groups': Select(attrs={'class':'form-control'}),
        }

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'veterinary': Select(attrs={'class':'form-control'}),
            'name':TextInput(attrs={'class':'form-control'}),
            'last_name':TextInput(attrs={'class':'form-control'}),
            'email':EmailInput(attrs={'class':'form-control'}),
            'phone':TextInput(attrs={'class':'form-control'}),
            'mobil':TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'veterinary': 'Veterinaria',
            'name':'Nombres',
            'last_name':'Apellidos',
            'email':'Email',
            'phone':'Telefono',
            'mobil':'Celular',
        }

class PetForm(ModelForm):
    class Meta:
        model = Pet
        fields = '__all__'