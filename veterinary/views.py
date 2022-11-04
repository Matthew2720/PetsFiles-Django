from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,permission_required
from .forms import *

# Create your views here.
def index(request):
    return render(request,'veterinary/index.html',{})

def prueba(request):
    return render(request,'veterinary/index2.html',{})

def pruebaRegistroVet(request):
    if request.method == 'POST':
        form = VeterinaryForm(request.POST)
        if form.is_valid:
            form.save()
            nit = request.POST['nit']
            veterinary = Veterinary.objects.get(nit = nit)
            user = User.objects.create(
                username = request.POST['nameVeterinary'],password=request.POST['password'],
                veterinary= veterinary
                )
            user.set_password(request.POST['password'])
            user.save()
            user.groups.add(2)
            user.save()
            return redirect('index')
            
    form = VeterinaryForm()
    context = {'form':form}
    return render(request,'veterinary/register.html',context)

@login_required(login_url='login')
def pruebaCliente(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('index')
        
    form = ClientForm()
    context = {'form':form}
    return render(request,'veterinary/registerClient.html',context)

def pruebaEmpleado(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('index')
        
    form = UserForm()
    context = {'form':form}
    return render(request,'veterinary/registerEmployee.html',context)