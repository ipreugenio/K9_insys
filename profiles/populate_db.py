from faker import Faker
import random
from datetime import timedelta, datetime
from profiles.models import User, Account, Personal_Info, Education
from planningandacquiring.models import K9, K9_Supplier, Dog_Breed
from deployment.models import Area, Location, Dog_Request, Incidents, Maritime, Team_Assignment
from django.contrib.auth.models import User as AuthUser
from training.models import Training, Training_Schedule



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

def generate_rank():
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

    randomizer = random.randint(0, 8)

    return RANK[randomizer][0]

def generate_bloodtype():
    BLOODTYPE = (
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O')
    )

    randomizer = random.randint(0, 3)

    return BLOODTYPE[randomizer][0]


def generate_religion():
    RELIGION = (
        ('Roman Catholic', 'Roman Catholic'),
        ('Christianity', 'Christianity'),
        ('Islam', 'Islam'),
        ('Iglesia ni Cristo', 'Iglesia ni Cristo'),
        ('Buddhist', 'Buddhist'),
    )

    randomizer = random.randint(0, 4)

    return RELIGION[randomizer][0]

def generate_skin_color():
    SKINCOLOR = (
        ('Light', 'Light'),
        ('Dark', 'Dark'),
        ('Yellow', 'Yellow'),
        ('Brown', 'Brown')
    )

    randomizer = random.randint(0, 3)

    return SKINCOLOR[randomizer][0]

def generate_position():
    POSITION = (
        ('Handler', 'Handler'),
        ('Veterinarian', 'Veterinarian'),
        ('Administrator', 'Administrator'),
        ('Team Leader', 'Team Leader'),
        ('Commander', 'Commander'),
        ('Operations', 'Operations'),
        ('Trainer', 'Trainer'),
    )

    randomizer = random.randint(0, 6)

    return POSITION[randomizer][0]

def generate_user():
    fake = Faker()


    handler_count = 300
    commander_count = 14
    teamleader_count = 45
    vet_count = 20
    operations = 1
    trainor = 4
    admin = 15

    ctr = 0
    for x in range(0, 400):

        position = ""

        if ctr <= 300:
            position = "Handler"
        elif ctr >= 301 and ctr <= 314:
            position = "Commander"
        elif ctr >= 315 and ctr <= 360:
            position = "Team Leader"
        elif ctr >= 361 and ctr <= 380:
            position = "Veterinarian"
        elif ctr == 381:
            position = "Operations"
        elif ctr >= 382 and ctr <= 385:
            position = "Trainer"
        else:
            position = 'Administrator'


        print("Rank : " + generate_rank())
        rank = generate_rank()

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

        print("Bloodtype : " + generate_bloodtype())
        blood_type = generate_bloodtype()
        print("Religion : " + generate_religion())
        religion = generate_religion()

        randomizer = random.randint(0, 1)

        civil_status = "?"
        if randomizer == 0:
            print("Civil Status : Single")
            civil_status = "Single"
        else:
            print("Civil Status : Married")
            civil_status = "Married"

        print("Skin Color : " + generate_skin_color())
        skin_color = generate_skin_color()
        print("Eye Color : " + fake.safe_color_name())
        eye_color = fake.safe_color_name()
        print("Hair Color : " + fake.safe_color_name())
        hair_color = fake.safe_color_name()

        username = first_name + last_name
        username = username.lower()
        print("Username : " + username)
        print("Email : " + username + "@gmail.com")
        email = username + "@gmail.com"
        print("Position : " + position)
        print()

        user = User.objects.create(rank = rank, firstname = first_name, lastname = last_name, middlename = "", nickname = "", birthdate = generated_date, birthplace = birthplace, gender = gender,
                                   civilstatus = civil_status, citizenship = "Filipino", religion = religion, bloodtype = blood_type, haircolor = hair_color, eyecolor = eye_color, skincolor = skin_color,
                                   position = position)
        user.save()
        generate_personal_info(user, last_name)
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

def generate_personal_info(user, last_name):
    fake = Faker()
    print("Cell Number : +63" + fake.msisdn()[:10])
    cellnum = fake.msisdn()[:10]
    print("Phone Number : " + fake.msisdn()[:7])
    phonenum = fake.msisdn()[:7]

    print("Father's Name : " + fake.first_name_male() + " " + last_name)
    father = fake.first_name_male() + " " + last_name
    mother_birth = fake.date_between(start_date="-30y", end_date="-20y")
    print("Mother's Name : " + fake.first_name_female() + " " + last_name)
    mother = fake.first_name_female() + " " + last_name
    father_birth = fake.date_between(start_date="-30y", end_date="-20y")

    print("Street : " + fake.street_name() + " St.")
    street = fake.street_name() + " St."
    print("Barangay : Brngy. " + fake.street_name())
    brngy = "Brngy. " + fake.street_name()
    city = generate_city_ph()
    province = "x province"

    tin = fake.msisdn()[:7]
    phil = fake.msisdn()[:7]

    personal = Personal_Info.objects.create(UserID = user, mobile_number = cellnum, tel_number = phonenum, street = street, barangay = brngy, city = city, province = province,
                                            mother_name = mother, father_name = father, mother_birthdate = mother_birth, father_birthdate = father_birth, tin = tin, philhealth = phil)
    personal.save()

    return None

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>END OF USER CREATION


def generate_breed():
    BREED = (
        ('Belgian Malinois', 'Belgian Malinois'),
        ('Dutch Sheperd', 'Dutch Sheperd'),
        ('German Sheperd', 'German Sheperd'),
        ('Golden Retriever', 'Golden Retriever'),
        ('Jack Russel', 'Jack Russel'),
        ('Labrador Retriever', 'Labrador Retriever'),
    )
    randomizer = random.randint(0, 5)

    return BREED[randomizer][0]

def generate_skill():
    SKILL = (
        ('NDD', 'NDD'),
        ('EDD', 'EDD'),
        ('SAR', 'SAR')
    )

    randomizer = random.randint(0, 2)

    return SKILL[randomizer][0]


# Get 90% of all k9s then assign a random skill to each one
def assign_skill_random():
    k9s = K9.objects.all()

    k9_id_list = []
    for k9 in k9s:
        k9_id_list.append(k9.id)

    k9_sample = random.sample(k9_id_list, int(len(k9_id_list)*.90))

    k9s = K9.objects.filter(pk__in = k9_sample)

    for k9 in k9s:
        k9.capability = generate_skill()
        k9.training_status = "Classified"
        k9.save()

    return k9_sample


# Get 80% of all classified k9s then assign a random handler to each one
def assign_handler_random():

    k9_sample = assign_skill_random()

    users = User.objects.filter(position = "Handler")

    user_id_list = []
    for user in users:
        user_id_list.append(user.id)

    k9_sample = random.sample(k9_sample, int(len(k9_sample)*.80))
    user_sample = random.sample(user_id_list, len(k9_sample)) #user sample now have the same length as k9 sample
    partnership = zip(k9_sample, user_sample)


    for item in partnership:
        k9 = K9.objects.get(id = item[0])
        user = User.objects.get(id = item[1])

        k9.handler = user
        k9.training_status = 'On-Training'
        k9.save()

    return k9_sample

#Get 70% of all k9s with handlers then end their training
def generate_training():
    fake = Faker()

    k9_sample = assign_handler_random() #Get all k9s with available handlers
    k9_sample = random.sample(k9_sample, int(len(k9_sample) * .70))

    k9s = K9.objects.filter(pk__in = k9_sample)

    GRADE = (
        # ("0", "0"),
        ("75", "75"),
        ("80", "80"),
        ("85", "85"),
        ("90", "90"),
        ("95", "95"),
        ("100", "100"),
    )

    for k9 in k9s:
        birthdate = k9.birth_date

        training_start_alpha = datetime.combine(birthdate, datetime.min.time())
        training_start_alpha = training_start_alpha + timedelta(days=365)


        training = Training.objects.filter(k9 = k9).get(training = k9.capability)

        remark = fake.paragraph(nb_sentences=2, variable_nb_sentences=True, ext_word_list=None)

        train_sched = Training_Schedule.objects.get(k9 = k9) #Because we have 1 instance of this per k9 instance
        train_sched.date_start = training_start_alpha
        train_sched.date_end = training_start_alpha + timedelta(days=20)

        grade_list = []
        stage = "Stage 0"
        for idx in range(9):
            randomizer = random.randint(0, 5)
            grade = GRADE[randomizer][0]
            grade_list.append(grade)

            if idx == 0:
                stage = "Stage 1.1"
            elif idx == 1:
                stage = "Stage 1.2"
            elif idx == 2:
                stage = "Stage 1.3"
            elif idx == 3:
                stage = "Stage 2.1"
            elif idx == 4:
                stage = "Stage 2.2"
            elif idx == 5:
                stage = "Stage 2.3"
            elif idx == 6:
                stage = "Stage 3.1"
            elif idx == 7:
                stage = "Stage 3.2"
            elif stage == 8:
                stage = "Stage 3.3"

            if idx <= 7:

                sched_remark = fake.paragraph(nb_sentences=2, variable_nb_sentences=True, ext_word_list=None)
                train_sched = Training_Schedule.objects.create(k9 = k9, date_start = training_start_alpha + timedelta(days=20 * idx + 1),
                                                               date_end = training_start_alpha + timedelta(days=20 * idx + 2), stage = stage, remarks = sched_remark)
                train_sched.save()


        training.stage1_1 = grade_list[0]
        training.stage1_2 = grade_list[1]
        training.stage1_3 = grade_list[2]

        training.stage2_1 = grade_list[3]
        training.stage2_2 = grade_list[4]
        training.stage2_3 = grade_list[5]

        training.stage3_1 = grade_list[6]
        training.stage3_2 = grade_list[7]
        training.stage3_3 = grade_list[8]

        training.remarks = remark
        training.stage = "Finished Training"
        training.save()

        k9.training_status = 'Trained'
        k9.training_level = "Finished Training"
        k9.save()

        print(str(k9))
        print("Grade : " + str(training.grade))

    return None

#Half of K9s are classified
def generate_k9():
    fake = Faker()
    for x in range (0, 300):

        randomizer = random.randint(0, 1)

        name = "?"
        gender = "?"
        if randomizer == 0:
            print("Name : " + fake.first_name_male())
            name = fake.first_name_male()
            print("Gender : Male")
            gender = "Male"
        else:
            print("Name : " + fake.first_name_female())
            name = fake.first_name_female()
            print("Gender : Female")
            gender = "Female"

        print("Color : " + fake.safe_color_name())
        color = fake.safe_color_name()
        print("Breed : " + generate_breed())
        breed = generate_breed()

        generated_date = fake.date_between(start_date="-3y", end_date="-1y")
        date_time = generated_date.strftime("%m/%d/%Y")
        print("Birthdate : " + date_time)


        #TODO Add K9s that are For-deployment and For-Breeding
        #Classifies other K9s
        k9 = K9.objects.create(name = name, breed = breed, sex = gender, color = color, birth_date = generated_date, source = "Procurement")
        k9.save()

        #TODO get supplier and randomize the k9's supplier
        if k9.source == "Procurement":
            contact = "+63" + fake.msisdn()[:10]
            supplier = K9_Supplier.objects.create(name = fake.name(), organization = fake.company(), address = fake.address(), contact_no = contact)
            supplier.save()
            k9.supplier = supplier
            k9.save()

    return None


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>END OF K9 CREATION


def generate_coordinates_ph():

    lat = random.uniform(7.823, 18.579)
    lng = random.uniform(118.975, 125.563)

    return [lat, lng]


def generate_area():

    print("GENERATE AREA FLAG")

    areas = ["National Capital Region", "Ilocos Region", "Cordillera Administrative Region", "Cagayan Valley",
                 "Central Luzon",
                 "Southern Tagalog Mainland", "Southwestern Tagalog Region", "Bicol Region", "Western Visayas",
                 "Central Visayas", "Eastern Visayas",
                 "Zamboanga Peninsula", "Northern Mindanao", "Davao Region", "SOCCSKSARGEN", "Caraga Region",
                 "Bangsamoro Autonomous Region"]

    for item in areas:
        area = Area.objects.create(name = item)
        area.save()


    return None


def generate_location():
    fake = Faker()
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

    if Area.objects.all() is None:
        generate_area()

    area_list = []
    for area in Area.objects.all():
        area_list.append(area)

    for item in CITY:
        print("City : " + item[0])
        print("Place : " + fake.address() + " port")
        place = fake.address() + " port"

        randomizer = random.randint(0, len(area_list) - 1)
        print("Area : " + str(area_list[randomizer]))
        area = area_list[randomizer]


        print("Coordinates : " + str(generate_coordinates_ph()))
        coordinates = generate_coordinates_ph()


        location = Location.objects.create(area = area, place = place, city = item[0], latitude = coordinates[0], longtitude = coordinates[1])
        location.save()
        team = Team_Assignment.objects.create(location = location)
        team.save()

    return None


def generate_event():
    fake = Faker()

    if Area.objects.all() is None:
        generate_area()

    area_list = []
    for area in Area.objects.all():
        area_list.append(area)


    if Location.objects.all() is None:
        generate_location()

    location_list = []
    for location in Location.objects.all():
        location_list.append(location)


    for x in range(0, 150):
        print("Requester : " + fake.company())
        requester = fake.company()
        print("Cell Number : +63" + fake.msisdn()[:10])
        cell =  "+63" + fake.msisdn()[:10]

        randomizer = random.randint(0, 1)

        event_type = "?"
        k9s_required = 0
        if randomizer == 0:
            print("Event Type : Big Event")
            event_type = "Big Event"
            print("Number of K9s. Required : " + str(random.randint(6, 12)))
            k9s_required = random.randint(6, 12)

        else:
            print("Event Type : Small Event")
            event_type = "Small Event"
            print("Number of K9s. Required : " + str(random.randint(1, 5)))
            k9s_required = random.randint(2, 5)

        print("Location : " + fake.address())
        location = fake.address()
        print("City : " + generate_city_ph())
        city = generate_city_ph()
        print("Coordinates : " + str(generate_coordinates_ph()))
        coordinates = generate_coordinates_ph()

        start_date = fake.date_between(start_date="+10d", end_date="+60d")
        #start_date = generated_date.strftime("%m/%d/%Y")
        end_date = start_date + timedelta(days= random.randint(1, 14))
        #end_date = end_date.strftime("%m/%d/%Y")

        #print("Start Date : " + start_date)
        #print("End Date : " + end_date)

        print("Remarks : " + fake.paragraph(nb_sentences=2, variable_nb_sentences=True, ext_word_list=None))
        remarks = fake.paragraph(nb_sentences=2, variable_nb_sentences=True, ext_word_list=None)
        event_name = fake.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None)
        print()

        email = requester.lower() + "@gmail.com"

        randomizer = random.randint(0, len(area_list) - 1)
        print("Area : " + str(area_list[randomizer]))
        area = area_list[randomizer]

        request = Dog_Request.objects.create(requester = requester, location = location, city = city, sector_type = event_type, phone_number = cell, email_address = email, event_name = event_name,
                                             remarks = remarks, area = area, k9s_needed = k9s_required, start_date = start_date, end_date = end_date, latitude = coordinates[0], longtitude = coordinates[1])
        request.save()

        if request.sector_type == "Big Event":
            request.status = "Approved"
            request.save()

    return None

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>END OF Requests and Locations CREATION



def generate_incident():
    fake = Faker()
    for x in range(0, 250):
        if User.objects.filter(position = "Handler") is None:
            generate_user()

        if Location.objects.all() is None:
            generate_location()

        user_list = []
        for user in User.objects.all():
            user_list.append(user)

        location_list = []
        for location in Location.objects.all():
            location_list.append(location)

        TYPE = (
            ('Explosives Related', 'Explosives Related'),
            ('Narcotics Related', 'Narcotics Related'),
            ('Search and Rescue Related', 'Search and Rescue Related'),
            )


        randomizer = random.randint(0, 2)

        type = TYPE[randomizer][0]

        randomizer = random.randint(0, len(user_list) - 1)
        user = user_list[randomizer]
        incident_txt = fake.paragraph(nb_sentences=2, variable_nb_sentences=True, ext_word_list=None)
        print("Incident : " + incident_txt)
        print("Recorded by : " + str(user))

        randomizer = random.randint(0, len(location_list) - 1)
        location = location_list[randomizer]
        print("Location : " + str(location))

        remarks = fake.paragraph(nb_sentences=2, variable_nb_sentences=True, ext_word_list=None)

        date = fake.date_between(start_date="-30y", end_date="-20y")

        incident = Incidents.objects.create(user = user, date = date, incident = incident_txt, location = location, type = type, remarks = remarks)
        incident.save()

    return None

def generate_maritime():
    fake = Faker()
    for x in range(0, 500):
        BOAT_TYPE = (
            ('Domestice Passenger Vessels', 'Domestice Passenger Vessels'),
            ('Motorbancas', 'Motorbancas'),
            ('Fastcrafts', 'Fastcrafts'),
            ('Cruise Ships', 'Cruise Ships'),
            ('Tugboat', 'Tugboat'),
            ('Barge', 'Barge'),
            ('Tanker', 'Tanker')
        )



        if Location.objects.all() is None:
            generate_location()

        location_list = []
        for location in Location.objects.all():
            location_list.append(location)

        randomizer = random.randint(0, len(location_list) - 1)
        location = location_list[randomizer]
        print("Location : " + str(location))

        randomizer = random.randint(0, len(BOAT_TYPE) - 1)
        boat_type = BOAT_TYPE[randomizer][0]
        print("Boat type : " + boat_type)

        date = fake.date_between(start_date="-30y", end_date="-20y")

        passenger_count = random.randint(20, 100)

        maritime = Maritime.objects.create(location = location, boat_type = boat_type, datetime = date, passenger_count = passenger_count)
        maritime.save()

    return None

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>END OF Maritimes and Incidents CREATION

#TODO Fix K9.training_stage set at "Stage 0" regardless of training progress

#ADVANCED POPULATE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#TODO Assign  a number of k9s to ports
#TODO assign a number of k9s to events(take into account the restrictions)


def generate_dogbreed():
   
    arr = ['Belgian Malinois','Dutch Sheperd','German Sheperd','Golden Retriever','Jack Russel','Labrador Retriever']

    temperament_list = ['Friendly', 'Skittish', 'Timid', 'Wild', 'Adventurous']

    for data in arr:
        randomizer = random.randint(0, 4)
        temperament = temperament_list[randomizer]

        Dog_Breed.objects.create(breed=data,sex='Male',life_span=10,temperament=temperament,colors=generate_skin_color(), weight=20,male_height=10,female_height=10,skill_recommendation='NDD',skill_recommendation2='EDD',skill_recommendation3='SAR',litter_number=7,value=15000)
		
    for data2 in arr:
        randomizer = random.randint(0, 4)
        temperament = temperament_list[randomizer]

        Dog_Breed.objects.create(breed=data2,sex='Female',life_span=10,temperament=temperament,colors=generate_skin_color(), weight=20,male_height=10,female_height=10,skill_recommendation='NDD',skill_recommendation2='EDD',skill_recommendation3='SAR',litter_number=7,value=17000)

    return None


def assign_commander_random():

    if Area is None:
        generate_area()
    else:
        areas = Area.objects.all()
        commanders = User.objects.filter(position = "Commander")

        area_list = []
        for area in areas:
            area_list.append(area)

        commander_list = []
        for commander in commanders:
            commander_list.append(commander)

        commander_list = random.sample(commander_list, len(commander_list)-1)

        partnership = zip(commander_list, area_list)

        for item in partnership:
            area = item[1]
            area.commander = item[0]
            area.save()

    return None

def fix_dog_duplicates():

    k9s = K9.objects.all()

    k9_list = []
    for k9 in k9s:
        k9_list.append(k9.name)

    # Get unique names
    k9_list = list(set(k9_list))

    for item in k9_list:
        k9s = K9.objects.filter(name = item)
        ctr = 1
        for k9 in k9s:
            k9.name = k9.name + " " + str(ctr)
            k9.save()

    return None