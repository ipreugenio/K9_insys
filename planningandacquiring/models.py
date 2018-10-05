from django.db import models
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import date as d

# Create your models here.

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

    serial_number = models.CharField('serial_number', max_length=200)
    name = models.CharField('name', max_length=200)
    #handler = models.ForeignKey(Handler, on_delete=models.CASCADE)
    breed = models.CharField('breed', max_length=200)
    sex = models.CharField('sex', choices=SEX, max_length=200, default="Unspecified")
    color = models.CharField('color', choices=COLOR, max_length=200, default="Unspecified")
    birth_date = models.DateField('birth_date', blank=True)
    age = models.IntegerField('age', default = 0)
    year_retired = models.DateField('year_retired', blank=True, null=True)
    assignment = models.CharField('assignment', max_length=200, default="None")
    status = models.CharField('status', max_length=200, default="unclassified")
    microchip = models.CharField('microchip', max_length=200)
    

    def __str__(self):
        return str(self.name)

    def calculate_age(self):
        #delta = dt.now().date() - self.birth_date
        #return delta.days
        today = d.today()
        birthdate = self.birth_date
        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        super(K9, self).save(*args, **kwargs)

#TODO
#FAMILY TREE - MOTHER AND FATHER

class Medicine(models.Model):
    name = models.CharField('name', max_length=200)
    description = models.CharField('description', max_length=200)

class Medicine_Assignment(models.Model):
    milligram = models.DecimalField('milligram', decimal_places=3, max_digits=12, default=0)
    K9 = models.ForeignKey(K9, on_delete=models.CASCADE)

class Equipment(models.Model):
    name = models.CharField('name', max_length=200)
    description = models.CharField('description', max_length=200)

