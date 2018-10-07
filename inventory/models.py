from django.db import models
from planningandacquiring.models import Medicine, Miscellaneous
# Create your models here.

#Medicine
class Medicine(models.Model):
    UOM = (
        ('mg', 'mg'),
        ('mL', 'mL'),
    )
    medicine = models.CharField(max_length=100)
    dose = models.DecimalField('dose', default=0, max_digits=50, decimal_places=2)
    uom = models.CharField('uom', choices=UOM, max_length=10, default='mg')
    description = models.CharField(max_length=100, blank=True, null=True)
    medicine_fullname = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.medicine
    
    def dosage(self):
        return str(self.dose) +' ' + str(self.uom)
        
    def save(self, *args, **kwargs):
        self.medicine_fullname = str(self.medicine) +' ' + str(self.dose) + str(self.uom) 
        super(Medicine, self).save(*args, **kwargs)
        

class Medicine_Inventory(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)

    def __str__(self):
        return self.medicine

#TODO
# add user
class Medicine_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Medicine_Inventory, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)

    def __str__(self):
        return self.inventory

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

    def __str__(self):
        return self.food

#TODO
# add user
class Food_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Food_Inventory, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)

    def __str__(self):
        return self.inventory

#Miscellaneous
class Miscellaneous(models.Model):
    UOM = (
        ('pc', 'pc'),
        ('pack', 'pack'),
        ('box', 'box'),
        ('roll', 'roll'),
        ('can', 'can'),
        ('bottle', 'bottle'),
        ('tube', 'tube'),
    )

    miscellaneous = models.CharField(max_length=100)
    uom = models.CharField(max_length=100, choices=UOM)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.miscellaneous

class Miscellaneous_Inventory(models.Model):
    miscellaneous = models.ForeignKey(Miscellaneous, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
 
    def __str__(self):
        return self.miscellaneous

#TODO
# add user
class Miscellaneous_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Miscellaneous_Inventory, on_delete=models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)

    def __str__(self):
        return self.inventory