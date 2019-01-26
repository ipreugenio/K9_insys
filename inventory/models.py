from django.db import models

from profiles.models import User
# Create your models here.

#TODO inventory information before

#Medicine
class Medicine(models.Model):
    UOM = (
        ('mg', 'mg'),
        ('mL', 'mL'),
        ('suspension', 'suspension'),
    )
    TYPE = (
        ('Tablet', 'Tablet'),
        ('Capsule', 'Capsule'),
        ('Bottle', 'Bottle'),
        ('Vaccine', 'Vaccine'),
    )
    medicine = models.CharField(max_length=100)
    med_type = models.CharField('med_type', choices=TYPE, max_length=50, default='Drug')
    dose = models.DecimalField('dose', default=0, max_digits=50, decimal_places=2)
    uom = models.CharField('uom', max_length=10, default='unit', blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    price = models.DecimalField('price', max_digits=50, decimal_places=2, null=True)
    used_yearly = models.IntegerField('used_yearly', default=0)
    duration = models.IntegerField('duration', default=0)
    medicine_fullname = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.medicine_fullname

    def dosage(self):
        return str(self.dose) +' ' + str(self.uom)

    def save(self, *args, **kwargs):
        self.medicine_fullname = str(self.medicine) +' - ' + str(self.dose) + str(self.uom)
        if self.med_type == 'Vaccine':
            self.used_yearly = 365 / int(self.duration)
        super(Medicine, self).save(*args, **kwargs)


class Medicine_Inventory(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)

    def __str__(self):
        return self.medicine.medicine_fullname
#TODO
# add user
class Medicine_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Medicine_Inventory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)

    def __str__(self):
        return self.inventory.medicine.medicine_fullname


class Medicine_Received_Trail(models.Model):
    inventory = models.ForeignKey(Medicine_Inventory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField('quantity', default=0)
    date_received = models.DateField('date_received', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)
    expiration_date = models.DateField('expiration_date', null=True, blank=True)
    
    def __str__(self):
        return self.inventory.medicine.medicine_fullname

class Medicine_Subtracted_Trail(models.Model):
    inventory = models.ForeignKey(Medicine_Inventory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, default="")
    price = models.DecimalField('price', max_digits=50, decimal_places=2, default=0)
    quantity = models.IntegerField('quantity', default=0)
    date_subtracted = models.DateField('date_subtracted', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)

    def __str__(self):
        return self.inventory.medicine.medicine_fullname

    def save(self, *args, **kwargs):
        self.name = str(self.inventory.medicine.medicine_fullname)
        self.price = str(self.inventory.medicine.price)
        super(Medicine_Subtracted_Trail, self).save(*args, **kwargs)
#Food
class Food(models.Model):
    FOODTYPE = (
        ('Adult Dog Food', 'Adult Dog Food'),
        ('Puppy Dog Food', 'Puppy Dog Food'),
    )

    food = models.CharField(max_length=100)
    foodtype = models.CharField('foodtype', choices=FOODTYPE, max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField('price', max_digits=50, decimal_places=2, null=True)

    def __str__(self):
        return self.food

class Food_Inventory(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)

    def __str__(self):
        return self.food.food

#TODO
# add user
class Food_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Food_Inventory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)

    def __str__(self):
        return self.inventory.food.food

class Food_Received_Trail(models.Model):
    inventory = models.ForeignKey(Food_Inventory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField('quantity', default=0)
    date_received = models.DateField('date_received', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)

    def __str__(self):
        return self.inventory.food.food

class Food_Subtracted_Trail(models.Model):
    inventory = models.ForeignKey(Food_Inventory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField('quantity', default=0)
    date_subtracted = models.DateField('date_subtracted', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)

    def __str__(self):
        return self.inventory.food.food

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

    TYPE = (
        ('Equipment', 'Equipment'),
        ('Vet Supply', 'Vet Supply'),
        ('Others', 'Others'),
    )

    miscellaneous = models.CharField(max_length=100)
    uom = models.CharField(max_length=100, choices=UOM, default="pack")
    misc_type = models.CharField(max_length=100, choices=TYPE, default="Equipment")
    description = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField('price', max_digits=50, decimal_places=2, null=True)

    def __str__(self):
        return self.miscellaneous

class Miscellaneous_Inventory(models.Model):
    miscellaneous = models.ForeignKey(Miscellaneous, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)

    def __str__(self):
        return self.miscellaneous.miscellaneous

#TODO
# add user
class Miscellaneous_Inventory_Count(models.Model):
    inventory = models.ForeignKey(Miscellaneous_Inventory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField('quantity', default=0)
    date_counted = models.DateField('date_counted', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)

    def __str__(self):
        return self.inventory.miscellaneous.miscellaneous

class Miscellaneous_Received_Trail(models.Model):
    inventory = models.ForeignKey(Miscellaneous_Inventory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField('quantity', default=0)
    date_received = models.DateField('date_received', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)

    def __str__(self):
        return self.inventory.miscellaneous.miscellaneous

class Miscellaneous_Subtracted_Trail(models.Model):
    inventory = models.ForeignKey(Miscellaneous_Inventory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField('quantity', default=0)
    date_subtracted = models.DateField('date_subtracted', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)

    def __str__(self):
        return self.inventory.miscellaneous.miscellaneous

class DamagedEquipemnt(models.Model):
    CONCERN = (
        ('Broken', 'Broken'),
        ('Lost', 'Lost'),
        ('Stolen', 'Stolen'),
    )

    inventory = models.ForeignKey(Miscellaneous, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField('quantity', default=0)
    concern = models.CharField('concern', max_length=100, choices=CONCERN)
    date = models.DateField('date', auto_now_add=True)
    time = models.TimeField('time', auto_now_add=True, blank=True)

    def __str__(self):
        return self.inventory.miscellaneous
