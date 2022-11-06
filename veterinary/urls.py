from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registro/",views.registerVet, name="registerVet"),
    path("registro/cliente",views.registerClient, name="registerClient"),
    path("registro/empleado",views.registerEmployee, name="registerEmployee"),
    path("home/",views.home,name="home"),
    path("ver/clientes",views.detailClient,name='detailClient')
]