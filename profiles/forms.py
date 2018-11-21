from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime
from .models import User, Personal_Info, Education, Account
from deployment.models import Location

class DateInput(forms.DateInput):
    input_type = 'date'

class add_User_form(forms.ModelForm):
    RANK = (
        ('MCPO', 'MCPO'),
        ('SCPO', 'SCPO'),
        ('CPO', 'CPO'),
        ('PO1', 'PO1'),
        ('PO2', 'PO2'),
        ('PO3', 'PO3'),
        ('SN1/SW1', 'SN1/SW1'),
        ('SN2/SW2', 'SN2/SW2'),
        ('ASN/ASW', 'ASN/ASW'),
        ('CCGM', 'CCGM'),
        ('ADMIRAL', 'ADMIRAL'),
        ('VICE ADMIRAL', 'VICE ADMIRAL'),
        ('REAR ADMIRAL', 'REAR ADMIRAL'),
        ('COMMO', 'COMMO'),
        ('CAPT', 'CAPT'),
        ('CDR', 'CDR'),
        ('LCDR', 'LCDR'),
        ('LT', 'LT'),
        ('LTJG', 'LTJG'),
        ('ENS', 'ENS'),
        ('P/ENS', 'P/ENS')
    )

    RELIGION = (
        ('Roman Catholic','Roman Catholic'),
        ('Christianity','Christianity'),
        ('Islam','Islam'),
        ('Iglesia ni Cristo','Iglesia ni Cristo'),
        ('Buddhists','Buddhists'),
    )
    CITIZENSHIP = (
        ('FILIPINO','FILIPINO'),
    )
    rank = forms.CharField(max_length=50, label='rank', widget=forms.Select(choices=RANK))
    religion = forms.CharField(max_length=50, label='religion', widget=forms.Select(choices=RELIGION))
    citizenship = forms.CharField(max_length=50, label='religion', widget=forms.Select(choices=CITIZENSHIP))

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'nickname', 'position', 'rank', 'extensionname', 'middlename',
                  'gender', 'birthdate', 'birthplace', 'civilstatus', 'citizenship', 'religion', 'bloodtype',
                  'distinct_feature', 'haircolor', 'eyecolor', 'skincolor', 'height', 'weight',
                  'headsize', 'footsize', 'bodybuild')
        widgets = {
            'birthdate': DateInput()
        }

        def __init__(self, *args, **kwargs):
            super(add_User_form, self).__init__(*args, **kwargs)
            self.fields['extensionname'].required = False

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

class add_user_account(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email_address', 'password')

        widgets = {
            'password': forms.PasswordInput(),
        }
