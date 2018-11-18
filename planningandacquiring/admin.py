from django.contrib import admin
from .models import K9, K9_Parent, K9_Quantity

# Register your models here.

admin.site.register(K9)
admin.site.register(K9_Parent)
admin.site.register(K9_Quantity)
