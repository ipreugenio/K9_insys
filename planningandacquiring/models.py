from django.db import models
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import date as d
from inventory.models import Medicine, Miscellaneous, Food

from profiles.models import User

class Date(models.Model):
    date_from = models.DateField('date_from', blank=True, null=True)
    date_to = models.DateField('date_to', blank=True, null=True)

class K9(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    COLOR = (
        ('Brown', 'Brown'),
        ('Black', 'Black'),
        ('Gray', 'Gray'),
        ('White', 'White'),
        ('Yellow', 'Yellow'),
        ('Mixed', 'Mixed')
    )

    BREED = (

        ('Belgian Malinois', 'Belgian Malinois'),
        ('Dutch Sheperd', 'Dutch Sheperd'),
        ('German Sheperd', 'German Sheperd'),
        ('Golden Retriever', 'Golden Retriever'),
        ('Jack Russel', 'Jack Russel'),
        ('Labrador Retriever', 'Labrador Retriever'),
        ('Mixed', 'Mixed'),
    )

    #TODO Dog sizes based on breed, see docs
    serial_number = models.CharField('serial_number', max_length=200 , default='Unassigned Serial Number')
    name = models.CharField('name', max_length=200)
    #handler = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    breed = models.CharField('breed', choices=BREED, max_length=200)
    sex = models.CharField('sex', choices=SEX, max_length=200, default="Unspecified")
    color = models.CharField('color', choices=COLOR, max_length=200, default="Unspecified")
    birth_date = models.DateField('birth_date', blank=True)
    age = models.IntegerField('age', default = 0)
    source = models.CharField('source', max_length=200, default="Not Specified")
    year_retired = models.DateField('year_retired', blank=True, null=True)
    assignment = models.CharField('assignment', max_length=200, default="None")
    status = models.CharField('status', max_length=200, default="Material Dog")
    training_status = models.CharField('training_status', max_length=200, default="Unclassified")
    training_level = models.CharField('training_level', max_length=200, default="Stage 0")
    capability = models.CharField('capability', max_length=200, default="None")
    microchip = models.CharField('microchip', max_length=200, default = 'Unassigned Microchip')
    
    def __str__(self):
        return str(self.name) + " : " + str(self.serial_number)

    def calculate_age(self):
        #delta = dt.now().date() - self.birth_date
        #return delta.days
        today = d.today()
        birthdate = self.birth_date
        bday = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if bday < 1:
            bday = 0
        return bday

    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        self.training_id = self.id
        '''
        Serial Numbers and Microchips are given after training
        lead_zero = str(self.id).zfill(5)
        serial_number = '#%s' % (lead_zero)
        self.serial_number = str(serial_number)
        '''
        super(K9, self).save(*args, **kwargs)


class K9_Past_Owner(models.Model):
    first_name = models.CharField('first_name', max_length=200)
    middle_name = models.CharField('middle_name', max_length=200)
    last_name = models.CharField('last_name', max_length=200)
    address = models.CharField('address', max_length=200)
    email = models.EmailField('email', max_length=200, default = "not specified")
    contact_no = models.CharField('contact_no', max_length=200, default = "not specified")

    def __str__(self):
        return str(self.first_name) +' '+ str(self.middle_name) + ' ' + str(self.last_name)

class K9_New_Owner(models.Model):
    first_name = models.CharField('first_name', max_length=200)
    middle_name = models.CharField('middle_name', max_length=200)
    last_name = models.CharField('last_name', max_length=200)
    address = models.CharField('address', max_length=200)
    email = models.EmailField('email', max_length=200)
    contact_no = models.CharField('contact_no', max_length=200)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.middle_name) + ' ' + str(self.last_name)

class K9_Donated(models.Model):
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE)
    owner = models.ForeignKey(K9_Past_Owner, on_delete=models.CASCADE)
    date_donated = models.DateField('date_donated', auto_now_add=True)

    def __str__(self):
        return str(self.k9)

class K9_Adopted(models.Model):
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE)
    owner = models.ForeignKey(K9_New_Owner, on_delete=models.CASCADE)
    date_adopted = models.DateField('date_adopted', auto_now_add=True)

    def __str__(self):
        return str(self.k9)


class K9_Parent(models.Model):
    mother = models.ForeignKey(K9, on_delete=models.CASCADE, related_name= "mother", blank=True, null=True)
    father = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="father", blank=True, null=True)
    offspring = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)

class K9_Quantity(models.Model):
    quantity = models.IntegerField('quantity', default=0)
    date_bought = models.DateField('date_bought', blank=True, null=True)


'''

Demand = k9s deployed and requested
all_current_non deployed
k9s near retirement

equipment
equipment_reusable

maintenance requirement left

>>>> TODO >>

demand[] = k9s_deployed + k9s_requested
forecasted_demand = forecast(demand[])
k9s_needed = forecasted_demand - k9_undeployed
current_relevant_k9 = (all_k9s - (retired + failed))
k9s_to_be_budgeted = forecasted_demand + current_relevant_k9
k9s_to_be_bought = k9s_to_be_budgeted - k9s_birthed

needed_equipment[] = forecasted_equipment[] - reusable_equipment[] + broken/missing
needed_medicine[] = forecasted_medicine[] - current_medicine[]
'''

#TODO Add inventory attr > How many dogs each item can cater
class Budget_allocation(models.Model):
    k9s_needed = models.IntegerField('k9s_needed', default=1)
    date_created = models.DateField('date_created', auto_now_add=True)
    date_tobe_budgeted = models.DateField('date_tobe_budgeted')
    #k9s_tobe_trained
    #k9s_tobe_bought
    #training_cost
    #grand_total

class Budget_food(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, blank=True, null=True) #1 sack per dog per month
    quantity = models.IntegerField('quantity', default=1)
    budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)

class Budget_equipment(models.Model):
    equipment = models.ForeignKey(Miscellaneous, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField('quantity', default=1)
    budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)

class Budget_medicine(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField('quantity', default = 1)
    budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)
