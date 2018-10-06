from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages

from planningandacquiring.models import K9
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
        messages.success(request, 'K9 has been successfully Classied!')

    context = {
        'title': data.name,
        'data': data,
    }
    return render (request, 'training/classify_k9_select.html', context)
    
def training_records(request):
    return render (request, 'training/training_records.html')