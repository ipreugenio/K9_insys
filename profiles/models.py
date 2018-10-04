from django.db import models
from datetime import date as d

# Create your models here.
class Users(models.Model):
    SEX = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    POSITION = (
        ('Handler', 'Handler'),
        ('Veterinarian', 'Veterinarian'),
        ('Administrator', 'Administrator')
    )

    CIVILSTATUS = (
        ('Single', 'Single'),
        ('Married', 'Married')
    )

    BLOODTYPE = (
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    )

    HAIRCOLOR = (
        ('Black', 'Black'),
        ('Brown', 'Brown')
    )

    EYECOLOR = (
        ('Black', 'Black'),
        ('Brown', 'Brown')
    )

    SKINCOLOR = (
        ('Light', 'Light'),
        ('Dark', 'Dark'),
        ('Yellow', 'Yellow'),
        ('Brown', 'Brown')
    )

    serial_number = models.CharField('serial_number', max_length=200)
    position = models.CharField('position', choices=POSITION, max_length=200)
    rank = models.CharField('rank', max_length=200)
    firstname = models.CharField('firstname', max_length=200)
    lastname = models.CharField('lastname', max_length=200)
    extensionname = models.CharField('extensionname', max_length=200, default="None")
    middlename = models.CharField('middlename', max_length=200)
    nickname = models.CharField('nickname', max_length=200)
    birthdate = models.DateField('birthdate', blank=True)
    age = models.IntegerField('age', default=0)
    birthplace = models.CharField('birthplace', max_length=200)
    gender = models.CharField('gender', choices=SEX, max_length=200)
    civilstatus = models.CharField('civilstatus', choices=CIVILSTATUS, max_length=200)
    citizenship = models.CharField('citizenship', max_length=200)
    religion = models.CharField('religion', max_length=200)
    bloodtype = models.CharField('bloodtype', choices=BLOODTYPE, max_length=200)
    distinct_feature = models.CharField('distinct_feature', max_length=200)
    haircolor = models.CharField('haircolor', choices=HAIRCOLOR, max_length=200)
    eyecolor = models.CharField('eyecolor', choices=EYECOLOR, max_length=200)
    skincolor = models.CharField('skincolor', choices=SKINCOLOR, max_length=200)
    #profile image dito
    height = models.IntegerField('height')
    weight = models.IntegerField('weight')
    headsize = models.IntegerField('headsize')
    footsize = models.IntegerField('footsize')
    bodybuild = models.CharField('bodybuild', max_length=200)

    def calculate_age(self):
        #delta = dt.now().date() - self.birth_date
        #return delta.days
        today = d.today()
        birthdate = self.birthdate
        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        super(Users, self).save(*args, **kwargs)

class Personal_Info(models.Model):
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    mobile_number = models.IntegerField('mobile_number')
    email_address = models.EmailField('email_address', max_length=200)
    tel_number = models.CharField('tel_number', max_length=200)
    street = models.CharField('street', max_length=200)
    barangay = models.CharField('barangay', max_length=200)
    city = models.CharField('city', max_length=200)
    province = models.CharField('province', max_length=200)
    mother_name = models.CharField('mother_name', max_length=200)
    mother_birthdate = models.DateField('mother_birthdate', max_length=200)
    father_name = models.CharField('father_name', max_length=200)
    father_birthdate = models.DateField('father_birthdate', max_length=200)
    tin = models.IntegerField('tin')
    philhealth = models.IntegerField('philhealth')

