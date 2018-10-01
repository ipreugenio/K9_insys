from django.contrib import admin

from inventory.models import Medicine, Food, Equipment
# Register your models here.

admin.site.register(Medicine)
admin.site.register(Food)
admin.site.register(Equipment)