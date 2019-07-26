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
from deployment.models import Dog_Request, Team_Dog_Deployed, K9_Schedule, Team_Assignment, K9_Pre_Deployment_Items

from pandas import DataFrame as df
import pandas as pd

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

# @periodic_task(run_every=timedelta(seconds=10))
# def test():
#     print('Hello')


#Steps 1 and 2 is in Handler Dashboard (Confirmation of Pre Deploment Items)

#Step 3
#Deploy Team (only the ones who have confirmed) once deployment date hits
# @periodic_task(run_every=crontab(hour=6, minute=30))
@periodic_task(run_every=timedelta(seconds=10))
def check_initial_deployment_dates():
    print('check_initial_deployment_dates code is run')
    schedules = K9_Schedule.objects.filter(status = 'Initial Deployment')

    today = datetime.today().date()

    deploy_k9_list = []
    for item in schedules:
        # try:
        delta = today - item.date_start
        pre_deps = K9_Pre_Deployment_Items.objects.filter(initial_sched=item)
        if delta.days >= 0:
            for pre_dep in pre_deps:
                if pre_dep.status == "Confirmed":
                    deploy = Team_Dog_Deployed.objects.filter(k9 = pre_dep.k9).filter(team_assignment = item.team).filter(date_pulled = None)
                    print("DEPLOY")
                    print(deploy)
                    if not deploy:
                        deploy_k9_list.append((pre_dep.k9 , item.team)) #TODO wala dapat duplicate

        # except: pass

    #TODO For every k9 in deploy_k9_list 1.)Create Team_Dog_deployed 2.) Change status to Deployed ./
    #TODO Assign new Team Leader with every Team_Dog_Deployed
    #TODO update k9s total_dogs_deployed per port

    print("DEPLOY k9 LIST")
    print(deploy_k9_list)

    for item in deploy_k9_list:
        k9 = item[0]
        team = item[1]
        k9.training_status = "Deployed"
        k9.save()
        deploy = Team_Dog_Deployed.objects.create(k9 = k9, status = "Pending", team_assignment = team)


    update_port_info()

    return None


def update_port_deployed_count(team):

    deployed = Team_Dog_Deployed.objects.filter(team_assignment = team)

    sar_count = 0
    ndd_count = 0
    edd_count = 0
    for item in deployed:
        if item.k9.capability == "SAR":
            sar_count += 1
        elif item.k9.capability == "NDD":
            ndd_count += 1
        else:
            edd_count += 1

    team.SAR_deployed = sar_count
    team.NDD_deployed = ndd_count
    team.EDD_deployed = edd_count
    team.save()


    return None


# Step 4
#Run this view as soon as deployment date hits then get all handlers from that team (immediatele after step 3)
# Get all handlers from team
def assign_TL(team):

    #Higher number = higher rank
    RANK_SORTED = (
        (1, "ASN/ASW"),
        (2, "SN2/SW2"),
        (3, "SN1/SW1"),
        (4, "PO3"),
        (5, 'PO2'),
        (6, 'PO1'),
        (7, 'CPO'),
        (8, 'SCPO'),
        (9, 'MCPO')
    )

    #TODO Confirm if sa K9_Schedule mag babase since hindi pa talaga deployed mga to, baka wala pa sila Team_Dog_Deployed
    deployment = Team_Dog_Deployed.objects.filter(team_assignment = team) # .exclude(date_pulled = None) #Includes unconfirmed deployed k9s

    handler_list = []

    try:
        for item in deployment:
            handler_list.append(item.handler)

        rank_list = []
        for handler in handler_list:
            is_ranked = 0
            for rank in RANK_SORTED:
                if handler.rank == rank[1]:
                    rank_list.append(rank[0])
                    is_ranked = 1

            if is_ranked == 0:
                rank_list.append(0)

        df_data = {
            'Rank': rank_list,
            'Handler': handler_list,

        }
        handler_rank_dataframe = df(data=df_data)
        handler_rank_dataframe.sort_values(by=['Rank'],
                                       ascending=[False], inplace=True) #TODO add another field for User model for "date of duty" then add another sorting process

        team_leader =  handler_rank_dataframe.iloc[0]['Handler']
        team.team_leader = team_leader
        team.save()
        team_leader.position = "Team Leader"
        team_leader.save()

    except: pass

    return None

def update_port_info():

    teams = Team_Assignment.objects.all()

    for team in teams:
        assign_TL(team)
        update_port_deployed_count(team)

    return None



#Step 5 is in TL Dashboard (Confirm Arrival)

# Step 6
# Check if TL has confirmed arrival. If not, escalate to admin
@periodic_task(run_every=crontab(hour=8, minute=30))
def check_initial_dep_arrival():

    k9s = K9.objects.filter(training_status = "Deployed")

    for k9 in k9s:
        team = Team_Dog_Deployed.objects.get(k9 = k9) #Dapat meron since deployed na siya
        pre_dep = K9_Pre_Deployment_Items.objects.get(k9 = k9)

        initial_sched = pre_dep.initial_sched

        delta = initial_sched.date_start - datetime.today().date()

        if delta.days > 5 and pre_dep.arrived == False:
            team.date_pulled = datetime.today().date()
            k9.training_status = "MIA"
            k9.save()
            team.save()
            # 1.) Pull out 2.) Change unit statuses to MIA 3.) Update Port details (TL and number of k9s assigned)

    update_port_info()

    return None