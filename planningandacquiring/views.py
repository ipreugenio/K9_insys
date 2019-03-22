from django.shortcuts import render
from django.http import Http404

from .forms import add_donated_K9_form, add_donator_form, add_K9_parents_form, add_offspring_K9_form, select_breeder, budget_food, budget_equipment, budget_medicine, budget_vaccine, budget_vet_supply, budget_date
from .models import K9, K9_Past_Owner, K9_Donated, K9_Parent, K9_Quantity, Budget_allocation, Budget_equipment, Budget_food, Budget_medicine, Budget_vaccine, Budget_vet_supply

from .forms import add_donated_K9_form, add_donator_form, add_K9_parents_form, add_offspring_K9_form, select_breeder
from .models import K9, K9_Past_Owner, K9_Donated, K9_Parent, K9_Quantity, Budget_allocation, Budget_equipment, Budget_food, Budget_medicine, Dog_Breed

from training.models import Training
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates, Sum
from django.http import JsonResponse
from django.contrib import messages
from .forms import ReportDateForm, add_breed_form
from deployment.models import Dog_Request, Team_Assignment
from unitmanagement.models import Health, HealthMedicine, VaccinceRecord, VaccineUsed
from inventory.models import Food, Food_Subtracted_Trail, Medicine, Medicine_Inventory, Medicine_Subtracted_Trail, Miscellaneous, Miscellaneous_Subtracted_Trail
from django.db.models.functions import Trunc, TruncMonth, TruncYear, TruncDay
from django.db.models import Avg, Count, Min, Sum, Q
import dateutil.parser
from faker import Faker

#statistical imports
from math import *
from decimal import Decimal
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

from datetime import datetime as dt
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


def index(request):
    data = [[],[],[]]
    total = 0
    date_from = ''
    date_to = ''
    if request.method == 'POST':
        print(request.POST.get('date_from'))
        print(request.POST.get('date_to'))
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')

        i = Medicine_Subtracted_Trail.objects.values('name').distinct().filter(date_subtracted__range=[date_from, date_to])
        count=0

        c = [] #quantity
        d = [] #price

        #get quantity
        for x in i:
            q = Medicine_Subtracted_Trail.objects.filter(name=x['name']).aggregate(sum=Sum('quantity'))['sum']
            c.append(q)

        #get price
        #k=Medicine_Subtracted_Trail.objects.all()
        for x in i:
            p=Medicine.objects.get(medicine_fullname=x['name'])
            d.append(p.price)

        for x in i:
            print(x['name'])
            n=x['name']
            data[count].append(n)
            data[count].append(c[count])
            data[count].append(d[count]*c[count])
            total=total+d[count]*c[count]
            count= count+1
    context = {
        'title' : "Medicine Used Report",
        'data': data,
        'total':total,
        'date_from': date_from,
        'date_to':date_to,
    }
    return render (request, 'planningandacquiring/index.html', context)

def report(request):
    form = ReportDateForm()
    context = {
        'Title' : "REPORT",
        'form': form,
        }
    return render (request, 'planningandacquiring/report.html', context)

#Form format
def add_donated_K9(request):
    form = add_donated_K9_form(request.POST)
    style = "ui teal message"
    if request.method == 'POST':
        if form.is_valid():
            k9 = form.save()
            k9.source = "Procurement"
            k9.save()

            request.session['k9_id'] = k9.id

            #create Training object when k9 is created, self.id of k9 will be the value of training_id
            #Training.objects.create(k9=k9, training='EDD')
            #Training.objects.create(k9=k9, training='NDD')
            #Training.objects.create(k9=k9, training='SAR')

            return HttpResponseRedirect('confirm_donation/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
            print(form)

    context = {
        'Title' : "Add New K9",
        'form' : form,
        'style': style,
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

    context = {
        'Title': "Add New K9",
        'k9': k9,

    }
    return render(request, 'planningandacquiring/confirm_K9_donation.html', context)

def donation_confirmed(request):
    k9_id = request.session['k9_id']

    k9 = K9.objects.get(id=k9_id)

    if 'ok' in request.POST:
        return render(request, 'planningandacquiring/donation_confirmed.html')
    else:
        #delete training record
        training = Training.objects.filter(k9=k9)
        training.delete()
        #delete k9
        k9.delete()

        context = {
            'Title': "Add New K9",
            'form': add_donated_K9_form,
        }
        return render(request, 'planningandacquiring/add_donated_K9.html', context)

#TODO Add capability to add a single parent
#TODO Added k9s not immediately showing up in breeding form

def add_K9_parents(request):

    form = add_K9_parents_form(request.POST)
    style = "ui teal message"
    mothers = K9.objects.filter(sex="Female").filter(training_status = "For-Breeding").filter(age__gte = 1)
    fathers = K9.objects.filter(sex="Male").filter(training_status = "For-Breeding").filter(age__gte = 1)

    mother_list = []
    father_list = []

    for mother in mothers:
        mother_list.append(mother)

    for father in fathers:
        father_list.append(father)

    if request.method == 'POST':

        if form.is_valid():

            mother_id = form.cleaned_data['mother']
            father_id = form.cleaned_data['father']

            #Tests if data id can be retrieved and related to tables
            mother = K9.objects.get(id = mother_id)
            father = K9.objects.get(id = father_id)


            request.session["mother_id"] = mother.id
            request.session["father_id"] = father.id

            return HttpResponseRedirect('confirm_K9_parents/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')



    context = {
        'Title': "K9_Breeding",
        'form': form,
        'style': style,
        'mothers' : mother_list,
        'fathers' : father_list
    }

    return render(request, 'planningandacquiring/add_K9_parents.html', context)

def confirm_K9_parents(request):
    mother_id = request.session["mother_id"]
    father_id = request.session["father_id"]

    mother = K9.objects.get(id=mother_id)
    father = K9.objects.get(id=father_id)

    context = {
        'mother': mother,
        'father': father,
    }

    return render(request, 'planningandacquiring/confirm_K9_parents.html', context)

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
        context = {
            'Title': "Receive Donated K9",
            'form': add_K9_parents_form,
            'mothers': mother_list,
            'fathers': father_list
        }
        return render(request, 'planningandacquiring/add_K9_parents.html', context)


def add_offspring_K9(request):
     form = add_offspring_K9_form(request.POST)
     style = "ui teal message"

     if request.method == 'POST':
         if form.is_valid():
             k9 = form.save()
             k9.source = "Breeding"
             mother_id = request.session['mother_id']
             father_id = request.session['father_id']
             mother = K9.objects.get(id=mother_id)
             father = K9.objects.get(id=father_id)

             if mother.breed != father.breed:
                breed = "Mixed"
             else:
                breed = mother.breed

             k9.breed = breed
             k9.save()

             request.session['offspring_id'] = k9.id

             return HttpResponseRedirect('confirm_breeding/')

         else:
             style = "ui red message"
             messages.warning(request, 'Invalid input data!')
             print(form)

     context = {
         'Title': "Receive Donated K9",
         'form': form,
         'style': style,
     }

     return render(request, 'planningandacquiring/add_K9_offspring.html', context)

def confirm_breeding(request):
    offspring_id = request.session['offspring_id']
    mother_id = request.session['mother_id']
    father_id = request.session['father_id']

    offspring = K9.objects.get(id=offspring_id)
    mother = K9.objects.get(id=mother_id)
    father = K9.objects.get(id=father_id)

    context = {
        'Title': "Receive Donated K9",
        'offspring': offspring,
        'mother': mother,
        'father': father,
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
        #Training.objects.create(k9=offspring, training='EDD')
        #Training.objects.create(k9=offspring, training='NDD')
        #Training.objects.create(k9=offspring, training='SAR')

        return render(request, 'planningandacquiring/breeding_confirmed.html')
    else:
        #delete training record
        training = Training.objects.filter(k9=offspring)
        training.delete()
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

        context = {
            'Title': "Receive Donated K9",
            'form': add_K9_parents_form,
            'mothers': mother_list,
            'fathers': father_list,
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
    context = {
        'Title' : 'K9 List',
        'k9' : k9
    }

    return render(request, 'planningandacquiring/K9_list.html', context)

#Detailview format
def K9_detailview(request, id):
    k9 = K9.objects.get(id = id)

    if request.method == "POST":
        print(request.POST.get('radio'))
        k9.training_status = request.POST.get('radio')
        k9.save()
        messages.success(request, 'K9 is now ' + k9.training_status + '!')

    try:
        parent = K9_Parent.objects.get(offspring=k9)
    except K9_Parent.DoesNotExist:
        context = {
            'Title': 'K9 Details',
            'k9' : k9,
        }
    else:
        parent_exist = 1
        context = {
            'Title': 'K9 Details',
            'k9': k9,
            'parent': parent,
            'parent_exist': parent_exist
        }

    return render(request, 'planningandacquiring/K9_detail.html', context)

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
        if ctr >= test_index-1: # +1 if data is differenced
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
            'recommended': recommended
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

def budgeting(request):

    reload = True
    context = {'reload': reload, 'title': 'Budgeting'}

    #REQUEST FORECAST
    dog_request = Dog_Request.objects.all().order_by('start_date')
    request_date = []

    for data in dog_request:
        date = data.start_date
        request_date.append(date.year)

    request_date = list(set(request_date))
    request_date.sort()
    request_quantity = []

    #Aggregate sum from same year
    for year in request_date:
        sum = 0
        for data in dog_request:
            temp_year = data.start_date
            if temp_year.year == year:
                current_needed_peryear = data.total_dogs_demand - data.total_dogs_deployed
                if current_needed_peryear < 0:
                    current_needed_peryear = 0
                sum += current_needed_peryear
        request_quantity.append(sum)


    if len(request_date) <= 12:
        fill_gap = fill_data_gap(request_date, request_quantity)

        request_date = fill_gap[0]
        request_quantity = fill_gap[1]

    # #TEST
    # year = 2006
    # value = 5
    # for x in range(11):
    #     year +=1
    #     value += randint(1, 3)
    #     request_date.append(year)
    #     request_quantity.append(value)

    print("REQUEST DATE")
    print(request_date)
    print("REQUEST QUANTITY")
    print(request_quantity)

    try:
        request_forecast = forecast_result(request_date, request_quantity, "Forecast for K9 Requests")
    except:
        return render(request, 'planningandacquiring/budgeting.html', context)


    #DOGS DEMAND
    dog_demand = Team_Assignment.objects.all()
    dogs_needed = 0
    for demand in dog_demand:
        temp = demand.total_dogs_demand - demand.total_dogs_deployed #TODO Confirm
        if temp < 0:
            temp = 0
        dogs_needed += temp

    '''
    unclassified, classified, on-training, trained, for-breeding, for-adoption, for-deployment, deployed, adopted, breeding, sick, recovery, dead, retired
    '''

    # #DOGS AVAILABLE IN THE FUTURE
    # deployed_dogs = K9.objects.filter(training_status = 'Deployed').filter(training_status = 'Dead').filter(training_status = 'Retired').filter(training_status = 'Adopted').count()

    #ALL CURRENT DOGS
    all_current_dogs = K9.objects.exclude(Q(training_status = 'Adopted') | Q(training_status = 'Dead')).count()
    all_current_dogs_obj = K9.objects.exclude(Q(training_status = 'Adopted') | Q(training_status = 'Dead'))

    untrained_dogs = K9.objects.filter(Q(training_status = 'Unclassified') | Q(training_status = 'Classified') | Q(training_status = 'On-Training')).count()
    deployable_dogs = K9.objects.filter(training_status = 'For-Deployment').count()
    breeding_dogs = K9.objects.filter(training_status = 'For-Breeding').count()
    deployed_dogs = K9.objects.filter(training_status = 'Deployed').count()
    forecasted_dogs = request_forecast[4]
    forecasted_dogs = int(forecasted_dogs)
    required_dogs = dogs_needed - (deployed_dogs - (untrained_dogs + breeding_dogs + deployable_dogs)) # Remove dogs deployed in requests
    recommended_dogs = untrained_dogs + deployable_dogs + breeding_dogs + deployed_dogs + required_dogs + forecasted_dogs

    #TODO error handling if there are no prior year estimate
    #TODO error handling if an inventory item is removed
    #TODO display all actuals in template
    #TODO Script Compute current estimate - Actuals in template
    now = dt.now()
    previous_budget_alloc = Budget_allocation.objects.exclude(date_created__year__gte = now.year).latest('id')

    medicine_previous_price = []
    medicine_previous_total = []
    medicine_actual = [] # Quantity * previous bid

    previous_medicine_budget = Budget_medicine.objects.filter(budget_allocation = previous_budget_alloc)

    #MEDICINE BUDGET
    medicine_name_list = []
    medicine_forecast_list = []
    medicine_price_list = []
    medicine_ids = []
    medicine_current = []

    medicines = Medicine.objects.exclude(med_type = 'Vaccine')

    medicine_spendings = 0

    for medicine in medicines:
        inventory = Medicine_Inventory.objects.get(medicine = medicine)
        medicine_usage = Medicine_Subtracted_Trail.objects.filter(inventory = inventory.id)

        med_date_list = []
        med_quantity_list = []

        if medicine_usage:
            for usage in medicine_usage:
                date = usage.date_subtracted
                med_date_list.append(date.year)

            med_date_list = list(set(med_date_list))


            for year in med_date_list:
                sum = 0
                for usage in medicine_usage:
                    date = usage.date_subtracted
                    if date.year == year:
                        sum += usage.quantity
                med_quantity_list.append(sum)
        else:
            med_date_list.append(dt.now().year)
            med_quantity_list.append(inventory.quantity)

        if len(med_date_list) <= 12:
            fill_gap = fill_data_gap(med_date_list, med_quantity_list)
            med_date_list = fill_gap[0]
            med_quantity_list = fill_gap[1]

        try:
            medicine_forecast = forecast_result(med_date_list, med_quantity_list, "Forecast for " + str(medicine.medicine))
        except:
            return render(request, 'planningandacquiring/budgeting.html', context)

        medicine_name_list.append(medicine.medicine)
        medicine_forecast_list.append(medicine_forecast[4])
        medicine_price_list.append(medicine.price)
        medicine_ids.append(medicine.id)
        medicine_current.append(inventory.quantity)

        select_price = 0
        for item in previous_medicine_budget:

            if item.medicine.id == medicine.id:
                medicine_previous_price.append(item.price)
                medicine_previous_total.append(item.total)
                select_price = item.price

        medicine_usage_lastyear = Medicine_Subtracted_Trail.objects.filter(inventory=inventory.id).filter(
            date_subtracted__year=now.year)

        usage_total = 0
        for item in medicine_usage_lastyear:
            usage_total += item.quantity

        medicine_actual.append(usage_total * select_price)
        medicine_spendings += (usage_total * select_price)


    vaccine_previous_price = []
    vaccine_previous_total = []
    vaccine_actual = []

    previous_vaccine_budget = Budget_vaccine.objects.filter(budget_allocation=previous_budget_alloc)

    vaccine_spendings = 0

    #VACCINE BUDGET
    vaccines = Medicine.objects.filter(med_type = 'Vaccine')
    vaccine_names_list = []
    vaccine_used_yearly_list = []
    vaccine_price_list = []
    vaccine_ids = []
    vaccine_current = []
    for vaccine in vaccines:
        inventory = Medicine_Inventory.objects.get(medicine=vaccine)

        vaccine_names_list.append(vaccine.medicine)
        vaccine_used_yearly_list.append(vaccine.used_yearly)
        vaccine_price_list.append(vaccine.price)
        vaccine_ids.append(vaccine.id)
        vaccine_current.append(inventory.quantity)

        select_price = 0
        for item in previous_vaccine_budget:
            if item.vaccine.id == vaccine.id:
                vaccine_previous_price.append(item.price)
                vaccine_previous_total.append(item.total)
                select_price = item.price

        vaccine_usage_lastyear = Medicine_Subtracted_Trail.objects.filter(inventory=inventory.id).filter(
            date_subtracted__year=now.year)

        usage_total = 0
        for item in vaccine_usage_lastyear:
            usage_total += item.quantity

        vaccine_actual.append(usage_total * select_price)
        vaccine_spendings += (usage_total * select_price)

    #FOOD BUDGET

    adult_actual = 0
    puppy_actual = 0
    milk_actual = 0

    food_spendings = 0

    usage_lastyear = Food_Subtracted_Trail.objects.filter(
            date_subtracted__year=now.year)

    for item in usage_lastyear:
        if item.inventory.foodtype == "Adult Dog Food":
            adult_actual += item.quantity
        if item.inventory.foodtype == "Puppy Dog Food":
            puppy_actual += item.quantity
        if item.inventory.foodtype == "Milk":
            milk_actual += item.quantity

    food_spendings = adult_actual + puppy_actual + milk_actual

    previous_food_budget_adult = Budget_food.objects.filter(food = "Adult Food").get(budget_allocation=previous_budget_alloc)
    adult_actual = adult_actual * previous_food_budget_adult.price
    previous_food_budget_puppy = Budget_food.objects.filter(food="Puppy Food").get(budget_allocation=previous_budget_alloc)
    puppy_actual = puppy_actual * previous_food_budget_puppy.price
    previous_food_budget_milk = Budget_food.objects.filter(food="Milk").get(budget_allocation=previous_budget_alloc)
    milk_actual = milk_actual * previous_food_budget_milk.price


    adult_previous_price = previous_food_budget_adult.price
    adult_previous_total = previous_food_budget_adult.total

    puppy_previous_price = previous_food_budget_puppy.price
    puppy_previous_total = previous_food_budget_puppy.total

    milk_previous_price = previous_food_budget_milk.price
    milk_previous_total = previous_food_budget_milk.total


    adult_food = Food.objects.filter(foodtype = "Adult Dog Food")
    puppy_food = Food.objects.filter(foodtype = "Puppy Dog Food")
    milk = Food.objects.filter(foodtype = "Milk")

    adult_food_quantity = 0
    for item in adult_food:
        adult_food_quantity += item.quantity

    puppy_food_quantity = 0
    for item in puppy_food:
        puppy_food_quantity += item.quantity

    milk_quantity = 0
    for item in milk:
        milk_quantity += item.quantity

    adult_food_data = []
    puppy_food_data = []

    breeds = ['Labrador Retriever', 'Golden Retriever', 'German/Dutch Shepard', 'German Malinois', 'Jack Russel']
    breed_counts = [K9.objects.filter(breed = 'Labrador Retriever').count(),
                    K9.objects.filter(breed = 'Golden Retriever').count(),
                    K9.objects.filter(Q(breed = 'German Shepard') | Q(breed = 'Dutch Shepard')).count(),
                    K9.objects.filter(breed = 'German Malinois').count(),
                    K9.objects.filter(breed = 'Jack Russel').count()]
    min_breed_cons = [12, 21, 21 ,21, 6]
    max_breed_cons = [15, 24, 24, 24, 9]
    adult_consumption = ['12.00 - 15.00', '21.00 - 24.00', '21.00 - 24.00', '21.00 - 24.00', '6.00 - 9.00']
    min_total_cons = []
    max_total_cons = []

    adult_table_total_min = 0
    adult_table_total_max = 0
    ctr = 0
    for breed_count in breed_counts:
        min = breed_count * min_breed_cons[ctr]
        min_total_cons.append(min)
        adult_table_total_min += min

        max = breed_count * max_breed_cons[ctr]
        max_total_cons.append(max)
        adult_table_total_max += max

        ctr+= 1

    adult_yearly_total_min = 0
    adult_yearly_total_max = 0

    ctr = 0
    for breed in breeds:
        temp_list = []

        temp_list.append(breeds[ctr])
        temp_list.append(breed_counts[ctr])
        temp_list.append(adult_consumption[ctr])
        temp_list.append(min_total_cons[ctr])
        temp_list.append(max_total_cons[ctr])

        adult_yearly_total_min += min_total_cons[ctr]
        adult_yearly_total_max += max_total_cons[ctr]

        adult_food_data.append(temp_list)

        ctr+= 1

    adult_yearly_total_min = adult_yearly_total_min*12
    adult_yearly_total_max = adult_yearly_total_max*12

    age_group = ['3rd - 4th week', '5th - 6th week', '7th - 8th week', '9th - 10th week', '11th - 12th week', '3-4 months', '5 - 6 months', '7- 8 months', '9 - 12 months']
    age_group_counts = [K9.objects.filter(Q(age_days__gte = 21) & Q(age_days__lte = 28)).count(),
                        K9.objects.filter(Q(age_days__gte=29) & Q(age_days__lte=35)).count(),
                        K9.objects.filter(Q(age_days__gte=36) & Q(age_days__lte=42)).count(),
                        K9.objects.filter(Q(age_days__gte=43) & Q(age_days__lte=50)).count(),
                        K9.objects.filter(Q(age_days__gte=51) & Q(age_days__lte=58)).count(),
                        K9.objects.filter(Q(age_month__gte=3) & Q(age_days__lte=4)).count(),
                        K9.objects.filter(Q(age_month__gte=5) & Q(age_days__lte=6)).count(),
                        K9.objects.filter(Q(age_month__gte=7) & Q(age_days__lte=8)).count(),
                        K9.objects.filter(Q(age_month__gte=9) & Q(age_days__lte=12)).count(),
                        ]

    temp = 0
    ctr = 0
    temp_list = []

    for item in age_group_counts:
        temp += item
        temp_list.append(item)
        ctr += 1

    age_group_counts = temp_list

    milk_cons = [.45, .67, .67, .84, 1.01, None, None, None, None]
    puppy_food_cons = [None, 1.12, 1.68, 2.52, 3.36, 7.50, 10.50, 13.50, 15.00]

    puppy_total_cons = []
    milk_total_cons = []

    puppy_yearly_total = 0
    milk_yearly_total = 0

    ctr = 0
    for item in age_group:
        if milk_cons[ctr] != None:
            milk_temp = milk_cons[ctr] * age_group_counts[ctr]
            milk_total_cons.append(milk_temp)
            milk_yearly_total += milk_temp
        else:
            milk_total_cons.append(None)

        if puppy_food_cons[ctr] != None:
            puppy_temp = puppy_food_cons[ctr] * age_group_counts[ctr]
            puppy_total_cons.append(puppy_temp)
            puppy_yearly_total += puppy_temp
        else:
            puppy_total_cons.append(None)

        ctr += 1

    ctr = 0
    for item in age_group:
        temp_list = []
        temp_list.append(age_group[ctr])
        temp_list.append(age_group_counts[ctr])
        temp_list.append(milk_cons[ctr])
        temp_list.append(puppy_food_cons[ctr])
        temp_list.append(milk_total_cons[ctr])
        temp_list.append(puppy_total_cons[ctr])

        puppy_food_data.append(temp_list)

        ctr += 1


    #EQUIPMENT BUDGET

    equipment_previous_price = []
    equipment_previous_total = []
    equipment_actual = []

    previous_equipment_budget = Budget_equipment.objects.filter(budget_allocation=previous_budget_alloc)

    equipment = Miscellaneous.objects.filter(misc_type = "Equipment")

    equipment_name = []
    equipment_price = []
    equipment_ids = []
    equipment_quantity = []

    equipment_spendings = 0

    for item in equipment:
        equipment_name.append(item.miscellaneous)
        equipment_price.append(item.price)
        equipment_ids.append(item.id)
        equipment_quantity.append(item.quantity)

        select_price = 0
        for equip in previous_equipment_budget:
            if equip.equipment.id == item.id:
                equipment_previous_price.append(equip.price)
                equipment_previous_total.append(equip.total)
                select_price = equip.price

        equipment_usage_lastyear = Miscellaneous_Subtracted_Trail.objects.filter(inventory=item.id).filter(
            date_subtracted__year=now.year)

        usage_total = 0
        for item in equipment_usage_lastyear:
            usage_total += item.quantity

        equipment_actual.append(usage_total * select_price)
        equipment_spendings += (usage_total * select_price)


    #VET SUPPLY BUDGET

    vet_supply_previous_price = []
    vet_supply_previous_total = []
    vet_supply_actual = []

    previous_vet_supply_budget = Budget_vet_supply.objects.filter(budget_allocation=previous_budget_alloc)

    vet_supply_spendings = 0

    vet_supply = Miscellaneous.objects.filter(misc_type="Vet Supply")

    vet_supply_name = []
    vet_supply_price = []
    vet_supply_ids = []
    vet_supply_quantity = []
    vet_supply_forecast = []
    vet_supply_uom = []

    for supply in vet_supply:
        inventory = supply#Miscellaneous.objects.filter(misc_type="Vet Supply")#Medicine_Inventory.objects.get(medicine = medicine)
        supply_usage = Miscellaneous_Subtracted_Trail.objects.filter(inventory = inventory.id)

        supply_date_list = []
        supply_quantity_list = []

        if supply_usage:
            for usage in supply_usage:
                date = usage.date_subtracted
                supply_date_list.append(date.year)

            supply_date_list = list(set(supply_date_list))

            for year in supply_date_list:
                sum = 0
                for usage in supply_usage:
                    date = usage.date_subtracted
                    if date.year == year:
                        sum += usage.quantity
                supply_quantity_list.append(sum)
        else:
            supply_date_list.append(dt.now().year)
            supply_quantity_list.append(inventory.quantity)

        if len(supply_date_list) <= 12:
            fill_gap = fill_data_gap(supply_date_list, supply_quantity_list)
            supply_date_list = fill_gap[0]
            supply_quantity_list = fill_gap[1]

        try:
            supply_forecast = forecast_result(supply_date_list, supply_quantity_list, "Forecast for " + str(supply.miscellaneous))
        except:
            return render(request, 'planningandacquiring/budgeting.html', context)

        vet_supply_forecast.append(supply_forecast[4])


    for item in vet_supply:
        vet_supply_name.append(item.miscellaneous)
        vet_supply_price.append(item.price)
        vet_supply_ids.append(item.id)
        vet_supply_quantity.append(item.quantity)
        vet_supply_uom.append(item.uom)

        select_price = 0
        for vet in previous_vet_supply_budget:
            if vet.vet_supply.id == item.id:
                vet_supply_previous_price.append(vet.price)
                vet_supply_previous_total.append(vet.total)
                select_price = vet.price

        vet_supply_usage_lastyear = Miscellaneous_Subtracted_Trail.objects.filter(inventory=item.id).filter(
            date_subtracted__year=now.year)

        usage_total = 0
        for item in vet_supply_usage_lastyear:
            usage_total += item.quantity

        vet_supply_actual.append(usage_total * select_price)
        vet_supply_spendings += (usage_total * select_price)


    print("REQUEST_FORECAST[4]")
    print(request_forecast[4])

    deworming_req = 0
    dhppil_cv_req = 0
    heartworming_req = 0
    antirabies_req = 0
    bordetella_req = 0
    dhppil4_req = 0
    tick_flea_req = 0

    deworming = 0
    dhppil_cv = 0
    heartworming = 0
    antirabies = 0
    bordetella = 0
    dhppil4 = 0
    tick_flea = 0


    for k9 in all_current_dogs_obj:

        vacc = VaccinceRecord.objects.get(k9=k9)

        deworming_req += 4
        dhppil_cv_req += 3
        heartworming_req += 8
        antirabies_req += 1
        bordetella_req += 2
        dhppil4_req += 2
        tick_flea_req += 7


        if vacc.deworming_1 == True:
            deworming += 1
        if vacc.deworming_2 == True:
            deworming += 1
        if vacc.deworming_3 == True:
            deworming += 1
        if vacc.deworming_4 == True:
            deworming += 1

        if vacc.dhppil_cv_1 == True:
            dhppil_cv += 1
        if vacc.dhppil_cv_2 == True:
            dhppil_cv += 1
        if vacc.dhppil_cv_3 == True:
            dhppil_cv += 1

        if vacc.heartworm_1 == True:
            heartworming += 1
        if vacc.heartworm_2 == True:
            heartworming += 1
        if vacc.heartworm_3 == True:
            heartworming += 1
        if vacc.heartworm_4 == True:
            heartworming += 1
        if vacc.heartworm_5 == True:
            heartworming += 1
        if vacc.heartworm_6 == True:
            heartworming += 1
        if vacc.heartworm_7 == True:
            heartworming += 1
        if vacc.heartworm_8 == True:
            heartworming += 1

        if vacc.anti_rabies == True:
            antirabies += 1

        if vacc.bordetella_1 == True:
            bordetella += 1
        if vacc.bordetella_2 == True:
            bordetella += 1

        if vacc.dhppil4_1 == True:
            dhppil4 += 1
        if vacc.dhppil4_2 == True:
            dhppil4 += 1

        if vacc.tick_flea_1 == True:
            tick_flea += 1
        if vacc.tick_flea_2 == True:
            tick_flea += 1
        if vacc.tick_flea_3 == True:
            tick_flea += 1
        if vacc.tick_flea_4 == True:
            tick_flea += 1
        if vacc.tick_flea_5 == True:
            tick_flea += 1
        if vacc.tick_flea_6 == True:
            tick_flea += 1
        if vacc.tick_flea_7 == True:
            tick_flea += 1


    grandspendings = medicine_spendings + vaccine_spendings + food_spendings + equipment_spendings + vet_supply_spendings

    #Forms

    med_field_count = len(medicine_name_list)
    vac_field_count = len(vaccine_names_list)
    equip_field_count = len(equipment_name)
    vet_field_count = len(vet_supply_name)

    MedicineFormset = formset_factory(budget_medicine, extra = med_field_count)
    VaccineFormset = formset_factory(budget_vaccine, extra = vac_field_count)
    #food_formset = formset_factory(budget_food, extra=2)
    FoodForm = budget_food
    EquipmentFormset = formset_factory(budget_equipment, extra = equip_field_count)
    Vet_supplyFormset = formset_factory(budget_vet_supply, extra = vet_field_count)


    #TODO detail view of budgets

    style = ""
    if request.method == "POST":
        medicine_formset = MedicineFormset(request.POST, prefix="medicine")
        vaccine_formset = VaccineFormset(request.POST, prefix="vaccine")
        food_form = FoodForm(request.POST, prefix="food")
        equipment_formset = EquipmentFormset(request.POST, prefix="equipment")
        vet_supply_formset = Vet_supplyFormset(request.POST, prefix="vet_supply")


        if medicine_formset.is_valid() and vaccine_formset.is_valid() and food_form.is_valid() and equipment_formset.is_valid() and vet_supply_formset.is_valid():

            budget_alloc = Budget_allocation()
            budget_alloc.save()
            budget_alloc = Budget_allocation.objects.get(id=budget_alloc.id)

            print("MEDICINE SET")
            ctr = 0
            for med_form in medicine_formset:
                cd = med_form.cleaned_data

                name = medicine_name_list[ctr]
                id = medicine_ids[ctr]
                medicine = Medicine.objects.get(id = id)
                quantity = cd.get('quantity')
                budget = cd.get('budget')
                price = cd.get('price')

                print(name)
                print(quantity)
                print(budget)
                print(price)

                med_budget = Budget_medicine(medicine = medicine, quantity = quantity, price = price, total = budget, budget_allocation = budget_alloc)
                med_budget.save()
                ctr += 1
            print("Medicine Total")
            med_total = request.POST.get('medicine_total')
            print(med_total)

            print("VACCINE SET")
            ctr = 0
            for vac_form in vaccine_formset:
                cd = vac_form.cleaned_data

                name = vaccine_names_list[ctr]
                id = vaccine_ids[ctr]
                vaccine = Medicine.objects.get(id = id)
                quantity = cd.get('quantity')
                budget = cd.get('budget')
                price = cd.get('price')
                print(name)
                print(quantity)
                print(budget)

                vac_budget = Budget_vaccine(vaccine=vaccine, quantity=quantity, price=price, total=budget,
                                             budget_allocation=budget_alloc)
                vac_budget.save()
                ctr += 1

            print("Vaccine Total")
            vac_total = request.POST.get('vaccine_total')
            print(vac_total)


            print("FOOD SET")
            cd = food_form.cleaned_data

            budget_puppy = cd.get('budget_puppy')
            budget_milk = cd.get('budget_milk')
            budget_adult = cd.get('budget_adult')

            quantity_puppy = cd.get('quantity_puppy')
            quantity_milk = cd.get('quantity_milk')
            quantity_adult = cd.get('quantity_adult')

            price_puppy = cd.get('price_puppy')
            price_milk = cd.get('price_milk')
            price_adult = cd.get('price_adult')

            puppy_budget = Budget_food(food="Puppy Food", quantity=quantity_puppy, price=price_puppy, total=budget_puppy,
                                       budget_allocation=budget_alloc)

            puppy_budget.save()

            milk_budget = Budget_food(food="Milk", quantity=quantity_milk, price=price_milk, total=budget_milk,
                                       budget_allocation=budget_alloc)

            milk_budget.save()

            adult_budget = Budget_food(food="Adult Food", quantity=quantity_adult, price=price_adult, total=budget_adult,
                                       budget_allocation=budget_alloc)

            adult_budget.save()

            print("Food Total")
            food_total = request.POST.get('food_total')
            print(food_total)

            print("EQUIPMENT SET")
            ctr = 0
            for equip_form in equipment_formset:
                cd = equip_form.cleaned_data

                name = equipment_name[ctr]
                id = equipment_ids[ctr]
                equipment = Miscellaneous.objects.get(id = id)
                quantity = cd.get('quantity')
                budget = cd.get('budget')
                price = cd.get('price')
                print(name)
                print(quantity)
                print(budget)

                equip_budget = Budget_equipment(equipment=equipment, quantity=quantity, price=price, total=budget,
                                            budget_allocation=budget_alloc)
                equip_budget.save()

                ctr += 1

            print("Equipment Total")
            equip_total = request.POST.get('equipment_total')
            print(equip_total)

            print("VET SUPPLY SET")
            ctr = 0
            for supply_form in vet_supply_formset:
                cd = supply_form.cleaned_data

                name = vet_supply_name
                id = vet_supply_ids[ctr]
                vet_supply = Miscellaneous.objects.get(id = id)
                quantity = cd.get('quantity')
                budget = cd.get('budget')
                price = cd.get('price')
                print(name)
                print(quantity)
                print(budget)

                supply_budget = Budget_vet_supply(vet_supply=vet_supply, quantity=quantity, price=price, total=budget,
                                              budget_allocation=budget_alloc)
                supply_budget.save()

                ctr += 1

            print("Vet Supply Total")
            vet_total = request.POST.get('vet_supply_total')
            print(vet_total)

            print("GRAND TOTAL")
            grandtotal = request.POST.get('grand_total')
            print(grandtotal)

            budget_alloc.food_total = food_total
            budget_alloc.equipment_total = equip_total
            budget_alloc.medicine_total = med_total
            budget_alloc.vaccine_total = vac_total
            budget_alloc.vet_supply_total = vet_total

            budget_alloc.k9_request_forecast = request_forecast[4]
            budget_alloc.k9_needed_for_demand = required_dogs
            budget_alloc.k9_cuurent = all_current_dogs

            budget_alloc.grand_total = grandtotal
            budget_alloc.save()

            style = "ui green message"
            messages.success(request, 'Budget Estimate has been successfully saved!')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    else:

        medicine_formset = MedicineFormset(prefix="medicine")
        vaccine_formset = VaccineFormset(prefix="vaccine")
        food_form = FoodForm(prefix="food")
        equipment_formset = EquipmentFormset(prefix="equipment")
        vet_supply_formset = Vet_supplyFormset(prefix="vet_supply")

    print("TEST SUPPLY FORECAST")
    print(vet_supply_forecast)

    print(previous_medicine_budget)
    print(medicine_ids)
    context = {
        'title': 'Budget Estimate for January - December, ' + str(date.today().year + 1),
        'style' : style,
        'request_forecast': request_forecast[4],
        # 'dogs_needed': dogs_needed,
        # 'undeployed_dogs': deployed_dogs,
        'all_current_dogs': all_current_dogs,
        #'dogs_to_budget': dogs_to_budget,

        'untrained_dogs' : untrained_dogs,
        'deployable_dogs' : deployable_dogs,
        'breeding_dogs' : breeding_dogs,
        'deployed_dogs' : deployed_dogs,
        'forecasted_dogs' : forecasted_dogs,
        'required_dogs' : required_dogs,
        'recommended_dogs': recommended_dogs,

        'graph': request_forecast[0],
        'models': request_forecast[1],
        'errors': request_forecast[2],
        'predictions': request_forecast[3],

        'medicine_name': medicine_name_list,
        'medicine_forecast': medicine_forecast_list,
        'medicine_price': medicine_price_list,
        'medicine_current' :medicine_current,
        'medicine_previous_price' : medicine_previous_price,
        'medicine_previous_total': medicine_previous_total,
        'medicine_actual': medicine_actual,

        'vaccine_name': vaccine_names_list,
        'vaccine_used_yearly': vaccine_used_yearly_list,
        'vaccine_price': vaccine_price_list,
        'vaccine_current': vaccine_current,
        'vaccine_previous_price': vaccine_previous_price,
        'vaccine_previous_total': vaccine_previous_total,
        'vaccine_actual': vaccine_actual,

        'deworming_req' : deworming_req,
        'dhppil_cv_req' : dhppil_cv_req,
        'heartworming_req' : heartworming_req,
        'antirabies_req' : antirabies_req,
        'bordetella_req' : bordetella_req,
        'dhppil4_req' : dhppil4_req,
        'tick_flea_req' :tick_flea_req,
        'deworming' : deworming,
        'dhppil_cv' : dhppil_cv,
        'heartworming'  : heartworming,
        'antirabies' :  antirabies,
        'bordetella' : bordetella,
        'dhppil4' : dhppil4,
        'tick_flea' :tick_flea,

        'adult_food_quantity': Decimal(adult_food_quantity),
        'puppy_food_quantity': Decimal(puppy_food_quantity),
        'milk_quantity': Decimal(milk_quantity),

        'adult_food_data': adult_food_data,
        'adult_yearly_total_min' :adult_yearly_total_min,
        'adult_yearly_total_max' : adult_yearly_total_max,
        'puppy_food_data' : puppy_food_data,

        'milk_yearly_total': milk_yearly_total,
        'puppy_yearly_total': puppy_yearly_total,

        'adult_previous_price': adult_previous_price,
        'adult_previous_total': adult_previous_total,
        'adult_actual': adult_actual,
        'puppy_previous_price': puppy_previous_price,
        'puppy_previous_total': puppy_previous_total,
        'puppy_actual': puppy_actual,
        'milk_previous_price': milk_previous_price,
        'milk_previous_total': milk_previous_total,
        'milk_actual': milk_actual,


        'equipment_name': equipment_name,
        'equipment_quantity': equipment_quantity,
        'equipment_price': equipment_price,
        'equipment_previous_price': equipment_previous_price,
        'equipment_previous_total': equipment_previous_total,
        'equipment_actual': equipment_actual,


        'vet_supply_name': vet_supply_name,
        'vet_supply_quantity': vet_supply_quantity,
        'vet_supply_price': vet_supply_price,
        'vet_supply_forecast': vet_supply_forecast,
        'vet_supply_uom': vet_supply_uom,
        'vet_supply_previous_price': vet_supply_previous_price,
        'vet_supply_previous_total': vet_supply_previous_total,
        'vet_supply_actual': vet_supply_actual,

        'medicine_formset' : medicine_formset,
        'vaccine_formset' : vaccine_formset,
        'food_form' : food_form,
        'equipment_formset' : equipment_formset,
        'vet_supply_formset' : vet_supply_formset,

        'medicine_spendings': medicine_spendings,
        'vaccine_spendings': vaccine_spendings,
        'food_spendings': food_spendings,
        'equipment_spendings': equipment_spendings,
        'vet_supply_spendings': vet_supply_spendings,
        'grandspendings': grandspendings,
    }

    return render(request, 'planningandacquiring/budgeting.html', context)


#TODO Add date to be budgeted selection
def budgeting_list(request):
    budgets = Budget_allocation.objects.all()
    form = budget_date(request.POST or None)


    if request.method == 'POST':

        return HttpResponseRedirect('budgeting/')

    context ={
        'budgets' : budgets,
        'date': form,
        'Title' : "Create Budget"
    }

    return render(request, 'planningandacquiring/budget_list.html', context)

def budgeting_detail(request):

    context = {
        '':''
    }

    return render(request, 'planningandacquiring/budget_detail.html', context)


def breeding_recommendation(request):

    k9_list_breed = None
    k9_list_skill = None
    k9_list_breed_skill = None

    form = select_breeder(request.POST or None)
    if request.method == 'POST':

        k9 = form['k9'].value()
        k9 = K9.objects.get(id = int(k9))

        if form.is_valid():
            if k9.sex == "Male":
                k9_list_breed = K9.objects.filter(breed = k9.breed).filter(training_status = 'For-Breeding').exclude(id = k9.id).filter(sex = "Female")
                k9_list_skill = K9.objects.filter(capability = k9.capability).filter(training_status = 'For-Breeding').exclude(id = k9.id).filter(sex = "Female")
                k9_list_breed_skill = K9.objects.filter(capability = k9.capability).filter(breed = k9.breed).filter(training_status = 'For-Breeding').exclude(id = k9.id).filter(sex = "Female")
            elif k9.sex == "Female":
                k9_list_breed = K9.objects.filter(breed=k9.breed).filter(training_status='For-Breeding').exclude(id=k9.id).filter(sex = "Male")
                k9_list_skill = K9.objects.filter(capability=k9.capability).filter(training_status='For-Breeding').exclude(id=k9.id).filter(sex = "Male")
                k9_list_breed_skill = K9.objects.filter(capability=k9.capability).filter(breed=k9.breed).filter(training_status='For-Breeding').exclude(id=k9.id).filter(sex = "Male")
    print(k9_list_breed)
    print(k9_list_skill)
    print(k9_list_breed_skill)

    context = {
        'test': "test",
        'form': form,
        'k9_list_breed': k9_list_breed,
        'k9_list_skill': k9_list_skill,
        'k9_list_breed_skill': k9_list_breed_skill,
    }

    return render(request, 'planningandacquiring/breeding_recommendation.html', context)

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

    context = {
        'Title': "Add Breed",
        'form': form,
        'style': style,
    }
    print(form)
    return render(request, 'planningandacquiring/add_breed.html', context)


def breed_listview(request):
    breed = Dog_Breed.objects.all()

    context = {
        'Title': 'Breed List',
        'breed': breed
    }

    return render(request, 'planningandacquiring/view_breed.html', context)

def budgeting_report(request):
    date = dt.now()
    year = date.year
    prev_year = year - 1

    medicine = Medicine_Subtracted_Trail.objects.filter(date_subtracted__year = prev_year)
    food = Food_Subtracted_Trail.objects.filter(date_subtracted__year = prev_year)
    miscellaneous = Miscellaneous_Subtracted_Trail.objects.filter(date_subtracted__year = prev_year)


    previous_budget_alloc = Budget_allocation.objects.exclude(date_created__year__gte = year).latest('id')
    recent_budget_alloc = Budget_allocation.objects.latest('id')

    budget_medicine = Budget_medicine.objects.filter(budget_allocation = previous_budget_alloc)
    budget_equipment = Budget_equipment.objects.filter(budget_allocation = previous_budget_alloc)
    budget_food = Budget_food.objects.filter(budget_allocation = previous_budget_alloc)
    budget_vaccine = Budget_vaccine.objects.filter(budget_allocation = previous_budget_alloc)
    budget_vet_supply = Budget_vet_supply.objects.filter(budget_allocation = previous_budget_alloc)

    recent_budget_medicine = Budget_medicine.objects.filter(budget_allocation=recent_budget_alloc)
    recent_budget_equipment = Budget_equipment.objects.filter(budget_allocation=recent_budget_alloc)
    recent_budget_food = Budget_food.objects.filter(budget_allocation=recent_budget_alloc)
    recent_budget_vaccine = Budget_vaccine.objects.filter(budget_allocation=recent_budget_alloc)
    recent_budget_vet_supply = Budget_vet_supply.objects.filter(budget_allocation=recent_budget_alloc)

    list_recent_budg_med_price = []
    for item in recent_budget_medicine:
        list_recent_budg_med_price.append(item.price)

    context = {
        'medicine' : medicine,
        'food': food,
        'miscellaneous': miscellaneous,
        'budget_alloc': previous_budget_alloc,
        'budget_medicine': budget_medicine,
        'budget_equipment': budget_equipment,
        'budget_food': budget_food,
        'budget_vaccine': budget_vaccine,
        'budget_vet_supply': budget_vet_supply,
        'year': year,
        'recent_budget_medicine': recent_budget_medicine,
        'recent_budget_equipment': recent_budget_equipment,
        'recent_budget_food': recent_budget_food,
        'recent_budget_vaccine': recent_budget_vaccine,
        'recent_budget_vet_supply': recent_budget_vet_supply,
        'list_recent_budg_med_price': list_recent_budg_med_price,
    }

    return render(request, 'planningandacquiring/budgeting_report.html', context)