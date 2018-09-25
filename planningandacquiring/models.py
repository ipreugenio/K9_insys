from django.db import models

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
    year_retired = models.DateField('year_retired', blank=True)
    assignment = models.CharField('assignment', max_length=200)
    microchip = models.CharField('microchip', max_length=200)

class Medicine(models.Model):
    name = models.CharField('name', max_length=200)
    description = models.CharField('description', max_length=200)

class Medicine_Assignment(models.Model):
    milligram = models.DecimalField('milligram', decimal_places=3, max_digits=12, default=0)
    K9 = models.ForeignKey(K9, on_delete=models.CASCADE)

class Equipment(models.Model):
    name = models.CharField('name', max_length=200)
    description = models.CharField('description', max_length=200)
