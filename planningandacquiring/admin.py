from django.contrib import admin
from .models import K9, K9_Father, K9_Mother

# Register your models here.

admin.site.register(K9)
admin.site.register(K9_Father)
admin.site.register(K9_Mother)