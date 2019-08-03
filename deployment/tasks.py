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
from inventory.models import Medicine, Medicine_Inventory, Medicine_Subtracted_Trail, Food, Food_Subtracted_Trail, Miscellaneous, Miscellaneous_Subtracted_Trail
from profiles.models import User

from pandas import DataFrame as df
import pandas as pd

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



def update_port_deployed_count(team):

    deployed = Team_Dog_Deployed.objects.filter(team_assignment = team).filter(date_pulled = None)

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
def assign_TL(team, handler_list_arg = None):

    team_leader = None

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
    deployment = Team_Dog_Deployed.objects.filter(team_assignment = team).filter(date_pulled = None) #Includes unconfirmed deployed k9s

    handler_list = []

    try:
        if handler_list_arg:
            handler_list = handler_list_arg
        else:
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

        if not handler_list_arg:
            team.team_leader = team_leader
            team.save()

        for item in deployment:
            if item.handler != team_leader:
                handler = item.handler.position = "Handler"
                handler.save()

        team_leader.position = "Team Leader"
        team_leader.save()

    except: pass

    if not handler_list_arg:
        return None
    else:
        return team_leader

def update_port_info(team_list):

    teams = Team_Assignment.objects.filter(pk__in = team_list)

    for team in teams:
        assign_TL(team)
        update_port_deployed_count(team)

    return None


def subtract_inventory(pre_dep, user):
    #TODO dapat get
    try:
        collar = Miscellaneous.objects.filter(miscellaneous__contains="Collar").exclude(quantity = 0)
        collar.quantity -= 1
        collar.save()
        Miscellaneous_Subtracted_Trail.objects.create(inventory = collar, quantity = 1, user = user)

        vest = Miscellaneous.objects.filter(miscellaneous__contains="Vest").exclude(quantity = 0)
        vest.quantity -= 1
        vest.save()
        Miscellaneous_Subtracted_Trail.objects.create(inventory=vest, quantity=1, user=user)

        leash = Miscellaneous.objects.filter(miscellaneous__contains="Leash").exclude(quantity = 0)
        leash.quantity -= 1
        leash.save()
        Miscellaneous_Subtracted_Trail.objects.create(inventory=vest, quantity=1, user=user)

        shipping_crate = Miscellaneous.objects.filter(miscellaneous__contains="Shipping Crate").exclude(quantity = 0)
        shipping_crate.quantity -= 1
        shipping_crate.save()
        Miscellaneous_Subtracted_Trail.objects.create(inventory=shipping_crate, quantity=1, user=user)

        food = Food.objects.filter(foodtype="Adult Dog Food").exclude(quantity = 0)
        food.quantity -= 1
        food.save()
        Food_Subtracted_Trail.objects.create(inventory=food, quantity=1, user=user)

        medicines = Medicine.objects.filter(med_type="Vitamins").exclude(quantity = 0)
        medicine_inv = Medicine_Inventory.objects.filter(medicine__in=medicines)
        medicine_inv.quantity -= 1
        medicine_inv.save()
        Medicine_Subtracted_Trail.objects.create(inventory=medicine_inv, quantity=1, user=user)

        grooming_kit = Miscellaneous.objects.filter(miscellaneous__contains="Grooming Kit").exclude(quantity = 0)
        grooming_kit.quantity -= 1
        grooming_kit.save()
        Miscellaneous_Subtracted_Trail.objects.create(inventory=grooming_kit, quantity=1, user=user)

        first_aid_kit = Miscellaneous.objects.filter(miscellaneous__contains="First Aid Kit").exclude(quantity = 0)
        first_aid_kit.quantity -= 1
        first_aid_kit.save()
        Miscellaneous_Subtracted_Trail.objects.create(inventory=first_aid_kit, quantity=1, user=user)

        oral_dextrose = Miscellaneous.objects.filter(miscellaneous__contains="Oral Dextrose").exclude(quantity = 0)
        oral_dextrose.quantity -= 1
        oral_dextrose.save()
        Miscellaneous_Subtracted_Trail.objects.create(inventory=oral_dextrose, quantity=1, user=user)

        ball = Miscellaneous.objects.filter(miscellaneous__contains="Ball").exclude(quantity = 0)
        ball.quantity -= 1
        ball.save()
        Miscellaneous_Subtracted_Trail.objects.create(inventory=ball, quantity=1, user=user)
    except:
        pass

    return None

#Steps 1 and 2 is in Handler Dashboard (Confirmation of Pre Deploment Items)

#Step 3
#Deploy Team (only the ones who have confirmed) once deployment date hits
# @periodic_task(run_every=crontab(hour=6, minute=30))
@periodic_task(run_every=timedelta(seconds=25))
def check_initial_deployment_dates():
    print('check_initial_deployment_dates code is running')
    schedules = K9_Schedule.objects.filter(status = 'Initial Deployment')

    print("Schedules")
    print(schedules)

    today = datetime.today().date()
    team_list = []

    for item in schedules:
        # try:
        delta = today - item.date_start
        pre_deps = K9_Pre_Deployment_Items.objects.filter(initial_sched=item)

        print("Pre Deps")
        print(pre_deps)

        team = item.team
        team_list.append(team.id)

        if delta.days >= 0: #TAKE NOTE OF THIS #TODO notification
            for pre_dep in pre_deps:
                print("PRE DEP STATUS")
                print(pre_dep.status)
                if pre_dep.status == "Confirmed" and pre_deps.count() >= 2: #Dapat atleast 2 sila nidedeploy
                    pre_dep.status = "Done"
                    pre_dep.save()
                    k9 = pre_dep.k9

                    k9.training_status = "Deployed"
                    k9.assignment = str(team)
                    k9.save()
                    deploy = Team_Dog_Deployed.objects.create(k9=k9, status="Pending", team_assignment=team)
                    deploy.save()
                    print(deploy)


                    #TODO dito pa lang ibabawas yung items

                elif pre_dep.status == "Pending" or pre_deps.count() < 2:
                    pre_dep.status = "Cancelled"
                    pre_dep.save()

        # except: pass

    #TODO For every k9 in deploy_k9_list 1.)Create Team_Dog_deployed 2.) Change status to Deployed ./
    #TODO Assign new Team Leader with every Team_Dog_Deployed
    #TODO update k9s total_dogs_deployed per port

    team_list = list(set(team_list))
    update_port_info(team_list)

    return None

#TODO all Team dogs deployed under the team of TL with "Pending status)
#Step 5 is in TL Dashboard (Confirm Arrival)

# Step 6
# Check if TL has confirmed arrival. If not, escalate to admin
# @periodic_task(run_every=crontab(hour=8, minute=30))
@periodic_task(run_every=timedelta(seconds=30))
def check_initial_dep_arrival():

    deployed = Team_Dog_Deployed.objects.filter(date_pulled=None).filter(status = "Pending").exclude(team_assignment = None)

    team_list = []
    for item in deployed:
        k9 = item.k9

        pre_dep = K9_Pre_Deployment_Items.objects.get(k9=k9)
        initial_sched = pre_dep.initial_sched
        delta = initial_sched.date_start - datetime.today().date()

        if delta.days > 5: #TODO Escalate first to admin rather than straight up MIA agad
            item.date_pulled = datetime.today().date()
            k9.training_status = "MIA"
            k9.save()
            item.save()

        if item.team_assignment:
            team_list.append(item.team_assignment.id)

    update_port_info(team_list)

    return None


@periodic_task(run_every=timedelta(seconds=10))
def test():
    print('Test Hello')

# @periodic_task(run_every=timedelta(seconds=10))
# def test_error():
#     k9 = K9.objects.get(id = 3000)


def update_request_info(dog_request):

    try:
        request = Dog_Request.objects.get(id = dog_request.id)
        deployed = Team_Dog_Deployed.objects.filter(team_requested = request).count()
        request.k9s_deployed = deployed
        request.save()

    except: pass

    return None

#Request Deployment
#1.) Create a Team_Dog_Deployed for every sched happening today (exclude K9_schedules with existing Team_Dog_Deployed) (status is pending and date pulled is none) exclude team_requested = None
#2.) Every K9 in Team_Dog_Deployed have their training_statuses temporarily set to #Deployed
#3.) Update dog_request info (k9s deployed)

#TODO remove creation of duplicates
# @periodic_task(run_every=crontab(hour=8, minute=30))
@periodic_task(run_every=timedelta(seconds=30))
def deploy_dog_request():
    # When Schedule is today, change training status to deployed
    scheds = K9_Schedule.objects.filter(date_start=date.today()).filter(status = "Request").exclude(dog_request = None)

    for sched in scheds: #per k9
        # sched.k9.training_status = 'Deployed'
        # sched.k9.save()

        # temporarily pull out from port
        recent_port_deploy = Team_Dog_Deployed.objects.filter(team_requested=sched.dog_request).filter(date_pulled=None).latest('date_added')
        recent_port_deploy.date_pulled = datetime.today().date()
        recent_port_deploy.save()

        if Team_Dog_Deployed.objects.filter(k9 = sched.k9, team_requested = sched.dog_request, status="Pending").count() == 0:
            deploy = Team_Dog_Deployed.objects.create(k9 = sched.k9, team_requested = sched.dog_request, status="Pending")
        handler = sched.k9.handler
        handler.position = "Handler"
        handler.save()
        update_request_info(sched.dog_request)


        tl = sched.dog_request.team_leader

        try:
            handler_to_tl = User.objects.get(id = tl.id)
            handler_to_tl.position = "Team Leader"
            handler_to_tl.save()
        except: pass


    return None


#Pull out dogs where request end date is now
# @periodic_task(run_every=crontab(hour=8, minute=30))
@periodic_task(run_every=timedelta(seconds=30))
def pull_dog_request():

    requests = Dog_Request.objects.filter(end_date = date.today())

    for request in requests:
        try:
            deployed = Team_Dog_Deployed.objects.filter(date_pulled = None).get(team_requested = request)
            deployed.date_pulled = date.today()
            deployed.save()

            handler = deployed.handler
            handler.position = "Handler"
            handler.save()

            #TODO Create Team_Dog_Deployed for last port assignment
            recent_port = Team_Dog_Deployed.objects.filter(k9=deployed.k9).exclude(team_assignment=None).exclude(date_pulled = None).latest('date_pulled')

            if Team_Dog_Deployed.objects.filter(k9 = deployed.k9, team_assignment = recent_port.team_assignment, status="Pending").count() == 0:
                new_deploy = Team_Dog_Deployed.objects.create(k9 = deployed.k9, team_assignment = recent_port.team_assignment, status="Pending")
        except: pass
    return None

#Every nth hour, check if arrival is confirmed by checking if Team_Dog_deployed status is still pending after start date
def check_arrival_to_request(dog_request):

    deployed = Team_Dog_Deployed.objects.filter(team_requested = dog_request)

    for item in deployed:
        if item.status == "Pending" and dog_request.start_date == date.today():
            deployed.date_pulled = date.today()
            deployed.save()
            k9 = item.k9
            k9.training_status = "MIA"
            k9.save()
        # creation of TDD is through deploy_dog_request()

    return None

#Every nth hour, check if arrival is confirmed by checking if Team_Dog_deployed status is still pending after 5 days after recent request date pull
def check_arrival_to_ports_via_request(team_assignment):

    deployed = Team_Dog_Deployed.objects.filter(team_assignment=team_assignment)
    recent_request_deployment = Team_Dog_Deployed.objects.filter(k9=deployed.k9).exclude(team_request=None).exclude(date_pulled = None).latest('date_pulled')
    today = datetime.today().date()
    for item in deployed:
        delta = today - recent_request_deployment.date
        if item.status == "Pending" and delta.days >= 5:
            deployed.date_pulled = date.today()
            deployed.save()
            k9 = item.k9
            k9.training_status = "MIA"
            k9.save()
        #creation of TDD is through pull_dog_request()

    return None


# @periodic_task(run_every=crontab(hour=8, minute=30))
# @periodic_task(run_every=timedelta(seconds=30))
def check_arrivals():

    team_assignments = Team_Assignment.objects.all()
    dog_requests = Dog_Request.objects.all() #TODO filter for currently ongoing dog requests

    team_list = []
    for team_assignment in team_assignments:
        check_arrival_to_ports_via_request(team_assignment)
        team_list.append(team_assignment.id)

    for dog_request in dog_requests:
        check_arrival_to_request(dog_request)
        update_request_info()

    update_port_info(team_list)

#     return None