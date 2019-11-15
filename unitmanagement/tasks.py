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
from unitmanagement.models import Notification, PhysicalExam, Health, Handler_Incident, Handler_On_Leave, \
    Handler_K9_History, Temporary_Handler, Request_Transfer, Emergency_Leave
from profiles.serializers import NotificationSerializer
# Create your tasks here
# The @shared_task decorator lets you create tasks that can be used by any app(s).
#from celery.schedules import crontab
from profiles.models import User
from django.db.models import Avg, Count, Min, Sum, Q

from deployment.tasks import assign_TL
from deployment.templatetags.index import current_team
#TODO
#ADD POSITION, OTHER_ID

# TODO UNITMANAGEMENT NOTIFS
#8AM
# @periodic_task(run_every=crontab(hour=8, minute=0))
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
# @periodic_task(run_every=crontab(hour=6, minute=0))
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
# @periodic_task(run_every=crontab(hour=23, minute=0))
def delete():
    notif_delete = Notification.objects.filter(datetime=datetime.today().date() - timedelta(days=60))
    notif_delete.delete()

# @periodic_task(run_every=crontab(hour=6, minute=0))
def tri_monthly_checkup():

    k9s = K9.objects.all()
    for k9 in k9s:
        k9_phex = PhysicalExam.objects.filter(k9 = k9).latest('id')
        delta = datetime.today().date() - k9_phex.date
        if k9_phex.cleared == True and delta.days >= 90:  # 3 months
            K9_Schedule.objects.create(date_start = k9_phex.date + relativedelta(months=3), status = "Tri Monthly Checkup")

    return None

#@periodic_task(run_every=crontab(hour=12, minute=30))
def check_leave_window(is_emergency = False, handler = None):
    today = datetime.today().date()

    if is_emergency == True:
        leaves = Emergency_Leave.objects.filter(handler = handler).filter(status = "Ongoing")
    else:
        leaves = Handler_On_Leave.objects.filter(status="Approved").filter(incident='On-Leave').filter(date_from = today - timedelta(days=1))

    for leave in leaves:
        handler = leave.handler

        if is_emergency == True and handler is not None:
            k9 = K9.objects.filter(handler = handler).last()
        else:
            k9 = leave.k9


        team_member_k9s = K9.objects.filter(assignment = k9.assignment)
        team_members = []
        for k9 in team_member_k9s:
            team_members.append(k9.handler)

        # k9.handler = "None"
        # k9.training_level = "Handler_on_Leave"
        # k9.save()

        # TODO assign temporary team leader
        if handler.position == "Team Leader":
            TL = assign_TL(team_members)
        else:
            #TODO manually retrieve Team_assignment
            tdd = Team_Dog_Deployed.objects.exclude(team_assignment=None).filter(
                date_pulled=None).filter(handler__in = team_members)
            team_list = []
            for x in tdd:
                team_list.append(x.team_assignment.id)
            team = Team_Assignment.objects.filter(id__in = team_list).last()
            TL = team.team_leader

        Temporary_Handler.objects.create(k9 = k9, original = k9.handler, temp = TL, date_given = datetime.today().date())

        if is_emergency == False:
            handler.status = "On-Leave"
            handler.save()


#@periodic_task(run_every=crontab(hour=12, minute=30))
def check_returning_from_leave():
    today = datetime.today().date()
    returning = Handler_On_Leave.objects.filter(status="Approved").filter(incident='On-Leave').filter(date_to=today + timedelta(days=1))

    for item in returning:
        handler = item.handler
        k9 = item.k9

        try:
            temp_handler = Temporary_Handler.objects.filter(k9 = k9, date_returned = None)
            temp_handler.date_returned = datetime.today().date()
            temp_handler.save()

            handler.status = "Working"
            handler.save()

            # k9.training_level = "Deployed"
            # k9.save()

            team = Team_Assignment.objects.get(team = k9.assignment)
            assign_TL(team)

        except:
            pass

#@periodic_task(run_every=crontab(hour=12, minute=30))
def check_transfer():

    transfers = Request_Transfer.objects.filter(date_of_transfer = datetime.today().date()).filter(status = "Approved")

    for transfer in transfers:
        ...
        #TODO select units related to transfer
        #TODO implement transfer


    return None

#@periodic_task(run_every=crontab(hour=12, minute=30))
def adjust_appointments():
    #1.) Get all checkups starting from 2 weeks in the past
    checkups = K9_Schedule.objects.filter(status="Checkup").exclude(
        date_start__lt=datetime.today().date() - timedelta(days=14)) #TODO confirm if all dates should be included (or atleast 1 week into the past)

    #2.) Check if K9s have an upcoming deployment
    k9_list = []
    deployment_list = []
    for sched in checkups:
        k9_list.append(sched.k9)
        deployment = K9_Schedule.objects.filter(status="Initial Deployment").filter(k9=sched.k9).exclude(
            date_start__lt=datetime.today().date()).first()
        deployment_list.append(deployment.date_start)

    k9_exclude_list = []  # Does not need to be checkuped
    #3.) For k9s with upcoming deployments, check if they are already done with phex prior to deployment
    for k9 in k9_list:
        try:
            checkup = PhysicalExam.objects.filter(dog=k9).latest('id')
            delta = datetime.today().date() - checkup.date
            if checkup.cleared == True and delta.days <= 90:  # 3 months
                k9_exclude_list.append(k9)
        except:
            pass

    #4.) exclude k9s already done with checkup
    checkups = checkups.exclude(k9__in=k9_exclude_list)
    # 5.) Reschedule k9s that have missed their checkups, prioritizing those who have earlier deployments
    ctr = 0
    date_index = datetime.today().date() + timedelta(days=1)
    for item in checkups:
        if ctr < 10:
            item.date_start = date_index
            item.save()
            ctr += 1
        else:
            date_index += timedelta(days=1)
            item.date_start = date_index
            item.save()
            ctr = 0

    return None

#@periodic_task(run_every=crontab(hour=12, minute=30))
def check_transfers():

    #TODO unit confirmation after transfer

    today = datetime.today().date()
    transfers = Request_Transfer.objects.filter(date_of_transfer__lte = today).filter(status = "Approved")
    for transfer in transfers:
        transfer.status = "Done"
        transfer.save()

        k9 = K9.objects.filter(handler = transfer.handler).last()
        k9.assignment = transfer.location_to.team
        k9.save()

        Team_Dog_Deployed.objects.create(k9=k9, handler=k9.handler, team_assignment=transfer.location_to,
                                         date_added=today)

        team_dog_deployed = Team_Dog_Deployed.objects.filter(k9=k9).filter(team_assignment=transfer.location_from).latest('id')
        team_dog_deployed.date_pulled = today
        team_dog_deployed.save()


    return None



