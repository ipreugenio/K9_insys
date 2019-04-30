from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('planningandacquiring', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Dog_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester', models.CharField(max_length=100, verbose_name='requester')),
                ('location', models.CharField(max_length=100, verbose_name='location')),
                ('phone_number', models.CharField(default='n/a', max_length=100, verbose_name='phone_number')),
                ('email_address', models.EmailField(blank=True, max_length=100, null=True, verbose_name='email')),
                ('remarks', models.CharField(blank=True, max_length=200, null=True, verbose_name='remarks')),
                ('EDD_needed', models.IntegerField(default=0, verbose_name='EDD_needed')),
                ('NDD_needed', models.IntegerField(default=0, verbose_name='NDD_needed')),
                ('SAR_needed', models.IntegerField(default=0, verbose_name='SAR_needed')),
                ('EDD_deployed', models.IntegerField(default=0, verbose_name='EDD_deployed')),
                ('NDD_deployed', models.IntegerField(default=0, verbose_name='NDD_deployed')),
                ('SAR_deployed', models.IntegerField(default=0, verbose_name='SAR_deployed')),
                ('total_dogs_demand', models.IntegerField(default=0, verbose_name='total_dogs_demand')),
                ('total_dogs_deployed', models.IntegerField(default=0, verbose_name='total_dogs_deployed')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='start_date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='end_date')),
                ('status', models.CharField(default='Pending', max_length=100, verbose_name='status')),
            ],
        ),
        migrations.CreateModel(
            name='Incidents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='date')),
                ('type', models.CharField(choices=[('Explosives Related', 'Explosives Related'), ('Narcotics Related', 'Narcotics Related'), ('Search and Rescue Related', 'Search and Rescue Related'), ('Others', 'Others')], default='Others', max_length=100, verbose_name='type')),
                ('remarks', models.TextField(blank=True, max_length=200, null=True, verbose_name='remarks')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField(blank=True, null=True, verbose_name='date_start')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='date_end')),
                ('dog_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deployment.Dog_Request')),
                ('k9', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(choices=[('Alaminos', 'Alaminos'), ('Angeles', 'Angeles'), ('Antipolo', 'Antipolo'), ('Bacolod', 'Bacolod'), ('Bacoor', 'Bacoor'), ('Bago', 'Bago'), ('Baguio', 'Baguio'), ('Bais', 'Bais'), ('Balanga', 'Balanga'), ('Batac', 'Batac'), ('Batangas', 'Batangas'), ('Bayawan', 'Bayawan'), ('Baybay', 'Baybay'), ('Bayugan', 'Bayugan'), ('Biñan', 'Biñan'), ('Bislig', 'Bislig'), ('Bogo', 'Bogo'), ('Borongan', 'Borongan'), ('Butuan', 'Butuan'), ('Cabadbaran', 'Cabadbaran'), ('Cabanatuan', 'Cabanatuan'), ('Cabuyao', 'Cabuyao'), ('Cadiz', 'Cadiz'), ('Cagayan de Oro', 'Cagayan de Oro'), ('Calamba', 'Calamba'), ('Calapan', 'Calapan'), ('Calbayog', 'Calbayog'), ('Caloocan', 'Caloocan'), ('Candon', 'Candon'), ('Canlaon', 'Canlaon'), ('Carcar', 'Carcar'), ('Catbalogan', 'Catbalogan'), ('Cauayan', 'Cauayan'), ('Cavite', 'Cavite'), ('Cebu', 'Cebu'), ('Cotabato', 'Cotabato'), ('Dagupan', 'Dagupan'), ('Danao', 'Danao'), ('Dapitan', 'Dapitan'), ('Dasmariñas', 'Dasmariñas'), ('Davao', 'Davao'), ('Digos', 'Digos'), ('Dipolog', 'Dipolog'), ('Dumaguete', 'Dumaguete'), ('El Salvador', 'El Salvador'), ('Escalante', 'Escalante'), ('Gapan', 'Gapan'), ('General Santos', 'General Santos'), ('General Trias', 'General Trias'), ('Gingoog', 'Gingoog'), ('Guihulngan', 'Guihulngan'), ('Himamaylan', 'Himamaylan'), ('Ilagan', 'Ilagan'), ('Iligan', 'Iligan'), ('Iloilo', 'Iloilo'), ('Imus', 'Imus'), ('Iriga', 'Iriga'), ('Isabela', 'Isabela'), ('Kabankalan', 'Kabankalan'), ('Kidapawan', 'Kidapawan'), ('Koronadal', 'Koronadal'), ('La Carlota', 'La Carlota'), ('Lamitan', 'Lamitan'), ('Laoag', 'Laoag'), ('Lapu‑Lapu', 'Lapu‑Lapu'), ('Las Piñas', 'Las Piñas'), ('Legazpi', 'Legazpi'), ('Ligao', 'Ligao'), ('Lipa', 'Lipa'), ('Lucena', 'Lucena'), ('Maasin', 'Maasin'), ('Mabalacat', 'Mabalacat'), ('Makati', 'Makati'), ('Malabon', 'Malabon'), ('Malaybalay', 'Malaybalay'), ('Malolos', 'Malolos'), ('Mandaluyong', 'Mandaluyong'), ('Mandaue', 'Mandaue'), ('Manila', 'Manila'), ('Marawi', 'Marawi'), ('Marikina', 'Marikina'), ('Masbate', 'Masbate'), ('Mati', 'Mati'), ('Meycauayan', 'Meycauayan'), ('Muñoz', 'Muñoz'), ('Muntinlupa', 'Muntinlupa'), ('Naga - Camarines Sur', 'Naga - Camarines Sur'), ('Naga - Cebu', 'Naga - Cebu'), ('Navotas', 'Navotas'), ('Olongapo', 'Olongapo'), ('Ormoc', 'Ormoc'), ('Oroquieta', 'Oroquieta'), ('Ozamiz', 'Ozamiz'), ('Pagadian', 'Pagadian'), ('Palayan', 'Palayan'), ('Panabo', 'Panabo'), ('Parañaque', 'Parañaque'), ('Pasay', 'Pasay'), ('Pasig', 'Pasig'), ('Passi', 'Passi'), ('Puerto Princesa', 'Puerto Princesa'), ('Quezon', 'Quezon'), ('Roxas', 'Roxas'), ('Sagay', 'Sagay'), ('Samal', 'Samal'), ('San Carlos - Negros Occidental', 'San Carlos - Negros Occidental'), ('San Carlos - Pangasinan', 'San Carlos - Pangasinan'), ('San Fernando - La Union', 'San Fernando - La Union'), ('San Fernando - Pampanga', 'San Fernando - Pampanga'), ('San Jose', 'San Jose'), ('San Jose del Monte', 'San Jose del Monte'), ('San Juan', 'San Juan'), ('San Pablo', 'San Pablo'), ('San Pedro', 'San Pedro'), ('Santa Rosa', 'Santa Rosa'), ('Santiago', 'Santiago'), ('Silay', 'Silay'), ('Sipalay', 'Sipalay'), ('Sorsogon', 'Sorsogon'), ('Surigao', 'Surigao'), ('Tabaco', 'Tabaco'), ('Tabuk', 'Tabuk'), ('Tacloban', 'Tacloban'), ('Tacurong', 'Tacurong'), ('Tagaytay', 'Tagaytay'), ('Tagbilaran', 'Tagbilaran'), ('Taguig', 'Taguig'), ('Tagum', 'Tagum'), ('Talisay - Cebu', 'Talisay - Cebu'), ('Talisay - Negros Occidental', 'Talisay - Negros Occidental'), ('Tanauan', 'Tanauan'), ('Tandag', 'Tandag'), ('Tangub', 'Tangub'), ('Tanjay', 'Tanjay'), ('Tarlac', 'Tarlac'), ('Tayabas', 'Tayabas'), ('Toledo', 'Toledo'), ('Trece Martires', 'Trece Martires'), ('Tuguegarao', 'Tuguegarao'), ('Urdaneta', 'Urdaneta'), ('Valencia', 'Valencia'), ('Valenzuela', 'Valenzuela'), ('Victorias', 'Victorias'), ('Vigan', 'Vigan'), ('Zamboanga', 'Zamboanga')], default='None', max_length=100, verbose_name='city')),
                ('place', models.CharField(default='Undefined', max_length=100, verbose_name='place')),
                ('sector_type', models.CharField(blank=True, choices=[('Mall', 'Mall'), ('Airport', 'Airport')], max_length=100, null=True, verbose_name='sector_type')),
                ('status', models.CharField(default='unassigned', max_length=100, verbose_name='status')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deployment.Area')),
            ],
        ),
        migrations.CreateModel(
            name='Team_Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=100, verbose_name='team')),
                ('EDD_demand', models.IntegerField(default=0, verbose_name='EDD_demand')),
                ('NDD_demand', models.IntegerField(default=0, verbose_name='NDD_demand')),
                ('SAR_demand', models.IntegerField(default=0, verbose_name='SAR_demand')),
                ('EDD_deployed', models.IntegerField(default=0, verbose_name='EDD_deployed')),
                ('NDD_deployed', models.IntegerField(default=0, verbose_name='NDD_deployed')),
                ('SAR_deployed', models.IntegerField(default=0, verbose_name='SAR_deployed')),
                ('total_dogs_demand', models.IntegerField(default=0, verbose_name='total_dogs_demand')),
                ('total_dogs_deployed', models.IntegerField(default=0, verbose_name='total_dogs_deployed')),
                ('date_added', models.DateField(auto_now_add=True, null=True, verbose_name='date_added')),
                ('location', models.ForeignKey(default='None', on_delete=django.db.models.deletion.CASCADE, to='deployment.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Team_Dog_Deployed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handler', models.CharField(blank=True, max_length=100, null=True, verbose_name='handler')),
                ('status', models.CharField(blank=True, default='Deployed', max_length=100, null=True, verbose_name='status')),
                ('date_added', models.DateField(auto_now_add=True, null=True, verbose_name='date_added')),
                ('date_pulled', models.DateField(blank=True, null=True, verbose_name='date_pulled')),
                ('k9', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
                ('team_assignment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deployment.Team_Assignment')),
                ('team_requested', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deployment.Dog_Request')),
            ],
        ),
        migrations.AddField(
            model_name='incidents',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deployment.Location'),
        ),
        migrations.AddField(
            model_name='incidents',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AddField(
            model_name='dog_request',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployment.Location'),
        ),
    ]
