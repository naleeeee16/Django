from django.contrib import admin

# Register your models here.
from .models import  Administrator, Zahtevzaregistraciju, Korisnik

admin.site.register(Administrator)
admin.site.register(Korisnik)
admin.site.register(Zahtevzaregistraciju)