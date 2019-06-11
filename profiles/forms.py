from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime
from .models import User, Personal_Info, Education, Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as Auth_User
from deployment.models import Location

class DateInput(forms.DateInput):
    input_type = 'date'

class add_User_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('image','firstname', 'lastname', 'nickname', 'position', 'rank', 'extensionname', 'middlename',
                  'gender', 'birthdate', 'birthplace', 'civilstatus', 'citizenship', 'religion', 'bloodtype',
                  'distinct_feature', 'haircolor', 'eyecolor', 'skincolor', 'height', 'weight',
                  'headsize', 'footsize', 'bodybuild')
        widgets = {
            'birthdate': DateInput()
        }

        def __init__(self, *args, **kwargs):
            super(add_User_form, self).__init__(*args, **kwargs)
            self.fields['extensionname'].required = False
            self.fields['distinct_feature'].required = False
            self.fields['image'].required = False

class add_personal_form(forms.ModelForm):
    class Meta:
        model = Personal_Info
        fields = ('mobile_number', 'tel_number', 'street',
                  'barangay', 'city', 'province', 'mother_name', 'mother_birthdate',
                  'father_name', 'father_birthdate', 'tin', 'philhealth')
        widgets = {
            'father_birthdate': DateInput(),
            'mother_birthdate': DateInput()
        }

class add_education_form(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('primary_education', 'secondary_education', 'tertiary_education', 'pe_schoolyear', 'se_schoolyear',
                  'te_schoolyear', 'pe_degree', 'se_degree', 'te_degree')

class add_user_account(UserCreationForm):
   
    class Meta:
        model = Auth_User
        fields = ('email', 'password1')
