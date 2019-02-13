from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
import time
from datetime import timedelta, date
from K9_insys.celery import app
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from planningandacquiring.models import K9
from unitmanagement.models import Notification, PhysicalExam
from inventory.models import Medicine_Inventory, Food_Inventory
# Create your tasks here
# The @shared_task decorator lets you create tasks that can be used by any app(s).

#@periodic_task(run_every=crontab(hour=6, minutes=0))
@periodic_task(run_every=timedelta(seconds=10)) #testing time
def everyday_6am():
    print("Execute every everyday at 6:00AM.")
    # code for morning routine
    # subtraction of food and vitamins if any

    # if dog is in heat code
    k9 = K9.objects.all() 
    phex = PhysicalExam.objects.all()

    for phex in phex:
        if date.today() ==  phex.due_notification():
            Notification.objects.create(k9=phex.dog, message= str(phex.dog.name) + ' is due for Physical Examination in 2 days.' + str(phex.date_next_exam))
        elif date.today() ==  phex.date_next_exam:
            Notification.objects.create(k9=phex.dog, message= str(phex.dog.name) + ' is due for Physical Examination today')

    #Vaccination due
    for k9 in k9:
        age = date.today() - k9.birth_date
        # TODO ADD PARAMS FOR IN HEAT
        # if age.days == [inheat month] :
        #     k9.in_heat = True
        #     k9.save()
        if age.days == 14 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 1st Deworming this week.')
        elif age.days == 28 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due 2nd Deworming this week.')
        elif age.days == 42 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due 3rd Deworming this week.')
        elif age.days == 42 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 1st DHPPiL+CV Vaccination this week.')
        elif age.days == 42 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 1st Heartworm Prevention this week.')
        elif age.days == 56 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 1st Bordetella Bronchiseptica Bacterin this week.')
        elif age.days == 56 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 1st Tick and Flea Prevention this week.')
        elif age.days == 63 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 2nd DHPPiL+CV this week.')
        elif age.days == 63 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 4th Deworming this week.')
        elif age.days == 70 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 2nd Heartworm Prevention this week.')
        elif age.days == 77 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 2nd Bordetella Bronchiseptica Bacterin this week.')
        elif age.days == 84 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for Anti-Rabies Vaccination this week.')
        elif age.days == 84 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 2nd Tick and Flea Prevention this week.')
        elif age.days == 84 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 3rd DHPPiL+CV Vaccination this week.')
        elif age.days == 98 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 3rd Heartworm Prevention this week.')
        elif age.days == 105 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 1st DHPPiL4 Vaccination this week.')
        elif age.days == 112 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 3rd Tick and Flea Prevention this week.')
        elif age.days == 126 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 2nd DHPPiL4 Vaccination this week.')
        elif age.days == 126 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 4th Heartworm Prevention this week.')
        elif age.days == 140 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 4th Tick and Flea Prevention this week.')
        elif age.days == 154 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 5th Heartworm Prevention this week.')
        elif age.days == 168 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 5th Tick and Flea Prevention this week.')
        elif age.days == 183 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 6th Heartworm Prevention this week.')        
        elif age.days == 196 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 6th Tick and Flea Prevention this week.')
        elif age.days == 210 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 7th Heartworm Prevention this week.')
        elif age.days == 224 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 7th Tick and Flea Prevention this week.')
        elif age.days == 238 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 8th Heartworm Prevention this week.')        

# TODO SUBTRACTION OR ANYTHING WHEN TIME IS 6PM, FOOD_INVENTORY, ETC
# @periodic_task(run_every=crontab(hour=18, minutes=0))
# @periodic_task(run_every=timedelta(seconds=10)) #testing time
# def everyday_6pm():
#     #code for evening routine
#     k9 = K9.objects.all() 
        