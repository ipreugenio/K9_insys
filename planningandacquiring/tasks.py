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

    k9_breed = K9.objects.all(training_status='For-Breeding')

    for k9_breed in k9_breed:
        if k9_breed.estrus_date == date.today() and k9_breed.age >= 1:
            Notification.objects.create(k9=k9_breed, message=str(
                k9_breed) + ' is recommended to mate this week as she is most fertile!', notif_type='heat_cycle',
                                        position='Veterinarian')

        if k9_breed.last_proestrus_date == date.today():
            Notification.objects.create(k9=k9_breed, message=str(k9_breed) + ' is in heat!', notif_type='heat_cycle')

        # if k9_breed.metestrus_date == date.today():
        #     Notification.objects.create(k9=k9_breed, message='If you mated ' + str(
        #         k9_breed) + ', she is about to show signs of pregnancy!', notif_type='heat_cycle',
        #                                 position='Veterinarian')
        
        for p in p:
            p.last_proestrus_date = p.next_proestrus_date
            p.save()