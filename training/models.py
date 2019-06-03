from django.db import models
from planningandacquiring.models import K9
from profiles.models import User
from deployment.models import Location

from datetime import datetime as dt
from datetime import timedelta as td
from datetime import date as d
# Create your models here.

class K9_Genealogy(models.Model):
    o = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)
    m = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="m", blank=True, null=True)
    f = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="f", blank=True, null=True)
    depth = models.IntegerField('depth',default=0) # family tree level
    zero = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="zero", blank=True, null=True) #latest born

class K9_Handler(models.Model):
    handler = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "handler", blank=True, null=True)
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="k9", blank=True, null=True)
    deployment_area = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="deployment_area", blank=True, null=True)

    def __str__(self):
        # handler = User.objects.get(id=self.handler.id)
        # k9 = K9.objects.get(id=self.k9.id)
        # handler_name = str(handler)
        # k9_name = k9.name
        return str(handler) + " : " + str(k9.name)

class Training(models.Model):
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)
    training = models.CharField('training', max_length=50, default="None")
    stage = models.CharField('stage', max_length=200, default="Stage 0")
    stage1_1 = models.IntegerField('stage1_1', blank=True, null=True, default=0)
    stage1_2 = models.IntegerField('stage1_2', blank=True, null=True, default=0)
    stage1_3 = models.IntegerField('stage1_3', blank=True, null=True, default=0)
    stage2_1 = models.IntegerField('stage2_1', blank=True, null=True, default=0)
    stage2_2 = models.IntegerField('stage2_2', blank=True, null=True, default=0)
    stage2_3 = models.IntegerField('stage2_3', blank=True, null=True, default=0)
    stage3_1 = models.IntegerField('stage3_1', blank=True, null=True, default=0)
    stage3_2 = models.IntegerField('stage3_2', blank=True, null=True, default=0)
    stage3_3 = models.IntegerField('stage3_3', blank=True, null=True, default=0)
    grade = models.IntegerField('grade', blank=True, null=True)
    remarks = models.CharField('remarks', max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.k9) +' - ' + str(self.training) +' : ' + str(self.stage)

class K9_Adopted_Owner(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField('first_name', max_length=200)
    middle_name = models.CharField('middle_name', max_length=200)
    last_name = models.CharField('last_name', max_length=200)
    address = models.CharField('address', max_length=200)
    sex = models.CharField('sex', choices=SEX, max_length=200, default="Unspecified")
    age = models.IntegerField('age', default = 0)
    birth_date = models.DateField('birth_date')
    email = models.EmailField('email', max_length=200)
    contact_no = models.CharField('contact_no', max_length=200)
    date_adopted = models.DateField('date_adopted', auto_now_add=True)

    def calculate_age(self):
        today = d.today()
        birthdate = self.birth_date
        bday = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if bday < 1:
            bday = 0
        return bday

    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        super(K9_Adopted_Owner, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.middle_name) + ' ' + str(self.last_name)

class Record_Training(models.Model):
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE)
    handler = models.ForeignKey(User, on_delete=models.CASCADE)
    on_leash = models.BooleanField(default=False)
    off_leash = models.BooleanField(default=False)
    obstacle_course = models.BooleanField(default=False)
    panelling = models.BooleanField(default=False)
    port_plant = models.CharField('port_plant', default="", max_length=200)
    port_find = models.CharField('port_find', default="", max_length=200)
    port_time = models.CharField('port_time', default="", max_length=200)
    building_plant = models.CharField('building_plant', default="", max_length=200)
    building_find = models.CharField('building_find', default="", max_length=200)
    building_time = models.CharField('building_time', default="", max_length=200)
    vehicle_plant = models.CharField('vehicle_plant', default="", max_length=200)
    vehicle_find = models.CharField('vehicle_find', default="", max_length=200)
    vehicle_time = models.CharField('vehicle_time', default="", max_length=200)
    baggage_plant = models.CharField('baggage_plant', default="", max_length=200)
    baggage_find = models.CharField('baggage_find', default="", max_length=200)
    baggage_time = models.CharField('baggage_time', default="", max_length=200)
    others_plant = models.CharField('others_plant', default="", max_length=200)
    others_find = models.CharField('others_find', default="", max_length=200)
    others_time = models.CharField('others_time', default="", max_length=200)
    daily_rating = models.CharField('daily_rating', default="", max_length=200)
    MARSEC = models.BooleanField(default=False)
    MARLEN = models.BooleanField(default=False)
    MARSAR = models.BooleanField(default=False)
    MAREP = models.BooleanField(default=False)
    morning_feed = models.CharField('morning_feed', default="", max_length=200)
    evening_feed = models.CharField('evening_feed', default="", max_length=200)
    date_today = models.DateField('date_today', auto_now_add = True)