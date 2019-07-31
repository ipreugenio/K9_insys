from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
import time
from K9_insys.celery import app
import celery.decorators
from celery.schedules import crontab
from celery.decorators import periodic_task

from datetime import timedelta, date, datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from planningandacquiring.models import K9
from deployment.models import Dog_Request, Team_Dog_Deployed, K9_Schedule, Team_Assignment
from inventory.models import Medicine_Inventory, Medicine_Received_Trail, Medicine_Subtracted_Trail, Food, Food_Subtracted_Trail
from inventory.models import Safety_Stock
from unitmanagement.models import Notification, PhysicalExam, Health, Handler_Incident
from profiles.serializers import NotificationSerializer
# Create your tasks here
# The @shared_task decorator lets you create tasks that can be used by any app(s).
#from celery.schedules import crontab
from profiles.models import User
from django.db.models import Avg, Count, Min, Sum
#TODO
#ADD POSITION, OTHER_ID

# TODO UNITMANAGEMENT NOTIFS
#8AM
@periodic_task(run_every=crontab(hour=8, minute=0))

def unitmanagement_notifs():
    k9 = K9.objects.all()
    phex = PhysicalExam.objects.all()
    p = K9.objects.filter(next_proestrus_date=date.today())

    # PHYSICAL EXAMINATION DUE
    for phex in phex:
        if date.today() == phex.due_notification():
            Notification.objects.create(k9=phex.dog, message=str(
                phex.dog.name) + ' is due for Physical Examination in next week.' + str(phex.date_next_exam),
                                        notif_type='physical_exam', position='Veterinarian')
        elif date.today() == phex.date_next_exam:
            Notification.objects.create(k9=phex.dog,
                                        message=str(phex.dog.name) + ' is due for Physical Examination today',
                                        notif_type='physical_exam', position='Veterinarian')

    # VACCINATION DUE
    for k9 in k9:
        age = date.today() - k9.birth_date
        if age.days == 14:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 1st Deworming this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 28:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due 2nd Deworming this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 42:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due 3rd Deworming this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 42:
            Notification.objects.create(k9=k9,
                                        message=str(k9.name) + ' is due for 1st DHPPiL+CV Vaccination this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 42:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 1st Heartworm Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 56:
            Notification.objects.create(k9=k9, message=str(
                k9.name) + ' is due for 1st Bordetella Bronchiseptica Bacterin this week.', notif_type='vaccination',
                                        position='Veterinarian')
        elif age.days == 56:
            Notification.objects.create(k9=k9,
                                        message=str(k9.name) + ' is due for 1st Tick and Flea Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 63:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 2nd DHPPiL+CV this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 63:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 4th Deworming this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 70:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 2nd Heartworm Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 77:
            Notification.objects.create(k9=k9, message=str(
                k9.name) + ' is due for 2nd Bordetella Bronchiseptica Bacterin this week.', notif_type='vaccination',
                                        position='Veterinarian')
        elif age.days == 84:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for Anti-Rabies Vaccination this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 84:
            Notification.objects.create(k9=k9,
                                        message=str(k9.name) + ' is due for 2nd Tick and Flea Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 84:
            Notification.objects.create(k9=k9,
                                        message=str(k9.name) + ' is due for 3rd DHPPiL+CV Vaccination this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 98:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 3rd Heartworm Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 105:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 1st DHPPiL4 Vaccination this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 112:
            Notification.objects.create(k9=k9,
                                        message=str(k9.name) + ' is due for 3rd Tick and Flea Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 126:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 2nd DHPPiL4 Vaccination this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 126:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 4th Heartworm Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 140:
            Notification.objects.create(k9=k9,
                                        message=str(k9.name) + ' is due for 4th Tick and Flea Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 154:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 5th Heartworm Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 168:
            Notification.objects.create(k9=k9,
                                        message=str(k9.name) + ' is due for 5th Tick and Flea Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 183:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 6th Heartworm Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 196:
            Notification.objects.create(k9=k9,
                                        message=str(k9.name) + ' is due for 6th Tick and Flea Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 210:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 7th Heartworm Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 224:
            Notification.objects.create(k9=k9,
                                        message=str(k9.name) + ' is due for 7th Tick and Flea Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')
        elif age.days == 238:
            Notification.objects.create(k9=k9, message=str(k9.name) + ' is due for 8th Heartworm Prevention this week.',
                                        notif_type='vaccination', position='Veterinarian')

            # health change to working if done with medicine
    health = Health.objects.filter(status='Pending')

    for h in health:
        if h.date_done == date.today():

            Notification.objects.create(k9=h.dog, message=str(h.dog.name) + ' will be done with medication today!',
                                        notif_type='medicine_done', position='Veterinarian', other_id=h.id)


        if date.today() == h.date_done:
            h.status = 'Done'
            h.dog.status = 'Working Dog'

    # TODO
    # Handler on leave end_date is today
    hi = Handler_Incident.objects.filter(status='Approved')

    for hi in hi:
        if hi.date_to == date.today():
            hi.status = 'Done'
            hi.save()
            # get handler and k9
            h = User.objects.get(id=hi.handler.id)
            k9 = K9.objects.get(id=hi.k9.id)
            h.status = 'Working'
            h.save()

            if h.retain_last_handler == True:
                k9.partnered = True
                k9.handler = h
                h.partnered = True

                k9.save()
                h.save()

            try:
                # where dog is deployed
                td = Team_Dog_Deployed.objects.filter(k9=k9).latest()

                try:
                    # where location is updated
                    ta = Team_Assignment.objects.get(id=td.team_assignment.id)

                    # create new team dog
                    Team_Dog_Deployed.objects.create(k9=k9, handler=h, team_assignment=ta,
                                                     date_added=date.today())

                    if k9.capability == 'EDD':
                        ta.EDD_deployed = ta.EDD_deployed + 1
                    elif k9.capability == 'NDD':
                        ta.NDD_deployed = ta.NDD_deployed + 1
                    elif k9.capability == 'SAR':
                        ta.SAR_deployed = ta.SAR_deployed + 1

                    ta.save()
                except Team_Assignment.DoesNotExist:
                    pass
            except Team_Dog_Deployed.DoesNotExist:
                pass

            # TODO DEPLOYMENT NOTIFS

# 8:30AM
@periodic_task(run_every=crontab(hour=6, minute=0))
def deployment_notifs():
    request = Dog_Request.objects.all()

    # DOG REQUEST LOCATION
    for request in request:
        # start date
        if date.today() == request.due_start():
            Notification.objects.create(message=str(request.location) + ' deployment requested by ' +
                                                str(request.requester) + ' is due to start next week.',
                                        notif_type='dog_request', other_id=request.id)
        elif date.today() == request.start_date:
            Notification.objects.create(message=str(request.location) + ' deployment requested by ' +
                                                str(request.requester) + ' will start today.', notif_type='dog_request',
                                        other_id=request.id)

        # end date
        elif date.today() == request.due_end():
            Notification.objects.create(message=str(request.location) + ' deployment requested by ' +
                                                str(request.requester) + ' is due to end next week.',
                                        notif_type='dog_request', other_id=request.id)
        elif date.today() == request.end_date:
            Notification.objects.create(message=str(request.location) + ' deployment requested by ' +
                                                str(request.requester) + ' will end today.', notif_type='dog_request',
                                        other_id=request.id)


# 12AM
#DELETE FUNCTION WHERE 2MONTHS OF NOTIFICATION IS DELETED
@periodic_task(run_every=crontab(hour=23, minute=0))
def delete():
    notif_delete = Notification.objects.filter(datetime=date.today - timedelta(days=60))
    notif_delete.delete()

