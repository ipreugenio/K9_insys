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
  
    class Meta:
        model = Medicine
        fields = ( 'medicine', 'dose', 'mass')


#Food
class FoodForm(forms.ModelForm):
    
   FOODTYPE = (
        ('Adult Dog Food', 'Adult Dog Food'),
        ('Puppy Dog Food', 'Puppy Dog Food'),
    )

    foodtype = forms.CharField(max_length=10, label = 'foodtype', widget = forms.Select(choices=FOODTYPE))
  
    class Meta:
        model = Food
        fields = ( 'food', 'foodtype')

#Equipment
class EquipmentForm(forms.ModelForm):
    
    class Meta:
        model = Equipment
        fields = ( 'equipment', 'description', 'quantity')
    


