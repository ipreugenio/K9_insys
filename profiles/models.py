from django.db import models
from datetime import date as d

# Create your models here.
class User(models.Model):
    SEX = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    POSITION = (
        ('Handler', 'Handler'),
        ('Veterinarian', 'Veterinarian'),
        ('Administrator', 'Administrator')
    )

    CIVILSTATUS = (
        ('Single', 'Single'),
        ('Married', 'Married')
    )

    BLOODTYPE = (
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    )

    HAIRCOLOR = (
        ('Black', 'Black'),
        ('Brown', 'Brown')
    )

    EYECOLOR = (
        ('Black', 'Black'),
        ('Brown', 'Brown')
    )

    SKINCOLOR = (
        ('Light', 'Light'),
        ('Dark', 'Dark'),
        ('Yellow', 'Yellow'),
        ('Brown', 'Brown')
    )

    STATUS = (
        ('Working', 'Working'),
        ('Sick', 'Sick'),
        ('On-Leave', 'On-Leave'),
        ('Retired', 'Retired'),
        ('Dead', 'Dead')
    )

    image = models.FileField(upload_to='profile_image', default='profile_image/default.png', blank=True, null=True)
    position = models.CharField('position', choices=POSITION, max_length=200)
    rank = models.CharField('rank', max_length=200, default="None", blank=True)
    fullname = models.CharField('fullname', max_length=200, default="None", blank=True)
    firstname = models.CharField('firstname', max_length=200, default="None", blank=True)
    lastname = models.CharField('lastname', max_length=200, default="None", blank=True)
    extensionname = models.CharField('extensionname', max_length=200, default="None", blank=True)
    middlename = models.CharField('middlename', max_length=200, default="None", blank=True)
    nickname = models.CharField('nickname', max_length=200, default="None", blank=True)
    birthdate = models.DateField('birthdate', blank=True)
    age = models.IntegerField('age', default=0)
    birthplace = models.CharField('birthplace', max_length=200, default="None", blank=True)
    gender = models.CharField('gender', choices=SEX, max_length=200, default="None", blank=True)
    civilstatus = models.CharField('civilstatus', choices=CIVILSTATUS, max_length=200)
    citizenship = models.CharField('citizenship', max_length=200, default="None", blank=True)
    religion = models.CharField('religion', max_length=200)
    bloodtype = models.CharField('bloodtype', choices=BLOODTYPE, max_length=200)
    distinct_feature = models.CharField('distinct_feature', max_length=200, blank=True, null=True)
    haircolor = models.CharField('haircolor', choices=HAIRCOLOR, max_length=200, default="None", blank=True)
    eyecolor = models.CharField('eyecolor', choices=EYECOLOR, max_length=200, default="None", blank=True)
    skincolor = models.CharField('skincolor', choices=SKINCOLOR, max_length=200, default="None", blank=True)
    height = models.IntegerField('height')
    weight = models.IntegerField('weight')
    headsize = models.IntegerField('headsize')
    footsize = models.IntegerField('footsize')
    bodybuild = models.CharField('bodybuild', max_length=200)
    status = models.CharField('status', choices=STATUS, max_length=200, default="Working")
    partnered = models.BooleanField(default=False)
    capability = models.CharField('capability', max_length=200, default="None")
    # edd = models.BooleanField(default=False)
    # ndd = models.BooleanField(default=False)
    # sar = models.BooleanField(default=False)
    
    def calculate_age(self):
        # delta = dt.now().date() - self.birth_date
        # return delta.days
        today = d.today()
        birthdate = self.birthdate
        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        self.fullname = str(self.lastname)+ ', ' +str(self.firstname)+ ' ' + str(self.middlename) 
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.firstname) + ' ' + str(self.middlename) + ' ' + str(self.lastname)


class Personal_Info(models.Model):
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

    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = models.CharField('mobile_number', max_length=200)
    tel_number = models.CharField('tel_number', max_length=200)
    street = models.CharField('street', max_length=200)
    barangay = models.CharField('barangay', max_length=200)
    city = models.CharField('city', choices=CITY, max_length=100, default='None')
    province = models.CharField('province', max_length=200)
    mother_name = models.CharField('mother_name', max_length=200)
    mother_birthdate = models.DateField('mother_birthdate', max_length=200)
    father_name = models.CharField('father_name', max_length=200)
    father_birthdate = models.DateField('father_birthdate', max_length=200)
    tin = models.IntegerField('tin')
    philhealth = models.IntegerField('philhealth')

class Education(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    primary_education = models.CharField('primary_education', max_length=200)
    secondary_education = models.CharField('secondary_education', max_length=200)
    tertiary_education = models.CharField('tertiary_education', max_length=200)
    pe_schoolyear = models.CharField('pe_schoolyear', max_length=200)
    se_schoolyear = models.CharField('se_schoolyear', max_length=200)
    te_schoolyear = models.CharField('te_schoolyear', max_length=200)
    pe_degree = models.CharField('pe_degree', max_length=200)
    se_degree = models.CharField('se_degree', max_length=200)
    te_degree = models.CharField('te_degree', max_length=200)


class Account(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    serial_number = models.CharField('serial_number', max_length=200)
    email_address = models.EmailField('email_address', max_length=200)
    password = models.CharField('password', max_length=200)

    def __str__(self):
        return str(self.UserID.id) + ' ' + str(self.serial_number)
