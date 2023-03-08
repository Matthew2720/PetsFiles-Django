from django.forms import ModelForm, TextInput, EmailInput, Select, PasswordInput, CharField, DecimalField, \
    inlineformset_factory
from django.forms import HiddenInput, DateInput, DateTimeInput, NumberInput, ChoiceField, Form
from xdg.Exceptions import ValidationError

from .models import *


class DateTimePickerInput(DateTimeInput):
    input_type = 'datetime-local'


class VeterinaryForm(ModelForm):
    class Meta:
        model = Veterinary
        fields = '__all__'
        widgets = {
            'nameVeterinary': TextInput(attrs={'class': 'form-control'}),
            'cityVeterinary': TextInput(attrs={'class': 'form-control'}),
            'nit': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'direccion': TextInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nameVeterinary': 'Veterinaria ',
            'cityVeterinary': 'Ciudad ',
            'nit': 'Nit ',
            'email': 'Email ',
            'direccion': 'Direccion',
            'password': 'Contraseña '
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'direccion', 'email', 'groups')
        help_texts = {
            'username': None, 'first_name': None, 'last_name': None, 'password': None,
            'direccion': None, 'email': None, 'groups': None
        }
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
            'direccion': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'groups': Select(attrs={'class': 'form-control'}),
        }


class UserFormWithoutPassword(UserForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'direccion', 'email')
        help_texts = {
            'username': None, 'first_name': None, 'last_name': None, 'password': None,
            'direccion': None, 'email': None, 'groups': None
        }
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
            'direccion': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'groups': Select(attrs={'class': 'form-control'}),
        }


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'veterinary': HiddenInput(attrs={'class': 'form-control form-input'}),
            'name': TextInput(attrs={'class': 'form-control form-input'}),
            'last_name': TextInput(attrs={'class': 'form-control form-input'}),
            'document': TextInput(attrs={'class': 'form-control form-input'}),
            'email': EmailInput(attrs={'class': 'form-control form-input'}),
            'phone': TextInput(attrs={'class': 'form-control form-input'}),
        }
        labels = {
            'veterinary': 'Veterinaria',
            'name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Email',
            'phone': 'Telefono',
            'document': 'Cedula'
        }


class PetForm(ModelForm):
    def __init__(self, VeterinaryLogued, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(veterinary=VeterinaryLogued)

    class Meta:
        model = Pet
        fields = '__all__'
        CHOICES = (('Macho', 'Macho'), ('Hembra', 'Hembra'),)
        CHOICESPECIES = (('Felino', 'Felino'), ('Canino', 'Canino'), ('Aves', 'Aves'), ('Otro', 'Otro'))
        widgets = {
            'client': Select(attrs={'class': 'form-control'}),
            'namePet': TextInput(attrs={'class': 'form-control'}),
            'species': Select(attrs={'class': 'form-control'}, choices=CHOICESPECIES),
            'gender': Select(attrs={'class': 'form-control'}, choices=CHOICES),
            'birthdate': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'client': 'Cliente',
            'namePet': 'Nombre de la Mascota',
            'species': 'Especie',
            'gender': 'Genero',
            'birthdate': 'Fecha de nacimiento'
        }


class EventForm(ModelForm):
    def __init__(self, VeterinaryLogued, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pet'].queryset = Pet.objects.select_related('client__veterinary').filter(
            client__veterinary=VeterinaryLogued)
        self.fields['doctor'].queryset = User.objects.filter(veterinary=VeterinaryLogued, is_doctor=True)

    class Meta:
        model = Events
        exclude = ('is_active', 'end', 'client')
        CHOICES = (
            ('1', 'Consultorio 1'),
            ('2', 'Consultorio 2'),
            ('3', 'Consultorio 3'),
            ('4', 'Consultorio 4'),
            ('5', 'Consultorio 5'),
            ('6', 'Consultorio 6'),
        )
        CHOICESTYPE = (
            ('Consulta', 'Consulta'),
            ('Hospitalizacion', 'Hospitalizacion'),
            ('Vacunacion', 'Vacunacion'),
            ('Guarderia', 'Guarderia'),
            ('Sala de belleza', 'Sala de belleza'),
            ('Consulta intermitente', 'Consulta intermitente'),
        )
        widgets = {
            'name': Select(attrs={'class': 'form-control'}, choices=CHOICESTYPE),
            'start': DateTimePickerInput(attrs={'class': 'form-control'}),
            'end': DateTimePickerInput(attrs={'class': 'form-control'}),
            'pet': Select(attrs={'class': 'form-control'}),
            'doctor': Select(attrs={'class': 'form-control'}),
            'room': Select(attrs={'class': 'form-control'}, choices=CHOICES),
        }
        labels = {
            'pet': 'Mascota',
            'doctor': 'Especialista',
            'room': 'Consultorio',
            'start': 'Fecha',
            'name': 'Tipo de servicio'
        }


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'desc': TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'name': 'Nombre',
            'desc': 'Descripcion'
        }


class OrderForm(Form):
    ORDER_CHOICES = (
        ('name', 'Nombre Ascendente'),
        ('-name', 'Nombre Descendente'),
        ('cat__name', 'Categoría Ascendente'),
        ('-cat__name', 'Categoría Descendente'),
        ('stock', 'Stock Ascendente'),
        ('-stock', 'Stock Descendente'),
        ('pvp', 'Precio Ascendente'),
        ('-pvp', 'Precio Descendente'),
    )

    order_by = ChoiceField(choices=ORDER_CHOICES, required=False, label='Ordenar por')


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'cat', 'stock', 'pvp']
        labels = {
            'name': 'Nombre',
            'cat': 'Categoría',
            'stock': 'Stock',
            'pvp': 'Precio de venta'
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'cat': Select(attrs={'class': 'form-control'}),
            'stock': NumberInput(attrs={'class': 'form-control'}),
            'pvp': NumberInput(attrs={'class': 'form-control'}),
        }


class SaleForm(ModelForm):
    client_document = CharField(max_length=20, required=True, label='Cliente (documento)',
                                widget=TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    class Meta:
        model = Sale
        exclude = ['client', 'created_by', 'total']

    def clean_client_document(self):
        client_document = self.cleaned_data.get('client_document')
        try:
            client = Client.objects.get(document=client_document)
        except Client.DoesNotExist:
            raise ValidationError("El cliente no existe.")
        return client_document

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.client = Client.objects.get(document=self.cleaned_data['client_document'])
        if commit:
            instance.save()
        return instance


class DetSaleForm(ModelForm):
    iva = DecimalField(max_digits=8, decimal_places=2, label='IVA',
                       widget=NumberInput(attrs={'class': 'form-control', 'step': '0.01' , 'name': 'iva'}))
    subtotal = DecimalField(max_digits=10, decimal_places=2, label='Subtotal',
                            widget=NumberInput(attrs={'class': 'form-control', 'readonly': True, 'name': 'subtotal'}))
    pvp = DecimalField(max_digits=10, decimal_places=2, label='Precio',
                       widget=NumberInput(attrs={'class': 'form-control', 'readonly': True, 'name': 'pvp'}))

    class Meta:
        model = DetSale
        fields = ['product', 'quantity']

        widgets = {
            'product': Select(attrs={'class': 'form-control', 'onChange': 'update_price()', 'name': 'product'}),
            'quantity': NumberInput(attrs={'class': 'form-control', 'min': 1 , 'name': 'quantity'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()


SaleFormSet = inlineformset_factory(Sale, DetSale, form=DetSaleForm, extra=8)
