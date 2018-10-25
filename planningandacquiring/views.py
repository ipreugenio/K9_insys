from django.shortcuts import render
from .forms import add_donated_K9_form, add_donator_form, add_K9_parents_form, add_offspring_K9_form
from .models import K9, K9_Past_Owner, K9_Donated, K9_Parent, K9_Quantity
from inventory.models import Medicine_Subtracted_Trail, Medicine
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates, Sum
from django.http import JsonResponse
from django.contrib import messages
from .forms import ReportDateForm

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
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.statespace.varmax import VARMAX
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.api import Holt
from random import random, randint
from statsmodels.tsa.stattools import adfuller, kpss
import statsmodels.api as sm

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
            return HttpResponseRedirect('confirm_donation/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
            print(form)

    context = {
        'Title' : "Receive Donated K9",
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
        'Title': "Receive Donated K9",
        'k9': k9,

    }
    return render(request, 'planningandacquiring/confirm_K9_donation.html', context)

def donation_confirmed(request):
    k9_id = request.session['k9_id']

    k9 = K9.objects.get(id=k9_id)

    if 'ok' in request.POST:
        return render(request, 'planningandacquiring/donation_confirmed.html')
    else:
        k9.delete()
        context = {
            'Title': "Receive Donated K9",
            'form': add_donated_K9_form,
        }
        return render(request, 'planningandacquiring/add_donated_K9.html', context)

def add_K9_parents(request):

    form = add_K9_parents_form(request.POST)
    style = "ui teal message"
    if request.method == 'POST':
        if form.is_valid():
            parents = form.save(commit=False)
            mother = parents.mother
            father = parents.father


            mother = K9.objects.get(id = mother.id)
            father = K9.objects.get(id = father.id)

            print("MOTHER")
            print(mother)
            print("FATHER")
            print(father)

            request.session["mother_id"] = mother.id
            request.session["father_id"] = father.id

            return HttpResponseRedirect('confirm_K9_parents/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
            print(form)

    context = {
        'Title': "K9_Breeding",
        'form': form,
        'style': style,

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
    if 'ok' in request.POST:
        return HttpResponseRedirect('add_K9_offspring_form/')
    else:
        context = {
            'Title': "Receive Donated K9",
            'form': add_K9_parents_form,
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
        return render(request, 'planningandacquiring/breeding_confirmed.html')
    else:
        offspring.delete()
        context = {
            'Title': "Receive Donated K9",
            'form': add_K9_parents_form
        }
        return render(request, 'planningandacquiring/add_donated_K9.html', context)


#Listview format
def K9_listview(request):
    k9 = K9.objects.all()

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


# Make a prediction give regression coefficients and lag obs
def predict(coef, history):
    yhat = coef[0]
    for i in range(1, len(coef)):
        yhat += coef[i] * history[-i]

    return yhat


def Autoregression(data):
    X = difference(data.values)
    size = int(len(X) * 0.66)
    data = data[0:size]
    model = AR(data)
    return model

def Moving_Average(data):
    X = difference(data.values)
    size = int(len(X) * 0.66)
    data = data[0:size]
    model = ARMA(data, order=(0, 1))
    return model

def Autoregressive_Moving_Average(data):
    X = difference(data.values)
    size = int(len(X) * 0.66)
    data = data[0:size]
    model = ARMA(data, order=(2, 1))
    return model

def Autoregressive_Integrated_Moving_Average(data):
    X = difference(data.values)
    size = int(len(X) * 0.66)
    data = data[0:size]
    model = ARIMA(data, order=(1, 1, 1))
    return model

def Seasonal_Autoregressive_Moving_Average(data):
    X = difference(data.values)
    size = int(len(X) * 0.66)
    data = data[0:size]
    model = SARIMAX(data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 1))
    return model

def Simple_Exponential_Smoothing(data):
    X = difference(data.values)
    size = int(len(X) * 0.66)
    data = data[0:size]
    model = SimpleExpSmoothing(data)
    return model

def Holt_Winters_Exponential_Smoothing(data):
    X = difference(data.values)
    size = int(len(X) * 0.66)
    data = data[0:size]
    model = ExponentialSmoothing(data)
    return model


def forecast(timeseries, model):


    # split dataset
    X = difference(timeseries.values)

    #Use 66% of data for training
    size = int(len(X) * 0.66)
    train, test = X[0:size], X[size:]

    data = timeseries[0:size]

    # train data
    #model = AR(data) >> Model is now a def parameter

    print("Model")
    print (model)

    model_fit = model.fit()
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
    error = mean_squared_error(test, predictions)
    root_error = sqrt(error)
    root_error = int(root_error * 10 ** 2) / 10.0 ** 2
    print('Test MSE: %.3f' % error)
    print('Test RMSE: %.3f' % root_error)
    print("Prediction : " + str(yhat))


    yhat = yhat.flatten()
    yhat = yhat.tolist()
    yhat = yhat[0]
    yhat = round(yhat)

    data = []
    data.append(predictions)
    data.append(yhat)
    data.append(root_error)

    return data


#(original timeseries df, scatter models, graph title)
def graph_forecast(timeseries, models, title):
    original_date = []
    original_quantity = []

    #test data is 66% of all data
    test_index = len(timeseries) * 0.66

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
    predicted_quantity = []
    predicted_date = []

    # test data is 66% of all data
    test_index = len(timeseries) * 0.66

    ctr = 0
    for index, row in timeseries.iterrows():
        if ctr >= test_index:
            predicted_date.append(index)
        ctr += 1

    ctr = 0
    for array in prediction:
        for row in array:
            if ctr != test_index:
                predicted_quantity.append(row)
        ctr += 1

    forecast = go.Scatter(
        x=list(predicted_date),
        y=list(predicted_quantity),
        name=title
    )

    return forecast

def Average(lst):
    return sum(lst) / len(lst)

def K9_forecast(request):
    quantity_set = K9_Quantity.objects.all().order_by('date_bought')

    quantity = []
    date = []

    for data in quantity_set:
        date_object = data.date_bought
        dt64 = np.datetime64(str(date_object))

        date.append(dt64)
        quantity.append(data.quantity)

    df = pd.DataFrame({'Date': list(date),
                       'Quantity': list(quantity),
                       })

    ts = df.set_index('Date')

    size = int(len(ts) * 0.66)
    print(size)
    A_model = ts.rolling(size).mean()
    print(A_model)
    X = difference(ts.values)
    train, test = X[0:size], X[size:]

    non_difference_train = ts.values[0:size]

    flat_train = non_difference_train.flatten()
    list_train = flat_train.tolist()


    mean = Average(list_train)
    mean = round(mean)

    # error = mean_squared_error(list_train, A_model)
    # root_error = sqrt(error)
    # mean_root_error = int(root_error * 10 ** 2) / 10.0 ** 2

    mean_d = []
    mean_q = []

    for index, row in A_model.iterrows():
        mean_q.append(row["Quantity"])
        mean_d.append(index)


    A_Scatter = go.Scatter(
        x=list(mean_d),
        y=list(mean_q),
        name="Mean"
    )



    models = []
    errors = []
    predictions = []

    models.append("Mean")
    errors.append("")
    predictions.append(mean)

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

    '''
    SARMA_model = Seasonal_Autoregressive_Moving_Average(ts)
    SARMA = forecast(ts, SARMA_model)
    SARMA_scatter = scatter_model(ts, SARMA, "Seasonal Autoregressive Integrated Moving Average (SARIMA)")
  
    
    SES_model = Simple_Exponential_Smoothing(ts)
    SES = exp_smoothing_forecast(ts, SES_model)
    SES_scatter = scatter_model(ts, SES, "Simple Exponential Smoothing (SES)")

   
    HWES_model = Holt_Winters_Exponential_Smoothing(ts)
    HWES = forecast(ts, HWES_model)
    HWES_scatter = scatter_model(ts, HWES, "Simple Exponential Smoothing (SES)")
    '''


    Scatter_Models = [A_Scatter, AR_scatter, MA_scatter, ARMA_scatter, ARIMA_scatter]

    graph_title = "Forecasting K9s to be Bought Using Various Models"
    graph = graph_forecast(ts, Scatter_Models, graph_title)


    context = {
        'title': 'Forecasting',
        'graph': graph,
        'models': models,
        'errors': errors,
        'predictions': predictions
    }

    return render(request, 'planningandacquiring/forecast_k9_required.html', context)