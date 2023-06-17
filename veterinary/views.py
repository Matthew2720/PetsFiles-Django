import base64
import json
from decimal import Decimal
from io import BytesIO

import matplotlib.pyplot as plt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q, F, Sum
from django.db.models.functions import TruncMonth
from django.http import FileResponse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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
    ServiceForm,
)
from .models import User, Veterinary, Pet, Client, Events, Product, DetSale, Sale, Services, Category


def index(request):
    return render(request, "veterinary/index.html", {})


def support(request):
    return render(request, "veterinary/support.html", {})


def send_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        nombre = request.POST['Nombre']
        mensaje = request.POST['message']
        send_mail(
            'Solicitud de Soporte',
            'Hola, ' + nombre + ' ha enviado un mensaje: ' + mensaje + ' Puedes contactarlo a través de su correo electrónico: ' + email,
            settings.EMAIL_HOST_USER,
            ['godofreddo017@gmail.com'],
            fail_silently=False,
        )
        messages.success(request, "La solicitud fue enviada correctamente")
        return redirect('support')


def check_notifications(request):
    if not request.user.is_authenticated:
        veterinary_logued = Veterinary.objects.get(id=1)
    else:
        veterinary_logued = request.user.veterinary

    if not Client.objects.filter(veterinary=veterinary_logued).exists():
        messages.info(request, 'Registra clientes')

    if not Pet.objects.filter(client__veterinary=veterinary_logued).exists():
        messages.info(request, 'Registra mascotas')

    if not Category.objects.filter(veterinary=veterinary_logued).exists():
        messages.info(request, 'Registra categorias y productos')

    if not Events.objects.filter(veterinary=veterinary_logued).exists():
        messages.info(request, 'Registra tu primer cita')


# region client


@login_required(login_url="login")
def detailClient(request):
    veterinaryLogued = request.user.veterinary
    form = ClientForm(initial={"veterinary": veterinaryLogued})
    if request.method == "POST":
        search_query = request.POST.get("search", "")
        clients = Client.objects.filter(
            Q(name__icontains=search_query) | Q(document__icontains=search_query),
            veterinary=veterinaryLogued
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
            pet_instance = formPet.save(commit=False)
            pet_instance.veterinary = VeterinaryLogued
            pet_instance.save()
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
        if event.name == 'CL':
            name = 'Clinica'
        elif event.name == 'CO':
            name = 'Consulta'
        elif event.name == 'VA':
            name = 'Vacunacion'
        elif event.name == 'GU':
            name = 'Guarderia'
        elif event.name == 'PE':
            name = 'Peluqueria'
        else:
            name = event.name

        out.append(
            {
                "title": f"{event.pet} - {name}",
                "id": event.id,
                "start": event.start.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.start.strftime("%Y-%m-%dT%H:%M:%S"),
                "client": event.pet.client_name,
                "pet": event.pet,
                "room": event.room,
            }
        )

    form = EventForm(veterinary_logued)
    context = {"form": form, "events": out}
    return render(request, "veterinary/registerDate.html", context)


# detail event
@login_required(login_url="login")
def tutorial(request):
    request.user.has_seen_video = False
    request.user.save()
    return redirect("home")


@login_required(login_url="login")
def home(request):
    veterinary_logued = request.user.veterinary
    if not request.user.has_seen_video:
        request.user.has_seen_video = True
        request.user.save()
        play_video = True
    else:
        play_video = False

    if request.method == "POST":
        form = EventForm(veterinary_logued, request.POST)
        if form.is_valid:
            event = form.save(commit=False)
            event.veterinary = veterinary_logued
            if event.start is not None:
                event.save()
                if event.name == 'GU' or event.name == 'PE' or event.name == 'CL':
                    Services.objects.create(
                        pet=event.pet,
                        type=event.name,
                        start=event.start,
                        end=None,
                        details='Detalles adicionales',
                        veterinary_id=veterinary_logued.id
                    )
                return redirect("home")
            else:
                messages.error(request, "La fecha no puede estar vacia, no se guardo el registro")
                return redirect("home")
        else:
            messages.error(request, form.errors)
            return redirect("home")

    all_events_query = Events.objects.select_related("pet__client__veterinary").filter(
        pet__client__veterinary=veterinary_logued
    )
    out = []
    form = EventForm(veterinary_logued)
    for event in all_events_query:
        if event.name == 'CL':
            name = 'Clinica'
        elif event.name == 'CO':
            name = 'Consulta'
        elif event.name == 'VA':
            name = 'Vacunacion'
        elif event.name == 'GU':
            name = 'Guarderia'
        elif event.name == 'PE':
            name = 'Peluqueria'
        else:
            name = event.name

        out.append(
            {
                "title": f"{event.pet} - {name}",
                "id": event.id,
                "start": event.start.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": event.start.strftime("%Y-%m-%dT%H:%M:%S"),
                "client": event.pet.client_name,
                "pet": event.pet,
                "room": event.room,
            }
        )

    context = {
        "events": out,
        "form": form,
        "play_video": play_video,
    }

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
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nameVeterinary = cleaned_data.get("nameVeterinary")
            email = cleaned_data.get("email")
            nit = cleaned_data.get("nit")
            if Veterinary.objects.filter(nameVeterinary=nameVeterinary).exists():
                form.add_error("nameVeterinary", "Esta veterinaria ya se encuentra registrada en nuestro sistema.")
            if Veterinary.objects.filter(email=email).exists():
                form.add_error("email", "El correo electrónico ya está en uso.")
            if Veterinary.objects.filter(nit=nit).exists():
                form.add_error("nit", "El NIT ya está registrado.")
            if not form.errors:
                veterinary = form.save()
                user = User.objects.create(
                    username=nameVeterinary,
                    password=cleaned_data.get("password"),
                    veterinary=veterinary,
                )
                user.set_password(request.POST["password"])
                user.save()
                user.groups.add()
                user.save()
                return redirect("login")
    else:
        form = VeterinaryForm()

    context = {"form": form}
    return render(request, "veterinary/register.html", context)


# endregion

# region product
@login_required(login_url="login")
def detailProduct(request):
    veterinarylogued = request.user.veterinary
    products = Product.objects.filter(veterinary=veterinarylogued)
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
            category = form1.save(commit=False)
            category.veterinary = veterinarylogued
            category.save()
            messages.success(request, "Categoria agregada")
            return HttpResponseRedirect(request.path_info)
        elif form2.is_valid():
            product = form2.save(commit=False)
            product.veterinary = veterinarylogued
            product.save()
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

# region sale
@login_required(login_url="login")
def create_sale(request):
    veterinary_logued = request.user.veterinary
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['cli']
            date = form.cleaned_data['date_joined']

            request.session['sale_data'] = {
                'client_id': client.id,
                'client_name': client.name + " " + client.last_name,
                'client_document': client.document,
                'date': date.strftime('%Y-%m-%d %H:%M:%S %z')
            }
            return redirect('create_sale2')
    else:
        form = SaleForm()
    return render(request, 'veterinary/create_sale.html', {'form': form})


@login_required(login_url="login")
def create_sale2(request):
    sale_data = request.session.get('sale_data')
    print(sale_data)
    if request.method == 'POST':
        cart_json = json.loads(request.body)
        products = cart_json['products']
        total = cart_json['total']
        total_iva = int(cart_json['total_iva'])
        subtotal = total - total_iva
        client_id = sale_data.get('client_id')
        date = sale_data.get('date')

        if len(products) == 0:
            return HttpResponse("No se pueden guardar ventas sin productos")

        total_quantity = sum(int(product['quantity']) for product in products)
        if total_quantity == 0:
            return HttpResponse("No se pueden guardar ventas sin productos con stock")

        sale = Sale.objects.create(
            cli_id=client_id,
            date_joined=date,
            subtotal=Decimal(subtotal),
            iva=total_iva,
            total=Decimal(total)
        )

        for product in products:
            prod = Product.objects.get(id=product['id'])
            prod.stock = F('stock') - int(product['quantity'])
            prod.save()

            if int(product['quantity']) > 0:
                DetSale.objects.create(
                    sale=sale,
                    prod=get_object_or_404(Product, id=product['id']),
                    cant=int(product['quantity']),
                    price=Decimal(product['pvp']),
                    iva=Decimal(product['iva']),
                    subtotal=Decimal(product['subtotal'])
                )
        try:
            del request.session['sale_data']
            return redirect('create_sale')
        except Exception as e:
            print(e)
            return HttpResponse("Error al eliminar los datos de la sesión")

    context = {
        'client_name': sale_data.get('client_name'),
        'client_document': sale_data.get('client_document'),
        'date': sale_data.get('date'),
        'id': sale_data.get('client_id')
    }
    return render(request, 'veterinary/create_sale2.html', context)


@login_required(login_url="login")
@require_GET
def search(request):
    veterinary_logged = request.user.veterinary
    term = request.GET.get('term')
    if term:
        results = Product.objects.filter(Q(veterinary=veterinary_logged) & Q(name__icontains=term))
    else:
        results = Product.objects.filter(veterinary=veterinary_logged)

    data = [{'idProduct': r.id, 'full_name': r.name, 'stock': r.stock, 'pvp': r.pvp} for r in results]
    return JsonResponse({'results': data})



@login_required(login_url="login")
def check_sale_data(request):
    if 'sale_data' not in request.session:
        return JsonResponse({'status': 'not_found'})
    else:
        return JsonResponse({'status': 'found'})


@login_required(login_url="login")
def list_sale(request):
    veterinary_logued = request.user.veterinary
    query = request.GET.get('q')
    sales = Sale.objects.filter(cli__veterinary=veterinary_logued)

    if query:
        sales = sales.filter(Q(id__icontains=query) | Q(cli__document__icontains=query))

    sales = sales.select_related('cli').prefetch_related('detsale_set')

    for sale in sales:
        for det in sale.detsale_set.all():
            det.subtotal = det.cant * (det.price * (1 + det.iva / 100))
            det.subtotal = det.subtotal.quantize(Decimal('0.01'))

    context = {'sales': sales}
    return render(request, 'veterinary/sale_list.html', context)


# endregion

# region services
@login_required(login_url="login")
def detailClinic(request):
    pets = Services.objects.filter(state='Activo', type="CL")
    endService = Services.objects.filter(state='Finalizado', type='CL')
    if request.method == "POST":
        pets = Services.objects.filter(pet__namePet__icontains=request.POST.get("search", ""),
                                       state='Activo')
    context = {'pets': pets, 'endService': endService}
    return render(request, 'veterinary/detailClinic.html', context)


@login_required(login_url="login")
def detailDaycare(request):
    pets = Services.objects.filter(state='Activo', type="GU")
    endService = Services.objects.filter(state='Finalizado', type='GU')
    if request.method == "POST":
        pets = Services.objects.filter(pet__namePet__icontains=request.POST.get("search", ""),
                                       state='Activo')
    context = {'pets': pets, 'endService': endService}
    return render(request, 'veterinary/detailDaycare.html', context)


@login_required(login_url="login")
def detailSalon(request):
    pets = Services.objects.filter(state='Activo', type="PE")
    endService = Services.objects.filter(state='Finalizado', type='PE')
    if request.method == "POST":
        pets = Services.objects.filter(pet__namePet__icontains=request.POST.get("search", ""),
                                       state='Activo')
    context = {'pets': pets, 'endService': endService}
    return render(request, 'veterinary/detailSalon.html', context)


@login_required(login_url="login")
def deleteService(request, id):
    service = Services.objects.get(id=id)
    service.delete()
    return redirect('home')


@login_required(login_url="login")
def updateService(request, id):
    instanceService = Services.objects.get(id=id)
    fecha = instanceService.start
    form = ServiceForm(instance=instanceService)

    if request.method == 'POST':
        formService = ServiceForm(request.POST, instance=instanceService)
        if formService.is_valid():
            service = formService.save(commit=False)
            service.start = instanceService.start
            end_date = formService.cleaned_data.get('end')
            if end_date and end_date < instanceService.start:
                messages.error(request, "La fecha de finalización no puede ser anterior a la fecha de inicio.")
                return redirect("updateService", id=id)
            service.total_time = str((service.end - service.start).days)
            if service.total_time == '0':
                service.total_time = '1'
            service.save()
            return redirect('home')
        else:
            messages.error(request, "No se pudo actualizar el servicio")
            return redirect("updateService", id=id)

    return render(request, 'veterinary/updateService.html', {'form': form, 'fecha': fecha})


# endregion
# regionpdf

def manual_usuario_view(request):
    filename = 'manual_usuario.pdf'
    file = open(filename, 'rb')
    response = FileResponse(file, content_type='application/pdf')
    return response


# endregion

# region reportes
@login_required(login_url="login")
def report_sale(request):
    if request.method == "POST":
        option = request.POST.get('option')
        graphic = generate_chart(option)
        context = {
            'graphic': graphic
        }
        return render(request, 'veterinary/report_sale.html', context)
    return render(request, 'veterinary/report_sale.html', {})


def generate_chart(option):
    if option == 'month':
        # Aquí generas el gráfico de ventas por mes utilizando Matplotlib
        sales_by_month = Sale.objects.annotate(month=TruncMonth('date_joined')).values('month').annotate(
            total=Sum('total')).order_by('month')
        months = [sale['month'].strftime('%b %Y') for sale in sales_by_month]
        totals = [sale['total'] for sale in sales_by_month]
        fig, ax = plt.subplots()
        ax.bar(months, totals)
        ax.set_xlabel('Mes')
        ax.set_ylabel('Total de ventas')
        ax.set_title('Ventas por mes')
        plt.xticks(rotation=25, ha='right')
    elif option == 'category':
        # Aquí generas el gráfico de ventas por categoría utilizando Matplotlib
        sales_by_category = DetSale.objects.values('prod__cat__name').annotate(total=Sum('price')).order_by(
            'prod__cat__name')
        print(sales_by_category)
        categories = [sale['prod__cat__name'] for sale in sales_by_category]
        totals = [sale['total'] for sale in sales_by_category]
        fig, ax = plt.subplots()
        ax.bar(categories, totals)
        ax.set_xlabel('Categoría')
        ax.set_ylabel('Total de ventas')
        ax.set_title('Ventas por categoría')
        plt.xticks(rotation=25, ha='right')
    elif option == 'product':
        # Aquí generas el gráfico de ventas por producto utilizando Matplotlib
        sales_by_product = DetSale.objects.values('prod__name').annotate(total=Sum('price')).order_by('prod__name')
        products = [sale['prod__name'] for sale in sales_by_product]
        totals = [sale['total'] for sale in sales_by_product]
        fig, ax = plt.subplots()
        ax.bar(products, totals)
        ax.set_xlabel('Producto')
        ax.set_ylabel('Total de ventas')
        ax.set_title('Ventas por producto')
        plt.xticks(rotation=15, ha='right')

    # Una vez generado el gráfico, lo conviertes a imagen y lo renderizas en la vista
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic

# endregion





