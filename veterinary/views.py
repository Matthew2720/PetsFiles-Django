from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'veterinary/index.html',{})

def prueba(request):
    return render(request,'veterinary/index2.html',{})
