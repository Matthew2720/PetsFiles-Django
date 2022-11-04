from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registro/",views.pruebaRegistroVet, name="pruebaRegistro"),
    path("registro/cliente",views.registerClient, name="registerClient"),
    path("registro/empleado",views.pruebaEmpleado, name="pruebaEmpleado"),
]