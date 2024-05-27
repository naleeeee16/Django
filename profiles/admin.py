from django.contrib import admin

from .models import  Kolekcionar,Kreator, Kupac , Registrovanikorisnik

admin.site.register(Registrovanikorisnik)
admin.site.register(Kolekcionar)
admin.site.register(Kreator)
admin.site.register(Kupac)