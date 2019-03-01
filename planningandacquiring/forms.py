from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime

from .models import K9, K9_Past_Owner, K9_Parent, Date, Budget_allocation, Budget_medicine,Budget_food,Budget_equipment,Budget_vaccine,Budget_vet_supply

import datetime
import re

from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe


from .models import K9, K9_Past_Owner, K9_Parent, Date, Dog_Breed
from django.forms.widgets import CheckboxSelectMultiple


# __all__ = ('MonthYearWidget',)
#
# RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')
#
# class MonthYearWidget(Widget):
#     """
#     A Widget that splits date input into two <select> boxes for month and year,
#     with 'day' defaulting to the first of the month.
#
#     Based on SelectDateWidget, in
#
#     django/trunk/django/forms/extras/widgets.py
#
#
#     """
#     none_value = (0, '---')
#     month_field = '%s_month'
#     year_field = '%s_year'
#
#     def __init__(self, attrs=None, years=None, required=True):
#         # years is an optional list/tuple of years to use in the "year" select box.
#         self.attrs = attrs or {}
#         self.required = required
#         if years:
#             self.years = years
#         else:
#             this_year = datetime.date.today().year
#             self.years = range(this_year, this_year+10)
#
#     def render(self, name, value, attrs=None):
#         try:
#             year_val, month_val = value.year, value.month
#         except AttributeError:
#             year_val = month_val = None
#             if isinstance(value, basestring):
#                 match = RE_DATE.match(value)
#                 if match:
#                     year_val, month_val, day_val = [int(v) for v in match.groups()]
#
#         output = []
#
#         if 'id' in self.attrs:
#             id_ = self.attrs['id']
#         else:
#             id_ = 'id_%s' % name
#
#         month_choices = MONTHS.items()
#         if not (self.required and value):
#             month_choices.append(self.none_value)
#         month_choices.sort()
#         local_attrs = self.build_attrs(id=self.month_field % id_)
#         s = Select(choices=month_choices)
#         select_html = s.render(self.month_field % name, month_val, local_attrs)
#         output.append(select_html)
#
#         year_choices = [(i, i) for i in self.years]
#         if not (self.required and value):
#             year_choices.insert(0, self.none_value)
#         local_attrs['id'] = self.year_field % id_
#         s = Select(choices=year_choices)
#         select_html = s.render(self.year_field % name, year_val, local_attrs)
#         output.append(select_html)
#
#         return mark_safe(u'\n'.join(output))
#
#     def id_for_label(self, id_):
#         return '%s_month' % id_
#     id_for_label = classmethod(id_for_label)
#
#     def value_from_datadict(self, data, files, name):
#         y = data.get(self.year_field % name)
#         m = data.get(self.month_field % name)
#         if y == m == "0":
#             return None
#         if y and m:
#             return '%s-%s-%s' % (y, m, 1)
#         return data.get(name, None)



class DateInput(forms.DateInput):
    input_type = 'date'

class ReportDateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = ('date_from', 'date_to')
        widgets = {
            'date_from': DateInput(),
            'date_to': DateInput()
        }

class add_unaffiliated_K9_form(forms.ModelForm):
    class Meta:
        model = K9
        fields = ('name', 'breed', 'sex', 'color', 'birth_date')
        widgets = {
            'birth_date': DateInput(),
        }

class add_donated_K9_form(forms.ModelForm):
    class Meta:
        model = K9
        fields = ('name', 'breed', 'sex', 'color', 'birth_date')
        widgets = {
            'birth_date': DateInput(),
        }

class add_donator_form(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':'2', 'style':'resize:none;'}))

    class Meta:
        model = K9_Past_Owner
        fields = ('first_name', 'middle_name', 'last_name', 'sex', 'birth_date','email', 'contact_no', 'address')
        widgets = {
            'birth_date': DateInput(),
        }

class add_K9_parents_form(forms.Form):
    try:
        females = K9.objects.filter(sex = "Female").filter(training_status = "For-Breeding").filter(age__gte = 1)
        males = K9.objects.filter(sex = "Male").filter(training_status = "For-Breeding").filter(age__gte = 1)

        mother_list = []
        father_list = []

        for female in females:
            data = (female.id, female.name)
            mother_list.append(data)

        for male in males:
            data  = (male.id, male.name)
            father_list.append(data)

    except:
        mother_list = []
        father_list = []

    mother = forms.ChoiceField(choices=mother_list,
                              widget=forms.RadioSelect)
    father = forms.ChoiceField(choices=father_list,
                              widget=forms.RadioSelect)


    def __init__(self, *args, **kwargs):
        super(add_K9_parents_form, self).__init__(*args, **kwargs)

        females = K9.objects.filter(sex="Female").filter(training_status = "For-Breeding").filter(age__gte = 1)
        males = K9.objects.filter(sex="Male").filter(training_status = "For-Breeding").filter(age__gte = 1)

        mother_list = []
        father_list = []

        for female in females:
            data = (female.id, female.name)
            mother_list.append(data)

        for male in males:
            data = (male.id, male.name)
            father_list.append(data)

        self.fields['mother'].choices = mother_list
        self.fields['father'].choices = father_list


class add_offspring_K9_form(forms.ModelForm):
    class Meta:
        model = K9
        fields = ('name', 'sex', 'color', 'birth_date')
        widgets = {
            'birth_date': DateInput(),
        }

class select_breeder(forms.Form):
    k9 = forms.ModelChoiceField(queryset=K9.objects.filter(training_status = 'For-Breeding'))


#class select_date(forms.Form):

class budget_food(forms.Form):
    # class Meta:
    #     model = Budget_food
    #     fields = ('food', 'quantity', 'price', 'total', 'budget_allocation')
    budget_puppy = forms.IntegerField()
    budget_adult = forms.IntegerField()

class budget_equipment(forms.Form):
    # class Meta:
    #     model = Budget_equipment
    #     fields = ('equipment', 'quantity', 'price', 'total', 'budget_allocation')
    budget = forms.IntegerField()

class budget_medicine(forms.Form):
    # class Meta:
    #     model = Budget_medicine
    #     fields = ('medicine', 'quantity', 'price', 'total', 'budget_allocation')
    budget = forms.IntegerField()

class budget_vaccine(forms.Form):
    # class Meta:
    #     model = Budget_vaccine
    #     fields = ('vaccine', 'quantity', 'price', 'total', 'budget_allocation')
    budget = forms.IntegerField()

class budget_vet_supply(forms.Form):
    # class Meta:
    #     model = Budget_vet_supply
    #     fields = ('vet_supply', 'quantity', 'price', 'total', 'budget_allocation')
    budget = forms.IntegerField()

class budget_date(forms.Form):
    #date = forms.DateField()
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

class add_breed_form(forms.ModelForm):
    TEMPERAMENT = (
        ('Kind', 'Kind'),
        ('Outgoing', 'Outgoing'),
        ('Agile', 'Agile'),
        ('Intelligent', 'Intelligent'),
        ('Trusting', 'Trusting'),
        ('Even Tempered', 'Even Tempered'),
        ('Gentle', 'Gentle'),
        ('Reliable', 'Reliable'),
        ('Confident', 'Confident'),
        ('Friendly', 'Friendly'),
        ('Loyal', 'Loyal'),
        ('Alert', 'Alert'),
        ('Curious', 'Curious'),
        ('Watchful', 'Watchful'),
        ('Courageous', 'Courageous'),
        ('Affectionate', 'Affectionate'),
        ('Trainable', 'Trainable'),
        ('Protective', 'Protective'),
        ('Active', 'Active'),
        ('Obedient', 'Obedient'),
        ('Stubborn', 'Stubborn'),
        ('Athletic', 'Athletic'),
        ('Vocal', 'Vocal'),
        ('Energetic', 'Energetic')
    )

    COLORS = (
        ('Black', 'Black'),
        ('Chocolate', 'Chocolate'),
        ('Yellow', 'Yellow'),
        ('Dark Golden', 'Dark Golden'),
        ('Light Golden', 'Light Golden'),
        ('Cream', 'Cream'),
        ('Golden', 'Golden'),
        ('Brindle', 'Brindle'),
        ('Silver Brindle', 'Silver Brindle'),
        ('Gold Brindle', 'Gold Brindle'),
        ('Salt and Pepper', 'Salt and Pepper'),
        ('Gray Brindle', 'Gray Brindle'),
        ('Blue and Gray', 'Blue and Gray'),
        ('Tan', 'Tan'),
        ('Black-Tipped Fawn', 'Black-Tipped Fawn'),
        ('Mahogany', 'Mahogany'),
        ('White', 'White'),
        ('Black and White', 'Black and White'),
        ('White and Tan', 'White and Tan')
    )

    temperament = forms.MultipleChoiceField(required=False,
                                     widget=forms.CheckboxSelectMultiple, choices=TEMPERAMENT)
    colors = forms.MultipleChoiceField(required=False,
                                     widget=forms.CheckboxSelectMultiple, choices=COLORS)

    class Meta:
        model = Dog_Breed
        fields = ('breed', 'life_span', 'temperament', 'colors', 'weight', 'male_height', 'female_height', 'skill_recommendation')



