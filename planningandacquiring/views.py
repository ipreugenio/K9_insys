from django.shortcuts import render
from django.http import Http404

from .models import K9, K9_Past_Owner, K9_Donated, K9_Parent, K9_Quantity, Dog_Breed, K9_Supplier, K9_Litter, K9_Mated
from .forms import add_donated_K9_form, add_donator_form, add_K9_parents_form, add_offspring_K9_form, select_breeder, K9SupplierForm, date_mated_form, HistDateForm, DateForm

from planningandacquiring.models import Proposal_Budget, Proposal_Milk_Food, Proposal_Vac_Prev, Proposal_Medicine, Proposal_Vet_Supply, Proposal_Kennel_Supply, Proposal_Others, Actual_Budget, Actual_Milk_Food, Actual_Vac_Prev, Actual_Medicine, Actual_Vet_Supply, Actual_Kennel_Supply, Actual_Others

from training.models import Training
from profiles.models import Account, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.http import JsonResponse
from django.contrib import messages
from .forms import ReportDateForm, add_breed_form, k9_detail_form, SupplierForm, ProcuredK9Form
from deployment.models import Dog_Request, Team_Assignment

from unitmanagement.models import Health, HealthMedicine, VaccinceRecord, VaccineUsed
from inventory.models import Food, Food_Subtracted_Trail, Medicine, Medicine_Inventory, Medicine_Subtracted_Trail, Miscellaneous, Miscellaneous_Subtracted_Trail, Food_Received_Trail, Medicine_Received_Trail, Miscellaneous_Received_Trail

from unitmanagement.models import Health, HealthMedicine, VaccinceRecord, VaccineUsed, Notification
from inventory.models import Food, Medicine, Medicine_Inventory, Medicine_Subtracted_Trail, Miscellaneous

from django.db.models.functions import Trunc, TruncMonth, TruncYear, TruncDay
from django.db.models import aggregates, Avg, Count, Min, Sum, Q, Max
import dateutil.parser
from faker import Faker

#statistical imports
from math import *
from decimal import Decimal
from sklearn.metrics import mean_squared_error


from datetime import datetime as dt

from datetime import timedelta

from datetime import date

from faker import Faker

#statistical imports
from math import *
from decimal import Decimal
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

#graphing imports
from igraph import *
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.graph_objs.layout as lout

#forecasting imports
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from random import random, randint
from statsmodels.tsa.stattools import adfuller, kpss
import statsmodels.api as sm

import math
# Create your views here.

def notif(request):
    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)
    
    if user_in_session.position == 'Veterinarian':
        notif = Notification.objects.filter(position='Veterinarian').order_by('-datetime')
    elif user_in_session.position == 'Handler':
        notif = Notification.objects.filter(user=user_in_session).order_by('-datetime')
    else:
        notif = Notification.objects.filter(position='Administrator').order_by('-datetime')
   
    return notif

def user_session(request):
    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)
    return user_in_session

def index(request):

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    context = {

        'notif_data':notif_data,
        'count':count,
        'user':user,

    }

    return render(request, 'planningandacquiring/index.html', context)

def budgeting(request):
    # k9_value = 0
    # k9_cy = 0
    # k9_ny = 0
    # born_ny = 0
    # need_procure_ny = 0
    # total_k9 = 0,
    # dog_food = 0
    # total_food = 0
    # vac_ny = 0
    # vac_total = 0
    # b_ny_med = 0
    # total_medicine = 0
    # vet_arr = 0
    # vet_total = 0
    # ken_arr = 0
    # ken_total = 0
    # oth_arr = 0
    # oth_total = 0
    # train_arr = 0
    # train_total = 0 
    # grand_total = 0
    # stat = None
    next_year = dt.now().year + 1
    current_year = dt.now().year

    stat = True
    all_k9 = K9.objects.exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost")
    print(stat)

    #K9 to be born and die
    k9_breeded = K9_Mated.objects.filter(status='Pregnant')
    print(k9_breeded)
    ny_breeding = [] 
    ny_data = []
    for kb in k9_breeded:
        m = kb.date_mated  + timedelta(days=63)
        if m.year == next_year:
            ny = [kb.mother.breed, kb.mother.litter_no]
            ny_data.append(ny)
            ny_breeding.append(kb.mother.breed)
            #get k9, value, total count by breed
            
    kb_index = pd.Index(ny_breeding)

    b_values = kb_index.value_counts().keys().tolist() #k9 breed to be born
    b_counts = kb_index.value_counts().tolist() #number of k9 to be born by breed

    #Total count of all dogs born next year by breed,
    breed_u = np.unique(ny_breeding)

    p = pd.DataFrame(ny_data, columns=['Breed', 'Litter'])
    h = p.groupby(['Breed']).sum()

    total_born = []  
    total_born_count = []  
    for u in breed_u:
        total_born_count.append(h.loc[u].values[0])
        born = [u,h.loc[u].values[0]]
        total_born.append(born)

    ny_dead = []
    for kd in all_k9:
        b = Dog_Breed.objects.get(breed = kd.breed)
        if (kd.age + 1) >= b.life_span:
            ny_dead.append(kd.breed)
            

    kd_index = pd.Index(ny_dead)

    d_values = kd_index.value_counts().keys().tolist()
    d_counts = kd_index.value_counts().tolist()

    all_k = all_k9.values_list('breed', flat=True).order_by()

    all_ku = np.unique(all_k)

    all_dogs = K9.objects.exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count()

    all_kk = []
    for a in all_ku:
        c = all_k9.filter(breed=a).count()
        cc = [a,c]
        all_kk.append(cc)

    k9_cy = all_dogs
    k9_ny = all_dogs - sum(d_counts)
    k9_t_ny = k9_cy+50

    difference_k9 = k9_cy - k9_ny
    born_ny=0
    for b in k9_breeded:
        d = Dog_Breed.objects.get(breed=b.mother.breed)
        born_ny = born_ny + d.litter_number

    # born_ny =  sum(total_born_count)

    need_procure_ny = (50 + difference_k9) - born_ny
    if need_procure_ny <= 0:
        need_procure_ny = 0
    
    try:
        k9_value = round(Dog_Breed.objects.all().aggregate(avg=Avg('value'))['avg'], 2)
    except:
        k9_value = 15000

    #get dog food based on dog count
    # k9 = all_k9 - dead + born + Forecasted added_procured
    # monthly 

    # 1L = 1000grams
    total_milk = born_ny *  21 #liter
    total_puppy_food = ((born_ny * 15) * 9) / 20 #sack
    total_adult_food = (need_procure_ny+k9_ny) * 12 #sack

    dog_food = []

    #end
    milk = Food_Subtracted_Trail.objects.filter(inventory__foodtype='Milk').latest('date_subtracted')
    puppy = Food_Subtracted_Trail.objects.filter(inventory__foodtype='Puppy Dog Food').filter(inventory__unit='Sack - 20kg').latest('date_subtracted')
    adult = Food_Subtracted_Trail.objects.filter(inventory__foodtype='Adult Dog Food').filter(inventory__unit='Sack - 20kg').latest('date_subtracted')
    
    #get current quantity
    sum_milk = Food.objects.filter(foodtype='Milk').aggregate(sum=Sum('quantity'))['sum']
    sum_puppy = Food.objects.filter(foodtype='Puppy Dog Food').aggregate(sum=Sum('quantity'))['sum']
    sum_adult = Food.objects.filter(foodtype='Adult Dog Food').aggregate(sum=Sum('quantity'))['sum']

    #milk
    tm = total_milk - sum_milk
    tmp = milk.inventory.price
    tmt = round((tm*tmp),2)

    #puppy
    tp = Decimal(total_puppy_food)- Decimal(sum_puppy)
    tpp = puppy.inventory.price
    tpt = round((tp*tpp),2)

    #adult
    ta = total_adult_food - sum_adult
    tap = adult.inventory.price
    tat = round((ta*tap),2)

    dm = [milk,tmp,int(tm),tmt]
    dp = [puppy,tpp,int(tp),tpt]
    da = [adult,tap,int(ta),tat]
    
    if tmt > 0:
        dog_food.append(dm)
    if tpt > 0:
        dog_food.append(dp)
    if tat > 0:
        dog_food.append(da) 
    
    for (n,(item1,item2,item3,item4)) in enumerate(dog_food):
        total_food =+ item4

    #MEDICINE EXPIRATION
    mrt = Medicine_Received_Trail.objects.filter(expiration_date__year=next_year).filter(status='Pending').values('inventory').annotate(sum = Sum('quantity'))

    med_item_id = []
    med_item_q = []
    for m in mrt: 
        for key,value in m.items():
            if key == 'inventory':
                med_item_id.append(value)
            else:
                med_item_q.append(value)

    zip_a = zip(med_item_id, med_item_q)

    # Medicine that has expirations next year
    ny_med = []
    cy_med = [] 
    eny_ar_count = 0
    eny_bbb_count = 0
    eny_dw_count = 0
    eny_dcv_count = 0
    eny_dc4_count = 0
    eny_hw_count = 0
    eny_tf_count = 0
    
    for a,b in zip_a:  
        c = Medicine_Inventory.objects.get(id=a)
        x = [c, (c.quantity - b)]
        z = [c, c.quantity]
        ny_med.append(x)
        cy_med.append(z)

        if c.medicine.immunization == 'Anti-Rabies':
            eny_ar_count = eny_ar_count + b
        elif c.medicine.immunization == 'Bordetella Bronchiseptica Bacterin':
            eny_bbb_count = eny_bbb_count + b
        elif c.medicine.immunization == 'Deworming':
            eny_dw_count = eny_dw_count + b
        elif c.medicine.immunization == 'DHPPiL+CV':
            eny_dcv_count = eny_dcv_count + b
        elif c.medicine.immunization == 'DHPPiL4':
            eny_dc4_count = eny_dc4_count + b
        elif c.medicine.immunization == 'Heartworm':
            eny_hw_count = eny_hw_count + b
        elif c.medicine.immunization == 'Tick and Flea':
            eny_tf_count = eny_tf_count + b

    #get all medicine used in the current year exclude vaccine
    mst_cy = Medicine_Subtracted_Trail.objects.filter(date_subtracted__year=current_year).exclude(inventory__medicine__med_type='Vaccine').exclude(inventory__medicine__med_type='Preventive').values('inventory').distinct()
    mst_ny = []
    np_arr = np.array(ny_med)
    for mst in mst_cy:
        for key,value in mst.items():
            if key == 'inventory':
                c = Medicine_Inventory.objects.get(id=value)
                if c in np_arr:
                    for (n, (item1, item2)) in enumerate(ny_med):
                        if c == item1:
                            a = [c, item2, c.medicine.price]
                            mst_ny.append(a)
                else:
                    a = [c, c.quantity, c.medicine.price]
                    mst_ny.append(a)

    #med needed to procure next year and total
    b_ny_med = []
    total_medicine = 0
    for (n, (item1, item2, item3)) in enumerate(mst_ny):
        ms = Medicine_Subtracted_Trail.objects.filter(inventory=item1).aggregate(sum=Sum('quantity'))['sum']
        r = ms / k9_cy
        r = r * (k9_ny+born_ny+need_procure_ny) - item2

        if np.ceil(r) > 0:
            s = Decimal(np.ceil(r)) * Decimal(item3)
            ss = round(s, 2)
            b = [item1,item3,int(np.ceil(r)),ss]
            b_ny_med.append(b)
            total_medicine = total_medicine+ss
    
    # need_procure_ny == needed to be procured next year
    # born_ny == k9 born next year
    # k9_ny == k9 next year minus dead
    # k9_cy == k9 in current year

    #get all dogs that will be born/procured next year

    mst_vaccine_cy = Medicine_Subtracted_Trail.objects.filter(date_subtracted__year=current_year).filter(inventory__medicine__med_type='Vaccine').values('inventory').distinct().order_by('-date_subtracted')
    
    mst_vaccine_ny = []
    for mst in mst_vaccine_cy:
        for key,value in mst.items():
            if key == 'inventory':
                c = Medicine_Inventory.objects.get(id=value)
                # mst_arr = np.array(mst_vaccine_ny)
                if not c.medicine.immunization in np.array(mst_vaccine_ny):
                    a = [c,c.medicine.immunization,c.medicine.price]
                    mst_vaccine_ny.append(a)

    if not 'Anti-Rabies' in np.array(mst_vaccine_ny):
        try:
            mrt = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Anti-Rabies').values('inventory').annotate(sum=Sum('quantity'))

            inv = 0
            invq = 0
            temp =[]
            for i in mrt: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            a = [md,md.medicine.immunization,md.medicine.price]
            mst_vaccine_ny.append(a)
        except:
            pass

    elif not 'Bordetella Bronchiseptica Bacterin' in np.array(mst_vaccine_ny):
        try:
            mrt = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Bordetella Bronchiseptica Bacterin').values('inventory').annotate(sum=Sum('quantity'))

            inv = 0
            invq = 0
            temp =[]
            for i in mrt: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            a = [md,md.medicine.immunization,md.medicine.price]
            mst_vaccine_ny.append(a)
        except:
            pass

    elif not 'DHPPiL+CV' in np.array(mst_vaccine_ny):
        try:
            mrt = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='DHPPiL+CV').values('inventory').annotate(sum=Sum('quantity'))
            inv = 0
            invq = 0
            temp =[]
            for i in mrt: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            a = [md,md.medicine.immunization,md.medicine.price]
            mst_vaccine_ny.append(a)
        except:
            pass
    
    elif not 'DHPPiL4' in np.array(mst_vaccine_ny):
        try:
            mrt = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='DHPPiL4').values('inventory').annotate(sum=Sum('quantity'))
            inv = 0
            invq = 0
            temp =[]
            for i in mrt: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            a = [md,md.medicine.immunization,md.medicine.price]
            mst_vaccine_ny.append(a)
        except:
            pass

    #item, quantity, total
    vac_ny = []


    #3 dhppil_cv, 1 anti rabies, 2 bordertella, 2 dhppil4,
    #3 anti rabies, bordertella, dhppil4,
    
    for (n, (item1, item2, item3)) in enumerate(mst_vaccine_ny):
        if item2 == 'Anti-Rabies':
            mi = Medicine_Inventory.objects.filter(medicine__immunization=item2).aggregate(sum=Sum('quantity'))['sum']
            m = Medicine_Inventory.objects.get(id=item1.id)
            c = mi - eny_ar_count
            bn = int((born_ny + k9_ny) - c)
            pr = round(bn*m.medicine.price, 2)
            mi_a = [m,m.medicine.price,bn,pr]
            if pr > 0:
                vac_ny.append(mi_a)
        elif item2 == 'Bordetella Bronchiseptica Bacterin':
            mi = Medicine_Inventory.objects.filter(medicine__immunization=item2).aggregate(sum=Sum('quantity'))['sum']
            m = Medicine_Inventory.objects.get(id=item1.id)
            c = mi - eny_bbb_count
            bn = int(((born_ny*2) + k9_ny) - c)
            pr = round(bn*m.medicine.price, 2)
            mi_a = [m,m.medicine.price,bn,pr]
            if pr > 0:
                vac_ny.append(mi_a)
        elif item2 == 'DHPPiL+CV':
            mi = Medicine_Inventory.objects.filter(medicine__immunization=item2).aggregate(sum=Sum('quantity'))['sum']
            m = Medicine_Inventory.objects.get(id=item1.id)
            c = mi - eny_dcv_count
            bn = int(((born_ny*3) + k9_ny) - c)
            pr = round(bn*m.medicine.price, 2)
            mi_a = [m,m.medicine.price,bn,pr]
            if pr > 0:
                vac_ny.append(mi_a)
        elif item2 == 'DHPPiL4':
            mi = Medicine_Inventory.objects.filter(medicine__immunization=item2).aggregate(sum=Sum('quantity'))['sum']
            m = Medicine_Inventory.objects.get(id=item1.id)
            c = mi - eny_dc4_count
            bn = int(((born_ny*2) + k9_ny) - c)
            pr = round(bn*m.medicine.price, 2)
            mi_a = [m,m.medicine.price,bn,pr]
            if pr > 0:
                vac_ny.append(mi_a)
    #4 deworming, 8 heartworm, 7 tick&flee

# Deworming 
    try:
        data = Medicine_Subtracted_Trail.objects.filter(inventory__medicine__immunization='Deworming').values('inventory').annotate(sum=Sum('quantity'))
        print(data)
        inv = 0
        invq = 0
        temp =[]
        for i in data: 
            for key,value in i.items():
                if key == 'inventory':
                    i = value
                if key == 'sum':
                    s = value
                    a = [i, s]
                    temp.append(a)
    
        #medicine inventory, count
        for (n, (item1,item2)) in enumerate(temp):
            if item2 > invq:
                inv = item1
                invq = item2
        print(inv)
        md = Medicine_Inventory.objects.get(id=inv)
        dcq = Medicine_Inventory.objects.filter(medicine__immunization='Deworming').aggregate(sum=Sum('quantity'))['sum']
        dcq = dcq - eny_dw_count
        p_deworm = md.medicine.price
        q_deworm = int((born_ny * 7) + ((k9_ny+need_procure_ny) * 2) - dcq)
        t_deworm = p_deworm*q_deworm
        mi_a = [md,md.medicine.price,q_deworm,t_deworm]
        if t_deworm > 0:
            vac_ny.append(mi_a)

    except:
        data = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Deworming').values('inventory').annotate(sum=Sum('quantity'))

        inv = 0
        invq = 0
        temp =[]
        for i in data: 
            for key,value in i.items():
                if key == 'inventory':
                    i = value
                if key == 'sum':
                    s = value
                    a = [i, s]
                    temp.append(a)

        #medicine inventory, count
        for (n, (item1,item2)) in enumerate(temp):
            if item2 > invq:
                inv = item1
                inv1 = item2

        md = Medicine_Inventory.objects.get(id=inv)
        dcq = Medicine_Inventory.objects.filter(medicine__immunization='Deworming').aggregate(sum=Sum('quantity'))['sum']
        dcq = dcq - eny_dw_count
        p_deworm = md.medicine.price
        q_deworm = int((born_ny * 7) + ((k9_ny+need_procure_ny) * 2) - dcq)
        t_deworm = p_deworm*q_deworm
        mi_a = [md,md.medicine.price,q_deworm,t_deworm]
        if t_deworm > 0:
            vac_ny.append(mi_a)

    # Heartworm
    try:
        data = Medicine_Subtracted_Trail.objects.filter(inventory__medicine__immunization='Heartworm').values('inventory').annotate(sum=Sum('quantity'))
        
        inv = 0
        invq = 0
        temp =[]
        for i in data: 
            for key,value in i.items():
                if key == 'inventory':
                    i = value
                if key == 'sum':
                    s = value
                    a = [i, s]
                    temp.append(a)

        #medicine inventory, count
        for (n, (item1,item2)) in enumerate(temp):
            if item2 > invq:
                inv = item1
                inv1 = item2

        md = Medicine_Inventory.objects.get(id=inv)
        hcq = Medicine_Inventory.objects.filter(medicine__immunization='Heartworm').aggregate(sum=Sum('quantity'))['sum']
        hcq = hcq - eny_hw_count
        p_heatworm = md.medicine.price
        q_heatworm = int((born_ny * 8) + ((k9_ny+need_procure_ny) * 12) - hcq)
        t_heatworm = p_heatworm*q_heatworm
        mi_a = [md,md.medicine.price,q_heatworm,t_heatworm]
        if t_heatworm > 0:
            vac_ny.append(mi_a)
    except:
        data = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Heartworm').values('inventory').annotate(sum=Sum('quantity'))

        inv = 0
        invq = 0
        temp =[]
        for i in data: 
            for key,value in i.items():
                if key == 'inventory':
                    i = value
                if key == 'sum':
                    s = value
                    a = [i, s]
                    temp.append(a)

        #medicine inventory, count
        for (n, (item1,item2)) in enumerate(temp):
            if item2 > invq:
                inv = item1
                inv1 = item2

        md = Medicine_Inventory.objects.get(id=inv)
        hcq = Medicine_Inventory.objects.filter(medicine__immunization='Heartworm').aggregate(sum=Sum('quantity'))['sum']
        hcq = hcq - eny_hw_count
        p_heatworm = md.medicine.price
        q_heatworm = int((born_ny * 8) + ((k9_ny+need_procure_ny) * 12) - hcq)
        t_heatworm = p_heatworm*q_heatworm
        mi_a = [md,md.medicine.price,q_heatworm,t_heatworm]
        if t_heatworm > 0:
            vac_ny.append(mi_a)

    # Tick & Flee
    try:
        data = Medicine_Subtracted_Trail.objects.filter(inventory__medicine__immunization='Tick and Flea').values('inventory').annotate(sum=Sum('quantity'))

        inv = 0
        invq = 0
        temp =[]
        for i in data: 
            for key,value in i.items():
                if key == 'inventory':
                    i = value
                if key == 'sum':
                    s = value
                    a = [i, s]
                    temp.append(a)

        #medicine inventory, count
        for (n, (item1,item2)) in enumerate(temp):
            if item2 > invq:
                inv = item1
                inv1 = item2

        md = Medicine_Inventory.objects.get(id=inv)
        tcq = Medicine_Inventory.objects.filter(medicine__immunization='Tick and Flea').aggregate(sum=Sum('quantity'))['sum']
        tcq = tcq - eny_tf_count
        p_tickflea = md.medicine.price
        k_tf = k9_cy % 7
        q_tickflea = int((born_ny * 7 ) + ((k_tf/k9_cy) * (k9_ny+need_procure_ny)) - tcq)
        t_tickflea = round(Decimal(p_tickflea)*Decimal(q_tickflea), 2)
        mi_a = [md,md.medicine.price,q_tickflea,t_tickflea]
        if t_tickflea > 0:
            vac_ny.append(mi_a)
    except:
        data = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Tick and Flea').values('inventory').annotate(sum=Sum('quantity'))

        inv = 0
        invq = 0
        temp =[]
        for i in data: 
            for key,value in i.items():
                if key == 'inventory':
                    i = value
                if key == 'sum':
                    s = value
                    a = [i, s]
                    temp.append(a)

        #medicine inventory, count
        for (n, (item1,item2)) in enumerate(temp):
            if item2 > invq:
                inv = item1
                inv1 = item2

        md = Medicine_Inventory.objects.get(id=inv)
        tcq = Medicine_Inventory.objects.filter(medicine__immunization='Tick and Flea').aggregate(sum=Sum('quantity'))['sum']
        tcq = tcq - eny_tf_count
        p_tickflea = md.medicine.price
        k_tf = k9_cy % 7
        q_tickflea = int((born_ny * 7 ) + ((k_tf/k9_cy) * (k9_ny+need_procure_ny)) - tcq)
        t_tickflea = round(Decimal(p_tickflea)*Decimal(q_tickflea), 2)
        mi_a = [md,md.medicine.price,q_tickflea,t_tickflea]
        if t_tickflea > 0:
            vac_ny.append(mi_a)

    vac_total = 0
    for (n, (item1, item2, item3,item4)) in enumerate(vac_ny):
        vac_total = vac_total + item4
    #Vet Supply
    #item,quantity,total
    vet_arr=[]
    vet_total = 0
    mvi = Miscellaneous_Subtracted_Trail.objects.filter(inventory__misc_type="Vet Supply").filter(date_subtracted__year=current_year).values('inventory').distinct()

    for m in mvi: 
        for key,value in m.items():
            if key == 'inventory':
                c = Miscellaneous.objects.get(id=value)
                mvi_i = Miscellaneous_Subtracted_Trail.objects.filter(inventory=c).filter(date_subtracted__year=current_year).aggregate(sum=Sum('quantity'))['sum']
                tq = int((mvi_i/k9_cy) * (k9_ny+need_procure_ny+born_ny))
                tp = round(Decimal(tq)*Decimal(c.price), 2)
                mv = [c,c.price, int(np.ceil(tq)), tp]
                vet_total = vet_total+tp
                vet_arr.append(mv)
    

    #Kennel supplies 
    #item,quantity,total
    ken_arr=[]
    ken_total = 0

    mki = Miscellaneous_Subtracted_Trail.objects.filter(inventory__misc_type="Kennel Supply").filter(date_subtracted__year=current_year).values('inventory').distinct()

    for m in mki: 
        for key,value in m.items():
            if key == 'inventory':
                c = Miscellaneous.objects.get(id=value)
                mvi_i = Miscellaneous_Subtracted_Trail.objects.filter(inventory=c).filter(date_subtracted__year=current_year).aggregate(sum=Sum('quantity'))['sum']
                tq = int((mvi_i/k9_cy) * (k9_ny+need_procure_ny+born_ny))
                tp = round(Decimal(tq)*Decimal(c.price), 2)
                mv = [c,c.price, int(np.ceil(tq)), tp]
                ken_total = ken_total+tp
                ken_arr.append(mv)

    #get Others
    oth_arr = []
    oth_total = 0
    moi = Miscellaneous_Subtracted_Trail.objects.filter(inventory__misc_type="Others").filter(date_subtracted__year=current_year).values('inventory').distinct()
    #get all unique inventory and distribute to dogs

    for m in moi: 
        for key,value in m.items():
            if key == 'inventory':
                c = Miscellaneous.objects.get(id=value)
                mvi_i = Miscellaneous_Subtracted_Trail.objects.filter(inventory=c).filter(date_subtracted__year=current_year).aggregate(sum=Sum('quantity'))['sum']
                tq = int((mvi_i/k9_cy) * (k9_ny+need_procure_ny+born_ny))
                tp = round(Decimal(tq)*Decimal(c.price), 2)
                mv = [c,c.price, int(np.ceil(tq)), tp]
                oth_total = oth_total+tp
                oth_arr.append(mv)

    mat_dog = K9.objects.filter(status='Material Dog').count() + born_ny + need_procure_ny
    train_total = Decimal(mat_dog * 18000)
    
    train_arr = ['K9 Training',18000,mat_dog,train_total]

    grand_total=total_food+vac_total+total_medicine+vet_total+ken_total+oth_total+train_total
    
    if request.method == "POST":
        
        try:
            pb = Proposal_Budget.objects.filter(date_created__year=dt.today().year).latest('date_created')
            pb.k9_current = k9_ny
            pb.k9_needed = need_procure_ny
            pb.k9_breeded = born_ny
            pb.food_milk_total = total_food
            pb.vac_prev_total = vac_total
            pb.medicine_total = total_medicine
            pb.vet_supply_total = vet_total
            pb.kennel_total = ken_total
            pb.others_total = oth_total
            pb.training_total = train_total
            pb.grand_total = grand_total
            pb.date_created = dt.today()
            pb.save()

            Proposal_Milk_Food.objects.filter(proposal=pb).delete()
            Proposal_Vac_Prev.objects.filter(proposal=pb).delete()
            Proposal_Medicine.objects.filter(proposal=pb).delete()
            Proposal_Vet_Supply.objects.filter(proposal=pb).delete()
            Proposal_Kennel_Supply.objects.filter(proposal=pb).delete()
            Proposal_Others.objects.filter(proposal=pb).delete()
            
            #item, price, quantity, total
            for (n,(item1,item2,item3,item4)) in enumerate(dog_food):
                percentage = Decimal(item4/grand_total)
                Proposal_Milk_Food.objects.create(item=item1.inventory, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb)

            for (n, (item1, item2, item3,item4)) in enumerate(vac_ny):
                percentage = Decimal(item4/grand_total)
                Proposal_Vac_Prev.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb)
                
            for (n, (item1, item2, item3,item4)) in enumerate(b_ny_med):
                percentage = Decimal(item4/grand_total)
                Proposal_Medicine.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb)
                
            for (n, (item1, item2, item3,item4)) in enumerate(vet_arr):
                percentage = Decimal(item4/grand_total)
                Proposal_Vet_Supply.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb)
            
            for (n, (item1, item2, item3,item4)) in enumerate(ken_arr):
                percentage = Decimal(item4/grand_total)
                Proposal_Kennel_Supply.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb)
                
            for (n, (item1, item2, item3,item4)) in enumerate(oth_arr):
                percentage = Decimal(item4/grand_total)
                Proposal_Others.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb)
                
        except:
            pb = Proposal_Budget.objects.create(k9_current=k9_ny, k9_needed=need_procure_ny, k9_breeded=born_ny, food_milk_total=total_food, vac_prev_total=vac_total, medicine_total=total_medicine, vet_supply_total=vet_total, kennel_total=ken_total, others_total=oth_total, training_total=train_total, grand_total=grand_total, date_created=dt.today())

            #item, price, quantity, total
            for (n,(item1,item2,item3,item4)) in enumerate(dog_food):
                percentage = Decimal(item4/grand_total)
                Proposal_Milk_Food.objects.create(item=item1.inventory, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb)

            for (n, (item1, item2, item3,item4)) in enumerate(vac_ny):
                percentage = Decimal(item4/grand_total)
                Proposal_Vac_Prev.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb)
                
            for (n, (item1, item2, item3,item4)) in enumerate(b_ny_med):
                percentage = Decimal(item4/grand_total)
                Proposal_Medicine.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb)
                
            for (n, (item1, item2, item3,item4)) in enumerate(vet_arr):
                percentage = Decimal(item4/grand_total)
                Proposal_Vet_Supply.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb)
            
            for (n, (item1, item2, item3,item4)) in enumerate(ken_arr):
                percentage = Decimal(item4/grand_total)
                Proposal_Kennel_Supply.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb)
                
            for (n, (item1, item2, item3,item4)) in enumerate(oth_arr):
                percentage = Decimal(item4/grand_total)
                Proposal_Others.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb)
                


    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'today':dt.today(),
        'next_year':next_year,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'k9_value': k9_value,
        'k9_cy': k9_cy,
        'k9_ny': k9_ny,
        'born_ny': born_ny,
        'need_procure_ny':need_procure_ny,
        'total_k9': born_ny+k9_ny+need_procure_ny,
        'dog_food':dog_food,
        'total_food':total_food,
        'vac_ny':vac_ny,
        'vac_total':vac_total,
        'b_ny_med': b_ny_med,
        'total_medicine':total_medicine,
        'vet_arr': vet_arr,
        'vet_total': vet_total,
        'ken_arr': ken_arr,
        'ken_total': ken_total,
        'oth_arr': oth_arr,
        'oth_total': oth_total,
        'train_arr':train_arr,
        'train_total':train_total,
        'grand_total': grand_total,
        'stat': stat,
    }
    return render (request, 'planningandacquiring/budgeting.html', context)

def budgeting_list(request):

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    data = Proposal_Budget.objects.all()
    if request.method == 'POST':
        pass

    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data': data,
    }
    return render(request, 'planningandacquiring/budget_list.html', context)

def report(request):
    form = ReportDateForm()
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title' : "REPORT",
        'form': form,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        }
    return render (request, 'planningandacquiring/report.html', context)

def add_procured_k9(request):
    form = SupplierForm(request.POST or None)
    k9_formset = inlineformset_factory(K9_Supplier, K9, form=add_donated_K9_form, extra=1, can_delete=True)
    formset = k9_formset(request.POST, request.FILES)
    style = "ui green message"

    if request.method == "POST":
        if form.is_valid():
            supplier_data = form.cleaned_data['supplier']
            supplier = K9_Supplier.objects.get(name=supplier_data)

            if formset.is_valid():
                print("Formset is valid")
                for form in formset:
                   k9 = form.save(commit=False)
                   k9.supplier = supplier
                   k9.source = 'Procurement'
                   k9.training_status = 'Unclassified'
                   k9.save()

                style = "ui green message"
                messages.success(request, 'Procured K9s has been added!')
                
                return redirect('planningandacquiring:K9_list')
            else:
                for form in formset:
                    print(form.errors)
                style = "ui red message"
                messages.warning(request, 'Invalid input data!')
        
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

        return HttpResponseRedirect('../breeding_k9_confirmed/')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title' : "Procured K9",
        'form': SupplierForm(),
        'formset':k9_formset(),
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'style':style,
        }
    return render (request, 'planningandacquiring/add_procured_k9.html', context)

def add_supplier(request):
    form = K9SupplierForm(request.POST)
    style = ''
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            form.save()

            style = "ui green message"
            messages.success(request, 'Supplier has been added!')
            form = K9SupplierForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

        form.initial['organization'] = None
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title' : "Add K9 Supplier",
        'texthelp' : "Please input the Supplier information below.",
        'form': form,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'style':style,
        }
    return render (request, 'planningandacquiring/add_k9_supplier.html', context)

#Form format
def add_donated_K9(request):
    form = add_donated_K9_form(request.POST or None, request.FILES or None)
    style = "ui teal message"
    if request.method == 'POST':
        if form.is_valid():
            k9 = form.save()
            k9.training_status = "Unclassified"
            k9.source = "Procurement"
            k9.save()

            request.session['k9_id'] = k9.id


            return HttpResponseRedirect('confirm_donation/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
            print(form)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title' : "Add New K9",
        'form' : form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'planningandacquiring/add_donated_K9.html', context)

'''
def add_donator(request):
    form = add_donator_form(request.POST)
    style = "ui teal message"
    if request.method == 'POST':
        if form.is_valid():
            donator= form.save()

            request.session['donator_id'] = donator.id

            return HttpResponseRedirect('confirm_donation/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'Title': "Receive Donated K9",
        'form': form,
        'style': style,
    }

    return render(request, 'planningandacquiring/add_donator.html', context)
'''

def confirm_donation(request):

    k9_id = request.session['k9_id']
    k9= K9.objects.get(id = k9_id)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "Add New K9",
        'k9': k9,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render(request, 'planningandacquiring/confirm_K9_donation.html', context)

def donation_confirmed(request):
    k9_id = request.session['k9_id']

    k9 = K9.objects.get(id=k9_id)
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    if 'ok' in request.POST:
        VaccinceRecord.objects.create(k9=k9, deworming_1=True, deworming_2=True, deworming_3=True,
                                      deworming_4=True, dhppil_cv_1=True, dhppil_cv_2=True, dhppil_cv_3=True,
                                      heartworm_1=True, heartworm_2=True,
                                      heartworm_3=True, heartworm_4=True, heartworm_5=True, heartworm_6=True,
                                      heartworm_7=True, heartworm_8=True,
                                      anti_rabies=True, bordetella_1=True, bordetella_2=True, dhppil4_1=True,
                                      dhppil4_2=True, tick_flea_1=True,
                                      tick_flea_2=True, tick_flea_3=True, tick_flea_4=True, tick_flea_5=True,
                                      tick_flea_6=True, tick_flea_7=True)

        return render(request, 'planningandacquiring/donation_confirmed.html', context)
    else:
        #delete k9
        k9.delete()

        #NOTIF SHOW
        notif_data = notif(request)
        count = notif_data.filter(viewed=False).count()
        user = user_session(request)
        context = {
            'Title': "Add New K9",
            'form': add_donated_K9_form,
            'notif_data':notif_data,
            'count':count,
            'user':user,
        }
        return render(request, 'planningandacquiring/add_donated_K9.html', context)

def breeding_list(request):
    data1 = K9_Mated.objects.filter(status='Breeding')
    data2 = K9_Mated.objects.filter(status='Pregnant')
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "Breeding List",
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data1':data1,
        'data2':data2,
    }
    return render(request, 'planningandacquiring/breeding_list.html', context)

def confirm_failed_pregnancy(request, id):
    data = K9_Mated.objects.get(id=id) # get k9
    mom = K9.objects.get(id=data.mother.id)
    decision = request.GET.get('decision')
    
    if decision == 'confirm':
        data.status = 'Pregnant'
        mom.training_status = 'Breeding'

        messages.success(request, 'You have confirmed that ' + str(data.mother) + 'is pregnent.')

    elif decision == 'failed':
        data.status = 'Failed'
        mom.training_status = 'For-Breeding'
        K9_Litter.objects.create(mother=data.mother, father=data.father, litter_no=0)
        
        messages.success(request, 'You have confirmed that ' + str(data.mother) + ' is not pregnant.')

    data.save()
    mom.save()

    return redirect('planningandacquiring:breeding_list')

def add_K9_parents(request):
    style = "ui teal message"
    mother  = K9.objects.filter(sex="Female").filter(training_status = "For-Breeding").filter(age__gte = 1).filter(age__lte = 6).filter(reproductive_stage = "Estrus")
    father = K9.objects.filter(sex="Male").filter(training_status = "For-Breeding").filter(age__gte = 1).filter(age__lte = 6)
    
    mom = []
    sick = []
    b_arr = []
    for m in mother:
        h = Health.objects.filter(dog=m).count()
        mom.append(m)
        sick.append(h)

        birth = K9_Litter.objects.filter(mother=m).aggregate(sum=Sum('litter_no'))['sum']
        death = K9_Litter.objects.filter(mother=m).aggregate(sum=Sum('litter_died'))['sum']

        if birth != None or death != None:
            total = (birth / (birth+death)) * 100
        else:
            total=100
        
        b_arr.append(int(total))

    mlist = zip(mom,sick,b_arr)

    if request.method == 'POST':
        f = request.POST.get('radiof')
        m = request.POST.get('radiom')

        request.session["mother_id"] = m
        request.session["father_id"] = f

        return redirect('planningandacquiring:confirm_K9_parents')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "K9_Breeding",
        'style': style,
        'mlist' : mlist,
        'father' : father,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'planningandacquiring/add_K9_parents.html', context)

def confirm_K9_parents(request):
    form = date_mated_form(request.POST or None)
    mother_id = request.session["mother_id"]
    father_id = request.session["father_id"]

    mother = K9.objects.get(id=mother_id)
    father = K9.objects.get(id=father_id)

    if request.method == 'POST':
        if form.is_valid():
            mated = form.save(commit=False)
            mated.mother = mother
            mated.father = father
            mated.save()

            mother.training_status = 'Breeding'
            mother.save()

        return redirect('planningandacquiring:breeding_list')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'mother': mother,
        'father': father,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'form':form,
    }

    return render(request, 'planningandacquiring/confirm_K9_parents.html', context)

def mating_confirmed(request):
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render(request, 'planningandacquiring/mating_confirmed.html', context)

def K9_parents_confirmed(request):
    mothers = K9.objects.filter(sex="Female")
    fathers = K9.objects.filter(sex="Male")

    mother_list = []
    father_list = []

    for mother in mothers:
        mother_list.append(mother)

    for father in fathers:
        father_list.append(father)

    if 'ok' in request.POST:
        return HttpResponseRedirect('add_K9_offspring_form/')
    else:
        #NOTIF SHOW
        notif_data = notif(request)
        count = notif_data.filter(viewed=False).count()
        user = user_session(request)
        context = {
            'Title': "Receive Donated K9",
            'form': add_K9_parents_form,
            'mothers': mother_list,
            'fathers': father_list,
            'notif_data':notif_data,
            'count':count,
            'user':user,
        }
        return render(request, 'planningandacquiring/add_K9_parents.html', context)

#TODO
#formset
def add_K9_offspring(request, id):
    form = DateForm(request.POST or None)
    k9_formset = formset_factory(add_offspring_K9_form, extra=1, can_delete=True)
    formset = k9_formset(request.POST, request.FILES)
    style = ''

    data = K9_Mated.objects.get(id=id)
    data.status = 'Pregnancy Done'
    if data.mother.breed != data.father.breed:
        breed = 'Mixed'
    else:
        breed = data.mother.breed

    k9_count = 0

    
    if request.method == 'POST':
        data.mother.training_status = 'For-Breeding'
        data.save()
        if form.is_valid():
            date = form.cleaned_data['birth_date']

        if formset.is_valid():
            for form in formset:
                k9 = form.save(commit=False)
                k9.source = "Breeding"
                k9.breed = breed
                k9.birth_date = date
                k9.save()
                
                #K9 parents create
                K9_Parent.objects.create(mother=data.mother, father=data.father, offspring=k9)

                k9_count = k9_count+1

            died =  request.POST.get('litter_died')
            K9_Litter.objects.create(mother=data.mother, father=data.father, litter_no=k9_count, litter_died=died)
            
            #Mom
            mom = K9.objects.get(id=data.mother.id)
            mom.training_status='For-Breeding'
            mom.save()
            #Dad
            dad = K9.objects.get(id=data.father.id)
            dad.save()

            data.save()
            messages.success(request, 'You have added k9 offspring!')
            return redirect('planningandacquiring:breeding_list')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')


    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "Receive Donated K9",
        'form': form,
        # 'formset': k9_formset(),
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data':data,
    }

    return render(request, 'planningandacquiring/add_K9_offspring.html', context)

def breeding_k9_confirmed(request):
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render(request, 'planningandacquiring/breeding_confirmed.html', context)

def confirm_breeding(request):
    offspring_id = request.session['offspring_id']
    mother_id = request.session['mother_id']
    father_id = request.session['father_id']

    offspring = K9.objects.get(id=offspring_id)
    mother = K9.objects.get(id=mother_id)
    father = K9.objects.get(id=father_id)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "Receive Donated K9",
        'offspring': offspring,
        'mother': mother,
        'father': father,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'planningandacquiring/confirm_breeding.html', context)

def breeding_confirmed(request):
    offspring_id = request.session['offspring_id']
    mother_id = request.session['mother_id']
    father_id = request.session['father_id']

    offspring = K9.objects.get(id=offspring_id)
    mother = K9.objects.get(id=mother_id)
    father = K9.objects.get(id=father_id)

    if 'ok' in request.POST:
        k9_parent = K9_Parent(offspring = offspring, mother = mother, father = father)
        k9_parent.save()

        cvr = VaccinceRecord.objects.create(k9=offspring)
        VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_3')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil_cv_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='bordetella_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil_cv_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_4')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='bordetella_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='anti_rabies')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil_cv_3')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_3')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil4_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_3')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil4_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_4')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_4')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_5')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_5')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_6')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_6')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_7')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_7')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_8')


        #NOTIF SHOW
        notif_data = notif(request)
        count = notif_data.filter(viewed=False).count()
        context={
            'notif_data':notif_data,
            'count':count,
        }

        return render(request, 'planningandacquiring/breeding_confirmed.html', context)
    else:
        #delete offspring
        offspring.delete()

        mothers = K9.objects.filter(sex="Female")
        fathers = K9.objects.filter(sex="Male")

        mother_list = []
        father_list = []

        for mother in mothers:
            mother_list.append(mother)

        for father in fathers:
            father_list.append(father)

        #NOTIF SHOW
        notif_data = notif(request)
        count = notif_data.filter(viewed=False).count()
        user = user_session(request)
        context = {
            'Title': "Receive Donated K9",
            'form': add_K9_parents_form,
            'mothers': mother_list,
            'fathers': father_list,
            'notif_data':notif_data,
            'count':count,
            'user':user,
        }
        return render(request, 'planningandacquiring/add_K9_parents.html', context)


#Listview format
def K9_listview(request):

    k9 = K9.objects.all()

    #Test trunc
    #print(K9_Quantity.objects.annotate(day=TruncDay('date_bought')).values('day').annotate(total=Sum('quantity')).order_by('date_bought'))

    #Sample Aggregation by year
    '''
    k9_quantities = K9_Quantity.objects.all()
    
    my_list = []
    for k9_quantity in k9_quantities:
        date = k9_quantity.date_bought
        my_list.append(date.year)

    my_list = list(set(my_list))
    my_quantities = []

    for item in my_list:
        sum = 0
        for k9_quantity in k9_quantities:
            date = k9_quantity.date_bought
            if date.year == item:
                sum += k9_quantity.quantity
        my_quantities.append(sum)
    '''

    '''
    for x in range(50):
        date = fake.date_between(start_date='-6y', end_date='-1y')
        name = fake.name()
        dog = K9(name = name, birth_date = date)
        dog.save()'''
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title' : 'K9 List',
        'k9' : k9,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'planningandacquiring/K9_list.html', context)

#Detailview format
def K9_detailview(request, id):
    k9 = K9.objects.get(id = id)
    form = k9_detail_form(request.POST or None, request.FILES or None, instance=k9)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'K9 Details Updated!')

            if k9.training_status == 'For-Deployment' or k9.training_status == 'For-Breeding':
                k9.training_status = request.POST.get('radio')
                k9.save()

            return redirect('planningandacquiring:K9_detail', id = k9.id)

        # if 'change_training_status' in request.POST:
        #     print(request.POST.get('radio'))
        #     k9.training_status = request.POST.get('radio')
        #     k9.save()
        #     messages.success(request, 'K9 is now ' + k9.training_status + '!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    try:
        parent = K9_Parent.objects.get(offspring=k9)
    except K9_Parent.DoesNotExist:
        context = {
            'Title': 'K9 Details',
            'k9' : k9,
            'notif_data':notif_data,
            'count':count,
            'user':user,
            'form':form,
        }
    else:
        parent_exist = 1
        context = {
            'Title': 'K9 Details',
            'k9': k9,
            'parent': parent,
            'parent_exist': parent_exist,
            'notif_data':notif_data,
            'count':count,
            'user':user,
            'form':form,
        }

    return render(request, 'planningandacquiring/K9_detail.html', context)


##################### FORECASTING ########################

# create a difference transform of the dataset
def difference(dataset):
    diff = list()
    for i in range(1, len(dataset)):
        value = dataset[i] - dataset[i - 1]
        diff.append(value)
    return np.array(diff)

def inverse_difference(last_ob, value):

    return value + last_ob

def running_total(dataset):
    sum = list()
    cumsum = 0
    for i in range(1, len(dataset)):
        value = dataset[i]
        cumsum = cumsum + value
        sum.append(cumsum)
    return np.array(sum)


# Make a prediction give regression coefficients and lag obs
def predict(coef, history):
    yhat = coef[0]
    for i in range(1, len(coef)):
        yhat += coef[i] * history[-i]

    return yhat


def Autoregression(data):
    X = difference(data.values)
    X = difference(X)
    size = int(len(X) * 0.70)
    data = X[0:size]
    model = AR(data)
    model = model.fit(transparams=True)
    print("AR MODEL")
    print(model)
    return model

def Moving_Average(data):
    X = difference(data.values)
    X = difference(X)
    size = int(len(X) * 0.70)
    data = X[0:size]
    model = ARMA(data, order=(0, 1))
    model = model.fit(transparams=True)
    return model

def Autoregressive_Moving_Average(data):
    X = difference(data.values)
    X = difference(X)

    size = int(len(X) * 0.70)
    data = X[0:size]

    print("ARMA DATA")
    print(data)

    model = ARMA(data, order=(2, 1))
    model = model.fit(transparams=True, start_params=[1, .1, .1, .1])
    return model


def Autoregressive_Integrated_Moving_Average(data):
    X = difference(data.values)
    X = difference(X)
    size = int(len(X) * 0.70)
    data = X[0:size]
    print("ARIMA DATA")
    print(data)
    model = ARIMA(data, order=(2, 1, 1))
    model = model.fit(transparams=True, start_params=[1, .1, .1, .1])
    print("MODEL FIT ARIMA")
    print(model)
    return model


def Simple_Exponential_Smoothing(data):
    X = difference(data.values)
    size = int(len(X) * 0.70)
    data, datax =  data[0:size], data[-size:]
    test, train = X[0:size], X[size:]
    model = SimpleExpSmoothing(data)

    model_fit = model.fit()

    forecast = model_fit.fittedfcast
    temp = np.delete(forecast, 0)
    predict = model_fit.fcastvalues
    predict = predict.flatten()
    predict = predict.tolist()
    predict = predict[0]
    predict = round(predict)
    print("SES DATA")
    print(data)
    print("SES FORECASTS")
    print(forecast)
    print("SES PREDICT")
    print(predict)
    error = mean_squared_error(datax, temp)
    root_error = sqrt(error)
    root_error = int(root_error * 10 ** 2) / 10.0 ** 2

    SES = []

    SES.append(forecast)
    SES.append(predict)
    SES.append(root_error)

    print("SES COEF")
    coef = model_fit.params
    print(coef)

    return SES

def Holt_Exponential_Smoothing(data):
    X = difference(data.values)
    size = int(len(X) * 0.70)
    data, datax = data[0:size], data[-size:]
    model = ExponentialSmoothing(data, trend="add")

    model_fit = model.fit()

    forecast = model_fit.fittedfcast
    temp = np.delete(forecast, 0)
    predict = model_fit.fcastvalues
    predict = predict.flatten()
    predict = predict.tolist()
    predict = predict[0]
    predict = round(predict)
    fitted = model_fit.fittedvalues
    error = mean_squared_error(datax, temp)
    root_error = sqrt(error)
    root_error = int(root_error * 10 ** 2) / 10.0 ** 2

    HWES = []

    HWES.append(forecast)
    HWES.append(predict)
    HWES.append(root_error)

    print("HWES COEF")
    coef = model_fit.params
    print(coef)

    return HWES


#TODO Fix to work with both stationarity and non-stationarity
def forecast(timeseries, model):

    # split dataset
    X = difference(timeseries.values)
    X = difference(X)

    #TODO Differencing order should change depending on model.fit differencing order

    print("X")
    print(X)

    #Use 66% of data for training
    size = int(len(X) * 0.70)
    train, test = X[0:size], X[size:]
    traind, testd = timeseries.values[0:size], timeseries.values[size+2:]

    print("TRAIND")
    print(traind)
    print("TESTD")
    print(testd)

    print("Model")
    print (model)

    model_fit = model

    print("Model Fit")
    print(model_fit)

    #window = model_fit.k_ar
    coef = model_fit.params
    print ("COEF DATA TYPE")
    print(type(coef))
    print("COEF")
    print(coef)

    yhat = 0
    # walk forward over time steps in test
    history = [train[i] for i in range(len(train))]
    predictions = list()

    for t in range(len(test)):
        yhat = predict(coef, history)
        obs = test[t]
        predictions.append(yhat)
        history.append(obs)

    print("PREDICTIONS")
    print(predictions)

    #revert_differencing = summation(predictions)
    revert_differencing = [inverse_difference(testd[i], predictions[i]) for i in range(len(predictions))]
    error = mean_squared_error(testd, revert_differencing)
    root_error = sqrt(error)
    root_error = int(root_error * 10 ** 2) / 10.0 ** 2
    print('Test MSE: %.3f' % error)
    print('Test RMSE: %.3f' % root_error)
    print("Prediction : " + str(yhat))


    yhat = revert_differencing[-1]

    print("REVERT DIFFERENCING")
    print(revert_differencing)

    yhat = yhat.flatten()
    yhat = yhat.tolist()
    yhat = yhat[0]
    yhat = round(yhat)

    print("YHAT")
    print(yhat)

    data = []
    data.append(revert_differencing)
    data.append(yhat)
    data.append(root_error)

    return data


#(original timeseries df, scatter models, graph title)
def graph_forecast(timeseries, models, title):
    original_date = []
    original_quantity = []

    #test data(original) is 66% of all data
    test_index = len(timeseries) * 0.70

    for index, row in timeseries.iterrows():
        original_quantity.append(row["Quantity"])
        original_date.append(index)

    #original dataset
    dataset = go.Scatter(
        x=list(original_date),
        y=list(original_quantity),
        name="Original"
    )

    data = [dataset]

    for model in models:
        data.append(model)

    layout = go.Layout(
        title=title
    )

    fig = go.Figure(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    return graph

def scatter_model(timeseries, prediction, title):
    print("PREDICTION")
    print(prediction)

    predicted_quantity = []
    predicted_date = []

    # test data is 66% of all data
    test_index = len(timeseries) * 0.70

    ctr = 0
    for index, row in timeseries.iterrows():
        if ctr >= test_index: # +1 if data is differenced
            predicted_date.append(index)
        ctr += 1

    ctr = 0
    print("GRAPH PREDICTION")
    print(prediction)

    for array in prediction:
        for row in array:
            if ctr <= test_index:
                predicted_quantity.append(row)
        ctr += 1

    forecast = go.Scatter(
        x=list(predicted_date),
        y=list(predicted_quantity),
        name=title
    )

    return forecast


def scatter_model_float(timeseries, prediction, title):
    print("PREDICTION")
    print(prediction)


    predicted_quantity = []
    predicted_date = []

    # test data is 66% of all data
    test_index = len(timeseries) * 0.70

    ctr = 0
    for index, row in timeseries.iterrows():
        if ctr >= test_index :
            predicted_date.append(index)
        ctr += 1

    ctr = 0

    while len(prediction) > len(predicted_date):
        del prediction[0]

    for array in prediction:
        if ctr <= test_index:
            predicted_quantity.append(array)
        ctr += 1

    forecast = go.Scatter(
        x=list(predicted_date),
        y=list(predicted_quantity),
        name=title
    )

    print("FORECAST")
    print(forecast)

    return forecast


def Average(lst):
    return sum(lst) / len(lst)

#TODO turn this into a method not a view
def forecast_result(date_list, quantity_list, graph_title):
    #quantity_set = K9_Quantity.objects.all().order_by('date_bought')
    result = ""
    context = {
        'title': 'Forecasting',
        'graph': "",
        'models': "",
        'errors': "",
        'predictions': ""
    }

    if date_list or quantity_list:
        quantity = []
        date = []

        for date_item, quantity_item in zip(date_list, quantity_list):
            date_object = date_item
            dt64 = np.datetime64(str(date_object))

            date.append(dt64)
            quantity.append(quantity_item)

        df = pd.DataFrame({'Date': list(date),
                           'Quantity': list(quantity),
                       })
        df.dropna(inplace=True)

        #TODO Fix Order of Graph
        ts = df.set_index('Date')

        models = []
        errors = []
        predictions = []

        AR_model = Autoregression(ts)
        AR_forecast = forecast(ts, AR_model)
        AR = AR_forecast[0]
        AR_predict = AR_forecast[1]
        AR_scatter = scatter_model(ts, AR, "Autoregression (AR)")
        AR_error = AR_forecast[2]
        models.append("AR")
        errors.append(AR_error)
        predictions.append(AR_predict)

        MA_model = Moving_Average(ts)
        MA_forecast = forecast(ts, MA_model)
        MA = MA_forecast[0]
        MA_predict = MA_forecast[1]
        MA_scatter = scatter_model(ts, MA, "Moving Average (MA)")
        MA_error = MA_forecast[2]
        models.append("MA")
        errors.append(MA_error)
        predictions.append(MA_predict)


        ARMA_model = Autoregressive_Moving_Average(ts)
        ARMA_forecast = forecast(ts, ARMA_model)
        ARMA = ARMA_forecast[0]
        ARMA_predict = ARMA_forecast[1]
        ARMA_scatter = scatter_model(ts, ARMA, "Autoregressive Moving Average (ARMA)")
        ARMA_error = ARMA_forecast[2]
        models.append("ARMA")
        errors.append(ARMA_error)
        predictions.append(ARMA_predict)

        ARIMA_model = Autoregressive_Integrated_Moving_Average(ts)
        ARIMA_forecast = forecast(ts, ARIMA_model)
        ARIMA = ARIMA_forecast[0]
        ARIMA_predict = ARIMA_forecast[1]
        ARIMA_scatter = scatter_model(ts, ARIMA, "Autoregressive Integrated Moving Average (ARIMA)")
        ARIMA_error = ARIMA_forecast[2]
        models.append("ARIMA")
        errors.append(ARIMA_error)
        predictions.append(ARIMA_predict)


        SES_model = Simple_Exponential_Smoothing(ts)
        SES_forecasts = SES_model[0]
        SES_forecasts = SES_forecasts.tolist()
        SES_predict = SES_model[1]
        SES_error = SES_model[2]
        SES_scatter = scatter_model_float(ts, SES_forecasts, "Single Exponential Smoothing (SES)")
        models.append("SES")
        errors.append(str(SES_error))
        predictions.append(str(SES_predict))

        '''
        HES_model = Holt_Exponential_Smoothing(ts)
        HES_forecasts = HES_model[0]
        HES_forecasts = HES_forecasts.tolist()
        HES_predict = HES_model[1]
        HES_error = HES_model[2]
        HES_scatter = scatter_model_float(ts, HES_forecasts, "Holt's Exponential Smoothing (HES)")
        models.append("HES")
        errors.append(str(HES_error))
        predictions.append(str(HES_predict))
        '''

        Scatter_Models = [AR_scatter, MA_scatter, ARMA_scatter, ARIMA_scatter, SES_scatter,]

        #graph_title = "Forecasting K9s Demand Using Various Models"
        graph = graph_forecast(ts, Scatter_Models, graph_title)

        result = []
        result.append(graph)
        result.append(models)
        result.append(errors)
        result.append(predictions)

        recommended = 0
        ctr = 0

        new_errors = []
        for item in errors:
            new_errors.append(float(item))

        zipped_list = zip(result[2], predictions)
        print("ZIPPED LIST")
        print(set(zipped_list))

        # Partner errors and predictions, if prediction is < 0, remove it as an option for recommendation
        for (error, prediction) in  set(zipped_list):
            if prediction < 0:
                del errors[ctr]
                del predictions[ctr]
            ctr += 1


        print("Models")
        print(result[1])
        print("Errors")
        print(result[2])
        print("Predictions")
        print(result[3])

        print("NEWERRORS")
        print(new_errors)

        recommended_list = []
        zipped_list = zip(new_errors, predictions)

        #The prediction with the least error is recommended (add to list)
        for (error, prediction) in  set(zipped_list):
            print("ERROR")
            print(error)
            print("PREDICTION")
            print(prediction)
            if error == min(new_errors):
                recommended_list.append(int(prediction))

        print("RECOMMENDED LIST")
        print(recommended_list)

        #If (unlikely) there more the 1 item in recommendation, get the average
        if len(recommended_list) > 1:
            recommended = Average(recommended_list)
        else:
            recommended = recommended_list[0]

        result.append(recommended)


        context = {
            'title': 'Forecasting',
            'graph': graph,
            'models': models,
            'errors': errors,
            'predictions': predictions,
            'recommended': recommended,

            }

    return result
    #return render(request, 'planningandacquiring/forecast_k9_required.html', context)


def timeseries_generator():
    fake = Faker()
    for x in range(100):
        number = randint(1, 60)
        date = fake.date_between(start_date='-12y', end_date='-2y')

        date_quantity = K9_Quantity(quantity = number, date_bought = date)
        date_quantity.save()

    return None

def fill_data_gap(year_list, value_list):
    now = dt.now()
    current_year = now.year

    temp_year = int(max(year_list))
    new_year_list = []

    year_range = 15 - len(year_list)

    for x in range(0, year_range):
        new_year_list.append(temp_year)
        temp_year -= 1

    #average_result = Average(value_list)
    new_value_list = []

    #Remove Outliers
    #points above (Mean + 2*SD) and any points below (Mean - 2*SD)
    elements = np.array(value_list)

    mean = np.mean(elements, axis=0)
    sd = np.std(elements, axis=0)

    final_list = [x for x in value_list if (x > mean - 2 * sd)]
    final_list = [x for x in final_list if (x < mean + 2 * sd)]
    print(final_list)

    #Use the max and min randint values from final_list if there is a gap from new_year_list
    for y in new_year_list:
        count = 0
        for year in year_list:
            if year == y:
                new_value_list.append(value_list[count])
            else:
                if min(value_list) == max(value_list): # Add a padding if max and min is same value
                    new_value_list.append(randint(min(value_list) - 1, max(value_list) + 1))
                else:
                    new_value_list.append(randint(min(value_list), max(value_list)))
                #new_value_list.append(average_result)
            count += 1

    print("ORIGINAL YEAR LIST")
    print(year_list)
    print("ORIGINAL VALUE LIST")
    print(value_list)

    print("NEW YEAR LIST")
    print(new_year_list)
    print("NEW VALUE LIST")
    print(new_value_list)

    result = []
    new_year_list.reverse()
    new_value_list.reverse()
    result.append(new_year_list)
    result.append(new_value_list)

    print("REVERSE YEAR LIST")
    print(new_year_list)
    print("REVERSE VALUE LIST")
    print(new_value_list)
    print("RESULT")
    print(result)

    return result

#TODO Try Except All Forecasts
#TODO error handle all notes
#NOTE: Minimum number of years required is 10 years
#NOTE: Singular matrix error occurs when differencing is computed and nearly all values are the same (cannot be inverted)

##################### END FORECASTING ########################

def add_breed(request):
    form = add_breed_form(request.POST)
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            breed = form.save()
            breed.save()
            style = "ui green message"
            messages.success(request, 'Breed has been successfully Added!')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "Add Breed",
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    print(form)
    return render(request, 'planningandacquiring/add_breed.html', context)


def breed_listview(request):
    breed = Dog_Breed.objects.all()

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': 'Breed List',
        'breed': breed,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'planningandacquiring/view_breed.html', context)


################# BUDGETING ###################

def choose_date(request):
    form = HistDateForm(request.POST or None)
    success = 0
    # if request.method == 'POST':
    #     if form.is_valid():
    #         year = request.POST.get('hist_date')
    #         request.session["session_year"] = year


    #         try:
    #             budget_alloc = Budget_allocation.objects.filter(date_created__year=year).latest('id')
    #             success = 1
    #         except:
    #             messages.success(request, 'Budget Estimate for this year does not exist!')

    # if success == 1:
    #     return HttpResponseRedirect('detailed_budget/')

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()

    context = {
        'notif_data':notif_data,
        'count': count,
        'title': "",
        'form': form,
    }

    return render(request, 'planningandacquiring/choose_date.html', context)

def budgeting_detail(request, id):
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'planningandacquiring/budgeting_detail.html', context)

def budgeting_report(request):
 
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'notif': notif,
        'count': count,
    }

    return render(request, 'planningandacquiring/budgeting_report.html', context)
    
def detailed_budgeting(request):
 

    context = {
    
    }

    return render(request, 'planningandacquiring/detailed_budgeting.html', context)

################# END BUDGETING ###################


def load_supplier(request):

    supplier = None

    try:
        supplier_id = request.GET.get('supplier')
        supplier = K9_Supplier.objects.get(id=supplier_id)
    except:
        pass
    context = {
        'supplier': supplier,
    }

    return render(request, 'planningandacquiring/supplier_data.html', context)

def load_k9_reco(request):

    h_count_arr = []
    k9_arr = []
    b_arr = []

    try:
        id = request.GET.get('id')
        k9 = K9.objects.get(id=id)
        k9_data = K9.objects.filter(sex="Male").filter(training_status = "For-Breeding").filter(breed=k9.breed).filter(capability=k9.capability).filter(age__gte = 1).order_by('-litter_no')
        
        for k in k9_data:
            h_count = Health.objects.filter(dog=k).count()
            h_count_arr.append(h_count)   
            k9_arr.append(k)

            birth = K9_Litter.objects.filter(father=k).aggregate(sum=Sum('litter_no'))['sum']
            death = K9_Litter.objects.filter(father=k).aggregate(sum=Sum('litter_died'))['sum']

            if birth != None or death != None:
                total = (birth / (birth+death)) * 100
            else:
                total=100
            
            b_arr.append(int(total))

    except:
        pass
    print(k9_arr)
    print(b_arr)
    flist = zip(k9_arr,h_count_arr, b_arr)

    context = {
        'k9': k9,
        'flist':flist,
    }

    return render(request, 'planningandacquiring/breeding_reco_data.html', context)

def load_health(request):

    health = None
    k9 = None
    try:
        k9 = request.GET.get('k9')
        k9_id = request.GET.get('id')
        health = Health.objects.filter(dog__id=k9_id) 
    except:
        pass

    context = {
        'health': health,
        'k9': k9,
    }

    return render(request, 'planningandacquiring/health_data.html', context)

def load_form(request):
    formset = None
    try:
        num = request.GET.get('num')
        print(num)
        k9_formset = formset_factory(add_offspring_K9_form, extra=int(num), can_delete=False)
        formset = k9_formset(request.POST, request.FILES)
    except:
        pass

    context = {
        'formset': k9_formset(),
    }

    return render(request, 'planningandacquiring/offspring_form_data.html', context)