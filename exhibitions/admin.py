from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import  Izlozba, Kolekcija,Listanft, Portfolio, Pripada

admin.site.register(Izlozba)
admin.site.register(Kolekcija)
admin.site.register(Listanft)
admin.site.register(Portfolio)
admin.site.register(Pripada)

