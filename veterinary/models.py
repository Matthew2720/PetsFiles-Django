import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict


# Modelos MER.
class Veterinary(models.Model):
    nameVeterinary = models.CharField(max_length=50, blank=False, null=False, unique=True)
    cityVeterinary = models.CharField(max_length=50, blank=True, null=True)
    nit = models.CharField(max_length=50, blank=False, null=False, unique=True)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=60, blank=True, null=True)
    password = models.CharField(max_length=50, default='admin')

    def __str__(self):
        return self.nameVeterinary


# UserModel
class User(AbstractUser):
    direccion = models.CharField(max_length=50, blank=True, null=True)
    veterinary = models.ForeignKey(Veterinary, on_delete=models.PROTECT, null=True, blank=True)
    is_doctor = models.BooleanField(default=False)

    def set_veterinary(self, id):
        self.veterinary = id


# EndUserModel

class Client(models.Model):
    veterinary = models.ForeignKey(Veterinary, on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    document = models.CharField(max_length=20, unique=False, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=False, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    global_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('document', 'email', 'veterinary')


class Pet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    namePet = models.CharField(max_length=30, blank=False, null=False)
    species = models.CharField(max_length=30, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=False, null=False, default='Desconocido')

    # veterinary = models.CharField(max_length=50, default="None")

    def client_name(self):
        return self.pet.client.name

    def __str__(self):
        return self.namePet


class Events(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT)
    doctor = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={'is_doctor': True})
    name = models.CharField(max_length=255, null=True, blank=True, default="Consulta")
    end = models.DateTimeField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True, default=datetime.now)
    room = models.CharField(max_length=15, null=False)
    is_active = models.BooleanField(default=True)

    # def clean(self):
    #     if self.start < datetime.now():
    #         raise ValidationError ('No puede ser menor a la fecha actual')
    #     return super().clean()

    @property
    def client_name(self):
        return self.pet.client.name

    def __str__(self):
        return self.name

    # -----------PRUEBA MODELO --------#


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = '{} / {}'.format(self.name, self.cat.name)
        item['cat'] = self.cat.toJSON()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Sale(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='details')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale: {self.sale.id} - Product: {self.product.name} - Quantity: {self.quantity} - Price: {self.price}"
