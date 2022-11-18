from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registro/",views.registerVet, name="registerVet"),
    path("registro/cliente",views.registerClient, name="registerClient"),
    path("registro/mascota",views.registerPet, name="registerPet"),
    path("registro/empleado",views.registerEmployee, name="registerEmployee"),
    path("home/",views.home,name="home"),
    path("ver/clientes",views.detailClient,name='detailClient'),
    path("actualizar/clientes/<int:id>",views.updateClient,name='updateClient'),
    path("actualizar/mascota/<int:id>",views.updatePet,name='updatePet'),
    path("eliminar/clientes/<int:id>",views.deleteClient,name="deleteClient")
]