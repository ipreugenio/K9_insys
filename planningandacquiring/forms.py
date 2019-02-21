from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime
from .models import K9, K9_Past_Owner, K9_Parent, Date, Dog_Breed
from django.forms.widgets import CheckboxSelectMultiple

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


