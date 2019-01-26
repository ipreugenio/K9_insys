# Generated by Django 2.1a1 on 2018-11-23 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=200, verbose_name='serial_number')),
                ('email_address', models.EmailField(max_length=200, verbose_name='email_address')),
                ('password', models.CharField(max_length=200, verbose_name='password')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_education', models.CharField(max_length=200, verbose_name='primary_education')),
                ('secondary_education', models.CharField(max_length=200, verbose_name='secondary_education')),
                ('tertiary_education', models.CharField(max_length=200, verbose_name='tertiary_education')),
                ('pe_schoolyear', models.CharField(max_length=200, verbose_name='pe_schoolyear')),
                ('se_schoolyear', models.CharField(max_length=200, verbose_name='se_schoolyear')),
                ('te_schoolyear', models.CharField(max_length=200, verbose_name='te_schoolyear')),
                ('pe_degree', models.CharField(max_length=200, verbose_name='pe_degree')),
                ('se_degree', models.CharField(max_length=200, verbose_name='pe_degree')),
                ('te_degree', models.CharField(max_length=200, verbose_name='pe_degree')),
            ],
        ),
        migrations.CreateModel(
            name='Personal_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=200, verbose_name='mobile_number')),
                ('tel_number', models.CharField(max_length=200, verbose_name='tel_number')),
                ('street', models.CharField(max_length=200, verbose_name='street')),
                ('barangay', models.CharField(max_length=200, verbose_name='barangay')),
                ('city', models.CharField(choices=[('Alaminos', 'Alaminos'), ('Angeles', 'Angeles'), ('Antipolo', 'Antipolo'), ('Bacolod', 'Bacolod'), ('Bacoor', 'Bacoor'), ('Bago', 'Bago'), ('Baguio', 'Baguio'), ('Bais', 'Bais'), ('Balanga', 'Balanga'), ('Batac', 'Batac'), ('Batangas', 'Batangas'), ('Bayawan', 'Bayawan'), ('Baybay', 'Baybay'), ('Bayugan', 'Bayugan'), ('Biñan', 'Biñan'), ('Bislig', 'Bislig'), ('Bogo', 'Bogo'), ('Borongan', 'Borongan'), ('Butuan', 'Butuan'), ('Cabadbaran', 'Cabadbaran'), ('Cabanatuan', 'Cabanatuan'), ('Cabuyao', 'Cabuyao'), ('Cadiz', 'Cadiz'), ('Cagayan de Oro', 'Cagayan de Oro'), ('Calamba', 'Calamba'), ('Calapan', 'Calapan'), ('Calbayog', 'Calbayog'), ('Caloocan', 'Caloocan'), ('Candon', 'Candon'), ('Canlaon', 'Canlaon'), ('Carcar', 'Carcar'), ('Catbalogan', 'Catbalogan'), ('Cauayan', 'Cauayan'), ('Cavite', 'Cavite'), ('Cebu', 'Cebu'), ('Cotabato', 'Cotabato'), ('Dagupan', 'Dagupan'), ('Danao', 'Danao'), ('Dapitan', 'Dapitan'), ('Dasmariñas', 'Dasmariñas'), ('Davao', 'Davao'), ('Digos', 'Digos'), ('Dipolog', 'Dipolog'), ('Dumaguete', 'Dumaguete'), ('El Salvador', 'El Salvador'), ('Escalante', 'Escalante'), ('Gapan', 'Gapan'), ('General Santos', 'General Santos'), ('General Trias', 'General Trias'), ('Gingoog', 'Gingoog'), ('Guihulngan', 'Guihulngan'), ('Himamaylan', 'Himamaylan'), ('Ilagan', 'Ilagan'), ('Iligan', 'Iligan'), ('Iloilo', 'Iloilo'), ('Imus', 'Imus'), ('Iriga', 'Iriga'), ('Isabela', 'Isabela'), ('Kabankalan', 'Kabankalan'), ('Kidapawan', 'Kidapawan'), ('Koronadal', 'Koronadal'), ('La Carlota', 'La Carlota'), ('Lamitan', 'Lamitan'), ('Laoag', 'Laoag'), ('Lapu‑Lapu', 'Lapu‑Lapu'), ('Las Piñas', 'Las Piñas'), ('Legazpi', 'Legazpi'), ('Ligao', 'Ligao'), ('Lipa', 'Lipa'), ('Lucena', 'Lucena'), ('Maasin', 'Maasin'), ('Mabalacat', 'Mabalacat'), ('Makati', 'Makati'), ('Malabon', 'Malabon'), ('Malaybalay', 'Malaybalay'), ('Malolos', 'Malolos'), ('Mandaluyong', 'Mandaluyong'), ('Mandaue', 'Mandaue'), ('Manila', 'Manila'), ('Marawi', 'Marawi'), ('Marikina', 'Marikina'), ('Masbate', 'Masbate'), ('Mati', 'Mati'), ('Meycauayan', 'Meycauayan'), ('Muñoz', 'Muñoz'), ('Muntinlupa', 'Muntinlupa'), ('Naga - Camarines Sur', 'Naga - Camarines Sur'), ('Naga - Cebu', 'Naga - Cebu'), ('Navotas', 'Navotas'), ('Olongapo', 'Olongapo'), ('Ormoc', 'Ormoc'), ('Oroquieta', 'Oroquieta'), ('Ozamiz', 'Ozamiz'), ('Pagadian', 'Pagadian'), ('Palayan', 'Palayan'), ('Panabo', 'Panabo'), ('Parañaque', 'Parañaque'), ('Pasay', 'Pasay'), ('Pasig', 'Pasig'), ('Passi', 'Passi'), ('Puerto Princesa', 'Puerto Princesa'), ('Quezon', 'Quezon'), ('Roxas', 'Roxas'), ('Sagay', 'Sagay'), ('Samal', 'Samal'), ('San Carlos - Negros Occidental', 'San Carlos - Negros Occidental'), ('San Carlos - Pangasinan', 'San Carlos - Pangasinan'), ('San Fernando - La Union', 'San Fernando - La Union'), ('San Fernando - Pampanga', 'San Fernando - Pampanga'), ('San Jose', 'San Jose'), ('San Jose del Monte', 'San Jose del Monte'), ('San Juan', 'San Juan'), ('San Pablo', 'San Pablo'), ('San Pedro', 'San Pedro'), ('Santa Rosa', 'Santa Rosa'), ('Santiago', 'Santiago'), ('Silay', 'Silay'), ('Sipalay', 'Sipalay'), ('Sorsogon', 'Sorsogon'), ('Surigao', 'Surigao'), ('Tabaco', 'Tabaco'), ('Tabuk', 'Tabuk'), ('Tacloban', 'Tacloban'), ('Tacurong', 'Tacurong'), ('Tagaytay', 'Tagaytay'), ('Tagbilaran', 'Tagbilaran'), ('Taguig', 'Taguig'), ('Tagum', 'Tagum'), ('Talisay - Cebu', 'Talisay - Cebu'), ('Talisay - Negros Occidental', 'Talisay - Negros Occidental'), ('Tanauan', 'Tanauan'), ('Tandag', 'Tandag'), ('Tangub', 'Tangub'), ('Tanjay', 'Tanjay'), ('Tarlac', 'Tarlac'), ('Tayabas', 'Tayabas'), ('Toledo', 'Toledo'), ('Trece Martires', 'Trece Martires'), ('Tuguegarao', 'Tuguegarao'), ('Urdaneta', 'Urdaneta'), ('Valencia', 'Valencia'), ('Valenzuela', 'Valenzuela'), ('Victorias', 'Victorias'), ('Vigan', 'Vigan'), ('Zamboanga', 'Zamboanga')], default='None', max_length=100, verbose_name='city')),
                ('province', models.CharField(max_length=200, verbose_name='province')),
                ('mother_name', models.CharField(max_length=200, verbose_name='mother_name')),
                ('mother_birthdate', models.DateField(max_length=200, verbose_name='mother_birthdate')),
                ('father_name', models.CharField(max_length=200, verbose_name='father_name')),
                ('father_birthdate', models.DateField(max_length=200, verbose_name='father_birthdate')),
                ('tin', models.IntegerField(verbose_name='tin')),
                ('philhealth', models.IntegerField(verbose_name='philhealth')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('Handler', 'Handler'), ('Veterinarian', 'Veterinarian'), ('Administrator', 'Administrator')], max_length=200, verbose_name='position')),
                ('rank', models.CharField(max_length=200, verbose_name='rank')),
                ('firstname', models.CharField(max_length=200, verbose_name='firstname')),
                ('lastname', models.CharField(max_length=200, verbose_name='lastname')),
                ('extensionname', models.CharField(blank=True, default='None', max_length=200, verbose_name='extensionname')),
                ('middlename', models.CharField(max_length=200, verbose_name='middlename')),
                ('nickname', models.CharField(max_length=200, verbose_name='nickname')),
                ('birthdate', models.DateField(blank=True, verbose_name='birthdate')),
                ('age', models.IntegerField(default=0, verbose_name='age')),
                ('birthplace', models.CharField(max_length=200, verbose_name='birthplace')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=200, verbose_name='gender')),
                ('civilstatus', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married')], max_length=200, verbose_name='civilstatus')),
                ('citizenship', models.CharField(max_length=200, verbose_name='citizenship')),
                ('religion', models.CharField(max_length=200, verbose_name='religion')),
                ('bloodtype', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], max_length=200, verbose_name='bloodtype')),
                ('distinct_feature', models.CharField(max_length=200, verbose_name='distinct_feature')),
                ('haircolor', models.CharField(choices=[('Black', 'Black'), ('Brown', 'Brown')], max_length=200, verbose_name='haircolor')),
                ('eyecolor', models.CharField(choices=[('Black', 'Black'), ('Brown', 'Brown')], max_length=200, verbose_name='eyecolor')),
                ('skincolor', models.CharField(choices=[('Light', 'Light'), ('Dark', 'Dark'), ('Yellow', 'Yellow'), ('Brown', 'Brown')], max_length=200, verbose_name='skincolor')),
                ('height', models.IntegerField(verbose_name='height')),
                ('weight', models.IntegerField(verbose_name='weight')),
                ('headsize', models.IntegerField(verbose_name='headsize')),
                ('footsize', models.IntegerField(verbose_name='footsize')),
                ('bodybuild', models.CharField(max_length=200, verbose_name='bodybuild')),
                ('status', models.CharField(choices=[('Working', 'Working'), ('On-Leave', 'On-Leave'), ('Retired', 'Retired'), ('Dead', 'Dead')], default='Working', max_length=200, verbose_name='status')),
            ],
        ),
        migrations.AddField(
            model_name='personal_info',
            name='UserID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AddField(
            model_name='education',
            name='UserID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AddField(
            model_name='account',
            name='UserID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
    ]
