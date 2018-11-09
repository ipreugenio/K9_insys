from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
from planningandacquiring.models import K9, K9_Parent, K9_Quantity
from .models import K9_Genealogy, K9_Handler, User
from .forms import TestForm, add_handler_form
from collections import OrderedDict


#statistical imports
from math import *
from sklearn.metrics import mean_squared_error
import pandas as pd


import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from datetime import datetime, date
from dateutil.parser import parse

#graphing imports
import igraph
from igraph import *
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.graph_objs.layout as lout

#print(pd.__version__) #Version retrieved is not correct

from faker import Faker
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.statespace.varmax import VARMAX
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from random import random, randint
from statsmodels.tsa.stattools import adfuller, kpss
import statsmodels.api as sm


# Create your views here.

def index(request):
    return render (request, 'training/index.html')



def classify_k9_list(request):
    data_unclassified = K9.objects.filter(training_status="Unclassified")
    data_classified = K9.objects.filter(training_status="Classified")
    data_ontraining = K9.objects.filter(training_status="On-Training")
    data_trained = K9.objects.filter(training_status="Trained")


    context = {
        'data_unclassified': data_unclassified,
        'data_classified': data_classified,
        'data_ontraining': data_ontraining,
        'data_trained': data_trained,
    }
    return render (request, 'training/classify_k9_list.html', context)

#TODO Should be radio buttons
#TODO Restrict Viable dogs to be trained for those who are 6 months old
#TODO Add additional age for months
#TODO Add additional classification, for breeding
def classify_k9_select(request, id):
    data = K9.objects.get(id=id)

    if request.method == 'POST':
        print(request.POST.get('select_classify'))
        data.capability = request.POST.get('select_classify')
        data.training_status = "Classified"
        data.save()
        style = "ui green message" 
        messages.success(request, 'K9 has been successfully Classified!')

    try:
        parent = K9_Parent.objects.get(offspring=data)
    except K9_Parent.DoesNotExist:
        context = {
            'data': data,
        }
    else:
        parent_exist = 1
        context = {
            'data': data,
            'parent': parent,
            'parent_exist': parent_exist
        }

    return render (request, 'training/classify_k9_select.html', context)


def assign_k9_select(request, id):
    form = add_handler_form(request.POST)
    style = "ui teal message"
    handlers = User.objects.filter(position="Handler")
    k9 = K9.objects.get(id=id)

    if request.method == 'POST':
        if form.is_valid():
            handler_id = request.POST.get('handler')
            handler = User.objects.get(id=handler_id)
            K9_Handler.objects.create(k9 = k9, handler = handler)
            k9.training_status = "On-Training"
            k9.save()
            messages.success(request, 'K9 has been assigned to a handler!')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
            print(form)

    context = {
        'Title': "K9 Assignment for " + k9.name,
        'form': form,
        'style': style,
        'handler': handlers,
    }
    return render (request, 'training/assign_k9_select.html', context)

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



def training_records(request):
    return render(request, 'training/training_records.html')


def gender_count_between_breeds():
    k9_set = K9.objects.all()

    breed = []
    male_count = []
    female_count = []

    loop = 0
    for k9 in k9_set:
        breed.append(k9.breed)
        M = K9.objects.filter(sex='Male', breed=breed[loop])
        F = K9.objects.filter(sex='Female', breed=breed[loop])
        male_count.append(M.count())
        female_count.append(F.count())
        loop += 1

    male = go.Bar(
        x=breed,
        y=male_count,
        name="Male",
        text=male_count
    )

    female = go.Bar(
        x=breed,
        y=female_count,
        name="Female",
        text=female_count
    )

    data = [male, female]

    layout = go.Layout(
        title="Gender Count for " + str(k9_set.count()) + " Dogs Based on Breed",
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    return graph

def skill_count_between_breeds():
    k9_set = K9.objects.exclude(capability="None")

    breed = []
    sar_count = []
    ndd_count = []
    edd_count = []

    loop = 0
    for k9 in k9_set:
        breed.append(k9.breed)
        S = K9.objects.filter(capability='SAR', breed=breed[loop])
        N = K9.objects.filter(capability='NDD', breed=breed[loop])
        E = K9.objects.filter(capability='EDD', breed=breed[loop])
        sar_count.append(S.count())
        ndd_count.append(N.count())
        edd_count.append(E.count())
        loop += 1

    SAR = go.Bar(
        x=breed,
        y=sar_count,
        name="SAR",
        text=sar_count
    )

    NDD = go.Bar(
        x=breed,
        y=ndd_count,
        name="NDD",
        text=ndd_count
    )

    EDD = go.Bar(
        x=breed,
        y=edd_count,
        name="EDD",
        text=edd_count
    )

    data = [SAR, NDD, EDD]

    layout = go.Layout(
        title="Skill Count for " + str(k9_set.count()) + " Assigned Dogs Based on Breed",
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    return graph

def skill_percentage_between_sexes():
    k9_set = K9.objects.exclude(capability="None")
    m_sar_count = []
    m_ndd_count = []
    m_edd_count = []

    f_sar_count = []
    f_ndd_count = []
    f_edd_count = []
    for k9 in k9_set:
        if (k9.sex == "Male"):
            if (k9.capability == "SAR"):
                m_sar_count.append(None)
            elif (k9.capability == "NDD"):
                m_ndd_count.append(None)
            else:
                m_edd_count.append(None)
        else:
            if (k9.capability == "SAR"):
                f_sar_count.append(None)
            elif (k9.capability == "NDD"):
                f_ndd_count.append(None)
            else:
                f_edd_count.append(None)


    fig = go.Figure(
    data = [
        {
            "values": [len(m_sar_count), len(m_ndd_count), len(m_edd_count)], # count for males
            "labels": [
                "SAR", "NDD", "EDD"
            ],
            "text": ["SAR", "NDD", "EDD"],
            "textposition": "inside",
            "domain": {"x": [0, .48]},
            "name": "Males",
            "hoverinfo": "label+value+name",
            "hole": .4,
            "type": "pie"
        },
        {
            "values": [len(f_sar_count), len(f_ndd_count), len(f_edd_count)],
            "labels": [
                "SAR", "NDD", "EDD"
            ],
            "text": ["SAR", "NDD", "EDD"],
            "textposition": "inside",
            "domain": {"x": [.52, 1]},
            "name": "Females",
            "hoverinfo": "label+value+name",
            "hole": .4,
            "type": "pie"
        }],

    layout =  {
        "title": "Skill Percentage for " + str(k9_set.count()) + " Assigned Dogs Based on Sexes",
        "annotations": [
            {
                "font": {
                    "size": 20
                },
                "showarrow": False,
                "text": "Males",
                "x": 0.20,
                "y": 0.5
            },
            {
                "font": {
                    "size": 20
                },
                "showarrow": False,
                "text": "Females",
                "x": 0.8,
                "y": 0.5
            }
        ]
    }
    )

    graph = opy.plot(fig, auto_open=False, output_type='div')

    return graph

#TODO check if ratio ba talaga tawag dito just in case
def skill_count_ratio():
    k9_set = K9.objects.exclude(capability="None")

    SAR = K9.objects.filter(capability="SAR")
    NDD = K9.objects.filter(capability="NDD")
    EDD = K9.objects.filter(capability="EDD")

    labels = ['SAR', 'NDD', 'EDD']
    values = [SAR.count(), NDD.count(), EDD.count()]

    trace = go.Pie(labels=labels, values=values,
                    hoverinfo = 'label+value', textinfo = 'percent',)

    data = [trace]

    layout = go.Layout(
        title="Skill Ratio for " + str(k9_set.count()) + " Assigned Dogs",
    )

    fig = go.Figure(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    return graph

def K9_skill_classifier(request):

    bar_gender_count = gender_count_between_breeds()
    pie_skill_ratio = skill_count_ratio()
    bar_skill_count_from_breed = skill_count_between_breeds()
    pie_skill_percentage_from_sexes = skill_percentage_between_sexes()

    context = {
        'bar_gender_count': bar_gender_count,
        'pie_skill_ratio' : pie_skill_ratio,
        'bar_skill_count_from_breed': bar_skill_count_from_breed,
        'pie_skill_percentage_from_sexes': pie_skill_percentage_from_sexes
    }

    return render(request, 'training/k9_skill_classifier.html', context)

def make_annotations(pos, labels, M):
    #test = list(map(str, range(7)))
    font_size = 10
    font_color = 'rgb(250,250,250)'
    L=len(pos)
    '''
    if len(test)!=L:
        raise ValueError('The lists pos and text must have the same len')
    '''
    annotations = []#lout.Annotations()
    for k in range(L):
        annotations.append(
            dict (
                text=labels[k], # or replace labels with a different list for the text within the circle
                x=pos[k][0], y=2*M-pos[k][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def generate_family_tree(id):
    k9 = K9.objects.get(id=id)
    target = k9.name
    genepool = K9_Genealogy.objects.filter(zero = k9)

    g = Graph() #initialize graph

    names = []
    g.vs["name"] = []
    for gene in genepool:
        try:
            g.add_vertices(1)
            f = gene.f
            if f is not None:
                k9_f = K9.objects.get(id=f.id)
                names.append(str(k9_f.name))
        except K9.DoesNotExist:
            pass

        try:
            g.add_vertices(1)
            m = gene.m
            if m is not None:
                k9_m = K9.objects.get(id=m.id)
                names.append(str(k9_m.name))
        except K9.DoesNotExist:
            pass

        try:
            g.add_vertices(1)
            o = gene.o
            if o is not None:
                k9_o = K9.objects.get(id=o.id)
                names.append(str(k9_o.name))
        except K9.DoesNotExist:
            pass

    count_before = len(names)
    # Remove duplicates from this list.
    result = remove_duplicates(names)
    count_after = len(result)
    extras = count_before - count_after
    g.vs["name"] = result #remove_duplicates
    #for extra in range(extras):
        #g.delete_vertices(count_before+1)

    for gene in genepool:
        f = gene.f
        m = gene.m
        o = gene.o
        if f is not None:
            father = K9.objects.get(id=f.id)
            father_name = str(father.name)
            f_index = g.vs.find(name=father_name)
        if m is not None:
            mother = K9.objects.get(id=m.id)
            mother_name = str(mother.name)
            m_index = g.vs.find(name=mother_name)
        if o is not None:
            offspring = K9.objects.get(id=o.id)
            offspring_name = str(offspring.name)
            o_index = g.vs.find(name=offspring_name)

        connection = []

        if o is not None and f is not None:
            g.add_edges([(o_index, f_index)])
            connection.append("Father")
        if o is not None and m is not None:
            g.add_edges([(o_index, m_index)])
            connection.append("Mother")

        g.es["relation"] = connection

    #vertex_count = len(genes)
    #v_label = map(str, range(7))

    '''
    g.add_vertices(7) #Add Points
    g.add_edges([(0, 1), (0, 2), (2, 3), (3, 4), (4, 2), (2, 5), (5, 0), (6, 3), (5, 6)])# Add lines by specifying which vertex is connected to which

    #Add attributes to each vertex and edge (Note that these always follow index id)
    #vs = vertex, should have same number of vertices
    #es = edge, should have same number of edges
    g.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
    g.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
    g.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
    g.es["is_formal"] = [False, False, True, True, True, False, True, False, False]
    '''

    lay = g.layout("rt")

    position = {k: lay[k] for k in range(count_after)}
    Y = [lay[k][1] for k in range(count_after)]
    M = max(Y)

    es = EdgeSeq(g)  # sequence of edges
    E = [e.tuple for e in g.es]  # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2 * M - position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

    labels = g.vs["name"]
    relation = g.es["relation"]
    print(relation)

    lines = go.Scatter(x=Xe,
                       y=Ye,
                       mode='lines',
                       text=(list(relation)),
                       hoverinfo='text',
                       line=dict(color='rgb(210,210,210)', width=2),
                       )
    dots = go.Scatter(x=Xn,
                      y=Yn,
                      mode='markers',
                      name='',
                      marker=dict(  # symbol='dot',
                          size=50,
                          color='#6175c1',  # '#DB4551',
                          line=dict(color='rgb(50,50,50)', width=1)
                      ),
                      text=(list(labels)),
                      hoverinfo= 'text',
                      opacity=0.8
                      )

    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    layout = dict(title='Descendants of K9 '+ str(target),
                  autosize=True,
                  annotations=make_annotations(position, labels, M),
                  font=dict(size=12),
                  showlegend=False,
                  xaxis=lout.XAxis(axis),
                  yaxis=lout.YAxis(axis),
                  width=1000,
                  height=800,
                  margin=dict(l=40, r=40, b=85, t=100),
                  hovermode='closest',
                  plot_bgcolor='rgb(248,248,248)'
                  )

    data = [lines, dots]
    fig = dict(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    return graph

def skills_from_father_side(id):

    return None
def skills_from_mother_side(id):
    return None
def skills_from_gender(id):
    k9_family = K9_Genealogy.objects.filter(zero=id)

    k9_list = []
    for k9 in k9_family:
        if k9.o is not None:
            cursor = k9.o
            k9_list.append(cursor.id)
        if k9.f is not None:
            cursor = k9.f
            k9_list.append(cursor.id)
        if k9.m is not None:
            cursor = k9.m
            k9_list.append(cursor.id)

    k9_list = remove_duplicates(k9_list)

    k9_set = K9.objects.filter(pk__in=k9_list).exclude(capability="None")

    m_sar_count = []
    m_ndd_count = []
    m_edd_count = []

    f_sar_count = []
    f_ndd_count = []
    f_edd_count = []
    for k9 in k9_set:
        if (k9.sex == "Male"):
            if (k9.capability == "SAR"):
                m_sar_count.append(None)
            elif (k9.capability == "NDD"):
                m_ndd_count.append(None)
            else:
                m_edd_count.append(None)
        else:
            if (k9.capability == "SAR"):
                f_sar_count.append(None)
            elif (k9.capability == "NDD"):
                f_ndd_count.append(None)
            else:
                f_edd_count.append(None)

    fig = go.Figure(
        data=[
            {
                "values": [len(m_sar_count), len(m_ndd_count), len(m_edd_count)],  # count for males
                "labels": [
                    "SAR", "NDD", "EDD"
                ],
                "text": ["SAR", "NDD", "EDD"],
                "textposition": "inside",
                "domain": {"x": [0, .48]},
                "name": "Males",
                "hoverinfo": "label+value+name",
                "hole": .4,
                "type": "pie"
            },
            {
                "values": [len(f_sar_count), len(f_ndd_count), len(f_edd_count)],
                "labels": [
                    "SAR", "NDD", "EDD"
                ],
                "text": ["SAR", "NDD", "EDD"],
                "textposition": "inside",
                "domain": {"x": [.52, 1]},
                "name": "Females",
                "hoverinfo": "label+value+name",
                "hole": .4,
                "type": "pie"
            }],

        layout={
            "title": "Skill Percentage for " + str(k9_set.count()) + " Assigned Dogs from Descendants Based on Sexes",
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "Males",
                    "x": 0.20,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "Females",
                    "x": 0.8,
                    "y": 0.5
                }
            ]
        }
    )

    graph = opy.plot(fig, auto_open=False, output_type='div')

    return graph


def skill_in_general(id):
    k9_family = K9_Genealogy.objects.filter(zero = id)

    k9_list = []
    for k9 in k9_family:
        if k9.o is not None:
            cursor = k9.o
            k9_list.append(cursor.id)
        if k9.f is not None:
            cursor = k9.f
            k9_list.append(cursor.id)
        if k9.m is not None:
            cursor = k9.m
            k9_list.append(cursor.id)

    k9_list = remove_duplicates(k9_list)

    k9_set = K9.objects.filter(pk__in=k9_list).exclude(capability="None")

    SAR = K9.objects.filter(capability="SAR", pk__in=k9_list)
    NDD = K9.objects.filter(capability="NDD", pk__in=k9_list)
    EDD = K9.objects.filter(capability="EDD", pk__in=k9_list)

    labels = ['SAR', 'NDD', 'EDD']
    values = [SAR.count(), NDD.count(), EDD.count()]

    trace = go.Pie(labels=labels, values=values,
                   hoverinfo='label+value', textinfo='percent', )

    data = [trace]

    layout = go.Layout(
        title="Skill Ratio for " + str(k9_set.count()) + " Assigned Dogs from Descendants",
    )

    fig = go.Figure(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    return graph


def genealogy(request):

    form = TestForm

    tree = ""
    general = ""
    gender = ""

    if request.method == 'POST':

        form = TestForm(request.POST)
        cancel = 0
        k9 = form.data['k9']
        #data = K9_Genealogy.objects.filter(zero=k9)
        #data.delete()
        K9_Genealogy.objects.all().delete()

        target = K9.objects.get(id=k9)
        flag = 0 #SET FLAG FOR WHEN END OF TREE IS REACHED
        counter = 1  # SET INITIAL DEPTH

        k9s = [target]  # INITIAL: TARGET K9 per depth

        while flag == 0: #CONTINUE TREE GENERATION
            for k9 in k9s:# FOR EVERY K9 IN CURRENT DEPTH
                if k9:
                    try:
                        k9_parents = K9_Parent.objects.get(offspring=k9)  # FIND TARGET'S PARENTS
                    except K9_Parent.DoesNotExist:
                        pass
                    else:
                        cancel = 1
                        mother = k9_parents.mother #SET MOTHER
                        father = k9_parents.father #SET FATHER

                        tree = K9_Genealogy(o = k9, m = mother, f = father, depth = counter, zero = target)
                        tree.save()


            nodes = K9_Genealogy.objects.filter(depth = counter)

            k9s = []

            if nodes:
                for node in nodes:
                    m = node.m
                    f = node.f
                    k9s.append(m)# GET TARGET K9s for next depth (mothers)
                    k9s.append(f) # GET TARGET K9s for next depth (fathers)

            counter += 1 #INCREASE DEPTH

            if not k9s: #IF FINAL NODES HAVE NO PARENTS, EXIT TREE GENERATION
                flag = 1

            if cancel == 1:
                print("STR ID = " + str(target.id))
                tree = generate_family_tree(target.id)
                general = skill_in_general(target.id)
                gender = skills_from_gender(target.id)
                #TODO Put other family related graphs here

            else:
                tree = "K9 has no descendants!"


    context = {
            'form': form,
            'tree': tree,
            'skill_in_general': general,
            'skill_by_gender': gender
            }


    return render(request, 'training/genealogy.html', context)

