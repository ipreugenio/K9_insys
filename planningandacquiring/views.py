from django.shortcuts import render
from .forms import add_K9_form, add_donator_form
from .models import K9, K9_Past_Owner, K9_Donated
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
# Create your views here.

# Create your views here.

def index(request):
    return render (request, 'planningandacquiring/index.html')

#Form format
def add_donated_K9(request):
    form = add_K9_form(request.POST)
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

    return render(request, 'planningandacquiring/add_K9.html', context)

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
            'form': add_K9_form,
        }
        return render(request, 'planningandacquiring/add_K9.html', context)

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
    context = {
        'Title': 'K9 Details',
        'k9' : k9
    }

    return render(request, 'planningandacquiring/K9_detail.html', context)

'''
def delete_K9(request, id):
    k9 = K9.objects.get(id=id)
'''