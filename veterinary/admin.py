from django.contrib import admin
from .models import Veterinary,Client,Pet,User,Events
from .models import Category,Product,Sale,DetSale

admin.site.register(User)
admin.site.register(Veterinary)
admin.site.register(Client)
admin.site.register(Pet)
admin.site.register(Events)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(DetSale)
