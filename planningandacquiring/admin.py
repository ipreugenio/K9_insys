from django.contrib import admin
from .models import K9, K9_Parent, K9_Quantity, K9_Past_Owner, K9_New_Owner, K9_Donated, K9_Adopted

# Register your models here.

admin.site.register(K9)
admin.site.register(K9_Parent)
admin.site.register(K9_Quantity)
admin.site.register(K9_Past_Owner)
admin.site.register(K9_New_Owner)
admin.site.register(K9_Donated)
admin.site.register(K9_Adopted)
