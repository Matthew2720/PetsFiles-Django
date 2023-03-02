from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registro/",views.registerVet, name="registerVet"),
    path("registro/cliente",views.registerClient, name="registerClient"),
    path("registro/mascota",views.registerPet, name="registerPet"),
    path("registro/empleado",views.registerEmployee, name="registerEmployee"),
    path("registro/citas",views.registerDate, name="registerDate"),
    path("home/",views.home, name="home"),
    path("actualizar/empleado/<int:id>",views.updateEmployee,name='updateEmployee'),
    path("ver/clientes",views.detailClient,name='detailClient'),
    path("ver/mascotas",views.detailPet,name='detailPet'),
    path("ver/empleados",views.detailEmployee,name='detailEmployee'),
    path("actualizar/clientes/<int:id>",views.updateClient,name='updateClient'),
    path("actualizar/mascota/<int:id>",views.updatePet,name='updatePet'),
    path("actualizar/cita/<int:id>",views.updateDate,name='updateDate'),
    path("eliminar/clientes/<int:id>",views.deleteClient,name="deleteClient"),
    path("eliminar/cita/<int:id>",views.deleteEvent,name="deleteEvent"),
    path("eliminar/empleados/<int:id>",views.deleteEmployee,name="deleteEmployee"),
    path("eliminar/mascotas/<int:id>",views.deletePet,name="deletePet"),
    path("support",views.support,name="support"),
    path("ver/productos",views.detailProduct,name="detailProduct")
]