from django.contrib import admin
from .models import Veterinary,Client,Pet,User,Events

admin.site.register(User)
admin.site.register(Veterinary)
admin.site.register(Client)
admin.site.register(Pet)
admin.site.register(Events)
