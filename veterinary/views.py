from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from .forms import VeterinaryForm,UserForm,ClientForm,PetForm,UserFormWithoutPassword,DateForm
from .models import User,Veterinary,Pet,Client,Date


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
            return redirect('detailClient')
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
            return redirect('detailPet')
    else:
        form = PetForm()
        context = {
            'form':form
        }
        return render(request,'veterinary/registerPet.html',context)
#endregion

#region update
@login_required(login_url='login')
def updateClient(request,id):
    client = Client.objects.get(id=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect(detailClient)
    else:
        form = ClientForm(instance=client)
    context= {'formClient':form}
    return render(request,'veterinary/registerClient.html',context)
    
@login_required(login_url='login')
def updatePet(request,id):
    pet = Pet.objects.get(id=id)
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect(detailPet)
    else:
        form = PetForm(instance=pet)
    context= {'form':form}
    return render(request,'veterinary/registerPet.html',context)

@login_required(login_url='login')
def updateEmployee(request,id):
    employee = User.objects.get(id=id)
    if request.method == 'POST':
        actualizar = User.objects.update_or_create(
            id  =  id,
            defaults={
            'username': request.POST['username'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'] ,
            'direccion': request.POST['direccion'] ,
            'email': request.POST['email']})
        return redirect(detailEmployee)
    else:
        form = UserFormWithoutPassword(instance=employee)
    context= {'form':form}
    return render(request,'veterinary/registerEmployee.html',context)
#endregion

#region delete
@login_required(login_url='login')
def deleteClient(request,id):
    client = Client.objects.get(id=id)
    client.delete()
    return redirect('detailClient')

@login_required(login_url='login')
def deleteEmployee(request,id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('detailEmployee')

@login_required(login_url='login')
def deletePet(request,id):
    pet = Pet.objects.get(id=id)
    pet.delete()
    return redirect('detailPet')

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
    VeterinaryLogued = request.user.veterinary
    if request.method == 'POST':
            user = User.objects.create(
                username = request.POST['username'],first_name = request.POST['first_name'],last_name = request.POST['last_name'],
                password=request.POST['password'],direccion = request.POST['direccion'],email = request.POST['email'],
                veterinary= VeterinaryLogued
                )
            user.set_password(request.POST['password'])
            user.save()
            user.groups.add(request.POST['groups'])
            user.save()
            return redirect('detailEmployee')
    form = UserForm
    context = {'form':form}
    return render(request,'veterinary/registerEmployee.html',context)

@login_required(login_url='login')
def registerDate(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('detailPet')
        else:
            messages.error(request,'La fecha no puede ser anterior a la actual')
    else:
        form = DateForm()
    context = {'form' : form}
    return render(request,'veterinary/registerDate.html',context)
#endregion

#region login/details
@login_required(login_url='login')
def home(request):
    return render(request,'veterinary/home.html',{})

@login_required(login_url='login')
def detailClient(request):
    if request.method == 'POST':
        clients = Client.objects.filter(name__contains = request.POST.get('search',''))
    else:
        clients = Client.objects.all()
    context = {'clients':clients}
    return render(request,'veterinary/detailClient.html',context)

@login_required(login_url='login')
def detailPet(request):
    if request.method == 'POST':
        pet = Pet.objects.filter(namePet__contains = request.POST.get('search',''))
    else:
        pet = Pet.objects.all()
    context = {'pets':pet}
    return render(request,'veterinary/detailPet.html',context)

@login_required(login_url='login')
def detailEmployee(request):
    if request.method =='POST':
        employee = User.objects.filter(name__contains = request.POST.get ('search', ''))
    else:
        employee = User.objects.all()
    context = {'employees':employee}
    return render (request, 'veterinary/detailEmployee.html', context)

@login_required(login_url='login')
def detailDate(request):
    dates = Date.objects.all()
    dates = dates.values('date','hour')
    dateformat = []
    hourformat = []
    for c in dates:
        dateformat.append(str(c['date']))
        hourformat.append(str(c['hour']))
    lista = []
    for i in range(len(dateformat)):
        lista.append([[dateformat[i]],[hourformat[i]]])
    print(lista[0][0])
    context = {'Reservas': dateformat,'Horas':hourformat}
    return render(request,'veterinary/detailDate.html',context)
#endregion