from faker import Faker
import random
from datetime import timedelta, datetime
from profiles.models import User, Account, Personal_Info, Education
from planningandacquiring.models import K9, K9_Supplier, Dog_Breed
from deployment.models import Area, Location, Dog_Request, Incidents, Maritime, Team_Assignment, K9_Pre_Deployment_Items, \
    K9_Schedule, Team_Dog_Deployed
from django.contrib.auth.models import User as AuthUser
from training.models import Training, Training_Schedule, Training_History

from inventory.models import Miscellaneous, Food, Medicine_Inventory, Medicine

from deployment.tasks import assign_TL

import re

# For more info on faker.Faker, view https://faker.readthedocs.io/en/latest/index.html

# Populate DB process
#
# 1.)generate_user()
#   a.) Creates User
#   b.) Creates Personal Info
#   c.) Creates Education
#   d.) Creates Account
# 2.) generate_k9()
#   a.) Creates K9
#   b.) Creates Supplier


def generate_city_ph():

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
        ('Zamboanga', 'Zamboanga')
    )

    randomizer = random.randint(0, len(CITY) - 1)

    return CITY[randomizer][0]

# START USER CREATION
def generate_user():
    fake = Faker()

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
    )

    BLOODTYPE = (
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    )

    RELIGION = (
        ('Roman Catholic', 'Roman Catholic'),
        ('Christianity', 'Christianity'),
        ('Islam', 'Islam'),
        ('Iglesia ni Cristo', 'Iglesia ni Cristo'),
        ('Buddhist', 'Buddhist'),
    )

    SKINCOLOR = (
        ('Light', 'Light'),
        ('Dark', 'Dark'),
        ('Yellow', 'Yellow'),
        ('Brown', 'Brown')
    )

    ctr = 0
    for x in range(0, 400):

        position = ""

        if ctr <= 329:
            position = "Handler"
        elif ctr >= 330 and ctr <= 360:
            position = "Commander"
        elif ctr >= 361 and ctr <= 379:
            position = "Veterinarian"
        elif ctr == 380 or ctr == 381:
            position = "Operations"
        elif ctr >= 382 and ctr <= 385:
            position = "Trainer"
        else:
            position = 'Administrator'

        randomizer = random.randint(0, 8)
        rank = RANK[randomizer][0]

        randomizer = random.randint(0, 1)

        gender = "?"
        first_name = "?"
        if randomizer == 0:
            first_name = fake.first_name_male()
            print("First Name : " + first_name)
            gender = "Male"
        else:
            first_name = fake.first_name_female()
            print("First Name : " + first_name)
            gender = "Female"

        last_name = fake.last_name()
        print("Last Name :" + last_name)
        print("Gender : " + gender)

        generated_date = fake.date_between(start_date="-30y", end_date="-20y")
        birthdate = generated_date.strftime("%m/%d/%Y")
        print("Birthdate : " + birthdate)
        print("Birthplace : " + fake.address())
        birthplace = fake.address()

        randomizer = random.randint(0, 3)
        blood_type = BLOODTYPE[randomizer][0]
        randomizer = random.randint(0, 4)
        religion = RELIGION[randomizer][0]

        randomizer = random.randint(0, 1)

        civil_status = "?"
        if randomizer == 0:
            civil_status = "Single"
        else:
            civil_status = "Married"

        randomizer = random.randint(0, 3)
        skin_color = SKINCOLOR[randomizer][0]
        eye_color = fake.safe_color_name()
        hair_color = fake.safe_color_name()

        username = first_name + last_name
        username = username.lower()
        email = username + "@gmail.com"

        user = User.objects.create(rank = rank, firstname = first_name, lastname = last_name, middlename = "", nickname = "", birthdate = generated_date, birthplace = birthplace, gender = gender,
                                   civilstatus = civil_status, citizenship = "Filipino", religion = religion, bloodtype = blood_type, haircolor = hair_color, eyecolor = eye_color, skincolor = skin_color,
                                   position = position)
        user.save()

        cellnum = fake.msisdn()[:10]
        phonenum = fake.msisdn()[:7]

        father = fake.first_name_male() + " " + last_name
        mother_birth = fake.date_between(start_date="-30y", end_date="-20y")
        mother = fake.first_name_female() + " " + last_name
        father_birth = fake.date_between(start_date="-30y", end_date="-20y")

        street = fake.street_name() + " St."
        brngy = "Brngy. " + fake.street_name()
        city = generate_city_ph()
        province = "x province"

        tin = fake.msisdn()[:7]
        phil = fake.msisdn()[:7]

        personal = Personal_Info.objects.create(UserID=user, mobile_number=cellnum, tel_number=phonenum, street=street,
                                                barangay=brngy, city=city, province=province,
                                                mother_name=mother, father_name=father, mother_birthdate=mother_birth,
                                                father_birthdate=father_birth, tin=tin, philhealth=phil)
        personal.save()

        education = Education.objects.create(UserID = user, primary_education = "", secondary_education = "", tertiary_education = "", pe_schoolyear = "", se_schoolyear = "", te_schoolyear = "",
                                             pe_degree = "", se_degree = "", te_degree = "")
        education.save()
        serial_number = "O-" + str(user.id)
        # account = Account.objects.create(UserID = user, email_address = email, password = "zaq12wsx")
        # account.serial_number = "O-" + str(account.id)
        # account.save()
        AuthUser.objects.create_user(username=serial_number,
                                     email=email,
                                     password="zaq12wsx")
        #AuthUser.save()

        ctr += 1
    return None

# END USER CREATION

def generate_k9():
    fake = Faker()

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
    )

    suppliers = K9_Supplier.objects.all()
    if suppliers.count() == 0:
        for x in range(0, 12):
            contact = "+63" + fake.msisdn()[:10]
            supplier = K9_Supplier.objects.create(name=fake.name(), organization=fake.company(), address=fake.address(),
                                                  contact_no=contact)
            supplier.save()
        suppliers = K9_Supplier.objects.all()

    for x in range (0, 300):

        randomizer = random.randint(0, 1)
        name = "?"
        gender = "?"
        if randomizer == 0:
            name = fake.first_name_male()
            gender = "Male"
        else:
            name = fake.first_name_female()
            gender = "Female"

        randomizer = random.randint(0, 18)
        color = COLOR[randomizer][0]
        randomizer = random.randint(0, 5)
        breed = BREED[randomizer][0]

        generated_date = fake.date_between(start_date="-3y", end_date="-1y")
        date_time = generated_date.strftime("%m/%d/%Y")
        print("Birthdate : " + date_time)

        #Classifies other K9s
        k9 = K9.objects.create(name = name, breed = breed, sex = gender, color = color, birth_date = generated_date, source = "Procurement")
        k9.save()

        if k9.source == "Procurement":
            try:
                randomizer = random.randint(0, suppliers.count() - 1)
                supplier = K9_Supplier.objects.get(id = randomizer)
                k9.supplier = supplier
                k9.save()
            except: pass

    return None