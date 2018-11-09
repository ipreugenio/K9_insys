from django.db import models
from planningandacquiring.models import K9
from profiles.models import User
from inventory.models import Medicine, Miscellaneous
from profiles.models import User
# Create your models here.

class Health(models.Model):
    dog = models.ForeignKey(K9, on_delete=models.CASCADE)
    date = models.DateField('date', auto_now_add=True)
    problem = models.TextField('problem', max_length=200)
    treatment = models.TextField('treatment', max_length=200)
    status = models.CharField('status', max_length=200, default="Pending")

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
    date = models.DateField('date', auto_now_add=True)
    #veterinary = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    veterinary = models.CharField('veterinary', max_length=200, default="Change this to Foreign Key User")
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

    def __str__(self):
        return str(self.date) + ': ' + str(self.dog.name)

#TODO
#add vet user
class VaccinceRecord(models.Model):
    DISEASE = (
        ('BORDETELLA', 'BORDETELLA'),
        ('CORONAVIRUS', 'CORONAVIRUS'),
        ('DISTEPER', 'DISTEPER'),
        ('HEPATITIS', 'HEPATITIS'),
        ('LEPTOSPIROSIS', 'LEPTOSPIROSIS'),
        ('LYME', 'LYME'),
        ('MEASLES', 'MEASLES'),
        ('PARAINLUENZA', 'PARAINLUENZA'),
        ('PARVOVIRUS', 'PARVOVIRUS'),
        ('RABIES', 'RABIES'),
        ('TRACHEOBRONCHTIS', 'TRACHEOBRONCHTIS'),
    )

    dog = models.ForeignKey(K9, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    disease = models.CharField('disease', choices=DISEASE, max_length=200)
    date_vaccinated = models.DateField('date_vaccinated', auto_now_add=True)
    date_validity = models.DateField('date_validity', blank=True,)
    #veterinary = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return str(self.date_vaccinated) + ':' + str(self.disease) +'-' + str(self.dog.name)

class Requests(models.Model):
    CONCERN = (
        ('Broken', 'Broken'),
        ('Lost', 'Lost'),
        ('Stolen', 'Stolen'),
    )

    equipment = models.ForeignKey(Miscellaneous, on_delete=models.CASCADE)
    handler = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('date', auto_now_add=True)
    concern = models.CharField('concern', max_length=100, choices=CONCERN, default="")
    remarks = models.CharField('remarks', max_length=200, blank=True)
    request_status = models.CharField('request_status', max_length=200, default="Pending")
    date_approved = models.DateField('date_approved', blank=True, null=True)