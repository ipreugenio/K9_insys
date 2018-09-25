from django.db import models
from planningandacquiring.models import Medicine, Equipment
# Create your models here.

#Medicine
class Medicine_Inventory(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)

class Medicine_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Medicine_Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)

#Equipment
class Equipment_Inventory(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)

class Equipment_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Equipment_Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)