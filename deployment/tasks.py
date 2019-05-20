from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
import time
from K9_insys.celery import app
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import timedelta, date, datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from unitmanagement.models import Notification
from planningandacquiring.models import K9
from deployment.models import Dog_Request, Team_Dog_Deployed, K9_Schedule, Team_Assignment


#TODO TEST       
# Deployment Request 
# End of date, pull out all dogs, update, area, status = Done
# 9AM
#@periodic_task(run_every=crontab(hour=9, minute=0))
def deploy_dog():
    #When Schedule is today, change training status to deployed
    sched = K9_Schedule.objects.filter(date_start=date.today())

    for sched in sched:
        sched.k9.training_status = 'Deployed'
        sched.k9.save()

    #When request is done, change status and pull out all dogs
    req = Dog_Request.objects.filter(status='Approved').filter(end_date=date.today())
 
    for req in req:
        req.status = 'Done'
        req.save()
        dog_deployed = Team_Dog_Deployed.objects.filter(team_requested=req)
        for dog_deployed in dog_deployed:
            k9 = K9.objects.get(id=dog_deployed.k9.id)
            #code what to do with K9
            try:
                #last assignment 
                td = Team_Dog_Deployed.objects.filter(k9=k9).exclude(team_assignment=None).latest('date_pulled')
                k9.assignment = str(td.team_assignment)
                k9.training_status = 'Deployed'
                k9.save()
                #Create new Team dog deployed for team_assignment
                Team_Dog_Deployed.objects.create(team_assignment=td.team_assignment, k9=k9, status='Deployed',
                date_added=date.today(), handler = str(k9.handler.fullname))

                #update Team assignment
                ta = Team_Assignment.objects.get(id=td.team_assignment.id)
                if k9.capability == 'EDD':
                    ta.EDD_deployed = ta.EDD_deployed-1
                elif k9.capability == 'NDD':
                    ta.NDD_deployed = ta.NDD_deployed-1
                elif k9.capability == 'SAR':
                    ta.SAR_deployed = ta.SAR_deployed-1
                ta.save()
            except td.DoesNotExist:
                #has no last assignment
                k9.assignment = None
                k9.training_status = 'For-Deployment' 
                k9.save()
                 
            #code for team dog deployed
            dog_deployed.status = 'Done'
            dog_deployed.date_pulled = date.today()
            dog_deployed.save()

# TODO DEPLOYMENT NOTIFS TEST
# 1 week before start of deployment
# 1 week before end of deployment
# start and end of deployment
#8:30AM
@periodic_task(run_every=crontab(hour=8, minute=30))
def deployment_notifs():
    request = Dog_Request.objects.all()

    # DOG REQUEST LOCATION
    for request in request:
        # start date
        if date.today() ==  request.due_start():
            Notification.objects.create(message= str(request.location) + ' deployment requested by ' + 
            str(request.requester) + ' is due to start next week.', notif_type='dog_request', other_id=request.id)
        elif date.today() ==  request.start_date:
           Notification.objects.create(message= str(request.location) + ' deployment requested by ' + 
            str(request.requester) + ' will start today.', notif_type='dog_request', other_id=request.id)

        # end date
        elif date.today() ==  request.due_end():
            Notification.objects.create(message= str(request.location) + ' deployment requested by ' + 
            str(request.requester) + ' is due to end next week.', notif_type='dog_request', other_id=request.id)
        elif date.today() ==  request.end_date:
            Notification.objects.create(message= str(request.location) + ' deployment requested by ' + 
            str(request.requester) + ' will end today.', notif_type='dog_request', other_id=request.id)