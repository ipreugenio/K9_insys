from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
from planningandacquiring.models import K9, K9_Parent
from .models import K9_Genealogy
from .forms import TestForm
from collections import OrderedDict

#classifier stuff
import pandas as pd
import igraph
from igraph import *


import plotly.offline as opy
import plotly.graph_objs as go
import plotly.graph_objs.layout as lout

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
    
def training_records(request):
    context = {
        'title': 'Training Records',
    }
    return render (request, 'training/training_records.html', context)


def K9_skill_classifier(request):

    k9_set = K9.objects.all()

    breed = []
    male_count = []
    female_count = []

    loop = 0
    for k9 in k9_set:
        breed.append(k9.breed)
        M = K9.objects.filter(sex='M', breed=breed[loop])
        F = K9.objects.filter(sex='F', breed=breed[loop])
        male_count.append(M.count())
        female_count.append(F.count())
        loop += 1


    male = go.Bar(
        x=breed,
        y= male_count,
        name = "Male",
        text = male_count
    )

    female = go.Bar(
        x=breed,
        y= female_count,
        name="Female",
        text = female_count
    )

    data = [male, female]

    layout = go.Layout(
        title="Gender Count for " + str(k9_set.count()) + " Dogs",
        barmode='group'
        )

    fig = go.Figure(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    context = {
        'graph': graph,
    }

    return render(request, 'training/k9_skill_classifier.html', context)


def forecasting(request):

    return None


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

    print(str(count_before))
    print(str(count_after))
    print("COMPLETE " + str(names))
    print("INCOMPLETE " + str(g.vs["name"]))

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

        if o is not None and f is not None:
            g.add_edges([(o_index, f_index)])
        if o is not None and m is not None:
            g.add_edges([(o_index, m_index)])


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
    '''
    details = []

    for count in range(7):
        desc = "[Name: " + str(g.vs["name"][count]) + "] [Age: " + str(g.vs["age"][count]) + "] [Gender: " + str(g.vs["gender"][count]) +"]"
        details.append(desc)
    '''


    lines = go.Scatter(x=Xe,
                       y=Ye,
                       mode='lines',
                       line=dict(color='rgb(210,210,210)', width=1),
                       hoverinfo='none'
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

    layout = dict(title='Family Tree for K9 '+ str(target),
                  annotations=make_annotations(position, labels, M),
                  font=dict(size=12),
                  showlegend=False,
                  xaxis=lout.XAxis(axis),
                  yaxis=lout.YAxis(axis),
                  margin=dict(l=40, r=40, b=85, t=100),
                  hovermode='closest',
                  plot_bgcolor='rgb(248,248,248)'
                  )

    data = [lines, dots]
    fig = dict(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    '''
    nr_vertices = 7
    v_label = map(str, range(nr_vertices))
    print(v_label)
    G = Graph.Tree(nr_vertices, 2)  # 2 stands for children number
    lay = G.layout('rt')

    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    es = EdgeSeq(G)  # sequence of edges
    E = [e.tuple for e in G.es]  # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2 * M - position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

    labels = list(v_label)

    lines = go.Scatter(x=Xe,
                       y=Ye,
                       mode='lines',
                       line=dict(color='rgb(210,210,210)', width=1),
                       hoverinfo='none'
                       )
    dots = go.Scatter(x=Xn,
                      y=Yn,
                      mode='markers',
                      name='',
                      marker=dict(#symbol='dot',
                                  size=18,
                                  color='#6175c1',  # '#DB4551',
                                  line=dict(color='rgb(50,50,50)', width=1)
                                  ),
                      text= (list(labels)),
                      hoverinfo='text',
                      opacity=0.8
                      )

    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    layout = dict(title='Tree with Reingold-Tilford Layout',
                  annotations=make_annotations(position, v_label, M),
                  font=dict(size=12),
                  showlegend=False,
                  xaxis= lout.XAxis(axis),
                  yaxis= lout.YAxis(axis),
                  margin=dict(l=40, r=40, b=85, t=100),
                  hovermode='closest',
                  plot_bgcolor='rgb(248,248,248)'
                  )

    data = [lines, dots]
    fig = dict(data=data, layout=layout)
    fig['layout'].update(annotations=make_annotations(position, v_label, M))
    #py.iplot(fig, filename='Tree-Reingold-Tilf')


    #data = [lines, dots]
    #fig = go.Figure(data=data,layout=layout)
    #fig['layout'].update(annotations=make_annotations(position, v_label))
    graph = opy.plot(fig, auto_open=False, output_type='div')
    '''
    return graph

def genealogy(request):

    form = TestForm

    tree =""

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
                tree = generate_family_tree(target.id)
            else:
                tree = "K9 has no descendants!"

    context = {
            'form': form,
            'tree': tree,
            }


    return render(request, 'training/genealogy.html', context)