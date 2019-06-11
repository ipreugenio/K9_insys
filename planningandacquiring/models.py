from django.db import models
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import date as d
from dateutil.relativedelta import relativedelta
from inventory.models import Medicine, Miscellaneous, Food

#from unitmanagement.models import Notification


from profiles.models import User
from django.db.models import aggregates, Avg, Count, Min, Sum, Q, Max


class Date(models.Model):
    date_from = models.DateField('date_from', null=True)
    date_to = models.DateField('date_to', null=True)

class K9_Supplier(models.Model):
    name = models.CharField('name', max_length=200)
    organization = models.CharField('organization', max_length=200, default='Personal')
    address = models.CharField('address', max_length=200)
    contact_no = models.CharField('contact_no', max_length=200)

    def __str__(self):
        return str(self.name)

class K9_Breed(models.Model):
    SKILL = (
        ('NDD', 'NDD'),
        ('EDD', 'EDD'),
        ('SAR', 'SAR')
    )

    BREED = (
        ('Belgian Malinois', 'Belgian Malinois'),
        ('Dutch Sheperd', 'Dutch Sheperd'),
        ('German Sheperd', 'German Sheperd'),
        ('Golden Retriever', 'Golden Retriever'),
        ('Jack Russel', 'Jack Russel'),
        ('Labrador Retriever', 'Labrador Retriever'),
        ('Mixed', 'Mixed'),
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

    breed = models.CharField('breed', choices=BREED,  max_length=200, null=True)
    life_span = models.CharField('life_span', max_length=200, null=True)
    temperament = models.CharField('temperament', max_length=200, null=True)
    colors = models.CharField('colors', choices=COLORS, max_length=200, null=True)
    weight = models.CharField('weight', max_length=200, null=True)
    male_height = models.CharField('male_height', max_length=200, null=True)
    female_height = models.CharField('female_height', max_length=200, null=True)
    skill_recommendation = models.CharField('skill_recommendation', choices=SKILL, max_length=200, null=True)

    def __str__(self):
        return str(self.breed)

class K9(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    COLOR = (
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
    
    BREED = (
        ('Belgian Malinois', 'Belgian Malinois'),
        ('Dutch Sheperd', 'Dutch Sheperd'),
        ('German Sheperd', 'German Sheperd'),
        ('Golden Retriever', 'Golden Retriever'),
        ('Jack Russel', 'Jack Russel'),
        ('Labrador Retriever', 'Labrador Retriever'),
        ('Mixed', 'Mixed'),
    )

    STATUS = (
        ('Material Dog', 'Material Dog'),
        ('Working Dog', 'Working Dog'),
        ('Adopted', 'Adopted'),
        ('Due-For-Retirement', 'Due-For-Retirement'),
        ('Retired', 'Retired'),
        ('Dead', 'Dead'),
        ('Sick', 'Sick'),
        ('Stolen', 'Stolen'), 
        ('Lost', 'Lost'), 
        ('Accident', 'Accident'), 
    )
    
    REPRODUCTIVE = (
        ('Proestrus', 'Proestrus'),
        ('Estrus', 'Estrus'),
        ('Metestrus', 'Metestrus'),
        ('Anestrus', 'Anestrus'), 
    )
    SOURCE = (
        ('Procured', 'Procured'),
        ('Breeding', 'Breeding'),
    )

    TRAINING = (
        ('Puppy', 'Puppy'),
        ('Unclassified', 'Unclassified'),
        ('Classified', 'Classified'),
        ('On-Training', 'On-Training'),
        ('Trained', 'Trained'),
        ('For-Breeding', 'For-Breeding'),
        ('Breeding', 'Breeding'),
        ('For-Deployment', 'For-Deployment'),
        ('For-Adoption', 'For-Adoption'),
        ('Deployed', 'Deployed'),
        ('Light Duty', 'Light Duty'),
        ('Retired', 'Retired'),
        ('Dead', 'Dead'),
    )
    TRAINED = (
        ('Trained', 'Trained'),
        ('Failed', 'Failed'),
    )

    image = models.FileField(upload_to='k9_image', default='k9_image/k9_default.png', blank=True, null=True)
    serial_number = models.CharField('serial_number', max_length=200 , default='Unassigned Serial Number')
    name = models.CharField('name', max_length=200)
    handler = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    breed = models.CharField('breed', choices=BREED, max_length=200, blank=True, null=True)
    sex = models.CharField('sex', choices=SEX, max_length=200, default="Unspecified")
    color = models.CharField('color', choices=COLOR, max_length=200, default="Unspecified")
    birth_date = models.DateField('birth_date', null=True, blank=True)
    age = models.IntegerField('age', default = 0)
    source = models.CharField('source', max_length=200, default="Not Specified", choices=SOURCE)
    year_retired = models.DateField('year_retired', null=True, blank=True)
    death_date = models.DateField('death_date', null=True, blank=True)
    death_cert = models.FileField(upload_to='death_certificate', blank=True, null=True)
    assignment = models.CharField('assignment', max_length=200, default="None", null=True, blank=True)
    status = models.CharField('status', choices=STATUS, max_length=200, default="Material Dog")
    training_status = models.CharField('training_status', choices=TRAINING, max_length=200, default="Puppy")
    training_level = models.CharField('training_level', max_length=200, default="Stage 0")
    training_count = models.IntegerField('training_count', default = 0)
    capability = models.CharField('capability', max_length=200, default="None")
    #microchip = models.CharField('microchip', max_length=200, default = 'Unassigned Microchip')
    reproductive_stage = models.CharField('reproductive_stage', choices=REPRODUCTIVE, max_length=200, default="Anestrus")
    age_days = models.IntegerField('age_days', default = 0)
    age_month = models.IntegerField('age_month', default = 0)
    in_heat_months = models.IntegerField('in_heat_months', default = 6)
    last_proestrus_date = models.DateField(blank=True, null=True)
    next_proestrus_date = models.DateField(blank=True, null=True)
    estrus_date = models.DateField(blank=True, null=True)
    metestrus_date = models.DateField(blank=True, null=True)
    anestrus_date = models.DateField(blank=True, null=True)

    date_created = models.DateField('date_created', default=dt.now())

    supplier =  models.ForeignKey(K9_Supplier, on_delete=models.CASCADE, blank=True, null=True) #if procured
    litter_no = models.IntegerField('litter_no', default = 0)
    last_date_mated = models.DateField(blank=True, null=True)
    trained = models.CharField('trained', choices=TRAINED, max_length=100, blank=True, null=True)
    
    # def best_fertile_notification(self):
    #     notif = self.estrus_date - td(days=7)
    #     return notif

    def num_in_heat(self):
        return self.in_heat_months/12

    def in_heat_monthly(self):

        upcoming_year = int(dt.now().year) + 1

        months = [0,0,0,0,0,0,0,0,0,0,0,0]
        prostreus_temp = self.last_proestrus_date
        prostreus_temp_year = int(prostreus_temp.year)
        year = []
        while prostreus_temp_year <= upcoming_year:
            if prostreus_temp_year == upcoming_year:

                if prostreus_temp.month == 1:
                    months[0] += 1
                elif prostreus_temp.month == 2:
                    months[1] += 1
                elif prostreus_temp.month == 3:
                    months[2] += 1
                elif prostreus_temp.month == 4:
                    months[3] += 1
                elif prostreus_temp.month == 5:
                    months[4] += 1
                elif prostreus_temp.month == 6:
                    months[5] += 1
                elif prostreus_temp.month == 7:
                    months[6] += 1
                elif prostreus_temp.month == 8:
                    months[7] += 1
                elif prostreus_temp.month == 9:
                    months[8] += 1
                elif prostreus_temp.month == 10:
                    months[9] += 1
                elif prostreus_temp.month == 11:
                    months[10] += 1
                elif prostreus_temp.month == 12:
                    months[11] += 1

            prostreus_temp += relativedelta(months = self.in_heat_months)
            prostreus_temp_year = prostreus_temp.year

        return months

    def calculate_age(self):
        #delta = dt.now().date() - self.birth_date
        #return delta.days
        today = d.today()
        birthdate = self.birth_date
        bday = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if bday < 1:
            bday = 0
        return bday

    def calculate_months_before(birthday):
        today = d.today()
        birthdate = birthday
        bday = 13 - birthdate.month
        return bday

    def save(self, *args, **kwargs):
        #litter
        if self.sex == 'Female':
            try:
                f = K9_Litter.objects.filter(mother__id=self.id).aggregate(Max('litter_no'))
                self.litter_no = int(f['litter_no__max'])
            except:
                self.litter_no = 0
            
        else:
            try:
                m = K9_Litter.objects.filter(father__id=self.id).aggregate(Max('litter_no'))
                self.litter_no = int(m['litter_no__max'])
            except:
                self.litter_no = 0
            

        self.last_proestrus_date = self.birth_date + relativedelta(months=+6)
        days = d.today() - self.birth_date
        self.year_retired = self.birth_date + relativedelta(years=+10)
        self.age_month = self.age_days / 30
        self.age_days = days.days
        self.age = self.calculate_age()
        self.training_id = self.id 
        if self.age_days == 183:
            self.last_proestrus_date = d.today()
        
        if self.last_proestrus_date != None:
            self.estrus_date = self.last_proestrus_date + td(days=7)
            self.metestrus_date = self.estrus_date + td(days=20)
            self.anestrus_date = self.metestrus_date + td(days=90)
            self.next_proestrus_date = self.last_proestrus_date + relativedelta(months=+self.in_heat_months)
        
        if d.today() == self.last_proestrus_date: 
            self.reproductive_stage = 'Proestrus'
        elif d.today() == self.estrus_date:
            self.reproductive_stage = 'Estrus'
        elif d.today() == self.metestrus_date:
            self.reproductive_stage = 'Metestrus'
        elif d.today() == self.anestrus_date:
            self.reproductive_stage = 'Anestrus'
        else:
            pass

        if self.age == 9:
            self.training_status = 'Due-For-Retirement'
            self.status = 'Working Dog'
            #TODO notif 1 year
            from unitmanagement.models import Notification
            Notification.objects.create(message= str(self.name) +' is due to retire next year.')
        elif self.age == 10:
            self.training_status = 'Retired'
            self.year_retired = self.birth_date + td(days=(10*365))
            self.status = 'Retired'
        else:
            pass

        if self.sex == 'Male':
            self.in_heat_months = 0
            self.last_proestrus_date = None
            self.next_proestrus_date = None
            self.estrus_date = None
            self.metestrus_date = None
            self.anestrus_date = None
        

        # Serial Numbers and Microchips are given after training
        # lead_zero = str(self.id).zfill(5)
        # serial_number = '#%s' % (lead_zero)
        # self.serial_number = str(serial_number)
        super(K9, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.name) + " : " + str(self.serial_number)

class K9_Litter(models.Model):
    mother = models.ForeignKey(K9, related_name='dam', on_delete=models.CASCADE, blank=True, null=True)
    father = models.ForeignKey(K9, related_name='sire', on_delete=models.CASCADE, blank=True, null=True)
    litter_no = models.IntegerField('litter_no', blank=True, null=True)

class K9_Past_Owner(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    first_name = models.CharField('first_name', max_length=200)
    middle_name = models.CharField('middle_name', max_length=200)
    last_name = models.CharField('last_name', max_length=200)
    address = models.CharField('address', max_length=200)
    sex = models.CharField('sex', choices=SEX, max_length=200, default="Unspecified")
    birth_date = models.DateField('birth_date', blank=True, null=True)
    email = models.EmailField('email', max_length=200, default = "not specified")
    contact_no = models.CharField('contact_no', max_length=200, default = "not specified")

    def __str__(self):
        return str(self.first_name) +' '+ str(self.middle_name) + ' ' + str(self.last_name)

class K9_New_Owner(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    first_name = models.CharField('first_name', max_length=200)
    middle_name = models.CharField('middle_name', max_length=200)
    last_name = models.CharField('last_name', max_length=200)
    address = models.CharField('address', max_length=200)
    sex = models.CharField('sex', choices=SEX, max_length=200, default="Unspecified")
    #age = models.IntegerField('age', default = 0)
    birth_date = models.DateField('birth_date', blank=True, null=True)
    email = models.EmailField('email', max_length=200)
    contact_no = models.CharField('contact_no', max_length=200)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.middle_name) + ' ' + str(self.last_name)

class K9_Donated(models.Model):
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(K9_Past_Owner, on_delete=models.CASCADE)
    date_donated = models.DateField('date_donated', auto_now_add=True)

    def __str__(self):
        return str(self.k9)

class K9_Adopted(models.Model):
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE)
    owner = models.ForeignKey(K9_New_Owner, on_delete=models.CASCADE)
    date_adopted = models.DateField('date_adopted', auto_now_add=True)

    def __str__(self):
        return str(self.k9)


class K9_Parent(models.Model):
    mother = models.ForeignKey(K9, on_delete=models.CASCADE, related_name= "mother", blank=True, null=True)
    father = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="father", blank=True, null=True)
    offspring = models.ForeignKey(K9, on_delete=models.CASCADE, blank=True, null=True)

class K9_Mated(models.Model):
    mother = models.ForeignKey(K9, on_delete=models.CASCADE, related_name= "mom", blank=True, null=True)
    father = models.ForeignKey(K9, on_delete=models.CASCADE, related_name="dad", blank=True, null=True)  
    status = models.CharField('status', max_length=200, default = "Breeding")
    date_mated = models.DateField('date_mated', blank=True, null=True)  

class K9_Quantity(models.Model):
    quantity = models.IntegerField('quantity', default=0)
    date_bought = models.DateField('date_bought', null=True)


#TODO Add inventory attr > How many dogs each item can cater
#TODO VITAMINS
class Budget_allocation(models.Model):
    k9_request_forecast = models.IntegerField('k9_request_forecast', default=0)
    k9_needed_for_demand = models.IntegerField('k9s_needed_for_demand', default=0)
    k9_cuurent = models.IntegerField('k9_current', default=0)
    food_total = models.DecimalField('food_total', default=0, max_digits=50, decimal_places=2,)
    equipment_total = models.DecimalField('equipment_total', default=0, max_digits=50, decimal_places=2,)
    medicine_total = models.DecimalField('medicine_total', default=0, max_digits=50, decimal_places=2,)
    vaccine_total = models.DecimalField('vaccine_total', default=0, max_digits=50, decimal_places=2,)
    vet_supply_total = models.DecimalField('vet_supply_total', default=0, max_digits=50, decimal_places=2,)
    k9_total = models.DecimalField('k9_total', default=0, max_digits=50, decimal_places=2, )
    grand_total = models.DecimalField('grand_total', default=0, max_digits=50, decimal_places=2,)
    date_created = models.DateField('date_created', auto_now_add=True)
    date_tobe_budgeted = models.CharField('date_tobe_budgeted', null=True, max_length=200, default="-")

class Budget_food(models.Model):
    type = (
        ('Adult', 'Adult'),
        ('Puppy', 'Puppy'),
        ('Milk', 'Milk')
    )

    food = models.CharField('food', max_length=200, default="Adult")
    quantity = models.IntegerField('quantity', default=0)
    price = models.DecimalField('price', default=0, max_digits=50, decimal_places=2,)
    total = models.DecimalField('total', default=0, max_digits=50, decimal_places=2,)
    budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)

class Budget_equipment(models.Model):
    equipment = models.ForeignKey(Miscellaneous, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField('quantity', default=0)
    price = models.DecimalField('price', default=0, max_digits=50, decimal_places=2,)
    total = models.DecimalField('total', default=0, max_digits=50, decimal_places=2,)
    budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)

class Budget_medicine(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField('quantity', default = 0)
    price = models.DecimalField('price', default=0, max_digits=50, decimal_places=2,)
    total = models.DecimalField('total', default=0, max_digits=50, decimal_places=2,)
    budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)

class Budget_vaccine(models.Model):
    vaccine = models.ForeignKey(Medicine, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField('quantity', default = 0)
    price = models.DecimalField('price', default=0, max_digits=50, decimal_places=2,)
    total = models.DecimalField('total', default=0, max_digits=50, decimal_places=2,)
    budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)


# class Budget_vitamins(models.Model):
#     vitamins = models.ForeignKey(Medicine, on_delete=models.CASCADE, blank=True, null=True)
#     quantity = models.IntegerField('quantity', default = 0)
#     price = models.DecimalField('price', default=0, max_digits=50, decimal_places=2,)
#     budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)

class Budget_vet_supply(models.Model):
    vet_supply = models.ForeignKey(Miscellaneous, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField('quantity', default=0)
    price = models.DecimalField('price', default=0, max_digits=50, decimal_places=2,)
    total = models.DecimalField('total', default=0, max_digits=50, decimal_places=2,)
    budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)


class Budget_k9(models.Model):
    quantity = models.IntegerField('quantity', default=0)
    price = models.DecimalField('price', default=0, max_digits=50, decimal_places=2,)
    total = models.DecimalField('total', default=0, max_digits=50, decimal_places=2,)
    budget_allocation = models.ForeignKey(Budget_allocation, on_delete=models.CASCADE, blank=True, null=True)

class Dog_Breed(models.Model):
    SKILL = (
        ('NDD', 'NDD'),
        ('EDD', 'EDD'),
        ('SAR', 'SAR')
    )


    breed = models.CharField('breed', max_length=200, null=True)
    life_span = models.CharField('life_span', max_length=200, null=True)
    temperament = models.CharField('temperament', max_length=200, null=True)
    colors = models.CharField('colors', max_length=200, null=True)
    weight = models.CharField('weight', max_length=200, null=True)
    male_height = models.CharField('male_height', max_length=200, null=True)
    female_height = models.CharField('female_height', max_length=200, null=True)
    skill_recommendation = models.CharField('skill_recommendation', choices=SKILL, max_length=200, null=True, blank=True)
    skill_recommendation2 = models.CharField('skill_recommendation2', choices=SKILL, max_length=200, null=True, blank=True)
    skill_recommendation3 = models.CharField('skill_recommendation3', choices=SKILL, max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.breed)

