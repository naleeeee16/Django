from django.contrib import admin

# Register your models here.
from .models import Nft, Ocena

admin.site.register(Nft)
admin.site.register(Ocena)