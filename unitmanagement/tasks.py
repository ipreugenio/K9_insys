from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
import time
from K9_insys.celery import app
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from datetime import timedelta, date, datetime
from decimal import Decimal
from django.db.models import Sum

from planningandacquiring.models import K9
from deployment.models import Dog_Request
from unitmanagement.models import Notification, PhysicalExam
from inventory.models import Medicine_Inventory, Medicine_Received_Trail, Food, Food_Subtracted_Trail
# Create your tasks here
# The @shared_task decorator lets you create tasks that can be used by any app(s).

# TODO UNITMANAGEMENT NOTIFS
#@periodic_task(run_every=crontab(hour=6, minutes=0))
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
            Notification.objects.create(message= str(k9_breed) + ' is recommended to mate this week as she is most fertile!')

        if k9_breed.last_proestrus_date == date.today():
            Notification.objects.create(message= str(k9_breed) + ' is in heat!')

        if k9_breed.metestrus_date == date.today():
            Notification.objects.create(message= 'If you mated ' + str(k9_breed) + ', she is about to show signs of pregnancy!')

    # PHYSICAL EXAMINATION DUE
    for phex in phex:
        if date.today() ==  phex.due_notification():
            Notification.objects.create(k9=phex.dog, message= str(phex.dog.name) + ' is due for Physical Examination in next week.' + str(phex.date_next_exam))
        elif date.today() ==  phex.date_next_exam:
            Notification.objects.create(k9=phex.dog, message= str(phex.dog.name) + ' is due for Physical Examination today')

    # VACCINATION DUE
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

# TODO DEPLOYMENT NOTIFS
#@periodic_task(run_every=crontab(hour=6, minutes=0))
def deployment_notifs():
    request = Dog_Request.objects.all()

    # DOG REQUEST LOCATION
    for request in request:
        # start date
        if date.today() ==  request.due_start():
            Notification.objects.create(message= str(request.location) + ' deployment requested by ' + 
            str(request.requester) + ' is due to start next week.')
        elif date.today() ==  request.start_date:
           Notification.objects.create(message= str(request.location) + ' deployment requested by ' + 
            str(request.requester) + ' will start today.')

        # end date
        elif date.today() ==  request.due_end():
            Notification.objects.create(message= str(request.location) + ' deployment requested by ' + 
            str(request.requester) + ' is due to end next week.')
        elif date.today() ==  request.end_date:
            Notification.objects.create(message= str(request.location) + ' deployment requested by ' + 
            str(request.requester) + ' will end today.')

# TODO AUTO SUBTRACT 
# TODO Add Subtract trail for food
#@periodic_task(run_every=crontab(hour=6, minutes=0))
# every 5am?
def auto_subtract():
    # TODO Vitamins consumption

    # FOOD CONSUMPTION EVERYDAY
    k9_labrador = K9.objects.filter(breed='Labrador Retriever').filter(age__gte=1).count()
    k9_jack_russel = K9.objects.filter(breed='Jack Russel').filter(age__gte=1).count()
    k9_others = K9.objects.filter(age__gte=1).exclude(breed='Labrador Retriever').exclude(breed='Jack Russel').count()
    food = Food.objects.filter(foodtype='Adult Dog Food').exclude(quantity=0).order_by('quantity')

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
    delivery_days = 8 
    day_adult = Decimal(total) * delivery_days
    day_puppy = Decimal(food) * delivery_days
    day_milk = Decimal(milk) * delivery_days

    adult_dfq = Food.objects.filter(foodtype='Adult Dog Food').aggregate(sum=Sum('quantity'))['sum']
    puppy_dfq = Food.objects.filter(foodtype='Puppy Dog Food').aggregate(sum=Sum('quantity'))['sum']
    milk_q = Food.objects.filter(foodtype='Milk').aggregate(sum=Sum('quantity'))['sum']

    if adult_dfq <= day_adult:
        Notification.objects.create(message= 'Adult Dog Food is low. Its time to reorder!')
    if puppy_dfq <= day_puppy:
        Notification.objects.create(message= 'Puppy Dog Food is low. Its time to reorder!')
    if milk_q <= day_milk:
        Notification.objects.create(message= 'Milk is low. Its time to reorder!')
        

# LOW INVENTORY NOTIFS
#@periodic_task(run_every=timedelta(seconds=10))
def inventory_notifs():
    pass

@periodic_task(run_every=timedelta(seconds=10))
def test():

        