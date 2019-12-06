from faker import Faker
import random
from datetime import timedelta, datetime, date
from profiles.models import User, Account, Personal_Info, Education
from planningandacquiring.models import K9, K9_Supplier, Dog_Breed
from deployment.models import Area, Location, Dog_Request, Incidents, Maritime, Team_Assignment, K9_Pre_Deployment_Items, \
    K9_Schedule, Team_Dog_Deployed
from django.contrib.auth.models import User as AuthUser
from training.models import Training, Training_Schedule, Training_History
from inventory.models import Miscellaneous, Food, Medicine_Inventory, Medicine, Food_Received_Trail, Food_Subtracted_Trail, Food_Inventory_Count, Medicine_Received_Trail, Medicine_Subtracted_Trail, Medicine_Inventory_Count, Miscellaneous_Received_Trail, Miscellaneous_Subtracted_Trail, Miscellaneous_Inventory_Count
from deployment.models import Daily_Refresher

from unitmanagement.models import PhysicalExam
from itertools import groupby

from deployment.tasks import assign_TL
from django.db.models import Q
import re
'''
For more info on faker.Faker, view https://faker.readthedocs.io/en/latest/index.html

Populate DB process

REPORTS
1.)generate_dogbreed()
    a.)Creates Dog Breed Details

DEPLOYMENT
1.)create_predeployment_inventory()
    a.) Creates Pre Deployment Inventory Items
    b.) Creates Mandatory Vaccines and Prevention
2.)create_teams() - generate_user() first to assign commander
    a.) Creates Areas
    b.) Creates Locations
    c.) Creates Team_assignments
    d.) Assigns Commander

USER-K9
1.)generate_user()
  a.) Creates User
  b.) Creates Personal Info
  c.) Creates Education
  d.) Creates Account
2.) generate_k9()
  a.) Creates K9 (500 procured)
  b.) Creates Supplier
  c.) Assign Capability to 95% of procured k9s
  d.) Assign Handler to 80% of classified k9s
  e.) Complete training for 80% of partnered k9s
    - Creates Training
    - Creates Training_Sched
    - Creates Training_History
  f.) Make 90% of trained k9s "For-Deployment", the other 90% are "For-Breeding"
  g.) Assign 70% of "For-Deployment" k9s to a port
    - Creates Pre_Deployment_Items
    - Creates "Initial Deployment" K9 Schedule
    - Creates "Checkup" K9 Schedule
    - Creates Team Dog Deployed
    - Creates PhysicalExam
    - Assigns TL
'''

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

# START REPORT NECESSITIES
def generate_dogbreed():
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

    arr = ['Belgian Malinois', 'Dutch Sheperd', 'German Sheperd', 'Golden Retriever', 'Jack Russel',
           'Labrador Retriever']

    temperament_list = ['Friendly', 'Skittish', 'Timid', 'Wild', 'Adventurous']
    skill_list = ['EDD', 'NDD', 'SAR']

    for data in arr:
        randomizer = random.randint(0, 4)
        randomizer2 = random.randint(0, 2)
        temperament = temperament_list[randomizer]
        skill = skill_list[randomizer2]

        random_val1 = random.randint(10000, 15000)
        random_val2 = random.randint(15000, 20000)
        litter_val = random.randint(4, 8)

        arr1 = ['EDD', 'NDD', 'SAR']
        arr2 = []

        while len(arr1) != 0:
            randomizer2 = random.randint(0, 2)
            skill1 = skill_list[randomizer2]
            if skill1 in arr1:
                arr1.remove(skill1)
                arr2.append(skill1)

        randomizer = random.randint(0, 18)
        color = COLOR[randomizer][0]
        Dog_Breed.objects.create(breed=data, sex='Male', life_span=10, temperament=temperament,
                                 colors=color, weight=20, male_height=10, female_height=10,
                                 skill_recommendation=arr2[0], skill_recommendation2=arr2[1],
                                 skill_recommendation3=arr2[2], litter_number=litter_val, value=random_val1)

        Dog_Breed.objects.create(breed=data, sex='Female', life_span=10, temperament=temperament,
                                 colors=color, weight=20, male_height=10, female_height=10,
                                 skill_recommendation=arr2[0], skill_recommendation2=arr2[1],
                                 skill_recommendation3=arr2[2], litter_number=litter_val, value=random_val2)
        print("Generated Dog Breed : " + str(data))

    return None
# END REPORT NECESSITIES

# START DEPLOYMENT NECESSITIES
def create_predeployment_inventory():
    randomizer = random.randint(30, 100)
    collar = Miscellaneous.objects.create(miscellaneous="Collar", misc_type="Kennel Supply", uom="pc",
                                          quantity=randomizer, price=199.12)
    randomizer = random.randint(30, 100)
    vest = Miscellaneous.objects.create(miscellaneous="Vest", misc_type="Kennel Supply", uom="pc",
                                        quantity=randomizer, price=900.21)
    randomizer = random.randint(30, 100)
    leash = Miscellaneous.objects.create(miscellaneous="Leash", misc_type="Kennel Supply", uom="pc",
                                         quantity=randomizer, price=230.41)
    randomizer = random.randint(30, 100)
    shipping_crate = Miscellaneous.objects.create(miscellaneous="Shipping Crate", misc_type="Kennel Supply", uom="pc",
                                                  quantity=randomizer, price=1500.24)

    randomizer = random.randint(100, 250)
    food = Food.objects.create(food="Pedigree Sack", foodtype="Adult Dog Food", unit="Sack - 20kg", quantity=randomizer,price=1500)
    
    randomizer = random.randint(100, 250)
    Food.objects.create(food="Pedigree Puppy", foodtype="Puppy Dog Food", unit="kilograms", quantity=randomizer,price=120)
    
    randomizer = random.randint(100, 250)
    Food.objects.create(food="Pedigree", foodtype="Adult Dog Food", unit="kilograms", quantity=randomizer,price=120)
    
    randomizer = random.randint(100, 250)
    Food.objects.create(food="Pedigree Puppy Sack", foodtype="Puppy Dog Food", unit="Sack - 20kg", quantity=randomizer,price=1500)
    
    Food.objects.create(food="Cosi Milk", foodtype="Milk", unit="Box - 1L", quantity=randomizer,price=130)

    randomizer = random.randint(50, 150)
    medicine = Medicine.objects.create(medicine="LC Vit Multivitamins Syrup", med_type="Vitamins", uom="mL", price=149, dose=60)

    randomizer = random.randint(50, 150)
    Medicine.objects.create(medicine="Broncure", med_type="Bottle", uom="mL", price=220, dose=90)
    
    randomizer = random.randint(50, 150)
    Medicine.objects.create(medicine="Refamol", med_type="Capsule", uom="mg", price=32.05,dose=50)
    
    randomizer = random.randint(50, 150)
    Medicine.objects.create(medicine="Parvo Aid", med_type="Tablet", uom="mg", price=25.66, dose=25)
    
    randomizer = random.randint(50, 150)
    Medicine.objects.create(medicine="Papi Doxy", med_type="Bottle", uom="mL", price=173, dose=80)

    randomizer = random.randint(30, 100)
    grooming_kit = Miscellaneous.objects.create(miscellaneous="Grooming Kit", misc_type="Kennel Supply", uom="pc",
                                                quantity=randomizer, price=321.12)
    randomizer = random.randint(30, 100)
    first_aid_kit = Miscellaneous.objects.create(miscellaneous="First Aid Kit", misc_type="Kennel Supply", uom="pc",
                                                 quantity=randomizer, price=211.12)
    randomizer = random.randint(30, 100)
    oral_dextrose = Miscellaneous.objects.create(miscellaneous="Oral Dextrose", misc_type="Kennel Supply", uom="pc",
                                                 quantity=randomizer, price=140.12)
    randomizer = random.randint(30, 100)
    ball = Miscellaneous.objects.create(miscellaneous="Ball", misc_type="Kennel Supply", uom="pc",
                                        quantity=randomizer, price=260.33)

    # Create Mandatory Vaccine and Prevention
    randomizer = random.randint(100, 1000)
    Medicine.objects.create(medicine='Rabies Immune Globulin', med_type='Vaccine', immunization='Anti-Rabies',
                            price=randomizer)

    randomizer = random.randint(100, 1000)
    Medicine.objects.create(medicine='Bronchicine CAe', med_type='Vaccine',
                            immunization='Bordetella Bronchiseptica Bacterin', price=randomizer)

    randomizer = random.randint(100, 1000)
    Medicine.objects.create(medicine='VANGUARD PLUS 5 L4 CV', med_type='Vaccine', immunization='DHPPiL+CV',
                            price=randomizer)

    randomizer = random.randint(100, 1000)
    Medicine.objects.create(medicine='Versican Plus DHPPi/L4', med_type='Vaccine', immunization='DHPPiL4',
                            price=randomizer)

    randomizer = random.randint(100, 1000)
    Medicine.objects.create(medicine='PetArmor Sure Shot 2x', med_type='Preventive', immunization='Deworming',
                            price=randomizer)

    randomizer = random.randint(100, 1000)
    Medicine.objects.create(medicine='Heartgard', med_type='Preventive', immunization='Heartworm', price=randomizer)
    randomizer = random.randint(100, 1000)

    randomizer = random.randint(100, 1000)
    Medicine.objects.create(medicine='Frontline', med_type='Preventive', immunization='Tick and Flea', price=randomizer)

    #VET SUPPLY
    randomizer = random.randint(100, 1000)
    Miscellaneous.objects.create(miscellaneous='Adhesive Bandage',uom='pack', misc_type='Vet Supply', price=randomizer)
    
    randomizer = random.randint(100, 1000)
    Miscellaneous.objects.create(miscellaneous='Face Mask',uom='pack', misc_type='Vet Supply', price=randomizer)
    
    randomizer = random.randint(500, 800)
    Miscellaneous.objects.create(miscellaneous='Cotton Gauze Dressing',uom='pack', misc_type='Vet Supply',price=randomizer)
    
    randomizer = random.randint(300, 600)
    Miscellaneous.objects.create(miscellaneous='Medical Gloves',uom='box', misc_type='Vet Supply', price=randomizer)
    
    randomizer = random.randint(800, 1200)
    Miscellaneous.objects.create(miscellaneous='Surgical Suture',uom='box', misc_type='Vet Supply', price=randomizer)

    randomizer = random.randint(300, 800)
    Miscellaneous.objects.create(miscellaneous='Injection Syringe',uom='pc', misc_type='Vet Supply', price=randomizer)
    
    randomizer = random.randint(500, 1200)
    Miscellaneous.objects.create(miscellaneous='EDTA K2 K3 Blood Tube',uom='tube', misc_type='Vet Supply',price=randomizer)

    print("Generated inventory items")
    return None

def create_teams():
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

    #create areas
    areas = ["National Capital Region", "Ilocos Region", "Cordillera Administrative Region", "Cagayan Valley",
             "Central Luzon",
             "Southern Tagalog Mainland", "Southwestern Tagalog Region", "Bicol Region", "Western Visayas",
             "Central Visayas", "Eastern Visayas",
             "Zamboanga Peninsula", "Northern Mindanao", "Davao Region", "SOCCSKSARGEN", "Caraga Region",
             "Bangsamoro Autonomous Region"]

    for item in areas:
        area = Area.objects.create(name=item)
        area.save()
        print("Area Generated : " + str(area))

    area_list = []
    for area in Area.objects.all():
        area_list.append(area)

    commanders = User.objects.filter(position="Commander")

    commander_list = []
    for commander in commanders:
        commander_list.append(commander)

    commander_list = random.sample(commander_list, len(commander_list) - 1)

    partnership = zip(commander_list, area_list)

    for item in partnership:
        area = item[1]
        area.commander = item[0]
        area.save()
        print("Assigned " + str(item[0]) + " to " + str(item[1]))

    for item in CITY:
        place = fake.address() + " port"

        randomizer = random.randint(0, len(area_list) - 1)
        area = area_list[randomizer]

        lat = random.uniform(7.823, 18.579)
        lng = random.uniform(118.975, 125.563)

        # Create location
        location = Location.objects.create(area = area, place = place, city = item[0], latitude = lat, longtitude = lng)
        location.save()
        # Create team
        team = Team_Assignment.objects.create(location = location)
        team.save()
        print("Generated " + str(team))

    return None

# END DEPLOYMENT NECESSITIES

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
    for x in range(0, 500):

        position = ""

        if ctr <= 429:
            position = "Handler"
        elif ctr >= 430 and ctr <= 460:
            position = "Commander"
        elif ctr >= 461 and ctr <= 479:
            position = "Veterinarian"
        elif ctr == 480 or ctr == 481:
            position = "Operations"
        elif ctr >= 482 and ctr <= 485:
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
            gender = "Male"
        else:
            first_name = fake.first_name_female()
            gender = "Female"

        last_name = fake.last_name()

        generated_date = fake.date_between(start_date="-30y", end_date="-20y")
        birthdate = generated_date.strftime("%m/%d/%Y")
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

        # Create Users
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

        # Create Personal Information
        personal = Personal_Info.objects.create(UserID=user, mobile_number=cellnum, tel_number=phonenum, street=street,
                                                barangay=brngy, city=city, province=province,
                                                mother_name=mother, father_name=father, mother_birthdate=mother_birth,
                                                father_birthdate=father_birth, tin=tin, philhealth=phil)
        personal.save()

        # Create Education
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
        print("Generated " + str(ctr) + " out of 500 users")
    return None

# END USER CREATION

# START K9 CREATION
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

    SKILL = (
        ('NDD', 'NDD'),
        ('EDD', 'EDD'),
        ('SAR', 'SAR')
    )

    GRADE = (
        # ("0", "0"),
        ("75", "75"),
        ("80", "80"),
        ("85", "85"),
        ("90", "90"),
        ("95", "95"),
        ("100", "100"),
    )

    # START CREATE SUPPLIERS
    suppliers = K9_Supplier.objects.all()
    if suppliers.count() == 0:
        for x in range(0, 12):
            contact = "+63" + fake.msisdn()[:10]
            supplier = K9_Supplier.objects.create(name=fake.name(), organization=fake.company(), address=fake.address(),
                                                  contact_no=contact)
            supplier.save()
        suppliers = K9_Supplier.objects.all()
    # END CREATE SUPPLIERS

    # START CREATE PROCURED K9S
    # Initial K9 Count = 500
    idx = 0
    for x in range (0, 500):
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

        generated_date = fake.date_between(start_date="-2y", end_date="-2y")
        # date_time = generated_date.strftime("%m/%d/%Y")

        # Create procured k9s
        k9 = K9.objects.create(name = name, breed = breed, sex = gender, color = color, birth_date = generated_date, source = "Procurement", training_status = "Unclassified")
        k9.save()

        if k9.source == "Procurement":
            try:
                randomizer = random.randint(0, suppliers.count() - 1)
                supplier = K9_Supplier.objects.get(id = randomizer)
                k9.supplier = supplier
                k9.save()
            except: pass
        idx += 1
        print("Generated " + str(idx) + " out of 500 procured k9s")
    # END CREATE PROCURED K9S

    # START ASSIGN CAPABILITY
    k9s = K9.objects.all()
    k9_list = []
    for k9 in k9s:
        k9_list.append(k9)

    # 90% of k9s will be assigned a capability
    classified_k9_sample = random.sample(k9_list, int(len(k9_list) * .95))

    # Assign Capability
    for k9 in classified_k9_sample:
        randomizer = random.randint(0, 2)
        k9.capability = SKILL[randomizer][0]
        k9.training_status = "Classified"
        k9.save()
        print("Assigned capability " + str(SKILL[randomizer][0]) + " to " + str(k9))
    # END ASSIGN CAPABILITY

    # START ASSIGN HANDLER
    users = User.objects.filter(position="Handler")

    user_id_list = []
    for user in users:
        user_id_list.append(user.id)

    partnership_k9_sample = random.sample(classified_k9_sample, int(len(classified_k9_sample) * .80))
    if len(partnership_k9_sample) < len(user_id_list):
        user_sample = random.sample(user_id_list, len(partnership_k9_sample))  # user sample now have the same length as k9 sample (possible issue here if classified k9s are more than handlers)
    else:
        user_sample = user_id_list

    partnership = zip(partnership_k9_sample, user_sample)

    for item in partnership:
        k9 = K9.objects.get(id=item[0].id)
        user = User.objects.get(id=item[1])

        k9.handler = user
        k9.training_status = 'On-Training'
        k9.save()

        user.partnered = True
        user.save()
        print("Assigned Handler " + str(user) + " to " + str(k9))
    # END ASSIGN HANDLER

    # START CREATE TRAINING
    training_k9 = K9.objects.filter(training_status = 'On-Training')
    training_k9_list = []
    for k9 in training_k9:
        training_k9_list.append(k9)

    training_k9_sample = random.sample(training_k9_list, int(len(training_k9_list) * .80))

    for k9 in training_k9_sample:
        #create training history
        fake_date = fake.date_between(start_date='-5y', end_date='today')
        Training_History.objects.create(k9=k9,handler=k9.handler,date=fake_date)

        birthdate = k9.birth_date

        training_start_alpha = datetime.combine(birthdate, datetime.min.time())
        training_start_alpha = training_start_alpha + timedelta(days=365)
        try:
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
                elif idx == 8:
                    stage = "Stage 3.3"

                sched_remark = fake.paragraph(nb_sentences=2, variable_nb_sentences=True, ext_word_list=None)
                train_sched = Training_Schedule.objects.create(k9 = k9, date_start = training_start_alpha + timedelta(days=20 * idx + 1),
                                                                date_end = training_start_alpha + timedelta(days=20 * idx + 2), stage = stage, remarks = sched_remark)
                # train_sched.save()

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
            
            start_date = datetime(2019,1,1)
            end_date = datetime(2019,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            training.date_finished = f_date
            training.save()

            k9.training_status = 'Trained'
            k9.training_level = "Finished Training"
            k9.serial_number = 'SN-' + str(k9.id) + '-' + str(datetime.now().year)
            k9.trained = "Trained"
            k9.save()
            print("Created Training for " + str(k9))
        except:
            pass

    # END CREATE TRAINING

    # START BREEDING_or_DEPLOYMENT
    trained_k9s = K9.objects.filter(training_status="Trained").filter(training_level="Finished Training")
    k9_id_list = []
    for k9 in trained_k9s:
        k9_id_list.append(k9.id)
    for_breeding_k9_sample = random.sample(k9_id_list, int(len(k9_id_list) * .90))  # 90% of all trained k9s
    for_deployment_k9_sample = random.sample(for_breeding_k9_sample, int(len(for_breeding_k9_sample) * .90))  # 90% of all breeding k9s
    for id in for_deployment_k9_sample:
        try:
            for_breeding_k9_sample.remove(id)
        except:
            pass

    for id in for_deployment_k9_sample:
        try:
            k9 = K9.objects.get(id=id)
            k9.training_status = "For-Deployment"
            k9.status = "Working Dog"
            k9.birth_date = k9.birth_date - timedelta(days = 2190)
            k9.save()
            print(str(k9) + " is now For-Deployment")
        except:
            pass

    for id in for_breeding_k9_sample:
        try:
            k9 = K9.objects.get(id=id)
            k9.training_status = "For-Breeding"
            k9.status = "Working Dog"
            handler = k9.handler
            k9.handler = None
            handler.partnered = False
            k9.save()
            print(str(k9) + " is now For-Breeding")
        except:
            pass
    # END BREEDING_or_DEPLOYMENT

    #START CREATE PRE DEPLOYMENT SCHEDULES
    for_deployment_k9s = K9.objects.filter(training_status = "For-Deployment").filter(status = "Working Dog")
    k9_list = []
    for k9 in  for_deployment_k9s:
        k9_list.append(k9)
    for_deployment_k9_sample = random.sample(k9_list, int(len(k9_list) * .70))

    team_assign = Team_Assignment.objects.all()

    sublist_for_deployment_k9_sample = [for_deployment_k9_sample[i:i+3] for i in range(0, len(for_deployment_k9_sample), 3)]
    vets = User.objects.filter(position="Veterinarian")
    vet_list = []
    for vet in vets:
        vet_list.append(vet)

    idx = 0
    for team in team_assign:
        if idx < len(sublist_for_deployment_k9_sample) - 1:
            sublist = sublist_for_deployment_k9_sample[idx]
            randomizer = random.randint(1, 45)
            gen_birthdate = fake.date_between(start_date="-2y", end_date="-2y")
            deployment_date = gen_birthdate + timedelta(days=495 + randomizer)

            for k9 in sublist:
                deploy = K9_Schedule.objects.create(team=team, k9=k9, status="Initial Deployment",
                                                   date_start=deployment_date)
                K9_Schedule.objects.create(team=team, k9=k9, status="Checkup",
                                           date_start=deployment_date - timedelta(days=7))
                K9_Pre_Deployment_Items.objects.create(k9=k9, initial_sched=deploy, status="Done")
                Team_Dog_Deployed.objects.create(team_assignment=team, k9=k9,
                                                          date_added=deployment_date + timedelta(days=random.randint(1, 6)))
                randomizer = random.randint(0, len(vet_list) - 1)
                PhysicalExam.objects.create(dog = k9, veterinary = vet_list[randomizer], heart_rate = 32, respiratory_rate = 32, temperature = 32, weight = 32, cleared = True)

                if k9.capability == "SAR":
                    team.SAR_deployed += 1
                elif k9.capability == "NDD":
                    team.NDD_deployed += 1
                elif k9.capability == "EDD":
                    team.EDD_deployed += 1
                team.save()
                k9.assignment = team.team
                k9.save()
                print(str(k9) + " is deployed to " + str(team))

            assign_TL(team)
            idx += 1
        else:
            break


    #END PRE DEPLOYMENT SCHEDULES

    return None
# END K9 CREATION

# START MISC

def generate_requests():
    fake = Faker()

    pre_titles = ['An Evening of ', 'A Night to Celebrate ', 'A Celebration of Life and ', 'The Wonders of '
                  , 'In Observance of ', 'In Recognition of ', 'In Commemoration of ', 'Meetup for '
                  , 'The Future of ', 'The Technology of ', 'A Date with ']
    post_titles = [' Conference', ' Con', ' Competition', ' Hackathon', ' Fundraiser', ' Charity', ' Party'
                   , ' Bash', ' Ball', ' Gala', ' Shindig', 'athon', ' Celebration', ' Affair'
                   , ' Ceremony', ' Awards', ' Event of the Year!', ' Jubilee', ' Performance', ' Blast'
                   , ' Blowout', ' Rite', ' Show', ' Meetup', ' for Health', ' Workshop', ' Research Event'
                   , ' Summit', ' Course', ' Symposium', ' Town Hall Meeting', ' Games', ' Expo', ': The Event']

    location_list = []
    for location in Location.objects.all():
        location_list.append(location)

    area_list = []
    for area in Area.objects.all():
        area_list.append(area)

    for x in range(0, 150):
        requester = fake.company()
        cell = "+63" + fake.msisdn()[:10]

        randomizer = random.randint(0, 1)

        event_type = "?"
        k9s_required = 0
        if randomizer == 0:
            event_type = "Big Event"
            k9s_required = random.randint(5, 10)

        else:
            event_type = "Small Event"
            k9s_required = random.randint(2, 4)

        location = fake.address()
        city = generate_city_ph()

        lat = random.uniform(7.823, 18.579)
        lng = random.uniform(118.975, 125.563)

        start_date = fake.date_between(start_date="+10d", end_date="+60d")
        end_date = start_date + timedelta(days=random.randint(1, 14))

        remarks = fake.paragraph(nb_sentences=2, variable_nb_sentences=True, ext_word_list=None)
        event_name = fake.word()

        randomizer = random.randint(0, 1)

        if randomizer == 0:
            randomizer = random.randint(0, len(pre_titles) - 1)
            event_name = str(pre_titles[randomizer]) + event_name.capitalize()
        else:
            randomizer = random.randint(0, len(post_titles) - 1)
            event_name = event_name.capitalize() + str(post_titles[randomizer])

        email = requester.lower() + "@gmail.com"

        randomizer = random.randint(0, len(area_list) - 1)
        area = area_list[randomizer]

        request = Dog_Request.objects.create(requester=requester, location=location, city=city, sector_type=event_type,
                                             phone_number=cell, email_address=email, event_name=event_name,
                                             remarks=remarks, area=area, k9s_needed=k9s_required, start_date=start_date,
                                             end_date=end_date, latitude=lat, longtitude=lng)
        request.save()
        print("Event: " + event_name + ". " + str(x) + "/150 events")

        if request.sector_type == "Big Event":
            request.status = "Approved"
            request.save()

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

        location_list = []
        for location in Location.objects.all():
            location_list.append(location)

        randomizer = random.randint(0, len(location_list) - 1)
        location = location_list[randomizer]
        print("Location : " + str(location))

        randomizer = random.randint(0, len(BOAT_TYPE) - 1)
        boat_type = BOAT_TYPE[randomizer][0]
        print("Boat type : " + boat_type)

        date = fake.date_between(start_date="-10y", end_date="-5y")

        time = fake.time_object(end_datetime=None)

        # TODO Generate Time

        passenger_count = random.randint(20, 100)

        maritime = Maritime.objects.create(location = location, boat_type = boat_type, date = date, time = time, passenger_count = passenger_count)

    return None


# END MISC

#GENERATE PHYSICAL COUNT, RECEIVED, SUBTRACTED
def generate_inventory_trail():
    fake = Faker()
    admin = User.objects.filter(position='Administrator')
    admin = list(admin) #food received & count by admin
    
    vet = User.objects.filter(position='Veterinarian')
    vet = list(vet)
    # DATE OF THIS YEAR - 2019
    # FOOD
    food = Food.objects.all()
    #food = Food.objects.filter(foodtype='Milk')
    for data in food:
        #FOOD RECEIVED TRAIL
        for i in range(5):
            start_date = datetime(2019,1,1)
            end_date = datetime(2019,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            choice = random.choice(admin)
            randomizer = random.randint(50, 150)
            new_q = data.quantity+randomizer
            print(data,data.quantity,new_q)
            Food_Received_Trail.objects.create(inventory=data, user=choice,old_quantity=data.quantity, quantity=new_q, date_received=f_date)
            data.quantity = new_q
            data.save()

        #FOOD SUBTRACT TRAIL
        for i in range(3):
            start_date = datetime(2019,1,1)
            end_date = datetime(2019,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            randomizer = random.randint(0, 50)
            new_q = data.quantity-randomizer
            if new_q < 0:
                new_q = 0
            print(data,data.quantity,new_q)
            Food_Subtracted_Trail.objects.create(inventory=data, old_quantity=data.quantity, quantity=new_q,date_subtracted=f_date)
            data.quantity = new_q
            data.save()

        #FOOD PHYSICAL COUNT
        for i in range(3):
            start_date = datetime(2019,1,1)
            end_date = datetime(2019,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            randomizer = random.randint(100, 500)
            choice = random.choice(admin)
            new_q = randomizer
            print(data,data.quantity,new_q)
            Food_Inventory_Count.objects.create(inventory=data, user=choice, old_quantity=data.quantity, quantity=new_q,date_counted=f_date)
            data.quantity = new_q
            data.save()
            
    # MISC
    misc = Miscellaneous.objects.all()
    for data in misc:
        #MISCELLANEOUS RECEIVED TRAIL
        for i in range(5):
            start_date = datetime(2019,1,1)
            end_date = datetime(2019,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            choice = random.choice(admin)
            randomizer = random.randint(50, 150)
            new_q = data.quantity+randomizer
            print(data,data.quantity,new_q)
            Miscellaneous_Received_Trail.objects.create(inventory=data, user=choice,old_quantity=data.quantity, quantity=new_q, date_received=f_date)
            data.quantity = new_q
            data.save()

        #MISCELLANEOUS SUBTRACT TRAIL
        for i in range(3):
            start_date = datetime(2019,1,1)
            end_date = datetime(2019,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            randomizer = random.randint(0, 50)
            new_q = data.quantity-randomizer
            if new_q < 0:
                new_q = 0
            print(data,data.quantity,new_q)
            Miscellaneous_Subtracted_Trail.objects.create(inventory=data, old_quantity=data.quantity, quantity=new_q,date_subtracted=f_date)
            data.quantity = new_q
            data.save()

        #MISCELLANEOUS PHYSICAL COUNT
        for i in range(3):
            start_date = datetime(2019,1,1)
            end_date = datetime(2019,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            randomizer = random.randint(100, 500)
            choice = random.choice(admin)
            new_q = randomizer
            print(data,data.quantity,new_q)
            Miscellaneous_Inventory_Count.objects.create(inventory=data, user=choice, old_quantity=data.quantity, quantity=new_q,date_counted=f_date)
            data.quantity = new_q
            data.save()

    # MED
    med = Medicine_Inventory.objects.all()
    for data in med:
        #MEDICINE RECEIVED TRAIL
        for i in range(5):
            start_date = datetime(2019,1,1)
            end_date = datetime(2019,12,31)
            exp_date = datetime(2023,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            choice = random.choice(admin)
            randomizer = random.randint(50, 150)
            new_q = data.quantity+randomizer
            print(data,data.quantity,new_q)
            Medicine_Received_Trail.objects.create(inventory=data, user=choice,old_quantity=data.quantity, quantity=new_q, date_received=f_date,expiration_date=exp_date,status='Done')
            data.quantity = new_q
            data.save()

        #MEDICINE SUBTRACT TRAIL
        for i in range(3):
            start_date = datetime(2019,1,1)
            end_date = datetime(2019,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            randomizer = random.randint(0, 50)
            new_q = data.quantity-randomizer
            if new_q < 0:
                new_q = 0
            print(data,data.quantity,new_q)
            Medicine_Subtracted_Trail.objects.create(inventory=data, old_quantity=data.quantity, quantity=new_q,date_subtracted=f_date)
            data.quantity = new_q
            data.save()

        #MEDICINE PHYSICAL COUNT
        for i in range(3):
            start_date = datetime(2019,1,1)
            end_date = datetime(2019,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            randomizer = random.randint(100, 500)
            choice = random.choice(admin)
            new_q = randomizer
            print(data,data.quantity,new_q)
            Medicine_Inventory_Count.objects.create(inventory=data, user=choice, old_quantity=data.quantity, quantity=new_q,date_counted=f_date)
            data.quantity = new_q
            data.save()

    # DATE OF LAST YEAR - 2018
    # FOOD
    food = Food.objects.all()
    for data in food:
        #FOOD RECEIVED TRAIL
        for i in range(5):
            start_date = datetime(2018,1,1)
            end_date = datetime(2018,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            choice = random.choice(admin)
            randomizer = random.randint(50, 150)
            new_q = data.quantity+randomizer
            print(data,data.quantity,new_q)
            Food_Received_Trail.objects.create(inventory=data, user=choice,old_quantity=data.quantity, quantity=new_q, date_received=f_date)
            data.quantity = new_q
            data.save()

        #FOOD SUBTRACT TRAIL
        for i in range(3):
            start_date = datetime(2018,1,1)
            end_date = datetime(2018,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            randomizer = random.randint(0, 50)
            new_q = data.quantity-randomizer
            if new_q < 0:
                new_q = 0
            print(data,data.quantity,new_q)
            Food_Subtracted_Trail.objects.create(inventory=data, old_quantity=data.quantity, quantity=new_q,date_subtracted=f_date)
            data.quantity = new_q
            data.save()

        #FOOD PHYSICAL COUNT
        for i in range(3):
            start_date = datetime(2018,1,1)
            end_date = datetime(2018,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            randomizer = random.randint(100, 500)
            choice = random.choice(admin)
            new_q = randomizer
            print(data,data.quantity,new_q)
            Food_Inventory_Count.objects.create(inventory=data, user=choice, old_quantity=data.quantity, quantity=new_q,date_counted=f_date)
            data.quantity = new_q
            data.save()
            
    # MISC
    misc = Miscellaneous.objects.all()
    for data in misc:
        #MISCELLANEOUS RECEIVED TRAIL
        for i in range(5):
            start_date = datetime(2018,1,1)
            end_date = datetime(2018,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            choice = random.choice(admin)
            randomizer = random.randint(50, 150)
            new_q = data.quantity+randomizer
            print(data,data.quantity,new_q)
            Miscellaneous_Received_Trail.objects.create(inventory=data, user=choice,old_quantity=data.quantity, quantity=new_q, date_received=f_date)
            data.quantity = new_q
            data.save()

        #MISCELLANEOUS SUBTRACT TRAIL
        for i in range(3):
            start_date = datetime(2018,1,1)
            end_date = datetime(2018,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            randomizer = random.randint(0, 50)
            new_q = data.quantity-randomizer
            if new_q < 0:
                new_q = 0
            print(data,data.quantity,new_q)
            Miscellaneous_Subtracted_Trail.objects.create(inventory=data, old_quantity=data.quantity, quantity=new_q,date_subtracted=f_date)
            data.quantity = new_q
            data.save()

        #MISCELLANEOUS PHYSICAL COUNT
        for i in range(3):
            start_date = datetime(2018,1,1)
            end_date = datetime(2018,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            randomizer = random.randint(100, 500)
            choice = random.choice(admin)
            new_q = randomizer
            print(data,data.quantity,new_q)
            Miscellaneous_Inventory_Count.objects.create(inventory=data, user=choice, old_quantity=data.quantity, quantity=new_q,date_counted=f_date)
            data.quantity = new_q
            data.save()

    # MED
    med = Medicine_Inventory.objects.all()
    for data in med:
        #MEDICINE RECEIVED TRAIL
        for i in range(5):
            start_date = datetime(2018,1,1)
            end_date = datetime(2018,12,31)
            exp_date = datetime(2023,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            choice = random.choice(admin)
            randomizer = random.randint(50, 150)
            new_q = data.quantity+randomizer
            print(data,data.quantity,new_q)
            Medicine_Received_Trail.objects.create(inventory=data, user=choice,old_quantity=data.quantity, quantity=new_q, date_received=f_date,expiration_date=exp_date,status='Done')
            data.quantity = new_q
            data.save()

        #MEDICINE SUBTRACT TRAIL
        for i in range(3):
            start_date = datetime(2018,1,1)
            end_date = datetime(2018,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            randomizer = random.randint(0, 50)
            new_q = data.quantity-randomizer
            if new_q < 0:
                new_q = 0
            print(data,data.quantity,new_q)
            Medicine_Subtracted_Trail.objects.create(inventory=data, old_quantity=data.quantity, quantity=new_q,date_subtracted=f_date)
            data.quantity = new_q
            data.save()

        #MEDICINE PHYSICAL COUNT
        for i in range(3):
            start_date = datetime(2018,1,1)
            end_date = datetime(2018,12,31)
            f_date = fake.date_between(start_date=start_date, end_date=end_date)
            randomizer = random.randint(100, 500)
            choice = random.choice(admin)
            new_q = randomizer
            print(data,data.quantity,new_q)
            Medicine_Inventory_Count.objects.create(inventory=data, user=choice, old_quantity=data.quantity, quantity=new_q,date_counted=f_date)
            data.quantity = new_q
            data.save()

def generate_daily_refresher():
    fake = Faker()
 
    k9 = K9.objects.exclude(assignment='None').exclude(handler=None).exclude(serial_number='Unassigned Serial Number')
    k9_list = list(k9) 
    k9_sample = random.sample(k9_list, int(len(k9_list) * .15))
    for data in k9_sample:
        for i in range(2):
            start_date = datetime(2019,1,1)
            end_date = datetime(2019,12,31)
            
            choice = random.choice(k9_list)

            mar = ['MARSEC','MARLEN','MARSAR','MAREP']
            mar = random.choice(mar)

            port_plant = random.randint(1, 3)
            port_find = random.randint(0, port_plant)
            building_plant = random.randint(1, 3)
            building_find = random.randint(0, building_plant)
            vehicle_plant = random.randint(1, 3)
            vehicle_find = random.randint(0, vehicle_plant)
            baggage_plant = random.randint(1, 3)
            baggage_find = random.randint(0, baggage_plant)
            others_plant = random.randint(1, 3)
            others_find = random.randint(0, others_plant)
            
            port_date = fake.date_time_between(start_date=start_date, end_date="now", tzinfo=None)
            port_hour = int(port_date.time().hour)
            port_date = port_date - timedelta(hours=port_hour)

            port_time = port_date.time()

            building_date = fake.date_time_between(start_date=start_date, end_date="now", tzinfo=None)
            building_hour = int(building_date.time().hour)
            building_date = building_date - timedelta(hours=building_hour)

            building_time = building_date.time()

            vehicle_date = fake.date_time_between(start_date=start_date, end_date="now", tzinfo=None)
            vehicle_hour = int(vehicle_date.time().hour)
            vehicle_date = vehicle_date - timedelta(hours=vehicle_hour)

            vehicle_time = vehicle_date.time()

            baggage_date = fake.date_time_between(start_date=start_date, end_date="now", tzinfo=None)
            baggage_hour = int(baggage_date.time().hour)
            baggage_date = baggage_date - timedelta(hours=baggage_hour)

            baggage_time = baggage_date.time()

            others_date = fake.date_time_between(start_date=start_date, end_date="now", tzinfo=None)
            others_hour = int(others_date.time().hour)
            others_date = others_date - timedelta(hours=others_hour)

            others_time = others_date.time()

            dr = Daily_Refresher.objects.create(k9=choice,handler=choice.handler,date=port_date,morning_feed_cups=2,evening_feed_cups=2,on_leash=True,off_leash=True,obstacle_course=True,panelling=True, mar = mar, port_plant=port_plant, port_find=port_find, port_time=port_time, building_plant=building_plant,  building_find=building_find, building_time=building_time, vehicle_plant=vehicle_plant,  vehicle_find=vehicle_find, vehicle_time=vehicle_time, baggage_plant=baggage_plant,  baggage_find=baggage_find, baggage_time=baggage_time, others_plant=others_plant, others_find=others_find, others_time=others_time)

            print('DR'+str(i), dr.k9, dr.rating)
    
def generate_location_incident():
    fake = Faker()
    ta = Team_Assignment.objects.exclude(team_leader=None)
    ta_list = list(ta) 
    ta_sample = random.sample(ta_list, int(len(ta_list) * .25))
    user = User.objects.all()
    user_list = list(user) 

    incident_type = ['Explosives Related', 'Narcotics Related', 'Search and Rescue Related', 'Others']

    explosive = ['Bombing in Mall', 'Bombing in Airport', 'Bombing at Road', 'Terrorist Bombing']
    narcotics = ['Drug Bust', 'Airport Drug Traffic', 'Drug Trade', 'Drug Use at Mall']
    search = ['Landslide', 'Typhoon', 'Hurricane', 'Kidnapping', 'Arson', 'Earthquake']
    others = ['Attack', 'Bodyguard Duty', 'Security Duty']
    boat = ['Domestice Passenger Vessels', 'Motorbancas', 'Fastcrafts', 'Cruise Ships', 'Tugboat', 'Barge','Tanker']
    event = ['Big Event', 'Small Event']
    
    pre_titles = ['An Evening of ', 'A Night to Celebrate ', 'A Celebration of Life and ', 'The Wonders of ', 'In Observance of ', 'In Recognition of ', 'In Commemoration of ', 'Meetup for ', 'The Future of ', 'The Technology of ', 'A Date with ']
    post_titles = [' Conference', ' Con', ' Competition', ' Hackathon', ' Fundraiser', ' Charity', ' Party', ' Bash', ' Ball', ' Gala', ' Shindig', 'athon', ' Celebration', ' Affair', ' Ceremony', ' Awards', ' Event of the Year!', ' Jubilee', ' Performance', ' Blast', ' Blowout', ' Rite', ' Show', ' Meetup', ' for Health', ' Workshop', ' Research Event', ' Summit', ' Course', ' Symposium', ' Town Hall Meeting', ' Games', ' Expo', ': The Event']


    loc = []
    tl = []
    for ta in ta:
        if ta.location:
            loc.append(ta.location)
        if ta.team_leader:
            tl.append(ta.team_leader)

    start_date = datetime(2019,1,1)
    end_date = datetime(2019,12,31)

    for data in ta_sample:
        for i in range(10):
            f_date = fake.date_time_between(start_date=start_date, end_date=end_date, tzinfo=None)
            i_type = random.choice(incident_type)
            i_loc = random.choice(loc)
            i_tl = random.choice(tl)
            if i_type == 'Explosives Related':
                i_inc = random.choice(explosive) 
                i_rem = 'Explosive Remarks Here'
            elif i_type == 'Narcotics Related':
                i_inc = random.choice(narcotics)
                i_rem = 'Narcotics Remarks Here'
            elif i_type == 'Search and Rescue Related':
                i_inc = random.choice(search)
                i_rem = 'Search and Rescue Remarks Here'
            elif i_type == 'Others':
                i_inc = random.choice(others)
                i_rem = 'Other Remarks Here'
            
            # Incidents.objects.create(user=i_tl,date=f_date.date(),incident=i_inc,location=i_loc,type=i_type,remarks=i_rem)
            
            m_boat = random.choice(boat)
            p_count = random.randint(50, 150)

            # Maritime.objects.create(location=i_loc, boat_type=m_boat, date=f_date.date(), time=f_date.time(), passenger_count=p_count)
            # print(f_date,i_type,i_tl,i_loc,i_inc)

            city = generate_city_ph()
            pre_t = random.choice(pre_titles)
            post_t = random.choice(post_titles)
            e = random.choice(event)
            cellnum = fake.msisdn()[:10]
            u = random.choice(user_list)
            email = u.lastname.lower() + "@gmail.com"
            lat = random.uniform(7.823, 18.579)
            lng = random.uniform(118.975, 125.563)
            needed = random.randint(3, 10)
            deployed = random.randint(1, needed)

            s_date = datetime(2019,1,1)
            e_date = datetime(2019,6,30)

            ss_date = datetime(2019,7,1)
            ee_date = datetime(2019,12,10)

            sf_date = fake.date_between(start_date=start_date, end_date=end_date)
            ef_date = fake.date_between(start_date=start_date, end_date=end_date)
            
            s_loc = str(i_loc)
            place = s_loc.replace('port', '')
            Dog_Request.objects.create(requester=str(u),event_name=pre_t+post_t,location=place,city=city,sector_type=e,phone_number=cellnum,email_address=email,area=i_loc.area,k9s_needed=needed,k9s_deployed=deployed,status='Done',longtitude=lng,latitude=lat,team_leader=i_tl, start_date=sf_date, end_date=ef_date,remarks='No remarks')
            


       

'''
TODO

Create Incidents
Create Parents (Use For-Breeding K9s)
Create Litter
Create K9_mated
Create Health (Specially for K9s that have reach deployment/breeding decision)
Create Daily Refreshers
Create Budgeting Stuff

VaccineUsed Record for Procured K9s (Date of vaccination lang kailangan + Name of Diseases)4 diseases
Remove handlers on For-Breeding K9s, then status is unpartnered
Fix duplicate Names on k9s
Add K9(s) on final stage of training
Schedule K9s to request
Other Report stuff
'''
