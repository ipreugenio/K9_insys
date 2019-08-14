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

# @periodic_task(run_every=crontab(hour=9, minute=0))
# def test():
#    Notification.objects.create(message='meassage sent')
       
# 8:50AM
@periodic_task(run_every=crontab(hour=8, minute=50))
def due_retired_k9():
    k9 = K9.objects.all()
    for k9 in k9:
        due_year = k9.year_retired - relativedelta(year=-1) 
        if due_year == date.today():
            Notification.objects.create(message=str(k9) + ' is due for retirement next year!', 
            notif_type = 'retired_k9',
            position="Administrator")

@periodic_task(run_every=crontab(hour=8, minute=50))
def in_heat_notifs():
    # HEAT CYCLE
    # when it is time for the next heat, the last_heat = next_heat thus
    
    # updating the dates
    p = K9.objects.filter(next_proestrus_date=date.today())
    for p in p:
        p.last_proestrus_date = p.next_proestrus_date
        p.save()

    k9_breed = K9.objects.all(Q(training_status='For-Breeding') | Q(training_status='Breeding'))

    for k9_breed in k9_breed:
        if k9_breed.last_proestrus_date == date.today():
            Notification.objects.create(k9=k9_breed, message=str(k9_breed) + ' is in heat! Please prepare her for mating.', notif_type='heat_cycle')
            
        if k9_breed.last_estrus_date == date.today():
            Notification.objects.create(k9=k9_breed, message=str(k9_breed) + ' is best mated today! (1st session)', notif_type='heat_cycle')
    
        if (k9_breed.last_estrus_date + relativedelta(days=2)) == date.today():
            Notification.objects.create(k9=k9_breed, message=str(k9_breed) + ' is 2nd session of mating is today!', notif_type='heat_cycle')
            
        if (k9_breed.last_estrus_date + relativedelta(days=4)) == date.today():
            Notification.objects.create(k9=k9_breed, message=str(k9_breed) + ' is 3rd session of mating is today!', notif_type='heat_cycle')
            
    #TODO
    # k9 might be pregnant

    # k9 might give birth
    km = K9_Mated.objects.filter(status='Pregnant')
    for kmm in km:
        due = kmm.date_mated + relativedelta(days=63)
        if date.today() == due:
            Notification.objects.create(k9=kmm.mother, message=str(kmm.mother) + ' might give birth within this week!', notif_type='pregnancy')
            
    kb = K9_Mated.objects.filter(status='Breeding')
    for kbb in kb:
        due = kmm.date_mated + relativedelta(days=22)
        if date.today() == due:
            Notification.objects.create(k9=kbb.mother, message=' Please confirm if ' + str(kbb.mother) + 'is pregnant or not.', notif_type='breeding')
        
         

@periodic_task(run_every=timedelta(seconds=30)) 
    def k9_sched():
        # k9_schedule
        ke = K9_Schedule.objects.exclude(status='Checkup').filter(date_start__lt=date.today())
        for kee in ke:
            k9 = K9.objects.get(id=ks.k9.id)
            Notification.objects.create(k9=kee.k9, position='Handler', user=k9.handler,message='Your schedule deployment/event is today.', notif_type='initial_deployment')

        #Check-up
        ks = K9_Schedule.objects.filter(status='Checkup').filter(date_start=date.today())
        for kss in ks:
            k9 = K9.objects.get(id=ks.k9.id)

            Notification.objects.create(k9=kss.k9, position='Handler', user=k9.handler,message=str(k9) + 'is due for check-up today.', notif_type='checkup')
        
        