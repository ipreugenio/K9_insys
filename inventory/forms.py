from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime

from inventory.models import Medicine, Food, Equipment

class DateInput(forms.DateInput):
    input_type = 'date'


#Medicine
class MedicineForm(forms.ModelForm):
    
    MASS = (
        ('mg', 'mg'),
        ('mL', 'mL'),
    )
    
    mass = forms.CharField(max_length=10, label = 'mass', widget = forms.Select(choices=MASS))
    description = forms.CharField(widget = forms.Textarea(attrs={'rows':'3'}))
    dose = forms.DecimalField(widget = forms.NumberInput())

    class Meta:
        model = Medicine
        fields = ('medicine', 'dose', 'mass', 'description')

    def __init__(self, *args, **kwargs):
        super(MedicineForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
       

#Food
class FoodForm(forms.ModelForm):
    
    FOODTYPE = (
        ('Adult Dog Food', 'Adult Dog Food'),
        ('Puppy Dog Food', 'Puppy Dog Food'),
        ('Both', 'Both'),
    )

    foodtype = forms.CharField(max_length=100, label = 'foodtype', widget = forms.Select(choices=FOODTYPE))
    description = forms.CharField(widget = forms.Textarea(attrs={'rows':'3'}))

    class Meta:
        model = Food
        fields = ('food', 'foodtype', 'description')

    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False

#Equipment
class EquipmentForm(forms.ModelForm):
    
    description = forms.CharField(widget = forms.Textarea(attrs={'rows':'3'}))
    
    class Meta:
        model = Equipment
        fields = ( 'equipment', 'description')

    def __init__(self, *args, **kwargs):
        super(EquipmentForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
    


