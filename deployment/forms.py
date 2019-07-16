from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from datetime import date, datetime
from django.core.validators import validate_integer
from django.forms import fields

from deployment.models import Area, Location, Team_Assignment, Team_Dog_Deployed, Dog_Request, Incidents, Daily_Refresher
from planningandacquiring.models import K9
from profiles.models import Account, User
from django.contrib.sessions.models import Session

from django.contrib.gis import forms as geoforms

import datetime
import re
from six import string_types

from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe

class DateInput(forms.DateInput):
    input_type = 'date'

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ('name',)

class LocationForm(forms.ModelForm):
    CITY = (
        ('Alaminos', 'Alaminos'),
        ('Angeles', 'Angeles'),
        ('Antipolo', 'Antipolo'),
        ('Bacolod', 'Bacolod'),
        ('Bacoor', 'Bacoor'),
        ('Bago', 'Bago'),
        ('Baguio', 'Baguio'),
        ('Bais', 'Bais'),
        ('Balanga', 'Balanga'),
        ('Batac', 'Batac'),
        ('Batangas', 'Batangas'),
        ('Bayawan', 'Bayawan'),
        ('Baybay', 'Baybay'),
        ('Bayugan', 'Bayugan'),
        ('Biñan', 'Biñan'),
        ('Bislig', 'Bislig'),
        ('Bogo', 'Bogo'),
        ('Borongan', 'Borongan'),
        ('Butuan', 'Butuan'),
        ('Cabadbaran', 'Cabadbaran'),
        ('Cabanatuan', 'Cabanatuan'),
        ('Cabuyao', 'Cabuyao'),
        ('Cadiz', 'Cadiz'),
        ('Cagayan de Oro', 'Cagayan de Oro'),
        ('Calamba', 'Calamba'),
        ('Calapan', 'Calapan'),
        ('Calbayog', 'Calbayog'),
        ('Caloocan', 'Caloocan'),
        ('Candon', 'Candon'),
        ('Canlaon', 'Canlaon'),
        ('Carcar', 'Carcar'),
        ('Catbalogan', 'Catbalogan'),
        ('Cauayan', 'Cauayan'),
        ('Cavite', 'Cavite'),
        ('Cebu', 'Cebu'),
        ('Cotabato', 'Cotabato'),
        ('Dagupan', 'Dagupan'),
        ('Danao', 'Danao'),
        ('Dapitan', 'Dapitan'),
        ('Dasmariñas', 'Dasmariñas'),
        ('Davao', 'Davao'),
        ('Digos', 'Digos'),
        ('Dipolog', 'Dipolog'),
        ('Dumaguete', 'Dumaguete'),
        ('El Salvador', 'El Salvador'),
        ('Escalante', 'Escalante'),
        ('Gapan', 'Gapan'),
        ('General Santos', 'General Santos'),
        ('General Trias', 'General Trias'),
        ('Gingoog', 'Gingoog'),
        ('Guihulngan', 'Guihulngan'),
        ('Himamaylan', 'Himamaylan'),
        ('Ilagan', 'Ilagan'),
        ('Iligan', 'Iligan'),
        ('Iloilo', 'Iloilo'),
        ('Imus', 'Imus'),
        ('Iriga', 'Iriga'),
        ('Isabela', 'Isabela'),
        ('Kabankalan', 'Kabankalan'),
        ('Kidapawan', 'Kidapawan'),
        ('Koronadal', 'Koronadal'),
        ('La Carlota', 'La Carlota'),
        ('Lamitan', 'Lamitan'),
        ('Laoag', 'Laoag'),
        ('Lapu‑Lapu', 'Lapu‑Lapu'),
        ('Las Piñas', 'Las Piñas'),
        ('Legazpi', 'Legazpi'),
        ('Ligao', 'Ligao'),
        ('Lipa', 'Lipa'),
        ('Lucena', 'Lucena'),
        ('Maasin', 'Maasin'),
        ('Mabalacat', 'Mabalacat'),
        ('Makati', 'Makati'),
        ('Malabon', 'Malabon'),
        ('Malaybalay', 'Malaybalay'),
        ('Malolos', 'Malolos'),
        ('Mandaluyong', 'Mandaluyong'),
        ('Mandaue', 'Mandaue'),
        ('Manila', 'Manila'),
        ('Marawi', 'Marawi'),
        ('Marikina', 'Marikina'),
        ('Masbate', 'Masbate'),
        ('Mati', 'Mati'),
        ('Meycauayan', 'Meycauayan'),
        ('Muñoz', 'Muñoz'),
        ('Muntinlupa', 'Muntinlupa'),
        ('Naga - Camarines Sur', 'Naga - Camarines Sur'),
        ('Naga - Cebu', 'Naga - Cebu'),
        ('Navotas', 'Navotas'),
        ('Olongapo', 'Olongapo'),
        ('Ormoc', 'Ormoc'),
        ('Oroquieta', 'Oroquieta'),
        ('Ozamiz', 'Ozamiz'),
        ('Pagadian', 'Pagadian'),
        ('Palayan', 'Palayan'),
        ('Panabo', 'Panabo'),
        ('Parañaque', 'Parañaque'),
        ('Pasay', 'Pasay'),
        ('Pasig', 'Pasig'),
        ('Passi', 'Passi'),
        ('Puerto Princesa', 'Puerto Princesa'),
        ('Quezon', 'Quezon'),
        ('Roxas', 'Roxas'),
        ('Sagay', 'Sagay'),
        ('Samal', 'Samal'),
        ('San Carlos - Negros Occidental', 'San Carlos - Negros Occidental'),
        ('San Carlos - Pangasinan', 'San Carlos - Pangasinan'),
        ('San Fernando - La Union', 'San Fernando - La Union'),
        ('San Fernando - Pampanga', 'San Fernando - Pampanga'),
        ('San Jose', 'San Jose'),
        ('San Jose del Monte', 'San Jose del Monte'),
        ('San Juan', 'San Juan'),
        ('San Pablo', 'San Pablo'),
        ('San Pedro', 'San Pedro'),
        ('Santa Rosa', 'Santa Rosa'),
        ('Santiago', 'Santiago'),
        ('Silay', 'Silay'),
        ('Sipalay', 'Sipalay'),
        ('Sorsogon', 'Sorsogon'),
        ('Surigao', 'Surigao'),
        ('Tabaco', 'Tabaco'),
        ('Tabuk', 'Tabuk'),
        ('Tacloban', 'Tacloban'),
        ('Tacurong', 'Tacurong'),
        ('Tagaytay', 'Tagaytay'),
        ('Tagbilaran', 'Tagbilaran'),
        ('Taguig', 'Taguig'),
        ('Tagum', 'Tagum'),
        ('Talisay - Cebu', 'Talisay - Cebu'),
        ('Talisay - Negros Occidental', 'Talisay - Negros Occidental'),
        ('Tanauan', 'Tanauan'),
        ('Tandag', 'Tandag'),
        ('Tangub', 'Tangub'),
        ('Tanjay', 'Tanjay'),
        ('Tarlac', 'Tarlac'),
        ('Tayabas', 'Tayabas'),
        ('Toledo', 'Toledo'),
        ('Trece Martires', 'Trece Martires'),
        ('Tuguegarao', 'Tuguegarao'),
        ('Urdaneta', 'Urdaneta'),
        ('Valencia', 'Valencia'),
        ('Valenzuela', 'Valenzuela'),
        ('Victorias', 'Victorias'),
        ('Vigan', 'Vigan'),
        ('Zamboanga', 'Zamboanga'),
    )
    city = forms.CharField(max_length=50, label = 'city', widget = forms.Select(choices=CITY))
    place = forms.CharField(widget = forms.Textarea(attrs={'rows':'3', 'style':'resize:none;'}))
    class Meta:
        model = Location
        fields = ('area', 'city', 'place')

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['place'].widget.attrs['readonly'] = 'readonly'
        self.fields['place'].widget.attrs['placeholder'] = 'Please search for the location' 

class AssignTeamForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset = Location.objects.filter(status='unassigned'))
    team_leader = forms.ModelChoiceField(queryset = User.objects.filter(position='Team Leader').filter(assigned=False))

    class Meta:
        model = Team_Assignment
        fields = ('location', 'team_leader', 'team', 'EDD_demand', 'NDD_demand', 'SAR_demand')
    
    def __init__(self, *args, **kwargs):
        super(AssignTeamForm, self).__init__(*args, **kwargs)
        self.fields['team_leader'].queryset = User.objects.filter(position='Team Leader').filter(assigned=False)

class EditTeamForm(forms.ModelForm):
    class Meta:
        model = Team_Assignment
        fields = ('team', 'EDD_demand', 'NDD_demand', 'SAR_demand')

class RequestForm(forms.ModelForm):
    class Meta:
        model = Dog_Request
        fields = ('requester', 'location', 'email_address', 'phone_number', 'area', 'EDD_needed',
                  'NDD_needed', 'SAR_needed', 'start_date', 'end_date', 'event_name', 'event_type', 'remarks')

        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }
    
    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget.attrs['readonly'] = 'readonly'
        self.fields['location'].widget.attrs['placeholder'] = 'Please search for the location' 
        self.fields['remarks'].required = False

    def validate_date(self):
        date_start = self.cleaned_data['start_date']
        date_end = self.cleaned_data['end_date']

        if date_start > date_end:
            raise forms.ValidationError("Start and End dates are invalid! (Start Date must be < the End Date)")

        if date_start < date.today():
            raise forms.ValidationError("Start Date must be a future date!")


    def clean_phone_number(self):
        cd = self.cleaned_data['phone_number']
        regex = re.compile('[^0-9]')
        # First parameter is the replacement, second parameter is your input string

        return regex.sub('', cd)


class IncidentForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset = Location.objects.none(), empty_label=None)
    class Meta:
        model = Incidents
        fields = '__all__'

        widgets = {
            'date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(IncidentForm, self).__init__(*args, **kwargs)

        #self.fields['user'].intial = current_user

class DateForm(forms.Form):
    from_date = forms.DateField( widget=DateInput())
    to_date = forms.DateField(widget=DateInput())

        #self.fields['user'].intial = current_user

class GeoSearch(forms.Form):
    search = forms.CharField()

class GeoForm(geoforms.Form):
    point = geoforms.PointField(widget= geoforms.OSMWidget(attrs={'default_lon' : 120.993173,'default_lat' : 14.564752,
                                                            'default_zoom': 18, 'display_raw': False, 'map_width': 470, 'map_height': 500}))
    # 'map_srid': 900913 Gmaps srid (geographic) current is projected
    # 120.993173 lon, 14.564752 lat,  DLSU default coordinates
    # 13468861.763567935675383 lon, 1639088.708640566794202 lat,  DLSU default coordinates
    # 13476918.53413876 lon, 1632299.5848436863 lat, PCGK9 Taguig Coordinates (2D Plane)

    def __init__(self, *args, **kwargs):

        try:
            lat  = kwargs.pop("lat", None)
            lng = kwargs.pop("lng", None)
        except:
            pass

        try:
            width = kwargs.pop("width", None)
        except:
            pass

        super(GeoForm, self).__init__(*args, **kwargs)
        if lat and lng:
            self.fields['point'].widget.attrs['default_lat'] = lat
            self.fields['point'].widget.attrs['default_lon'] = lng
        if width:
            self.fields['point'].widget.attrs['map_width'] = width


class MonthYearWidget(Widget):
    """
    A Widget that splits date input into two <select> boxes for month and year,
    with 'day' defaulting to the first of the month.

    Based on SelectDateWidget, in

    django/trunk/django/forms/extras/widgets.py


    """
    none_value = (0, '---')
    month_field = '%s_month'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year+10)

    def render(self, name, value, attrs=None, renderer = None):
        try:
            year_val, month_val = value.year, value.month
        except AttributeError:
            year_val = month_val = None
            if isinstance(value, string_types):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        month_choices = list(MONTHS.items())
        if not (self.required and value):
            month_choices.append(self.none_value)
        month_choices.sort()
        local_attrs = self.build_attrs(base_attrs=self.attrs)
        s = Select(choices=month_choices)
        select_html = s.render(self.month_field % name, month_val, local_attrs)
        output.append(select_html)

        year_choices = [(i, i) for i in self.years]
        if not (self.required and value):
            year_choices.insert(0, self.none_value)
        local_attrs['id'] = self.year_field % id_
        s = Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        if y == m == "0":
            return None
        if y and m:
            return '%s-%s-%s' % (y, m, 1)
        return data.get(name, None)

class MonthYearForm(forms.Form):

    date = forms.DateField(
        required=False,
        widget=MonthYearWidget(years=range(2017,2041))
    )

class DailyRefresherForm(forms.ModelForm):

    class Meta:
        model = Daily_Refresher
        fields = '__all__'

        widgets = {
            'port_time': forms.TimeInput(format='%M:%S'),
            'building_time': forms.TimeInput(format='%M:%S'),
            'vehicle_time': forms.TimeInput(format='%M:%S'),
            'baggage_time': forms.TimeInput(format='%M:%S'),
            'others_time': forms.TimeInput(format='%M:%S'),
            'mar': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(DailyRefresherForm, self).__init__(*args, **kwargs)
        self.fields['rating'].required = False
        self.fields['mar'].required = False
        self.fields['on_leash'].required = False
        self.fields['off_leash'].required = False
        self.fields['obstacle_course'].required = False
        self.fields['panelling'].required = False
        self.fields['k9'].required = False
        self.fields['handler'].required = False