from django.shortcuts import render
from .forms import add_donated_K9_form, add_donator_form, add_K9_parents_form, add_offspring_K9_form
from .models import K9, K9_Past_Owner, K9_Donated, K9_Parent
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

# Create your views here.

def index(request):
    return render (request, 'planningandacquiring/index.html')

#Form format
def add_donated_K9(request):
    form = add_donated_K9_form(request.POST)
    style = "ui teal message"
    if request.method == 'POST':
        if form.is_valid():
            k9 = form.save()
            k9.source = "Donation"
            k9.save()

            request.session['k9_id'] = k9.id
            return HttpResponseRedirect('add_donator_form/')


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


def confirm_donation(request):

    k9_id = request.session['k9_id']
    donator_id = request.session['donator_id']

    k9= K9.objects.get(id = k9_id)
    donator = K9_Past_Owner.objects.get(id = donator_id)

    context = {
        'Title': "Receive Donated K9",
        'k9': k9,
        'donator': donator
    }

    return render(request, 'planningandacquiring/confirm_K9_donation.html', context)

def donation_confirmed(request):
    k9_id = request.session['k9_id']
    donator_id = request.session['donator_id']

    k9 = K9.objects.get(id=k9_id)
    donator = K9_Past_Owner.objects.get(id=donator_id)

    if 'ok' in request.POST:
        k9_donated = K9_Donated(k9 = k9, owner = donator)
        k9_donated.save()
        return render(request, 'planningandacquiring/donation_confirmed.html')
    else:
        k9.delete()
        donator.delete()
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
    context = {
        'Title' : 'K9 List',
        'k9' : k9
    }


    return render(request, 'planningandacquiring/K9_list.html', context)

#Detailview format
def K9_detailview(request, id):
    k9 = K9.objects.get(id = id)
    parent = K9_Parent.objects.get(offspring = k9)
    context = {
        'Title': 'K9 Details',
        'k9' : k9,
        'parent': parent
    }
    # TODO Add K9 parents to detail view

    return render(request, 'planningandacquiring/K9_detail.html', context)

'''
def delete_K9(request, id):
    k9 = K9.objects.get(id=id)
'''