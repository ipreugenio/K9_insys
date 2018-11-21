from django.shortcuts import render
from .forms import add_donated_K9_form, add_donator_form, add_K9_parents_form, add_offspring_K9_form
from .models import K9, K9_Past_Owner, K9_Donated, K9_Parent, K9_Quantity
from training.models import Training
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


from faker import Faker

#statistical imports
from math import *
from decimal import Decimal
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

#graphing imports
'''from igraph import *
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
import statsmodels.api as sm'''


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
            Training.objects.create(k9=k9, training='EDD')
            Training.objects.create(k9=k9, training='NDD')
            Training.objects.create(k9=k9, training='SAR')

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
        #delete training record
        training = Training.objects.filter(k9=k9)
        training.delete()
        #delete k9
        k9.delete()

        context = {
            'Title': "Receive Donated K9",
            'form': add_donated_K9_form,
        }
        return render(request, 'planningandacquiring/add_donated_K9.html', context)

#TODO Add capability to add a single parent
#TODO Added k9s not immediately showing up in breeding form

def add_K9_parents(request):

    form = add_K9_parents_form(request.POST)
    style = "ui teal message"
    mothers = K9.objects.filter(sex="Female")
    fathers = K9.objects.filter(sex="Male")

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
        Training.objects.create(k9=offspring, training='EDD')
        Training.objects.create(k9=offspring, training='NDD')
        Training.objects.create(k9=offspring, training='SAR')
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
    revert_differencing = [inverse_difference(testd[i], predictions[i]) for i in range(len(predictions))] #TODO check if inverse differencing is correct
    error = mean_squared_error(testd, revert_differencing) #TODO Confirm if forecast error parameters is correct
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

    data = []
    data.append(revert_differencing)
    data.append(yhat)
    data.append(root_error)

    return data


#(original timeseries df, scatter models, graph title)
def graph_forecast(timeseries, models, title):
    original_date = []
    original_quantity = []

    #test data is 66% of all data
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

def K9_forecast(request):
    quantity_set = K9_Quantity.objects.all().order_by('date_bought')

    context = {
        'title': 'Forecasting',
        'graph': "",
        'models': "",
        'errors': "",
        'predictions': ""
    }

    if quantity_set:
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

        graph_title = "Forecasting K9s Demand Using Various Models"
        graph = graph_forecast(ts, Scatter_Models, graph_title)


        context = {
            'title': 'Forecasting',
            'graph': graph,
            'models': models,
            'errors': errors,
            'predictions': predictions
        }

    return render(request, 'planningandacquiring/forecast_k9_required.html', context)

#Use in forecasting to test if original data is stationary
def test_stationarity(timeseries, index):
    # Determing rolling statistics
    # Set at which index will test data start

    rolmean = timeseries.rolling(index).mean()
    rolstd = timeseries.rolling(index).std()

    idx = pd.IndexSlice

    # Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries.iloc[:,0].values, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)

    #Check Root Mean Squared Error, the lower the better
    #rms = sqrt(mean_squared_error())
    #print(rms)

    ts_d = []
    ts_q = []

    for index, row in timeseries.iterrows():

        ts_q.append(row["Quantity"])
        ts_d.append(index)

    mean_d = []
    mean_q = []

    for index, row in rolmean.iterrows():
        mean_q.append(row["Quantity"])
        mean_d.append(index)

    std_d = []
    std_q = []

    for index, row in rolstd.iterrows():
        std_q.append(row["Quantity"])
        std_d.append(index)


    naive = go.Scatter(
        x=list(ts_d),
        y=list(ts_q),
        name = "Original"
    )
    ave = go.Scatter(
        x=list(mean_d),
        y=list(mean_q),
        name = "Rolling Mean"
    )
    sdev = go.Scatter(
        x=list(std_d),
        y=list(std_q),
        name = "Rolling Standard Deviation"
    )


    data = [naive, ave, sdev]

    layout = go.Layout(
        title="Stationary Test"
    )

    fig = go.Figure(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    return graph

def timeseries_generator():
    fake = Faker()
    for x in range(100):
        number = randint(1, 60)
        date = fake.date_between(start_date='-12y', end_date='-2y')

        date_quantity = K9_Quantity(quantity = number, date_bought = date)
        date_quantity.save()

    return None
