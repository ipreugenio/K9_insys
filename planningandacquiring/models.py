from django.db import models
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import date as d


# Create your models here.

#class K9_price(models.Model):


class K9(models.Model):
    SEX = (
        ('M', 'Male'),
        ('F', 'Female')
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
    #handler = models.ForeignKey(Handler, on_delete=models.CASCADE)
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

class Medicine(models.Model):
    name = models.CharField('name', max_length=200)
    description = models.CharField('description', max_length=200)

class Medicine_Assignment(models.Model):
    milligram = models.DecimalField('milligram', decimal_places=3, max_digits=12, default=0)
    K9 = models.ForeignKey(K9, on_delete=models.CASCADE)

class Miscellaneous(models.Model):
    name = models.CharField('name', max_length=200)
    description = models.CharField('description', max_length=200)

