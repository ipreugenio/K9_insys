from django.db import models

from profiles.models import User
from inventory.models import Medicine, Miscellaneous, Food, DamagedEquipemnt, Food
from inventory.models import Medicine_Inventory
from training.models import Training
from profiles.models import User
from deployment.models import K9_Schedule, Incidents
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.sessions.models import Session
from planningandacquiring.models import K9

# Create your models here.

#TODO
# either text or Fk from equipment
# verify: grooming kit, first aid kit, vitamins, and oral dextrose.
class K9_Pre_Deployment_Items(models.Model):
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, null=True, blank=True)    
    collar = models.CharField('collar', max_length=200)
    vest = models.CharField('vest', max_length=200)
    leash = models.CharField('leash', max_length=200)
    shipping_crate = models.CharField('shipping crate', max_length=200)
    leash = models.CharField('leash', max_length=200)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)
    food_quantity = models.IntegerField('quantity', default=0) 
    vitamins = models.ForeignKey(Medicine_Inventory, on_delete=models.CASCADE, null=True, blank=True)
    vitamins_quantity = models.IntegerField('quantity', default=0) 
    
class Handler_K9_History(models.Model):
    handler = models.ForeignKey(User, on_delete=models.CASCADE)
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE)    
    date = models.DateField('date', auto_now_add=True)

    def __str__(self):
        return str(self.handler) + ': ' + str(self.k9.capability)

class K9_Incident(models.Model):
    INCIDENT = (
        ('Stolen', 'Stolen'),
        ('Lost', 'Lost'),
        ('Accident', 'Accident'),
        ('Sick', 'Sick'),
    )
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, null=True, blank=True)
    incident = models.CharField('incident', max_length=100, choices=INCIDENT, default="")
    title = models.CharField('title', max_length=100)
    date = models.DateField('date', auto_now_add=True)
    description = models.TextField('description', max_length=200)
    status = models.CharField('status', max_length=200, default="Pending")
    clinic = models.CharField('clinic', max_length=200, null=True, blank=True)
    reported_by = models.CharField('reported_by', max_length=200, null=True, blank=True)


class Image(models.Model):
    incident_id = models.ForeignKey(K9_Incident, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to='incident_image', blank=True, null=True)


class Health(models.Model):
    dog = models.ForeignKey(K9, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField('date', auto_now_add=True)
    problem = models.TextField('problem', max_length=800, null=True, blank=True)
    treatment = models.TextField('treatment', max_length=800, null=True, blank=True)
    status = models.CharField('status', max_length=200, default="On-Going")
    veterinary = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.IntegerField('duration', null=True, blank=True)
    date_done = models.DateField('date_done', null=True, blank=True)
    incident_id = models.ForeignKey(K9_Incident, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to='prescription_image', blank=True, null=True,  default='prescription_image/no-image.jpg')
    follow_up = models.BooleanField(default=False)
    follow_up_date = models.DateField('follow_up_date', null=True, blank=True)
    follow_up_done = models.BooleanField(default=False)

    def __str__(self):

        return str(self.id) + ': ' + str(self.date) #+' - ' + str(self.dog.name)

    def expire(self):
        expired = self.date_done + timedelta(days=7)
        e = expired - date.today() 
        return e.days

    def expire_date(self):
        expired = self.date_done + timedelta(days=7) 
        return expired

    def save(self, *args, **kwargs):
        if self.date != None:
            self.date_done = self.date + timedelta(days=self.duration)

        if date.today() == self.date_done:
            self.dog.status = 'Working Dog'
        super(Health, self).save(*args, **kwargs)


class HealthMedicine(models.Model):
    TIME_OF_DAY = (
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Night', 'Night'),
        ('Morning/Afternoon', 'Morning/Afternoon'),
        ('Morning/Night', 'Morning/Night'),
        ('Afternoon/Night', 'Afternoon/Night'),
        ('Morning/Afternoon/Night', 'Morning/Afternoon/Night'),
    )

    health = models.ForeignKey(Health, on_delete=models.CASCADE, related_name='health')
    medicine = models.ForeignKey(Medicine_Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity', default=0)
    time_of_day = models.CharField('time_of_day', choices=TIME_OF_DAY, max_length=200, default="")
    duration = models.IntegerField('duration', default=1)

    def __str__(self):
        return str(self.id) + ': ' + str(self.health.date)  # + '-' + str(self.health.dog)



class Transaction_Health(models.Model):
    health = models.ForeignKey(Health, on_delete=models.CASCADE, null=True, blank=True, related_name='initial_health')
    health2 = models.ForeignKey(Health, on_delete=models.CASCADE, null=True, blank=True,  related_name='follow_health')
    incident = models.ForeignKey(K9_Incident, on_delete=models.CASCADE, null=True, blank=True, related_name='initial')
    follow_up = models.ForeignKey(K9_Incident, on_delete=models.CASCADE, null=True, blank=True, related_name='follow_up')
    status = models.CharField('status', max_length=200, default="Pending")
    
class PhysicalExam(models.Model):
    EXAMSTATUS = (
        ('Normal', 'Normal'),
        ('Abnormal', 'Abnormal'),
        ('Not Examined', 'Not Examined'),
    )

    dog = models.ForeignKey(K9, on_delete=models.CASCADE)
    veterinary = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cage_number = models.IntegerField('cage_number', default="0")
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
        notif = self.date_next_exam - timedelta(days=7)
        return notif

    def save(self, *args, **kwargs):
        # self.date_next_exam = self.date + timedelta(days=365)
        super(PhysicalExam, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.date) + ': ' + str(self.dog.name)

@receiver(post_save, sender=PhysicalExam)
def phex_next_date(sender, instance, **kwargs):
    if kwargs.get('created', False):
        instance.date_next_exam = instance.date + relativedelta(year=+1, )

class VaccinceRecord(models.Model):
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, null=True, blank=True)
    deworming_1 = models.BooleanField(default=False)     #2weeks
    deworming_2 = models.BooleanField(default=False)     #4weeks
    deworming_3 = models.BooleanField(default=False)     #6weeks
    deworming_4 = models.BooleanField(default=False)     #9weeks
   
    dhppil_cv_1 = models.BooleanField(default=False)     #6weeks *
    dhppil_cv_2 = models.BooleanField(default=False)     #9weeks *
    dhppil_cv_3 = models.BooleanField(default=False)     #12weeks *
    
    heartworm_1 = models.BooleanField(default=False)     #6weeks
    heartworm_2 = models.BooleanField(default=False)     #10weeks
    heartworm_3 = models.BooleanField(default=False)     #14weeks
    heartworm_4 = models.BooleanField(default=False)     #18weeks
    heartworm_5 = models.BooleanField(default=False)     #22weeks
    heartworm_6 = models.BooleanField(default=False)     #26weeks
    heartworm_7 = models.BooleanField(default=False)     #30weeks
    heartworm_8 = models.BooleanField(default=False)     #34weeks
   
    anti_rabies = models.BooleanField(default=False)     #12weeks *

    bordetella_1 = models.BooleanField(default=False)    #8weeks *
    bordetella_2 = models.BooleanField(default=False)    #11weeks *

    dhppil4_1 = models.BooleanField(default=False)       #15weeks *
    dhppil4_2 = models.BooleanField(default=False)       #18weeks *

    tick_flea_1 = models.BooleanField(default=False)     #8weeks
    tick_flea_2 = models.BooleanField(default=False)     #12weeks
    tick_flea_3 = models.BooleanField(default=False)     #16weeks
    tick_flea_4 = models.BooleanField(default=False)     #20weeks
    tick_flea_5 = models.BooleanField(default=False)     #24weeks
    tick_flea_6 = models.BooleanField(default=False)     #28weeks
    tick_flea_7 = models.BooleanField(default=False)     #32weeks

    def __str__(self):
        return str(self.k9)

    def save(self, *args, **kwargs):
        if self.dhppil4_2 == True:
            self.k9.training_status = 'Unclassified'
        super(VaccinceRecord, self).save(*args, **kwargs)


class VaccineUsed(models.Model):
    vaccine_record = models.ForeignKey(VaccinceRecord, on_delete=models.CASCADE, related_name='record')
    order = models.IntegerField('order', default=0)
    age = models.CharField('age', max_length=200, null=True, blank=True)
    disease = models.CharField('disease', max_length=200, null=True, blank=True)
    vaccine = models.ForeignKey(Medicine_Inventory, on_delete=models.CASCADE, null=True, blank=True)
    date_vaccinated = models.DateField('date_vaccinated', null=True, blank=True)
    veterinary = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to='health_image', blank=True, null=True)
    done = models.BooleanField(default=False)
    date = models.DateField('date', auto_now_add=True)
    
    def __str__(self):
        return str(self.vaccine_record) + ':' + str(self.disease) + '-' + str(self.date_vaccinated)


#TODO
# Request Equipment Connect to K9_Pre_Deployment Equipments
class Equipment_Request(models.Model):
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


class Handler_On_Leave(models.Model):
    handler = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, null=True, blank=True)
    incident = models.CharField('incident', max_length=100, default="On-Leave")
    date = models.DateField('date', auto_now_add=True)
    description = models.TextField('description', max_length=200)
    status = models.CharField('status', max_length=200, default="Pending")
    date_from = models.DateField('date_from', null=True, blank=True)
    date_to = models.DateField('date_to', null=True, blank=True)
    duration = models.IntegerField('duration', null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='admin')

    def save(self, *args, **kwargs):
        days = self.date_to - self.date_from
        self.duration = days.days
        super(Handler_On_Leave, self).save(*args, **kwargs)


class Handler_Incident(models.Model):
    INCIDENT = (
        ('Rescued People', 'Rescued People'),
        ('Made an Arrest', 'Made an Arrest'),
        ('Poor Performance', 'Poor Performance'),
        ('Accident', 'Accident'),
        ('MIA', 'MIA'),
        ('Died', 'Died'),
        ('Others', 'Others'),
    )
    handler = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, null=True, blank=True)
    incident = models.CharField('incident', choices=INCIDENT,max_length=100, null=True, blank=True)
    date = models.DateField('date', auto_now_add=True)
    description = models.TextField('description', max_length=200)
    status = models.CharField('status', max_length=200, default="Pending")
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='leader')


class Notification(models.Model):
    POSITION = (
        ('Administrator', 'Administrator'),
        ('Veterinarian', 'Veterinarian'),
        ('Handler', 'Handler'),
    )

    NOTIF_TYPE = (
        ('physical_exam', 'physical_exam'),
        ('vaccination', 'vaccination'),
        ('dog_request', 'dog_request'),
        ('inventory_low', 'inventory_low'), #VERIFY
        ('heat_cycle', 'heat_cycle'),
        ('location_incident', 'location_incident'),
        ('equipment_request', 'equipment_request'), #VERIFY
        ('k9_died', 'k9_died'), 
        ('k9_sick', 'k9_sick'),
        ('k9_stolen', 'k9_stolen'),
        ('k9_accident', 'k9_accident'),
        ('handler_died', 'handler_died'),
        ('handler_on_leave', 'handler_on_leave'),
        ('retired_k9', 'retired_k9'),
        ('medicine_done', 'medicine_done'),
        ('medicine_given', 'medicine_given'),
    )

    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    other_id = models.IntegerField(blank=True, null=True)
    notif_type = models.CharField('notif_type', max_length=100, choices=NOTIF_TYPE, blank=True, null=True)
    position = models.CharField('position', max_length=100, choices=POSITION, default="Administrator")
    message = models.CharField(max_length=200)
    viewed = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Notification, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.message) + ' : ' + str(self.datetime)


#When medicine is created, also create inventory instance
@receiver(post_save, sender=Medicine)
def create_medicine_inventory(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Medicine_Inventory.objects.create(medicine=instance, quantity=0)
# K9 Training
@receiver(post_save, sender=K9)
def create_training_record(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Training.objects.create(k9=instance, training='EDD')
        Training.objects.create(k9=instance, training='NDD')
        Training.objects.create(k9=instance, training='SAR')

#create vaccine record, and vaccine used
@receiver(post_save, sender=K9)
def create_k9_vaccines(sender, instance, **kwargs):
    if kwargs.get('created', False):
        if instance.source == 'Procured':
            cvr = VaccinceRecord.objects.create(k9=instance,  deworming_1=True, deworming_2=True, deworming_3=True,
            deworming_4=True, dhppil_cv_1=True, dhppil_cv_2=True, dhppil_cv_3=True, heartworm_1=True, heartworm_2=True,
            heartworm_3=True, heartworm_4=True, heartworm_5=True, heartworm_6=True, heartworm_7=True, heartworm_8=True,
            anti_rabies=True, bordetella_1=True, bordetella_2=True, dhppil4_1=True, dhppil4_2=True, tick_flea_1=True,
            tick_flea_2=True, tick_flea_3=True, tick_flea_4=True, tick_flea_5=True, tick_flea_6=True, tick_flea_7=True)

        else:
            cvr = VaccinceRecord.objects.create(k9=instance)
            VaccineUsed.objects.create(vaccine_record = cvr, age= '2 Weeks', disease='1st Deworming', order='1')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '4 Weeks', disease='2nd Deworming', order='2')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '6 Weeks', disease='3rd Deworming', order='3')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '6 Weeks', disease='1st dose DHPPiL+CV Vaccination', order='4')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '6 Weeks', disease='1st Heartworm Prevention', order='5')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '8 Weeks', disease='1st dose Bordetella Bronchiseptica Bacterin', order='6')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '8 Weeks', disease='1st Tick and Flea Prevention', order='7')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '9 Weeks', disease='2nd dose DHPPiL+CV', order='8')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '9 Weeks', disease='4th Deworming', order='9')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '10 Weeks', disease='2nd Heartworm Prevention', order='10')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '11 Weeks', disease='2nd dose Bordetella Bronchiseptica Bacterin', order='11')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '12 Weeks', disease='Anti-Rabies Vaccination', order='12')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '12 Weeks', disease='2nd Tick and Flea Prevention', order='13')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '12 Weeks', disease='3rd dose DHPPiL+CV Vaccination', order='14')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '14 Weeks', disease='3rd Heartworm Prevention', order='15')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '15 Weeks', disease='1st dose DHPPiL4 Vaccination', order='16')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '16 Weeks', disease='3rd Tick and Flea Prevention', order='17')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '18 Weeks', disease='2nd dose DHPPiL4 Vaccination', order='18')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '18 Weeks', disease='4th Heartworm Prevention', order='19')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '20 Weeks', disease='4th Tick and Flea Prevention', order='20')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '22 Weeks', disease='5th Heartworm Prevention', order='21')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '24 Weeks', disease='6th Heartworm Prevention', order='22')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '26 Weeks', disease='2nd dose DHPPiL4 Vaccination', order='23')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '28 Weeks', disease='6th Tick and Flea Prevention', order='24')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '30 Weeks', disease='7th Heartworm Prevention', order='25')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '32 Weeks', disease='7th Tick and Flea Prevention', order='26')
            VaccineUsed.objects.create(vaccine_record = cvr, age= '34 Weeks', disease='8th Heartworm Prevention', order='27')

#######################################################################################################################

#TODO EDIT 
@receiver(post_save, sender=PhysicalExam)
def phex_next_date(sender, instance, **kwargs):
    if kwargs.get('created', False):
        instance.date_next_exam = instance.date + relativedelta(year=+1,)

#TODO EDIT    
# HANDLER INCIDENT repored

@receiver(post_save, sender=Handler_Incident)
def create_handler_incident_notif(sender, instance, **kwargs):
    if kwargs.get('created', False):
        if instance.incident == 'Died':
            Notification.objects.create(user=instance.handler,
                                        position='Administrator',
                                        other_id=instance.id,
                                        notif_type='handler_died',
                                        message='Reported Dead! ' + str(instance.handler))
        else:

            Notification.objects.create(user = instance.handler,
                            position = 'Administrator',
                            other_id = instance.id,
                            notif_type = 'handler_on_leave',
                            message= 'On-Leave Request! ' + str(instance.handler))
#TODO HEALTH TEST                            
@receiver(post_save, sender=Health)
def create_handler_health_notif(sender, instance, **kwargs):
    if kwargs.get('created', False):
            Notification.objects.create(user = instance.dog.handler,
                            position = 'Handler',
                            other_id = instance.id,
                            notif_type = 'medicine_given',
                            message= 'Health Concern has been reviewed. See Details.')


#TODO K9 INCIDENT Add died and accident 
@receiver(post_save, sender=K9_Incident)
def create_k9_incident_notif(sender, instance, **kwargs):
    if kwargs.get('created', False):

        if instance.incident == 'Sick':
            Notification.objects.create(k9 = instance.k9,
                            position = 'Veterinarian',
                            other_id = instance.id,
                            notif_type = 'k9_sick',
                            message= str(instance.k9.name) + ' has a health concern! ')
        elif instance.incident == 'Lost': 
            Notification.objects.create(k9 = instance.k9,
                            position = 'Administrator',
                            other_id = instance.id,
                            notif_type = 'k9_lost',
                            message= str(instance.k9.name) + ' is reported Lost! ')
        elif instance.incident == 'Stolen': 
            Notification.objects.create(k9 = instance.k9,
                            position = 'Administrator',
                            other_id = instance.id,
                            notif_type = 'k9_stolen',
                            message= str(instance.k9.name) + ' is reported Stolen! ')

#TODO EQUIPMENT Verify
@receiver(post_save, sender=Equipment_Request)

def create_damaged_equipment_notif(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Notification.objects.create(user=instance.handler,
                                    position='Administrator',
                                    other_id=instance.id,
                                    notif_type='equipment_request',
                                    message='Equipment Concern!')



# When medicine is created, also create inventory instance
@receiver(post_save, sender=Medicine)
def create_medicine_inventory(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Medicine_Inventory.objects.create(medicine=instance, quantity=0)


# create vaccine record, and vaccine used
@receiver(post_save, sender=K9)
def create_k9_vaccines(sender, instance, **kwargs):
    if kwargs.get('created', False):
        pass
        # if instance.source == 'Procured':
        #     VaccinceRecord.objects.create(k9=instance, deworming_1=True, deworming_2=True, deworming_3=True,
        #     deworming_4=True, dhppil_cv_1=True, dhppil_cv_2=True, dhppil_cv_3=True,heartworm_1=True, heartworm_2=True,
        #     heartworm_3=True, heartworm_4=True, heartworm_5=True, heartworm_6=True,heartworm_7=True, heartworm_8=True,
        #     anti_rabies=True, bordetella_1=True, bordetella_2=True, dhppil4_1=True,dhppil4_2=True, tick_flea_1=True,
        #     tick_flea_2=True, tick_flea_3=True, tick_flea_4=True, tick_flea_5=True,tick_flea_6=True, tick_flea_7=True)
        #
        #     instance.training_status = 'Unclassified'
        #     instance.save()
        #
        # else:
        #     cvr = VaccinceRecord.objects.create(k9=instance)
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_1')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_2')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_3')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil_cv_1')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_1')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='bordetella_1')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_1')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil_cv_2')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_4')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_2')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='bordetella_2')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='anti_rabies')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_2')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil_cv_3')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_3')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil4_1')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_3')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil4_2')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_4')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_4')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_5')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_5')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_6')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_6')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_7')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_7')
        #     VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_8')


# Location incidentes reported

@receiver(post_save, sender=Incidents)
def location_incident(sender, instance, **kwargs):
    if kwargs.get('created', False):
        c = ''
        if instance.type == 'Explosives Related':
            c = ' has reported an '
        elif instance.type == 'Narcotics Related' or instance.type == 'Search and Rescue Related':
            c = ' has reported a '
        else:
            pass

        if c == '':
            Notification.objects.create(user=instance.user,
                                        position='Administrator',
                                        other_id=instance.id,
                                        notif_type='location_incident',
                                        message=str(instance.user) + ' has reported an incident at ' +
                                                str(instance.location) + '.')
        else:
            Notification.objects.create(user=instance.user,
                                        position='Administrator',
                                        other_id=instance.id,
                                        notif_type='location_incident',
                                        message=str(instance.user) + c + str(instance.type) +
                                                ' incident at ' + str(instance.location) + '.')


# When medicine is created, also create inventory instance
@receiver(post_save, sender=K9)
def create_training_record(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Training.objects.create(k9=instance, training='EDD')
        Training.objects.create(k9=instance, training='NDD')
        Training.objects.create(k9=instance, training='SAR')


@receiver(post_save, sender=Medicine)
def create_medicine_inventory(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Medicine_Inventory.objects.create(medicine=instance, quantity=0)

        Notification.objects.create(user = instance.user,
                                position = 'Administrator',
                                other_id=instance.id,
                                notif_type = 'location_incident',
                                message= str(instance.user) + c + str(instance.type) +
                                ' incident at ' + str(instance.location) + '.')

