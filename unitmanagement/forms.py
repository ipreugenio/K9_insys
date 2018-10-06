from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime
from django.forms import formset_factory, inlineformset_factory

from unitmanagement.models import PhysicalExam , Health, HealthMedicine
from planningandacquiring.models import K9
from inventory.models import Medicine
class DateInput(forms.DateInput):
    input_type = 'date'

class PhysicalExamForm(forms.ModelForm):
    EXAMSTATUS = (
        ('Normal', 'Normal'),
        ('Abnormal', 'Abnormal'),
        ('Not Examined', 'Not Examined'),
    )
    dog = forms.ModelChoiceField(queryset = K9.objects.all())
    general_appearance = forms.CharField(label = 'general_appearance', widget = forms.Select(choices=EXAMSTATUS))
    integumentary = forms.CharField(label = 'integumentary', widget = forms.Select(choices=EXAMSTATUS))
    musculo_skeletal = forms.CharField(label = 'musculo_skeletal', widget = forms.Select(choices=EXAMSTATUS))
    respiratory = forms.CharField(label = 'respiratory', widget = forms.Select(choices=EXAMSTATUS))
    genito_urinary = forms.CharField(label = 'genito_urinary', widget = forms.Select(choices=EXAMSTATUS))
    nervous = forms.CharField(label = 'nervous', widget = forms.Select(choices=EXAMSTATUS))
    circulatory = forms.CharField(label = 'circulatory', widget = forms.Select(choices=EXAMSTATUS))
    digestive = forms.CharField(label = 'digestive', widget = forms.Select(choices=EXAMSTATUS))
    mucous_membrances = forms.CharField(label = 'mucous_membrances', widget = forms.Select(choices=EXAMSTATUS))
    lymph_nodes = forms.CharField(label = 'lymph_nodes', widget = forms.Select(choices=EXAMSTATUS))
    eyes = forms.CharField(label = 'eyes', widget = forms.Select(choices=EXAMSTATUS))
    ears = forms.CharField(label = 'ears', widget = forms.Select(choices=EXAMSTATUS))
    remarks = forms.CharField(label = 'remarks', widget = forms.Textarea(attrs={'rows':'4'}))
    
    class Meta:
        model = PhysicalExam
        fields = ('dog', 'cage_number', 'general_appearance', 'integumentary',
        'musculo_skeletal', 'respiratory', 'genito_urinary', 'nervous', 'circulatory', 'digestive',
        'mucous_membrances', 'lymph_nodes', 'eyes', 'ears', 'remarks')

    def __init__(self, *args, **kwargs):
        super(PhysicalExamForm, self).__init__(*args, **kwargs)
        self.fields['cage_number'].required = False
        self.fields['remarks'].required = False

class HealthForm(forms.ModelForm):

    dog = forms.ModelChoiceField(queryset = K9.objects.all())
    problem = forms.CharField(label = 'problem', widget = forms.Textarea(attrs={'rows':'3'}))
    treatment = forms.CharField(label = 'treatment', widget = forms.Textarea(attrs={'rows':'3'}))

    class Meta:
        model = Health
        fields = ('dog','problem', 'treatment')

class HealthMedicineForm(forms.ModelForm):

    class Meta:
        model = HealthMedicine
        fields = ('health','medicine', 'quantity', 'dosage')

    health = forms.ModelChoiceField(queryset = Health.objects.all())
    medicine = forms.ModelChoiceField(queryset = Medicine.objects.all())
    
HealthMedicineFormSet = inlineformset_factory(Health, HealthMedicine, form=HealthMedicineForm, extra=1)