from django.db import models
from planningandacquiring.models import K9
from profiles.models import User
from inventory.models import Medicine, Miscellaneous, Food, DamagedEquipemnt
from inventory.models import Medicine_Inventory, Miscellaneous_Inventory, Food_Inventory
from profiles.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, date, timedelta
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
    cage_number = models.IntegerField('cage_number', default = "0")
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
    remarks = models.TextField('remarks', max_length=200, null=True, blank=True)
    date = models.DateField('date', auto_now_add=True)
    date_next_exam = models.DateField('date_next_exam', null=True, blank=True)

    def due_notification(self):
        notif = self.date_next_exam - timedelta(days=2)
        return notif

    def save(self, *args, **kwargs):
        self.date_next_exam = self.date + timedelta(days=365)
        super(PhysicalExam, self).save(*args, **kwargs)

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
        return 'PHP:' + str(self.k9)

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

class K9_Incident(models.Model):
    INCIDENT = (
        ('Died', 'Died'),
    )
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, null=True, blank=True)
    incident = models.CharField('incident', max_length=100, choices=INCIDENT, default="")
    date = models.DateField('date', auto_now_add=True)
    description = models.TextField('description', max_length=200)

class Handler_Incident(models.Model):
    INCIDENT = (
        ('Died', 'Died'),
    )
    handler = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    incident = models.CharField('incident', max_length=100, choices=INCIDENT, default="")
    date = models.DateField('date', auto_now_add=True)
    description = models.TextField('description', max_length=200)

class Notification(models.Model):
    INCIDENT = (
        ('Administrator', 'Administrator'),
        ('Veterinarian', 'Veterinarian'),
        ('Handler', 'Handler'),
    )

    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    position = models.CharField('position', max_length=100, choices=INCIDENT, default="Administrator")
    message = models.CharField(max_length=200)
    viewed = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.message) + ' : ' + str(self.datetime)

@receiver(post_save, sender=Handler_Incident)
def create_handler_incident_notif(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Notification.objects.create(user = instance.handler,
                            position = 'Administrator',
                            message= str(instance.handler) + ' has been reported dead.')

@receiver(post_save, sender=Requests)
def create_equipment_request_notif(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Notification.objects.create(user = instance.handler,
                            position = 'Administrator',
                            message= str(instance.handler) + ' has made an equipment request.')

@receiver(post_save, sender=DamagedEquipemnt)
def create_damaged_equipment_notif(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Notification.objects.create(user = instance.user,
                            position = 'Administrator',
                            message= str(instance.handler) + ' has reported an equipment concern.')

@receiver(post_save, sender=Medicine)
def create_medicine_inventory(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Medicine_Inventory.objects.create(medicine=instance, quantity=0)

@receiver(post_save, sender=Food)
def create_food_inventory(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Food_Inventory.objects.create(food=instance, quantity=0)

@receiver(post_save, sender=Miscellaneous)
def create_miscellaneous_inventory(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Miscellaneous_Inventory.objects.create(miscellaneous=instance, quantity=0)

#create vaccine record, and vaccine used
@receiver(post_save, sender=K9)
def create_k9_vaccines(sender, instance, **kwargs):
    if kwargs.get('created', False):
        cvr = VaccinceRecord.objects.create(k9=instance)
        VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_3')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil_cv_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='bordetella_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil_cv_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_4')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='bordetella_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='anti_rabies')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil_cv_3')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_3')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil4_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_3')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil4_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_4')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_4')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_5')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_5')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_6')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_6')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_7')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_7')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_8')
     