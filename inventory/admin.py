from django.contrib import admin

from inventory.models import Medicine, Food, Equipment, Medicine_Inventory, Food_Inventory, Equipment_Inventory
from inventory.models import Medicine_Inventory_Count, Food_Inventory_Count, Equipment_Inventory_Count
# Register your models here.

admin.site.register(Medicine)
admin.site.register(Food)
admin.site.register(Equipment)
admin.site.register(Medicine_Inventory)
admin.site.register(Food_Inventory)
admin.site.register(Equipment_Inventory)
admin.site.register(Medicine_Inventory_Count)
admin.site.register(Food_Inventory_Count)
admin.site.register(Equipment_Inventory_Count)
