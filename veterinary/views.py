from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from .forms import *

# Create your views here.
def index(request):
    return render(request,'veterinary/index.html',{})
#region register client/pet
@login_required(login_url='login')
def registerClient(request):
    VeterinaryLogued = request.user.veterinary
    if request.method == 'POST':
        formClient=ClientForm(request.POST)
        if formClient.is_valid:
            formClient.save()
            return redirect('registerClient')
    else:
        formClient = ClientForm(initial={'veterinary':VeterinaryLogued})
        context = {
            'formClient':formClient
        }
        return render(request,'veterinary/registerClient.html',context)

@login_required(login_url='login')
def registerPet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('registerPet')
    else:
        form = PetForm()
        context = {
            'form':form
        }
        return render(request,'veterinary/registerPet.html',context)
#endregion

#region update
def updateClient(request,id):
    client = Client.objects.get(id=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid:
            form.save()
            return redirect(detailClient)
    else:
        form = ClientForm(instance=client)
    context= {'formClient':form}
    return render(request,'veterinary/registerClient.html',context)
    

def updatePet(request,id):
    pass
#endregion

#region delete
def deleteClient(request,id):
    client = Client.objects.get(id=id)
    client.delete()
    return redirect('detailClient')

#endregion

#region register veterinary/employee
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

@login_required(login_url='login')
def registerEmployee(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('index')
        
    form = UserForm()
    context = {'form':form}
    return render(request,'veterinary/registerEmployee.html',context)
#endregion

#region login/details
@login_required(login_url='login')
def home(request):
    return render(request,'veterinary/home.html',{})

def detailClient(request):
    if request.method == 'POST':
        clients = Client.objects.filter(name__contains = request.POST.get('search',''))
        context = {'clients':clients}
        return render(request,'veterinary/detailClient.html',context)
    else:
        clients = Client.objects.all()
        context = {'clients':clients}
        return render(request,'veterinary/detailClient.html',context)
#endregion