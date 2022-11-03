from django.shortcuts import render,redirect
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
            return redirect('index')
        
    form = VeterinaryForm()
    context = {'form':form}
    return render(request,'veterinary/register.html',context)