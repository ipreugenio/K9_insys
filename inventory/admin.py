from django.contrib import admin

from inventory.models import Medicine, Food, Miscellaneous, Medicine_Inventory, Food_Inventory, Miscellaneous_Inventory
from inventory.models import Medicine_Inventory_Count, Food_Inventory_Count, Miscellaneous_Inventory_Count
from inventory.models import Medicine_Received_Trail, Food_Received_Trail, Miscellaneous_Received_Trail
# Register your models here.

admin.site.register(Medicine)
admin.site.register(Food)
admin.site.register(Miscellaneous)
admin.site.register(Medicine_Inventory)
admin.site.register(Food_Inventory)
admin.site.register(Miscellaneous_Inventory)
admin.site.register(Medicine_Inventory_Count)
admin.site.register(Food_Inventory_Count)
admin.site.register(Miscellaneous_Inventory_Count)
admin.site.register(Medicine_Received_Trail)
admin.site.register(Food_Received_Trail)
admin.site.register(Miscellaneous_Received_Trail)
