from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("prueba", views.prueba, name="prueba"),
    path("registro/",views.pruebaRegistroVet, name="pruebaRegistro"),
    path("registro/cliente",views.pruebaCliente, name="pruebaCliente"),
]