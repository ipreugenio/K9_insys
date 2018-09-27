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
    dose = models.DecimalField('dose', default=0, max_digits=50, decimal_places=2)
    mass = models.CharField('mass', choices=MASS, max_length=10, default='mg')
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.medicine
    
    def dosage(self):
        return str(self.dose) +' ' + str(self.mass)

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
        ('Both', 'Both'),
    )

    food = models.CharField(max_length=100)
    foodtype = models.CharField('foodtype', choices=FOODTYPE, max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.food

class Food_Inventory(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)

class Food_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Food_Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)

#Equipment
class Equipment(models.Model):
    equipment = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.equipment

class Equipment_Inventory(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)

class Equipment_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Equipment_Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)