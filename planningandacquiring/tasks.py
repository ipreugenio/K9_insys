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