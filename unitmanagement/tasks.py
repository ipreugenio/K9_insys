from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
import time
from K9_insys.celery import app
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import timedelta, date, datetime
from decimal import Decimal
from django.db.models import  Sum
from dateutil.relativedelta import relativedelta

from planningandacquiring.models import K9
from deployment.models import Dog_Request, Team_Dog_Deployed, K9_Schedule, Team_Assignment
from profiles.models import User
from unitmanagement.models import Notification, PhysicalExam

from inventory.models import Medicine_Inventory, Medicine_Received_Trail, Food, Food_Subtracted_Trail, Medicine_Subtracted_Trail
from inventory.models import Safety_Stock
from unitmanagement.models import Notification, PhysicalExam, Health, Handler_Incident
from profiles.serializers import NotificationSerializer
# Create your tasks here
# The @shared_task decorator lets you create tasks that can be used by any app(s).
#from celery.schedules import crontab

#TODO
#ADD POSITION, OTHER_ID

# TODO UNITMANAGEMENT NOTIFS
#8AM
@periodic_task(run_every=crontab(hour=8, minutes=0))
def unitmanagement_notifs():
    k9 = K9.objects.all() 
    phex = PhysicalExam.objects.all()
    p = K9.objects.filter(next_proestrus_date=date.today())

    # HEAT CYCLE
    # when it is time for the next heat, the last_heat = next_heat thus updating the dates
    for p in p:
        p.last_proestrus_date = p.next_proestrus_date
        p.save()

    k9_breed = K9.objects.all(training_status='For-Breeding') 
    for k9_breed in k9_breed:
        if k9_breed.estrus_date == date.today() and k9_breed.age >= 1:
            Notification.objects.create(k9=k9_breed, message= str(k9_breed) + ' is recommended to mate this week as she is most fertile!', notif_type='heat_cycle', position='Veterinarian')

        if k9_breed.last_proestrus_date == date.today():
            Notification.objects.create(k9=k9_breed, message= str(k9_breed) + ' is in heat!', notif_type='heat_cycle')

        if k9_breed.metestrus_date == date.today():
            Notification.objects.create(k9=k9_breed, message= 'If you mated ' + str(k9_breed) + ', she is about to show signs of pregnancy!', notif_type='heat_cycle', position='Veterinarian')

    # PHYSICAL EXAMINATION DUE
    for phex in phex:
        if date.today() ==  phex.due_notification():
            Notification.objects.create(k9=phex.dog, message= str(phex.dog.name) + ' is due for Physical Examination in next week.' + str(phex.date_next_exam), notif_type='physical_exam', position='Veterinarian')
        elif date.today() ==  phex.date_next_exam:
            Notification.objects.create(k9=phex.dog, message= str(phex.dog.name) + ' is due for Physical Examination today', notif_type='physical_exam', position='Veterinarian')

    # VACCINATION DUE
    for k9 in k9:
        age = date.today() - k9.birth_date
        if age.days == 14 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 1st Deworming this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 28 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due 2nd Deworming this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 42 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due 3rd Deworming this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 42 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 1st DHPPiL+CV Vaccination this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 42 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 1st Heartworm Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 56 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 1st Bordetella Bronchiseptica Bacterin this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 56 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 1st Tick and Flea Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 63 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 2nd DHPPiL+CV this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 63 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 4th Deworming this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 70 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 2nd Heartworm Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 77 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 2nd Bordetella Bronchiseptica Bacterin this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 84 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for Anti-Rabies Vaccination this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 84 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 2nd Tick and Flea Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 84 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 3rd DHPPiL+CV Vaccination this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 98 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 3rd Heartworm Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 105 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 1st DHPPiL4 Vaccination this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 112 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 3rd Tick and Flea Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 126 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 2nd DHPPiL4 Vaccination this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 126 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 4th Heartworm Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 140 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 4th Tick and Flea Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 154 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 5th Heartworm Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 168 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 5th Tick and Flea Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 183 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 6th Heartworm Prevention this week.', notif_type='vaccination', position='Veterinarian')        
        elif age.days == 196 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 6th Tick and Flea Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 210 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 7th Heartworm Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 224 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 7th Tick and Flea Prevention this week.', notif_type='vaccination', position='Veterinarian')
        elif age.days == 238 :
            Notification.objects.create(k9=k9, message= str(k9.name) + ' is due for 8th Heartworm Prevention this week.', notif_type='vaccination', position='Veterinarian')        
    
    #health change to working if done with medicine
    health = Health.objects.filter(status='Pending')

    for h in health:
        if h.date_done == date.today():
            Notification.objects.create(k9=h.dog, message= str(h.dog.name) + ' will be done with medication today!',
            notif_type='medicine_done', position='Veterinarian', other_id=h.id)        
        
        if date.today() == h.date_done:
            h.status = 'Done'
            h.dog.status = 'Working Dog'

    #TODO
    #Handler on leave end_date is today
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
                #where dog is deployed
                td = Team_Dog_Deployed.objects.filter(k9=k9).latest()
                
                try:
                #where location is updated
                    ta = Team_Assignment.objects.get(id=td.team_assignment.id)
                    
                    #create new team dog
                    Team_Dog_Deployed.objects.create(k9=k9, handler=h,team_assignment=ta,
                    date_added=date.today())

                    if k9.capability == 'EDD':
                        ta.EDD_deployed = ta.EDD_deployed+1
                    elif k9.capability == 'NDD':
                        ta.NDD_deployed = ta.NDD_deployed+1
                    elif k9.capability == 'SAR':
                        ta.SAR_deployed = ta.SAR_deployed+1

                    ta.save()
                except Team_Assignment.DoesNotExist:
                    pass
            except Team_Dog_Deployed.DoesNotExist:
                pass            



# TODO DEPLOYMENT NOTIFS
#8:30AM
@periodic_task(run_every=crontab(hour=8, minutes=30))
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


# 6AM
@periodic_task(run_every=crontab(hour=6, minutes=0))
def auto_subtract():
    # TODO Vitamins consumption
    vitamins = Medicine_Inventory.objects.filter(medicine__med_type='Vitamins').exclude(quantity=0).order_by('quantity')
    v = K9.objects.filter(status='Working Dog').count()

    # FOOD CONSUMPTION EVERYDAY
    k9_labrador = K9.objects.filter(breed='Labrador Retriever').filter(age__gte=1).count()
    k9_jack_russel = K9.objects.filter(breed='Jack Russel').filter(age__gte=1).count()
    k9_others = K9.objects.filter(age__gte=1).exclude(breed='Labrador Retriever').exclude(breed='Jack Russel').count()
    food = Food.objects.filter(foodtype='Adult Dog Food').exclude(quantity=0).order_by('quantity')

    for vitamins in vitamins:
        if v > 0:
            if v > vitamins.quantity:
                Medicine_Subtracted_Trail.objects.create(inventory=vitamins, quantity=vitamins.quantity)
                v = v-food.quantity
                vitamins.quantity = 0 
                vitamins.save()
            else: 
                Medicine_Subtracted_Trail.objects.create(inventory=vitamins, quantity=v)
                vitamins.quantity = vitamins.quantity-v
                v=0
                vitamins.save()


    # dog_count * food_per_day 
    lab = k9_labrador * 0.5
    jack = k9_jack_russel * 0.3
    oth = k9_others * 0.8
    total = lab+jack+oth
    t = Decimal(total)
    
    for food in food:
        if t > 0:
            if t > food.quantity:
                Food_Subtracted_Trail.objects.create(inventory=food, quantity=food.quantity)
                t = t-food.quantity
                food.quantity = 0 
                food.save()
            else: 
                Food_Subtracted_Trail.objects.create(inventory=food, quantity=t)
                food.quantity = food.quantity-t
                t=0
                food.save()
    
    # PUPPY FOOD CONSUMPTION
    # get puppy count by age
    third_fourth = K9.objects.filter(age_days__range=(21,28)).count() # 3rd-4th week : milk only
    fifth_sixth = K9.objects.filter(age_days__range=(29,42)).count() # 5th-6th week
    seventh_eight = K9.objects.filter(age_days__range=(43,57)).count() # 5th-6th week
    ninth_tenth = K9.objects.filter(age_days__range=(58,72)).count() # 9th-10th week
    eleventh_twelve = K9.objects.filter(age_days__range=(73,87)).count() # 11th-12th week

    four = K9.objects.filter(age_month=4).count() # 4 mos
    five = K9.objects.filter(age_month=5).count() # 5 mos
    six = K9.objects.filter(age_month=6).count() # 6 mos
    seven = K9.objects.filter(age_month=7).count() # 7 mos
    eight = K9.objects.filter(age_month=8).count() # 8 mos
    nine_twelve = K9.objects.filter(age_month__range=(9,12)).count() # 9-12 mos

    # get puppy milk per day consumption by age
    tf_milk = third_fourth * 32
    fs_milk = fifth_sixth * 48
    se_milk = seventh_eight * 48
    nt_milk = ninth_tenth * 60
    et_milk = eleventh_twelve * 72

    # get puppy food per day consumption by age
    fs_food = fifth_sixth * 0.08
    se_food = seventh_eight * 0.12
    nt_food = ninth_tenth * 0.18
    et_food = eleventh_twelve * 0.24
    four_food = four * 0.25
    five_food = five * 0.30
    six_food = six * 0.35
    seven_food = seven * 0.40
    eight_food = eight * 0.45
    nine_twelve_food = nine_twelve * 0.50

    milk = tf_milk + fs_milk + se_milk + nt_milk + et_milk
    food = fs_food + se_food + nt_food + et_food + four_food + five_food + six_food + seven_food + eight_food + nine_twelve_food
    
    query_milk = Food.objects.filter(foodtype='Milk').exclude(quantity=0).order_by('quantity')
    query_food = Food.objects.filter(foodtype='Puppy Dog Food').exclude(quantity=0).order_by('quantity')

    t_food = Decimal(food)
    t_milk = Decimal(milk)

    # Subtract Milk
    for query_milk in query_milk:
        if t_milk > 0:
            if t_milk > query_milk.quantity:
                Food_Subtracted_Trail.objects.create(inventory=food, quantity=query_milk.quantity)
                t_milk = t_milk-query_milk.quantity
                query_milk.quantity = 0 
                query_milk.save()
            else: 
                Food_Subtracted_Trail.objects.create(inventory=food, quantity=t_milk)
                query_milk.quantity = query_milk.quantity-t_milk
                t_milk=0
                query_milk.save()

    # Subtract Puppy Food
    for query_food in query_food:
        if t_food > 0:
            if t_food > query_food.quantity:
                Food_Subtracted_Trail.objects.create(inventory=food, quantity=query_food.quantity)
                t_food = t_food-query_food.quantity
                query_food.quantity = 0 
                query_food.save()
            else: 
                Food_Subtracted_Trail.objects.create(inventory=food, quantity=t_food)
                query_food.quantity = query_food.quantity-t_food
                t_food=0
                query_food.save()
    

    # EXPIRATION OF MEDICINE
    med_receive = Medicine_Received_Trail.objects.filter(expiration_date=date.today())
    med_inventory = Medicine_Inventory.objects.all()
    for med in med_receive: #receive trail
        for m in med_inventory: #inventory
            if m.medicine == med.inventory.medicine:
                m.quantity = m.quantity - med.quantity
                m.save()

    # TODO Get Delivery Days
    # INVENTORY LOW NOTIFICATION
    delivery_days = 4 
    day_adult = Decimal(total) * delivery_days
    day_puppy = Decimal(food) * delivery_days
    day_milk = Decimal(milk) * delivery_days

    try:
        stock = Safety_Stock.objects.get(id=1)
        stock.puppy_food = day_puppy
        stock.adult_food = day_adult
        stock.milk = milk
        stock.save()
    except (stock.DoesNotExist):
        ...

    adult_dfq = Food.objects.filter(foodtype='Adult Dog Food').aggregate(sum=Sum('quantity'))['sum']
    puppy_dfq = Food.objects.filter(foodtype='Puppy Dog Food').aggregate(sum=Sum('quantity'))['sum']
    milk_q = Food.objects.filter(foodtype='Milk').aggregate(sum=Sum('quantity'))['sum']

    if adult_dfq <= day_adult:
        Notification.objects.create(message= 'Adult Dog Food is low. Its time to reorder!', notif_type='inventory_low')
    if puppy_dfq <= day_puppy:
        Notification.objects.create(message= 'Puppy Dog Food is low. Its time to reorder!', notif_type='inventory_low')
    if milk_q <= day_milk:
        Notification.objects.create(message= 'Milk is low. Its time to reorder!', notif_type='inventory_low')
        

# 9AM
@periodic_task(run_every=crontab(hour=9, minutes=0))
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


@periodic_task(run_every=timedelta(seconds=10))
def test():
    # TODO
    print('Yey!')


# 8:50AM
@periodic_task(run_every=crontab(hour=8, minutes=50))
def due_retired_k9():
    k9 = K9.objects.all()
    for k9 in k9:
        due_year = k9.year_retired - relativedelta(year=-1) 
        if due_year == date.today()
            Notification.objects.create(message=str(k9) + ' is due for retirement next year!', 
            notif_type = 'retired_k9',
            position="Administrator")

# 12AM
#DELETE FUNCTION WHERE 2MONTHS OF NOTIFICATION IS DELETED
@periodic_task(run_every=crontab(hour=24, minutes=0))
def delete():
    notif_delete = Notification.objects.filter(datetime=date.today-timedelta(days=60))
    notif_delete.delete()
    
    
        