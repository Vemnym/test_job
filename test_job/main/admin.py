from django.contrib import admin
from .models import *

# Register your models here.


class DealsAdmin(admin.ModelAdmin):
    list_display = ("id", 'customer', 'item', 'total', 'quantity', 'date')


admin.site.register(Deals, DealsAdmin)