from django.db import models
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import date as d
from inventory.models import Medicine, Miscellaneous, Food
from profiles.models import User

class Date(models.Model):
    date_from = models.DateField('date_from', null=True)
    date_to = models.DateField('date_to', null=True)

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


    serial_number = models.CharField('serial_number', max_length=200 , default='Unassigned Serial Number')
    name = models.CharField('name', max_length=200)
    handler = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    breed = models.CharField('breed', choices=BREED, max_length=200)
    sex = models.CharField('sex', choices=SEX, max_length=200, default="Unspecified")
    color = models.CharField('color', choices=COLOR, max_length=200, default="Unspecified")
    birth_date = models.DateField('birth_date', null=True)
    age = models.IntegerField('age', default = 0)
    source = models.CharField('source', max_length=200, default="Not Specified")
    year_retired = models.DateField('year_retired', null=True)
    assignment = models.CharField('assignment', max_length=200, default="None")
    status = models.CharField('status', max_length=200, default="Material Dog")
    training_status = models.CharField('training_status', max_length=200, default="Unclassified")
    training_level = models.CharField('training_level', max_length=200, default="Stage 0")
    training_count = models.IntegerField('training_count', default = 0)
    capability = models.CharField('capability', max_length=200, default="None")
    microchip = models.CharField('microchip', max_length=200, default = 'Unassigned Microchip')

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
        if self.age == 9:
            self.training_status = 'Due-For-Retirement'
            self.status = 'Light Duty'
        elif self.age == 10:
            self.training_status = 'Retired'
            self.year_retired = self.birth_date + td(days=(10*365))
            self.status = 'Retired'
        else:
            pass
        # Serial Numbers and Microchips are given after training
        # lead_zero = str(self.id).zfill(5)
        # serial_number = '#%s' % (lead_zero)
        # self.serial_number = str(serial_number)
        super(K9, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.name) + " : " + str(self.serial_number)


class K9_Past_Owner(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    first_name = models.CharField('first_name', max_length=200)
    middle_name = models.CharField('middle_name', max_length=200)
    last_name = models.CharField('last_name', max_length=200)
    address = models.CharField('address', max_length=200)
    sex = models.CharField('sex', choices=SEX, max_length=200, default="Unspecified")
    birth_date = models.DateField('birth_date', null=True)
    email = models.EmailField('email', max_length=200, default = "not specified")
    contact_no = models.CharField('contact_no', max_length=200, default = "not specified")

    def __str__(self):
        return str(self.first_name) +' '+ str(self.middle_name) + ' ' + str(self.last_name)

class K9_New_Owner(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    first_name = models.CharField('first_name', max_length=200)
    middle_name = models.CharField('middle_name', max_length=200)
    last_name = models.CharField('last_name', max_length=200)
    address = models.CharField('address', max_length=200)
    sex = models.CharField('sex', choices=SEX, max_length=200, default="Unspecified")
    #age = models.IntegerField('age', default = 0)
    birth_date = models.DateField('birth_date', null=True)
    email = models.EmailField('email', max_length=200)
    contact_no = models.CharField('contact_no', max_length=200)

    # def calculate_age(self):
    #     today = d.today()
    #     birthdate = self.birth_date
    #     bday = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    #     if bday < 1:
    #         bday = 0
    #     return bday

    # def save(self, *args, **kwargs):
    #     self.age = self.calculate_age()
    #     super(K9_New_Owner, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.middle_name) + ' ' + str(self.last_name)

class K9_Donated(models.Model):
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)
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
    date_bought = models.DateField('date_bought', null=True)


#TODO Add inventory attr > How many dogs each item can cater
class Budget_allocation(models.Model):
    k9_request_forecast = models.IntegerField('k9_request_forecast', default=0)
    k9_needed_for_demand = models.IntegerField('k9s_needed_for_demand', default=0)
    k9_cuurent = models.IntegerField('k9_current', default=0)
    #training_cost
    #grand_total
    date_created = models.DateField('date_created', auto_now_add=True)
    date_tobe_budgeted = models.DateField('date_tobe_budgeted', null=True)

class Budget_food(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, blank=True, null=True) #1 sack per dog per month
    quantity = models.IntegerField('quantity', default=0)
    price = models.DecimalField('price', default=0, max_digits=50, decimal_places=2,)
    budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)

class Budget_equipment(models.Model):
    equipment = models.ForeignKey(Miscellaneous, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField('quantity', default=0)
    price = models.DecimalField('price', default=0, max_digits=50, decimal_places=2,)
    budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)

class Budget_medicine(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField('quantity', default = 0)
    price = models.DecimalField('price', default=0, max_digits=50, decimal_places=2,)
    budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)

class Dog_Breed(models.Model):
    SKILL = (
        ('NDD', 'NDD'),
        ('EDD', 'EDD'),
        ('SAR', 'SAR')
    )


    breed = models.CharField('breed', max_length=200, null=True)
    life_span = models.CharField('life_span', max_length=200, null=True)
    temperament = models.CharField('temperament', max_length=200, null=True)
    colors = models.CharField('colors', max_length=200, null=True)
    weight = models.CharField('weight', max_length=200, null=True)
    male_height = models.CharField('male_height', max_length=200, null=True)
    female_height = models.CharField('female_height', max_length=200, null=True)
    skill_recommendation = models.CharField('skill_recommendation', choices=SKILL, max_length=200, null=True)
