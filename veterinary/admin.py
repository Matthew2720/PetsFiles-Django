from django.contrib import admin
from .models import Veterinary,Client,Pet,User,Date

admin.site.register(User)
admin.site.register(Veterinary)
admin.site.register(Client)
admin.site.register(Pet)
admin.site.register(Date)


# Register your models here.
