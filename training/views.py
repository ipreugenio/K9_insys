from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
from planningandacquiring.models import K9, K9_Parent, K9_Quantity
from .models import K9_Genealogy, K9_Handler, User
from training.models import Training, K9_Adopted_Owner
from .forms import TestForm, add_handler_form
from planningandacquiring.forms import add_donator_form
from training.forms import TrainingUpdateForm, SerialNumberForm, AdoptionForms, ClassifySkillForm
import datetime
from deployment.models import Team_Assignment
from django.db.models import Sum


# from collections import OrderedDict

#graphing imports
import igraph
from igraph import *
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.graph_objs.layout as lout

#print(pd.__version__) #Version retrieved is not correct


def index(request):
    return render (request, 'training/index.html')

def adoption_form(request, id):
    data = K9.objects.get(id=id) # get k9
    form = AdoptionForms(request.POST or None)
    form.fields['email'].initial = ''
    form.fields['contact_no'].initial = ''
    #form.fields['k9'].initial = data
    #form.fields['k9'].initial = form.cleaned_data['data']
    #print(form.fields['k9'])

    if request.method == "POST":
        print(form.errors)
        form.k9 = data
        if form.is_valid():
            print('valid')
            form.save()
            no_id = form.save()
            no_id.k9 = data
            no_id.save()
            #print(no_id.k9)
            request.session['no_id'] = no_id.id
            return redirect('training:confirm_adoption', id = data.id)

    context = {
        'title': data,
        'form': form,
    }
    return render (request, 'training/adoption_form.html', context)

def confirm_adoption(request, id):
    data = K9.objects.get(id=id) # get k9
    no = request.session['no_id']
    new_owner = K9_Adopted_Owner.objects.get(id=no)
    if request.method == "POST":
        if 'ok' in request.POST:
            print('ok')
            data.training_status = 'Adopted'
            data.save()
            return redirect('training:adoption_confirmed')
        else:
            print('not ok')
            new_owner.delete()
            return redirect('training:adoption_form', id = data.id)
    context = {
        'title': data,
        'data': data,
    }
    return render (request, 'training/confirm_adoption.html', context)

def adoption_list(request):
    for_adoption = K9.objects.filter(training_status='For-Adoption')
    adopted = K9.objects.filter(training_status='Adopted')
    context = {
        'title': 'Adoption List',
        'for_adoption': for_adoption,
        'adopted': adopted,
    }

    return render (request, 'training/for_adoption_list.html', context)

def adoption_details(request, id):
    k9 = K9.objects.get(id=id)
    data = K9_Adopted_Owner.objects.get(k9=k9)

    context = {
        'title': data.k9,
        'data': data,
    }

    return render (request, 'training/adoption_details.html', context)


def unified_graph():
    k9_set = K9.objects.all()

    breeds = []

    sar_count_male = []
    ndd_count_male = []
    edd_count_male = []

    sar_count_female = []
    ndd_count_female = []
    edd_count_female = []

    skills = ['SAR', 'NDD', 'EDD']

    for k9 in k9_set:
        breeds.append(k9.breed)

    breeds = list(set(breeds))

    loop = 0
    for breed in breeds:
        SAR = K9.objects.filter(sex='Male', breed=str(breed), capability="SAR").count()
        NDD = K9.objects.filter(sex='Male', breed=str(breed), capability="NDD").count()
        EDD = K9.objects.filter(sex='Male', breed=str(breed), capability="EDD").count()

        sar_count_male.append(SAR)
        ndd_count_male.append(NDD)
        edd_count_male.append(EDD)

        loop += 1

    for breed in breeds:
        SAR = K9.objects.filter(sex='Female', breed=str(breed), capability="SAR").count()
        NDD = K9.objects.filter(sex='Female', breed=str(breed), capability="NDD").count()
        EDD = K9.objects.filter(sex='Female', breed=str(breed), capability="EDD").count()

        sar_count_female.append(SAR)
        ndd_count_female.append(NDD)
        edd_count_female.append(EDD)
        loop += 1

    sar_breed = []
    ndd_breed = []
    edd_breed = []
    for breed in breeds:
        sar_breed.append("SAR - " + str(breed))
        ndd_breed.append("NDD - " + str(breed))
        edd_breed.append("EDD - " + str(breed))

    print("K9 COUNT")
    print(str(k9_set.count()))
    print("X")
    print(sar_breed)
    print(ndd_breed)
    print(edd_breed)
    print("MALE")
    print(sar_count_male)
    print(ndd_count_male)
    print(edd_count_male)
    print("FEMALE")
    print(sar_count_female)
    print(ndd_count_female)
    print(edd_count_female)


    ctr = 0
    # SAR
    # for breed in breeds:
    # Tig 3 per breed

    sar_male = go.Bar(
        x=sar_breed,
        y=sar_count_male,
        name='Male'
    )
    ctr += 1
    sar_female = go.Bar(
        x=sar_breed,
        y=sar_count_female,
        name='Female'
    )
    ctr += 1

    # NDD
    # for breed in breeds:
    # Tig 3 per breed
    ndd_male = go.Bar(
        x=ndd_breed,
        y=ndd_count_male,
        name='Male'
    )
    ctr += 1
    ndd_female = go.Bar(
        x=ndd_breed,
        y=ndd_count_female,
        name='Female'
    )
    ctr += 1

    # EDD
    # for breed in breeds:
    # Tig 3 per breed
    edd_male = go.Bar(
        x=edd_breed,
        y=edd_count_male,
        name='Male'
    )
    ctr += 1
    edd_female = go.Bar(
        x=edd_breed,
        y=edd_count_female,
        name='Female'
    )
    ctr += 1

    data = [sar_male, sar_female, ndd_male, ndd_female, edd_male, edd_female]

    layout = go.Layout(
        title="K9 Count by Skill, Breed and Gender",
        barmode='stack'
    )

    fig = go.Figure(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    return graph

def classify_k9_list(request):
    data_unclassified = K9.objects.filter(training_status="Unclassified")
    data_classified = K9.objects.filter(training_status="Classified")
    data_ontraining = K9.objects.filter(training_status="On-Training")
    data_trained = K9.objects.filter(training_status="Trained")

    NDD_count = K9.objects.filter(capability='NDD').count()
    EDD_count = K9.objects.filter(capability='EDD').count()
    SAR_count = K9.objects.filter(capability='SAR').count()

    NDD_demand = list(Team_Assignment.objects.aggregate(Sum('NDD_demand')).values())[0]
    EDD_demand = list(Team_Assignment.objects.aggregate(Sum('EDD_demand')).values())[0]
    SAR_demand = list(Team_Assignment.objects.aggregate(Sum('SAR_demand')).values())[0]

    if not NDD_demand:
        NDD_demand = 0
    if not EDD_demand:
        EDD_demand = 0
    if not SAR_demand:
        SAR_demand = 0



    '''
    if k9 has failed 2 training records, disable reasign button
    '''

    context = {
        'title': 'K9 Classification',
        'data_unclassified': data_unclassified,
        'data_classified': data_classified,
        'data_ontraining': data_ontraining,
        'data_trained': data_trained,
        'EDD_count': EDD_count,
        'NDD_count': NDD_count,
        'SAR_count': SAR_count,
        'NDD_demand': NDD_demand,
        'EDD_demand': EDD_demand,
        'SAR_demand': SAR_demand,

    }
    return render (request, 'training/classify_k9_list.html', context)

def view_graphs(request, id):
    k9_id = request.session['k9_id']

    method_arrays = []

    skill_count_between_breeds_desc = ""
    skill_percentage_between_sexes_desc = ""
    skill_count_ratio_desc = ""
    skills_from_gender_desc = ""
    skills_in_general = ""

    method_arrays.append(skill_count_between_breeds(k9_id))
    method_arrays.append(skill_percentage_between_sexes(k9_id))
    method_arrays.append(skill_count_ratio())

    tree = genealogy(k9_id)
    genes = K9_Genealogy.objects.filter(zero=k9_id)
    if genes:
        method_arrays.append(skills_from_gender(k9_id))
        method_arrays.append(skill_in_general(k9_id))

    SAR_graph = []
    NDD_graph = []
    EDD_graph = []

    sar_description = []
    ndd_description = []
    edd_description = []

    ctr = 0
    for array in method_arrays:
        #Check if atleast one of the data has a score
        if method_arrays[ctr][1] == 1 or method_arrays[ctr][2] == 1 or method_arrays[ctr][3] == 1:
            #Save graph to the corresponding skill array
            if method_arrays[ctr][1] == 1:
                SAR_graph.append(method_arrays[ctr][0])
                str = "SAR is recommended because "
                sar_description.append(str + method_arrays[ctr][4])
            if method_arrays[ctr][2] == 1:
                NDD_graph.append(method_arrays[ctr][0])
                str = "NDD is recommended because "
                ndd_description.append(str + method_arrays[ctr][4])
            if method_arrays[ctr][3] == 1:
                EDD_graph.append(method_arrays[ctr][0])
                str = "EDD is recommended because "
                edd_description.append(str + method_arrays[ctr][4])

        ctr += 1

    #Check if skills are supported data, otherwise all of them are recommended
    graphs = ""
    descriptions = ""
    title = ""
    if SAR_graph or NDD_graph or EDD_graph:
        if id == 0:
            if SAR_graph:
                graphs = SAR_graph
                descriptions = sar_description
            else:
                graphs = ["There is no available data to support this skill!"]
            title = "Search and Rescue"
        elif id == 1:
            if NDD_graph:
                graphs = NDD_graph
                descriptions = ndd_description
            else:
                graphs = ["There is no available data to support this skill!"]
            title = "Narcotics Detection Dogs"
        elif id == 2:
            if EDD_graph:
                graphs = EDD_graph
                descriptions = edd_description
            else:
                graphs = ["There is no available data to support this skill!"]
            title = "Explosives Detection Dogs"
    elif not SAR_graph and not NDD_graph and not EDD_graph:
        graphs = ["All skills have no supporting data, pick any of the skills provided"]
        if id == 0:
            title = "Search and Rescue"
        elif id == 1:
            title = "Narcotics Detection Dogs"
        elif id == 2:
            title = "Explosives Detection Dogs"


    context = {'graphs': graphs,
               'descriptions': descriptions,
               'title': title}

    return render(request, 'training/view_graph.html', context)


#TODO Restrict Viable dogs to be trained for those who are 6 months old
#TODO Add additional age for months
#TODO Add Descriptions per graph
#TODO Add additional score for demand and number of skills assigned
def classify_k9_select(request, id):
    form = ClassifySkillForm(request.POST)
    request.session['k9_id'] = id
    data = K9.objects.get(id=id)
    title = data.name
    style = ""


    method_arrays = []


    #skill_demand() TODO Add demand score
    method_arrays.append(skill_count_between_breeds(id))
    method_arrays.append(skill_percentage_between_sexes(id))
    method_arrays.append(skill_count_ratio())

    tree = genealogy(id)
    genes = K9_Genealogy.objects.filter(zero = id)
    if genes:
        method_arrays.append(skills_from_gender(id))
        method_arrays.append(skill_in_general(id))

    SAR_score = 0
    NDD_score = 0
    EDD_score = 0

    #Save skills scores from methods then add all scores
    ctr = 0
    for array in method_arrays:
        SAR_score += method_arrays[ctr][1]
        NDD_score += method_arrays[ctr][2]
        EDD_score += method_arrays[ctr][3]

        ctr += 1


    print("SAR SCORE")
    print(SAR_score)
    print("NDD SCORE")
    print(NDD_score)
    print("EDD SCORE")
    print(EDD_score)

    #Save all aggregated skill scores in one array
    compact_score = []
    compact_score.append(SAR_score)
    compact_score.append(NDD_score)
    compact_score.append(EDD_score)

    recommended = [0, 0, 0]

    #Check which one has the highest score (regardless if all scores are 0)
    ctr = 0
    for x in compact_score:
        if x == max(compact_score):
            recommended[ctr] = 1
        ctr += 1

    #Mark as recommended those skills that are equal to the highest score
    max_score = max(recommended)
    recommended.append(max_score)
    print("RECOMMENDED")
    print(recommended)

    sar_recommended = ""
    ndd_recommended = ""
    edd_recommended = ""

    if recommended[0] == 1:
        sar_recommended = "Recommended!"
    if recommended[1] == 1:
        ndd_recommended = "Recommended!"
    if recommended[2] == 1:
        edd_recommended = "Recommended!"

    edd = Training.objects.filter(k9=data).get(training='EDD')
    ndd = Training.objects.filter(k9=data).get(training='NDD')
    sar = Training.objects.filter(k9=data).get(training='SAR')
    # TODO:
	#if already has capability and on training from other records,
	#previous record training will result to grade 0

    graph = unified_graph()

    if request.method == 'POST':
        print(data.capability)

        if data.capability == 'EDD':
            edd.grade = '0'
            edd.save()
        elif data.capability == 'NDD':
            ndd.grade = '0'
            ndd.save()
        elif data.capability == 'SAR':
            sar.grade = '0'
            sar.save()
        else:
            pass

        if data.training_status == 'On-Training':
            ...
        else:
            data.training_status = "Classified"

        data.training_count = data.training_count+1 
        data.capability = request.POST.get('radio')
        data.save()

        style = "ui green message"
        messages.success(request, 'K9 has been successfully Classified!')

    try:
        parent = K9_Parent.objects.get(offspring=data)
    except K9_Parent.DoesNotExist:
        context = {
            'data': data,
            'title': title,
            'style': style,
            'recommended': recommended,
            'tree': tree,
            'edd': edd,
            'ndd': ndd,
            'sar': sar,
            'sar_recommended': sar_recommended,
            'ndd_recommended': ndd_recommended,
            'edd_recommended': edd_recommended,
            'form': form,
            'graph': graph
        }
    else:
        parent_exist = 1
        context = {
            'data': data,
            'parent': parent,
            'parent_exist': parent_exist,
            'title': title,
            'style': style,
            'recommended': recommended,
            'tree': tree,
            'edd': edd,
            'ndd': ndd,
            'sar': sar,
            'sar_recommended': sar_recommended,
            'ndd_recommended': ndd_recommended,
            'edd_recommended': edd_recommended,
            'form': form,
            'graph': graph
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
            k9.handler = handler
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


def training_records(request):
    data = K9.objects.all()
    context = {
        'title': "Training Records",
        'data': data,
    }
    return render(request, 'training/training_records.html', context)

def training_update_form(request, id):
    data = K9.objects.get(id=id) # get k9
    training = Training.objects.filter(k9=data).get(training=data.capability) # get training record
    form = TrainingUpdateForm(request.POST or None, instance = training)

    if request.method == 'POST':
        #save training status
        if training.stage1_1 == True:
            training.stage1_1 = training.stage1_1
        else:
            training.stage1_1 = bool(request.POST.get('stage1_1'))
        if training.stage1_2 == True:
            training.stage1_2 = training.stage1_2
        else:
            training.stage1_2 = bool(request.POST.get('stage1_2'))
        if training.stage1_3 == True:
            training.stage1_3 = training.stage1_3
        else:
            training.stage1_3 = bool(request.POST.get('stage1_3'))
        if training.stage2_1 == True:
            training.stage2_1 = training.stage2_1
        else:
            training.stage2_1 = bool(request.POST.get('stage2_1'))
        if training.stage2_2 == True:
            training.stage2_2 = training.stage2_2
        else:
            training.stage2_2 = bool(request.POST.get('stage2_2'))
        if training.stage2_3 == True:
            training.stage2_3 = training.stage2_3
        else:
            training.stage2_3 = bool(request.POST.get('stage2_3'))
        if training.stage3_1 == True:
            training.stage3_1 = training.stage3_1
        else:
            training.stage3_1 = bool(request.POST.get('stage3_1'))
        if training.stage3_2 == True:
            training.stage3_2 = training.stage3_2
        else:
            training.stage3_2 = bool(request.POST.get('stage3_2'))
        if training.stage3_3 == True:
            training.stage3_3 = training.stage3_3
        else:
            training.stage3_3 = bool(request.POST.get('stage3_3'))

        training.remarks = request.POST.get('remarks')
        training.grade = request.POST.get('grade')
        training.save()
        data.save()

        stage = "Stage 0"

        if training.stage3_3 == True:
            stage = "Finished Training"
        elif training.stage3_2 == True:
            stage = "Stage 3.2"
        elif training.stage3_1 == True:
            stage= "Stage 3.1"
        elif training.stage2_3 == True:
            stage = "Stage 2.3"
        elif training.stage2_2 == True:
            stage = "Stage 2.2"
        elif training.stage2_1 == True:
            stage = "Stage 2.1"
        elif training.stage1_3 == True:
            stage = "Stage 1.3"
        elif training.stage1_2 == True:
            stage = "Stage 1.2"
        elif training.stage1_1 == True:
            stage = "Stage 1.1"

        training.stage = stage
        training.save()

        if training.stage == "Finished Training":
            data.training_status = "Trained"
        else:
            data.training_status = "On-Training"

        data.training_level = stage
        data.save()
        messages.success(request, 'Training Progress has been successfully Updated!')

        return redirect('training:training_update_form', id = id)
    context = {
        'title': data.name,
        'data': data,
        'form': form,
    }

    if data.capability == 'EDD':
        return render(request, 'training/training_update_edd.html', context)
    elif data.capability == 'NDD':
        return render(request, 'training/training_update_ndd.html', context)
    else:
        return render(request, 'training/training_update_sar.html', context)


#Trained Dog - Assign serial number Form
def serial_number_form(request, id):
    form = SerialNumberForm(request.POST or None)
    style = "ui teal message"
    data = K9.objects.get(id=id) # get k9

    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            data.serial_number ='SN-' + str(data.id) +'-'+str(datetime.datetime.now().year)
            data.microchip = request.POST.get('microchip')
            data.training_status = request.POST.get('dog_type')
            data.save()

            style = "ui green message"
            messages.success(request, 'K9 has been finalized!')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'form': form,
        'title': 'Trained K9 Finalization',
        'texthelp': 'Input Final Details Here',
        'actiontype': 'Submit',
        'style' : style,
    }
    return render (request, 'training/serial_number_form.html', context)

def fail_dog(request, id):
    data = K9.objects.get(id=id) # get k9
    data.training_status = "For-Adoption"
    data.save()
    training = Training.objects.filter(k9=data)

    for training in training:
        training.grade = '0'
        training.save()
    return redirect('training:classify_k9_list')

def training_details(request, id):
    data = K9.objects.get(id=id) # get k9
    edd = Training.objects.filter(k9=data).get(training='EDD') # get training record
    ndd = Training.objects.filter(k9=data).get(training='NDD')
    sar = Training.objects.filter(k9=data).get(training='SAR')

    print(edd.grade)
    context = {
        'title': str(data),
        'data': data,
        'edd':edd,
        'ndd':ndd,
        'sar':sar,
    }
    return render (request, 'training/training_details.html', context)

def adoption_confirmed(request):
    return render (request, 'training/adoption_confirmed.html')




def skill_count_between_breeds(id):
    k9_set = K9.objects.exclude(capability="None")

    breeds = []
    sar_count = []
    ndd_count = []
    edd_count = []

    for k9 in k9_set:
        breeds.append(k9.breed)

    breeds = list(set(breeds))

    print("BREEDS")
    print(breeds)

    for breed in breeds:
        S = K9.objects.filter(capability='SAR', breed=str(breed))
        N = K9.objects.filter(capability='NDD', breed=str(breed))
        E = K9.objects.filter(capability='EDD', breed=str(breed))
        sar_count.append(S.count())
        ndd_count.append(N.count())
        edd_count.append(E.count())


    skill_total = 0
    for count in sar_count:
        skill_total += count
    for count in ndd_count:
        skill_total += count
    for count in edd_count:
        skill_total += count


    SAR = go.Bar(
        x=breeds,
        y=sar_count,
        name="SAR",
    )

    NDD = go.Bar(
        x=breeds,
        y=ndd_count,
        name="NDD",
    )

    EDD = go.Bar(
        x=breeds,
        y=edd_count,
        name="EDD",
    )

    data = [SAR, NDD, EDD]


    layout = go.Layout(
        title="Skill Count of Classified Dogs Categorized by Breed (" + str(skill_total) + " Dogs)",
        xaxis =  {'title': 'Breeds'},
        yaxis =  {'title': 'Skill Count'},
    )

    fig = go.Figure(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    sar = 0
    ndd = 0
    edd = 0

    skill_count = []
    target_k9 = K9.objects.get(id = id)
    for dog in k9_set:
        if dog.capability == "SAR" and dog.breed == target_k9.breed:
            sar += 1
        if dog.capability == "NDD" and dog.breed == target_k9.breed:
            ndd += 1
        if dog.capability == "EDD" and dog.breed == target_k9.breed:
            edd += 1

    skill_count.append(sar)
    skill_count.append(ndd)
    skill_count.append(edd)

    print("SKILL COUNT")
    print(skill_count)

    SAR_score = 0
    NDD_score = 0
    EDD_score = 0

    desc2 = ""
    if max(skill_count) == sar and max(skill_count) != 0:
        SAR_score = 1
        desc2 = "SAR"
    if max(skill_count) == ndd and max(skill_count) != 0:
        NDD_score = 1
        desc2 = "NDD"
    if max(skill_count) == edd and max(skill_count) != 0:
        EDD_score = 1
        desc2 = "EDD"

    desc = str(target_k9.name) + " is a " + str(target_k9.breed) + ". " + str(max(skill_count)) + " out of " + str(max(skill_count)) + " trained dogs of the same breed are "+ str(desc2) + ". " + str(desc2) + " is the most recurring skill among " + target_k9.breed + "s."

    classifier = []
    classifier.append(graph)
    classifier.append(SAR_score)
    classifier.append(NDD_score)
    classifier.append(EDD_score)
    classifier.append(desc)

    return classifier


def skill_percentage_between_sexes(id):
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
        "title": "Skill Count of Classified Dogs Categorized by Gender (" + str(k9_set.count()) + " Dogs)",
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

    k9 = K9.objects.get(id=id)
    k9_gender = k9.sex

    skill_count = []

    if k9_gender == "Male":
        skill_count.append(len(m_sar_count))
        skill_count.append(len(m_ndd_count))
        skill_count.append(len(m_edd_count))
        SAR = skill_count[0]
        NDD = skill_count[1]
        EDD = skill_count[2]
    else:
        skill_count.append(len(f_sar_count))
        skill_count.append(len(f_ndd_count))
        skill_count.append(len(f_edd_count))
        SAR = skill_count[0]
        NDD = skill_count[1]
        EDD = skill_count[2]

    SAR_score = 0
    NDD_score = 0
    EDD_score = 0

    desc2 = ""
    if max(skill_count) == SAR and max(skill_count) != 0:
        SAR_score = 1
        desc2 = "SAR"
    if max(skill_count) == NDD and max(skill_count) != 0:
        NDD_score = 1
        desc2 = "NDD"
    if max(skill_count) == EDD and max(skill_count) != 0:
        EDD_score = 1
        desc2 = "EDD"

    desc = str(k9.name) + " is a " + str(k9_gender) + " dog. " + str(max(skill_count)) + " out of " + str(k9_set.count()) + " " + str(k9_gender) + " dogs are " + str(desc2) +". " + str(desc2) + " is the most recurring skill among trained " +  str(k9_gender) + " dogs."

    graph = opy.plot(fig, auto_open=False, output_type='div')

    classifier = []
    classifier.append(graph)
    classifier.append(SAR_score)
    classifier.append(NDD_score)
    classifier.append(EDD_score)
    classifier.append(desc)

    return classifier

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
        title="Skill Count of Classified Dogs (" + str(k9_set.count()) + " Dogs)",
    )

    fig = go.Figure(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    SAR_score = 0
    NDD_score = 0
    EDD_score = 0

    desc2 = ""
    if k9_set:
        if min(values) == SAR.count():
            SAR_score = 1
            desc2 = "SAR"
        if min(values) == NDD.count():
            NDD_score = 1
            desc2 = "NDD"
        if min(values) == EDD.count():
            EDD_score = 1
            desc2 = "EDD"

    desc = "only " + str(min(values)) + " out of " + str(k9_set.count()) + " K9s are assigned to " + str(desc2) + ". " + str(desc2) + " is currently the skill with the least amount of trained dogs."

    classifier = []
    classifier.append(graph)
    classifier.append(SAR_score)
    classifier.append(NDD_score)
    classifier.append(EDD_score)
    classifier.append(desc)

    return classifier


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
            "title": "Skill Count of Classified Ancestors Categorized by Gender (" + str(k9_set.count()) + " Dogs)",
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

    k9 = K9.objects.get(id= id)
    k9_gender = k9.sex

    skill_count = []


    if k9_gender == "Male":
        skill_count.append(len(m_sar_count))
        skill_count.append(len(m_ndd_count))
        skill_count.append(len(m_edd_count))
        SAR = skill_count[0]
        NDD = skill_count[1]
        EDD = skill_count[2]
    else:
        skill_count.append(len(f_sar_count))
        skill_count.append(len(f_ndd_count))
        skill_count.append(len(f_edd_count))
        SAR = skill_count[0]
        NDD = skill_count[1]
        EDD = skill_count[2]

    SAR_score = 0
    NDD_score = 0
    EDD_score = 0

    desc2 = ""
    if max(skill_count) == SAR and max(skill_count) != 0:
        SAR_score = 1
        desc2 = "SAR"
    if max(skill_count) == NDD and max(skill_count) != 0:
        NDD_score = 1
        desc2 = "NDD"
    if max(skill_count) == EDD and max(skill_count) != 0:
        EDD_score = 1
        desc2 = "EDD"

    desc = str(k9.name) + " is a " + str(k9_gender) + " K9 and " + str(max(skill_count)) + " out of " + str(k9_set.count()) + " " + str(k9_gender) + " ancestors are trained as " + str(desc2) + ". " + str(desc2) + " is the most recurring skill among trained " + str(k9_gender) + " descendants."

    classifier = []
    classifier.append(graph)
    classifier.append(SAR_score)
    classifier.append(NDD_score)
    classifier.append(EDD_score)
    classifier.append(desc)

    return classifier


def skill_in_general(id):
    target_k9 = K9.objects.get(id = id)
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

    k9_set = K9.objects.filter(pk__in=k9_list).exclude(capability="None").filter()


    '''
    unclassified, classified, on-training, trained, for-breeding, for-adoption, for-deployment, deployed, adopted, breeding, sick, recovery, dead, retired
    '''

    SAR = K9.objects.filter(capability="SAR", pk__in=k9_list)
    NDD = K9.objects.filter(capability="NDD", pk__in=k9_list)
    EDD = K9.objects.filter(capability="EDD", pk__in=k9_list)

    labels = ['SAR', 'NDD', 'EDD']
    values = [SAR.count(), NDD.count(), EDD.count()]

    trace = go.Pie(labels=labels, values=values,
                   hoverinfo='label+value', textinfo='percent', )

    data = [trace]

    layout = go.Layout(
        title="Skill Count of Classified Ancestors (" + str(k9_set.count()) + " dogs)",
    )

    fig = go.Figure(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    SAR_score = 0
    NDD_score = 0
    EDD_score = 0

    desc2 = ""
    if max(values) == SAR.count() and max(values) != 0 :
        SAR_score = 1
        desc2 = "SAR"
    if max(values) == NDD.count() and max(values) != 0:
        NDD_score = 1
        desc2 = "NDD"
    if max(values) == EDD.count() and max(values) != 0:
        EDD_score = 1
        desc2 = "EDD"

    desc = str(target_k9.name) + " has " + str(max(values)) + " out of " + str(k9_set.count()) + " ancestors who are trained as " + str(desc2) + ". " + str(desc2) + " is the most recurring skill among descendants."

    classifier = []
    classifier.append(graph)
    classifier.append(SAR_score)
    classifier.append(NDD_score)
    classifier.append(EDD_score)
    classifier.append(desc)

    return classifier


def genealogy(id):

    tree = ""
    general = ""
    gender = ""

    cancel = 0
    #data = K9_Genealogy.objects.filter(zero=k9)
    #data.delete()
    K9_Genealogy.objects.all().delete()

    target = K9.objects.get(id=id)
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
            #general = skill_in_general(target.id)
            #gender = skills_from_gender(target.id)
            #TODO Put other family related graphs here
        else:
            tree = None

    return tree

