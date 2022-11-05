from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from .forms import *

# Create your views here.
def index(request):
    return render(request,'veterinary/index.html',{})

@login_required(login_url='login')
def registerClient(request):
    VeterinaryLogued = request.user.veterinary
    if request.method == 'POST':
        if request.POST.get('identification',''):
            formClient=ClientForm(request.POST)
            form = PetForm()
            if formClient.is_valid:
                formClient.save()
                return redirect('registerClient')
        else:
            form = PetForm(request.POST)
            if form.is_valid:
                form.save()
                return redirect('registerClient')
    else:
        form = PetForm()
        formClient = ClientForm(initial={'veterinary':VeterinaryLogued})
        context = {
            'form':form,
            'formClient':formClient
        }
        return render(request,'veterinary/registerClient.html',context)

def registerVet(request):
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

def registerEmployee(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('index')
        
    form = UserForm()
    context = {'form':form}
    return render(request,'veterinary/registerEmployee.html',context)

@login_required
def home(request):
    return render(request,'veterinary/home.html',{})