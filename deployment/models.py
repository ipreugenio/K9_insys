from django.db import models
from planningandacquiring.models import K9


# Create your models here.

class Area(models.Model):
    name = models.CharField('name', max_length=100, default='')

    def __str__(self):
        return self.name

class Location(models.Model):

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

    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField('city', choices=CITY, max_length=100, default='None')
    place = models.CharField('place', max_length=100, default='Undefined')
    status = models.CharField('status', max_length=100, default="unassigned")

    def __str__(self):
        return str(self.area) + ' : ' + str(self.city) + ' City - ' + str(self.place)

class Team_Assignment(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    team = models.CharField('team', max_length=100)
    EDD_demand = models.IntegerField('EDD_demand', default=0)
    NDD_demand = models.IntegerField('NDD_demand', default=0)
    SAR_demand = models.IntegerField('SAR_demand', default=0)
    EDD_deployed = models.IntegerField('EDD_deployed', default=0)
    NDD_deployed = models.IntegerField('NDD_deployed', default=0)
    SAR_deployed = models.IntegerField('SAR_deployed', default=0)
    total_dogs_demand = models.IntegerField('total_dogs_demand', default=0)
    total_dogs_deployed = models.IntegerField('total_dogs_deployed', default=0)
    date_added = models.DateField('date_added', auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.team) + ' - ' + str(self.location)

    def save(self, *args, **kwargs):
        self.total_dogs_demand = int(self.EDD_demand) + int(self.NDD_demand) + int(self.SAR_demand)
        self.total_dogs_deployed = int(self.EDD_deployed) + int(self.NDD_deployed) + int(self.SAR_deployed)
        super(Team_Assignment, self).save(*args, **kwargs)

class Dog_Request(models.Model):
    requester = models.CharField('requester', max_length=100)
    location = models.CharField('location', max_length=100)
    phone_number = models.CharField('phone_number', max_length=100, default="n/a")
    email_address = models.EmailField('email', max_length=100, blank=True, null=True)
    remarks = models.CharField('remarks', max_length=200, blank=True, null=True)
    area = models.ForeignKey(Location, on_delete=models.CASCADE)
    EDD_needed = models.IntegerField('EDD_needed', default=0)
    NDD_needed = models.IntegerField('NDD_needed', default=0)
    SAR_needed = models.IntegerField('SAR_needed', default=0)
    EDD_deployed = models.IntegerField('EDD_deployed', default=0)
    NDD_deployed = models.IntegerField('NDD_deployed', default=0)
    SAR_deployed = models.IntegerField('SAR_deployed', default=0)
    total_dogs_demand = models.IntegerField('total_dogs_demand', default=0)
    total_dogs_deployed = models.IntegerField('total_dogs_deployed', default=0)
    start_date = models.DateField('start_date', null=True, blank=True)
    end_date = models.DateField('end_date', null=True, blank=True)
    status = models.CharField('status', max_length=100, default="Pending")

    def __str__(self):
        return str(self.requester) + ' - ' + str(self.location)

    def save(self, *args, **kwargs):
        self.total_dogs_demand = int(self.EDD_needed) + int(self.NDD_needed) + int(self.SAR_needed)
        self.total_dogs_deployed = int(self.EDD_deployed) + int(self.NDD_deployed) + int(self.SAR_deployed)
        super(Dog_Request, self).save(*args, **kwargs)

class Team_Dog_Deployed(models.Model):
    team_assignment = models.ForeignKey(Team_Assignment, on_delete=models.CASCADE, blank=True, null=True)
    team_requested = models.ForeignKey(Dog_Request, on_delete=models.CASCADE, blank=True, null=True) #Dog Rquest
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField('status', max_length=100, null=True, blank=True, default='Deployed')
    date_added = models.DateField('date_added', auto_now_add=True, null=True, blank=True)
    date_pulled = models.DateField('date_pulled' , null=True, blank=True)

    def __str__(self):
        return str(self.k9) + ' - ' + str(self.team_assignment)

class K9_Schedule(models.Model):
    k9 = models.ForeignKey(K9, on_delete=models.CASCADE, null=True, blank=True)
    dog_request = models.ForeignKey(Dog_Request, on_delete=models.CASCADE, null=True, blank=True)
    date_start = models.DateField('date_start', null=True, blank=True)
    date_end = models.DateField('date_end', null=True, blank=True)

class Incidents (models.Model):
    TYPE = (
        ('Explosives Related', 'Explosives Related'),
        ('Narcotics Related', 'Narcotics Related'),
        ('Search and Rescue Related', 'Search and Rescue Related'),
        ('Others', 'Others'),
    )

    date = models.DateField('date', null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField('type', choices=TYPE, max_length=100, default='Others')
    remarks = models.TextField('remarks', max_length=200, blank=True, null=True)

