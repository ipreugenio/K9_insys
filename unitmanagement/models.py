from django.db import models
from planningandacquiring.models import K9
from profiles.models import User
from inventory.models import Medicine
# Create your models here.

class Health(models.Model):
    dog = models.ForeignKey(K9, on_delete=models.CASCADE)
    date = models.DateField('date', auto_now_add=True)
    problem = models.TextField('problem', max_length=200)
    treatment = models.TextField('treatment', max_length=200)
    
    def __str__(self):
        return str(self.id) + ': ' + str(self.date) +' - ' + str(self.dog_name)

    def save(self, *args, **kwargs):
        self.dog_name = self.dog.name
        self.serial_number = self.dog.serial_number
        super(Health, self).save(*args, **kwargs)
#TODO
#try not to reference medicine foreign key so if Medicine is deleted, record is kept
class HealthMedicine(models.Model):
    health = models.ForeignKey(Health, on_delete=models.CASCADE)
    medicine_id = models.IntegerField('medicine_id',default=0)
    medicine = models.CharField('medicine', max_length=200)
    quantity = models.IntegerField('quantity', default=0)
    dosage = models.CharField('dosage', max_length=200, default="")

    def __str__(self):
        return str(self.id) + ': ' + str(self.health.date) + '-' + str(self.health.dog)

class PhysicalExam(models.Model):
    EXAMSTATUS = (
        ('Normal', 'Normal'),
        ('Abnormal', 'Abnormal'),
        ('Not Examined', 'Not Examined'),
    )

    dog = models.ForeignKey(K9, on_delete=models.CASCADE)
    dog_name = models.CharField('dog_name', max_length=200)
    serial_number = models.CharField('serial_number', max_length=200, default="#")
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
        return str(self.date) + ': ' + str(self.dog)

    def save(self, *args, **kwargs):
        self.dog_name = self.dog.name
        self.serial_number = self.dog.serial_number
        super(PhysicalExam, self).save(*args, **kwargs)