from django.contrib import admin
from .models import Veterinary,Client,Pet,User

admin.site.register(User)
admin.site.register(Veterinary)
admin.site.register(Client)
admin.site.register(Pet)


# Register your models here.
