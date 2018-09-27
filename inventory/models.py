from django.db import models
from planningandacquiring.models import Medicine, Equipment
# Create your models here.

#Medicine
class Medicine(models.Model):
    MASS = (
        ('mg', 'mg'),
        ('mL', 'mL'),
    )

    medicine = models.CharField(max_length=100)
    dose = models.IntegerField('dose', default=0)
    mass = models.CharField('mass', choices=MASS, max_length=10, default='mg')

class Medicine_Inventory(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)

class Medicine_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Medicine_Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)

#Food
class Food(models.Model):
    FOODTYPE = (
        ('Adult Dog Food', 'Adult Dog Food'),
        ('Puppy Dog Food', 'Puppy Dog Food'),
    )

    food = models.CharField(max_length=100)
    foodtype = models.CharField('foodtype', choices=FOODTYPE, max_length=50, default='Adult Dog Food')

class Food_Inventory(models.Model):
    medicine = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)

class Food_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Food_Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)

#Equipment
class Equipment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField('quantity', default=0)

class Equipment_Inventory(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)

class Equipment_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Equipment_Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)