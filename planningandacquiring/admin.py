from django.contrib import admin

from .models import K9, K9_Parent, K9_Quantity, K9_Donated, K9_Breed, K9_Supplier, K9_Litter, K9_Mated, Dog_Breed

from training.models import K9_Adopted_Owner

# Register your models here.

admin.site.register(K9)
admin.site.register(K9_Parent)
admin.site.register(K9_Quantity)
admin.site.register(K9_Adopted_Owner)

admin.site.register(Dog_Breed)

admin.site.register(K9_Supplier)
admin.site.register(K9_Breed)
admin.site.register(K9_Litter)
admin.site.register(K9_Mated)
