from django.db import models
from planningandacquiring.models import K9
from profiles.models import User
from inventory.models import Medicine, Miscellaneous, Medicine_Inventory
from profiles.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
# Create your models here.

class Health(models.Model):
    dog = models.ForeignKey(K9, on_delete=models.CASCADE)
    date = models.DateField('date', auto_now_add=True)
    problem = models.TextField('problem', max_length=200)
    treatment = models.TextField('treatment', max_length=200)
    status = models.CharField('status', max_length=200, default="Pending")
    veterinary = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id) + ': ' + str(self.date) +' - ' + str(self.dog.name)

class HealthMedicine(models.Model):
    health = models.ForeignKey(Health, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    dosage = models.CharField('dosage', max_length=200, default="")

    def __str__(self):
        return str(self.id) + ': ' + str(self.health.date) + '-' + str(self.health.dog.name)

class PhysicalExam(models.Model):
    EXAMSTATUS = (
        ('Normal', 'Normal'),
        ('Abnormal', 'Abnormal'),
        ('Not Examined', 'Not Examined'),
    )

    dog = models.ForeignKey(K9, on_delete=models.CASCADE)
    veterinary = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cage_number = models.IntegerField('dog', default = "0")
    general_appearance = models.CharField('general_appearance', choices=EXAMSTATUS, max_length=200)
    integumentary = models.CharField('integumentary', choices=EXAMSTATUS, max_length=200)
    musculo_skeletal = models.CharField('musculo_skeletal', choices=EXAMSTATUS, max_length=200)
    respiratory = models.CharField('respiratory', choices=EXAMSTATUS, max_length=200)
    genito_urinary = models.CharField('genito_urinary', choices=EXAMSTATUS, max_length=200)
    nervous = models.CharField('nervous', choices=EXAMSTATUS, max_length=200)
    circulatory = models.CharField('circulatory', choices=EXAMSTATUS, max_length=200)
    digestive = models.CharField('digestive', choices=EXAMSTATUS, max_length=200)
    mucous_membrances = models.CharField('mucous_membrances', choices=EXAMSTATUS, max_length=200)
    lymph_nodes = models.CharField('lymph_nodes', choices=EXAMSTATUS, max_length=200)
    eyes = models.CharField('eyes', choices=EXAMSTATUS, max_length=200)
    ears = models.CharField('ears', choices=EXAMSTATUS, max_length=200)
    remarks = models.TextField('remarks', max_length=200)
    date = models.DateField('date', auto_now_add=True)
    date_next_exam = models.DateField('date_next_exam', null=True, blank=True)

    def __str__(self):
        return str(self.date) + ': ' + str(self.dog.name)

#TODO
#add vet user
class VaccinceRecord(models.Model):
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, null=True, blank=True)
    deworming_1 = models.BooleanField(default=False)     #2weeks
    deworming_2 = models.BooleanField(default=False)     #4weeks
    deworming_3 = models.BooleanField(default=False)     #6weeks
    deworming_4 = models.BooleanField(default=False)     #9weeks
   
    dhppil_cv_1 = models.BooleanField(default=False)     #6weeks
    dhppil_cv_2 = models.BooleanField(default=False)     #9weeks
    dhppil_cv_3 = models.BooleanField(default=False)     #12weeks
    
    heartworm_1 = models.BooleanField(default=False)     #6weeks
    heartworm_2 = models.BooleanField(default=False)     #10weeks
    heartworm_3 = models.BooleanField(default=False)     #14weeks
    heartworm_4 = models.BooleanField(default=False)     #18weeks
    heartworm_5 = models.BooleanField(default=False)     #22weeks
    heartworm_6 = models.BooleanField(default=False)     #26weeks
    heartworm_7 = models.BooleanField(default=False)     #30weeks
    heartworm_8 = models.BooleanField(default=False)     #34weeks
   
    anti_rabies = models.BooleanField(default=False)     #12weeks

    bordetella_1 = models.BooleanField(default=False)    #8weeks
    bordetella_2 = models.BooleanField(default=False)    #11weeks

    dhppil4_1 = models.BooleanField(default=False)       #15weeks
    dhppil4_2 = models.BooleanField(default=False)       #18weeks

    tick_flea_1 = models.BooleanField(default=False)     #8weeks
    tick_flea_2 = models.BooleanField(default=False)     #12weeks
    tick_flea_3 = models.BooleanField(default=False)     #16weeks
    tick_flea_4 = models.BooleanField(default=False)     #20weeks
    tick_flea_5 = models.BooleanField(default=False)     #24weeks
    tick_flea_6 = models.BooleanField(default=False)     #28weeks
    tick_flea_7 = models.BooleanField(default=False)     #32weeks

    def __str__(self):
        return 'PHP:' + str(self.k9.name)

class VaccineUsed(models.Model):
    vaccine_record = models.ForeignKey(VaccinceRecord, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True, blank=True)
    disease = models.CharField('disease', max_length=200)
    date_vaccinated = models.DateField('date_vaccinated', null=True, blank=True)
    veterinary = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.vaccine_record) + ':' + str(self.disease) +'-' + str(self.date_vaccinated)

class Requests(models.Model):
    CONCERN = (
        ('Broken', 'Broken'),
        ('Lost', 'Lost'),
        ('Stolen', 'Stolen'),
    )

    equipment = models.ForeignKey(Miscellaneous, on_delete=models.CASCADE)
    handler = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField('date', auto_now_add=True)
    concern = models.CharField('concern', max_length=100, choices=CONCERN, default="")
    remarks = models.CharField('remarks', max_length=200, blank=True)
    request_status = models.CharField('request_status', max_length=200, default="Pending")
    date_approved = models.DateField('date_approved', blank=True, null=True)
