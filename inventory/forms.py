from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime

from inventory.models import Medicine, Food, Miscellaneous, Medicine_Inventory
from inventory.models import DamagedEquipemnt

class DateInput(forms.DateInput):
    input_type = 'date'

#Medicine
class MedicineForm(forms.ModelForm):

    UOM = (
        ('mg', 'mg'),
        ('mL', 'mL'),
    )

    uom = forms.CharField(max_length=10, label = 'uom', widget = forms.Select(choices=UOM))
    description = forms.CharField(widget = forms.Textarea(attrs={'rows':'3'}))
    dose = forms.DecimalField(widget = forms.NumberInput())

    class Meta:
        model = Medicine
        fields = ('medicine', 'dose', 'uom', 'description', 'price', 'med_type')

    def __init__(self, *args, **kwargs):
        super(MedicineForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['uom'].required = False 

class MedicineCountForm(forms.ModelForm):
    class Meta:
        model = Medicine_Inventory
        fields = ('medicine', 'quantity')
    
    def __init__(self, *args, **kwargs):
        super(MedicineCountForm, self).__init__(*args, **kwargs)
        self.fields['medicine'].required = False
        
#Food
class FoodForm(forms.ModelForm):

    FOODTYPE = (
        ('Adult Dog Food', 'Adult Dog Food'),
        ('Puppy Dog Food', 'Puppy Dog Food'),
        ('Milk', 'Milk'),
    )

    foodtype = forms.CharField(max_length=100, label = 'foodtype', widget = forms.Select(choices=FOODTYPE))
    description = forms.CharField(widget = forms.Textarea(attrs={'rows':'3'}))

    class Meta:
        model = Food
        fields = ('food', 'foodtype', 'description', 'price')

    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False

class FoodCountForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('food', 'quantity')

    def __init__(self, *args, **kwargs):
        super(FoodCountForm, self).__init__(*args, **kwargs)
        self.fields['food'].required = False

#Miscellaneous
class MiscellaneousForm(forms.ModelForm):

    UOM = (
        ('pc', 'pc'),
        ('roll', 'roll'),
        ('can', 'can'),
        ('bottle', 'bottle'),
        ('tube', 'tube'),
        ('box', 'box'),
    )

    TYPE = (
        ('Equipment', 'Equipment'),
        ('Vet Supply', 'Vet Supply'),

    )

    description = forms.CharField(widget = forms.Textarea(attrs={'rows':'3'}))
    uom = forms.CharField(max_length=10, label = 'uom', widget = forms.Select(choices=UOM))
    misc_type = forms.CharField(max_length=10, label = 'misc_type', widget = forms.Select(choices=TYPE))

    class Meta:
        model = Miscellaneous
        fields = ( 'miscellaneous', 'description', 'uom', 'price', 'misc_type')

    def __init__(self, *args, **kwargs):
        super(MiscellaneousForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False

class MiscellaneousCountForm(forms.ModelForm):
    class Meta:
        model = Miscellaneous
        fields = ('miscellaneous', 'quantity')

    def __init__(self, *args, **kwargs):
        super(MiscellaneousCountForm, self).__init__(*args, **kwargs)
        self.fields['miscellaneous'].required = False

class DamagedEquipmentForm(forms.ModelForm):
    CONCERN = (
        ('Broken', 'Broken'),
        ('Lost', 'Lost'),
        ('Stolen', 'Stolen'),
    )

    concern = forms.CharField(max_length=10, label = 'concern', widget = forms.Select(choices=CONCERN))
    inventory = forms.ModelChoiceField(queryset = Miscellaneous.objects.filter(misc_type="Equipment").order_by('miscellaneous'))

    class Meta:
        model = DamagedEquipemnt
        fields = ('inventory', 'quantity', 'concern')

class DateForm(forms.Form):
    from_date = forms.DateField( widget=DateInput())
    to_date = forms.DateField(widget=DateInput())
