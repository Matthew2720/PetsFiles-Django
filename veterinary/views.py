import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction
from django.forms import formset_factory
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from .forms import (
    VeterinaryForm,
    UserForm,
    ClientForm,
    PetForm,
    UserFormWithoutPassword,
    EventForm,
    CategoryForm,
    ProductForm,
    OrderForm,
    SaleForm,
    DetSaleForm,
)
from .models import User, Veterinary, Pet, Client, Events, Product


def index(request):
    return render(request, "veterinary/index.html", {})


def support(request):
    return render(request, "veterinary/support.html", {})


# region client


@login_required(login_url="login")
def detailClient(request):
    veterinaryLogued = request.user.veterinary
    form = ClientForm(initial={"veterinary": veterinaryLogued})
    if request.method == "POST":
        search_query = request.POST.get("search", "")
        clients = Client.objects.filter(
            name__contains=search_query, veterinary=veterinaryLogued
        )
        form_client = ClientForm(request.POST)
        if form_client.is_valid():
            document = form_client.cleaned_data["document"]
            email = form_client.cleaned_data["email"]
            if Client.objects.filter(Q(document=document) | Q(email=email)).exists():
                messages.error(
                    request,
                    "Ya existe un cliente con el mismo documento o correo electrónico.",
                )
            else:
                form_client.save()
                messages.success(request, "Cliente creado correctamente.")
                return redirect("detailClient")
    else:
        clients = Client.objects.filter(veterinary=veterinaryLogued)
    context = {"clients": clients, "form": form}
    return render(request, "veterinary/detailClient.html", context)


@login_required(login_url="login")
def updateClient(request, id):
    client = Client.objects.get(id=id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            identification = form.cleaned_data["document"]
            email = form.cleaned_data["email"]
            existing_client_identification = (
                Client.objects.filter(document=identification).exclude(id=id).exists()
            )
            existing_client_email = (
                Client.objects.filter(email=email).exclude(id=id).exists()
            )
            if existing_client_identification:
                messages.error(request, "El documento ya existe")
                return render(request, "veterinary/updateClient.html", {"form": form})
            elif existing_client_email:
                messages.error(request, "El email ya existe")
                return render(request, "veterinary/updateClient.html", {"form": form})
            else:
                form.save()
                return redirect(detailClient)
    else:
        form = ClientForm(instance=client)
    context = {"form": form}
    return render(request, "veterinary/updateClient.html", context)


@login_required(login_url="login")
def deleteClient(request, id):
    try:
        client = Client.objects.get(id=id)
        client.delete()
        messages.success(request, "El cliente se elimino correctamente")
    except:
        messages.error(request, "No se puede eliminar porque tiene mascotas asociadas")
    return redirect("detailClient")


# endregion

# region pet


@login_required(login_url="login")
def detailPet(request):
    VeterinaryLogued = request.user.veterinary
    if request.method == "POST":
        search_query = request.POST.get("search", "")
        pet = Pet.objects.select_related("client", "client__veterinary").filter(
            namePet__contains=search_query, client__veterinary=VeterinaryLogued
        )
        formPet = PetForm(VeterinaryLogued, request.POST)
        if formPet.is_valid():
            formPet.save()
            return redirect("detailPet")
    else:
        formPet = PetForm(VeterinaryLogued)
        pet = Pet.objects.select_related("client", "client__veterinary").filter(
            client__veterinary=VeterinaryLogued
        )
    context = {"pets": pet, "form": formPet}
    return render(request, "veterinary/detailPet.html", context)


@login_required(login_url="login")
def updatePet(request, id):
    veterinary_logued = request.user.veterinary
    pet = Pet.objects.get(id=id)
    if request.method == "POST":
        form = PetForm(veterinary_logued, request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect(detailPet)
    else:
        form = PetForm(veterinary_logued, instance=pet)
    context = {"form": form}
    return render(request, "veterinary/updatePet.html", context)


@login_required(login_url="login")
def deletePet(request, id):
    pet = Pet.objects.get(id=id)
    pet.delete()
    return redirect("detailPet")


# endregion

# region calendar


@login_required(login_url="login")
def registerDate(request):
    veterinary_logued = request.user.veterinary
    all_events_query = Events.objects.select_related("pet__client__veterinary").filter(
        pet__client__veterinary=veterinary_logued
    )
    out = []
    for event in all_events_query:
        out.append(
            {
                "title": f"{event.pet}" + "|" + f"{event.name}",
                "id": event.id,
                "start": event.start.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.start.strftime("%Y-%m-%dT%H:%M:%S"),
            }
        )

    form = EventForm(veterinary_logued)
    context = {"form": form, "events": out}
    return render(request, "veterinary/registerDate.html", context)


# detail event


@login_required(login_url="login")
def home(request):
    veterinary_logued = request.user.veterinary
    if request.method == "POST":
        form = EventForm(veterinary_logued, request.POST)
        if form.is_valid:
            form.save()
            return redirect("home")
    all_events_query = Events.objects.select_related("pet__client__veterinary").filter(
        pet__client__veterinary=veterinary_logued
    )
    out = []
    form = EventForm(veterinary_logued)
    for event in all_events_query:
        out.append(
            {
                "title": f"{event.pet}"
                         + "|"
                         + f"{event.client_name}"
                         + "|"
                         + f"{event.name}",
                "id": event.id,
                "start": event.start.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.start.strftime("%Y-%m-%dT%H:%M:%S"),
                "client": event.pet.client_name,
                "pet": event.pet,
                "room": event.room,
            }
        )
    context = {"events": out, "form": form}
    return render(request, "veterinary/home.html", context)


@login_required(login_url="login")
def updateDate(request, id):
    veterinary_logued = request.user.veterinary
    date = Events.objects.get(id=id)
    if request.method == "POST":
        form = EventForm(veterinary_logued, request.POST, instance=date)
        if form.is_valid():
            form.save()
            return redirect(home)
    else:
        form = EventForm(veterinary_logued, instance=date)
    context = {"form": form}
    return render(request, "veterinary/updateDate.html", context)


@login_required(login_url="login")
def deleteEvent(request, id):
    event = Events.objects.get(id=id)
    event.delete()
    return redirect("home")


# endregion

# region employee


@login_required(login_url="login")
def registerEmployee(request):
    VeterinaryLogued = request.user.veterinary
    if request.method == "POST":
        user = User.objects.create(
            username=request.POST["username"],
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            password=request.POST["password"],
            direccion=request.POST["direccion"],
            email=request.POST["email"],
            veterinary=VeterinaryLogued,
        )
        user.set_password(request.POST["password"])
        user.save()
        user.groups.add(request.POST["groups"])
        # Si el grupo seleccionado es "Medico Veterinario"
        if (
                request.POST["groups"] == "4"
                or request.POST["groups"] == "3"
                or request.POST["groups"] == 3
                or request.POST["groups"] == 4
        ):
            user.is_doctor = True
            user.save()
            print(user.is_doctor)
        user.save()
        return redirect("detailEmployee")
    form = UserForm
    context = {"form": form}
    return render(request, "veterinary/registerEmployee.html", context)


@login_required(login_url="login")
def detailEmployee(request):
    VeterinaryLogued = request.user.veterinary
    if request.method == "POST":
        employee = User.objects.filter(
            first_name__contains=request.POST.get("search", ""),
            veterinary=VeterinaryLogued,
        )
    else:
        employee = User.objects.filter(veterinary=VeterinaryLogued)
    context = {"employees": employee}
    return render(request, "veterinary/detailEmployee.html", context)


@login_required(login_url="login")
def updateEmployee(request, id):
    employee = User.objects.get(id=id)
    if request.method == "POST":
        actualizar = User.objects.update_or_create(
            id=id,
            defaults={
                "username": request.POST["username"],
                "first_name": request.POST["first_name"],
                "last_name": request.POST["last_name"],
                "direccion": request.POST["direccion"],
                "email": request.POST["email"],
            },
        )
        return redirect(detailEmployee)
    else:
        form = UserFormWithoutPassword(instance=employee)
    context = {"form": form}
    return render(request, "veterinary/registerEmployee.html", context)


@login_required(login_url="login")
def deleteEmployee(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("detailEmployee")


# endregion

# region register veterinary


def registerVet(request):
    if request.method == "POST":
        form = VeterinaryForm(request.POST)
        if form.is_valid:
            form.save()
            nit = request.POST["nit"]
            veterinary = Veterinary.objects.get(nit=nit)
            user = User.objects.create(
                username=request.POST["nameVeterinary"],
                password=request.POST["password"],
                veterinary=veterinary,
            )
            user.set_password(request.POST["password"])
            user.save()
            user.groups.add()
            user.save()
            return redirect("index")

    form = VeterinaryForm()
    context = {"form": form}
    return render(request, "veterinary/register.html", context)


# endregion


# region product
@login_required
def detailProduct(request):
    products = Product.objects.all()
    form1 = CategoryForm(request.POST or None)
    form2 = ProductForm(request.POST or None)
    order_form = OrderForm(request.GET or None)

    if order_form.is_valid():
        order_by = order_form.cleaned_data["order_by"]
        if order_by:
            products = products.order_by(order_by)

    products = products.filter(name__contains=request.POST.get("search", ""))
    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        if form1.is_valid() and request.POST.get("desc") != None:
            form1.save()
            messages.success(request, "Categoria agregada")
            return HttpResponseRedirect(request.path_info)
        elif form2.is_valid():
            form2.save()
            messages.success(request, "Producto agregado")
            return HttpResponseRedirect(request.path_info)

    context = {
        "form1": form1,
        "form2": form2,
        "order_form": order_form,
        "page_obj": page_obj,
    }

    return render(request, "veterinary/detailProduct.html", context)


@login_required(login_url="login")
def deleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("detailProduct")


@login_required(login_url="login")
def updateProduct(request, id):
    # veterinary_logued = request.user.veterinary
    product = Product.objects.get(id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("detailProduct")
    else:
        form = ProductForm(instance=product)
    context = {"form": form}
    return render(request, "veterinary/updateProduct.html", context)


# endregion

#region sale

def create_sale(request):
    DetSaleFormSet = formset_factory(DetSaleForm, extra=1)

    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        det_formset = DetSaleFormSet(request.POST)

        if sale_form.is_valid() and det_formset.is_valid():
            with transaction.atomic():
                # guardar la venta
                sale = sale_form.save()

                # guardar los detalles de la venta
                for det_form in det_formset:
                    det = det_form.save(commit=False)
                    det.sale = sale
                    det.save()

                # Actualizar la venta con el total
                sale.total = sale.subtotal * (1 + sale.iva / 100)
                sale.save()

            return redirect('sale_list')
        else:
            print(det_formset.errors)
            print(sale_form.errors.get_json_data().values())
            context = {
                'sale_form': sale_form,
                'det_formset': det_formset,
                'errors': list(sale_form.errors.get_json_data().values()) + det_formset.errors,
            }
    else:
        sale_form = SaleForm()
        det_formset = DetSaleFormSet()
        context = {
            'sale_form': sale_form,
            'det_formset': det_formset,
        }

    return render(request, 'veterinary/create_sale2.html', context)


def create_sale2(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("JSON OBTENIDO")
        print(data)
        return render(request, 'veterinary/create_sale2.html', {})
    return render(request, 'veterinary/create_sale2.html', {})

@require_GET
def search(request):
    term = request.GET.get('term')
    if term:
        results = Product.objects.filter(Q(name__icontains=term))
        data = [{'idProduct':r.id, 'full_name': r.name, 'stock': r.stock, 'pvp': r.pvp} for r in results]
        return JsonResponse({'results': data})
    else:
        results = Product.objects.all()
        data = [{'idProduct':r.id, 'full_name': r.name, 'stock': r.stock, 'pvp': r.pvp} for r in results]
        return JsonResponse({'results': data})


#endregion