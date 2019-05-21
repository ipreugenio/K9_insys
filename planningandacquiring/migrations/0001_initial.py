# Generated by Django 2.1.5 on 2019-05-21 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('inventory', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget_allocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('k9_request_forecast', models.IntegerField(default=0, verbose_name='k9_request_forecast')),
                ('k9_needed_for_demand', models.IntegerField(default=0, verbose_name='k9s_needed_for_demand')),
                ('k9_cuurent', models.IntegerField(default=0, verbose_name='k9_current')),
                ('food_total', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='food_total')),
                ('equipment_total', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='equipment_total')),
                ('medicine_total', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='medicine_total')),
                ('vaccine_total', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='vaccine_total')),
                ('vet_supply_total', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='vet_supply_total')),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='grand_total')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='date_created')),
                ('date_tobe_budgeted', models.DateField(null=True, verbose_name='date_tobe_budgeted')),
            ],
        ),
        migrations.CreateModel(
            name='Budget_equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='price')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='total')),
                ('budget_allocation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.Budget_allocation')),
                ('equipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Miscellaneous')),
            ],
        ),
        migrations.CreateModel(
            name='Budget_food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food', models.CharField(default='Adult', max_length=200, verbose_name='food')),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='price')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='total')),
                ('budget_allocation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.Budget_allocation')),
            ],
        ),
        migrations.CreateModel(
            name='Budget_medicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='price')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='total')),
                ('budget_allocation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.Budget_allocation')),
                ('medicine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Medicine')),
            ],
        ),
        migrations.CreateModel(
            name='Budget_vaccine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='price')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='total')),
                ('budget_allocation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.Budget_allocation')),
                ('vaccine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Medicine')),
            ],
        ),
        migrations.CreateModel(
            name='Budget_vet_supply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='price')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='total')),
                ('budget_allocation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.Budget_allocation')),
                ('vet_supply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Miscellaneous')),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(null=True, verbose_name='date_from')),
                ('date_to', models.DateField(null=True, verbose_name='date_to')),
            ],
        ),
        migrations.CreateModel(
            name='K9',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, default='k9_image/k9_default.png', null=True, upload_to='k9_image')),
                ('serial_number', models.CharField(default='Unassigned Serial Number', max_length=200, verbose_name='serial_number')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('breed', models.CharField(blank=True, choices=[('Belgian Malinois', 'Belgian Malinois'), ('Dutch Sheperd', 'Dutch Sheperd'), ('German Sheperd', 'German Sheperd'), ('Golden Retriever', 'Golden Retriever'), ('Jack Russel', 'Jack Russel'), ('Labrador Retriever', 'Labrador Retriever'), ('Mixed', 'Mixed')], max_length=200, null=True, verbose_name='breed')),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Unspecified', max_length=200, verbose_name='sex')),
                ('color', models.CharField(choices=[('Black', 'Black'), ('Chocolate', 'Chocolate'), ('Yellow', 'Yellow'), ('Dark Golden', 'Dark Golden'), ('Light Golden', 'Light Golden'), ('Cream', 'Cream'), ('Golden', 'Golden'), ('Brindle', 'Brindle'), ('Silver Brindle', 'Silver Brindle'), ('Gold Brindle', 'Gold Brindle'), ('Salt and Pepper', 'Salt and Pepper'), ('Gray Brindle', 'Gray Brindle'), ('Blue and Gray', 'Blue and Gray'), ('Tan', 'Tan'), ('Black-Tipped Fawn', 'Black-Tipped Fawn'), ('Mahogany', 'Mahogany'), ('White', 'White'), ('Black and White', 'Black and White'), ('White and Tan', 'White and Tan')], default='Unspecified', max_length=200, verbose_name='color')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth_date')),
                ('age', models.IntegerField(default=0, verbose_name='age')),
                ('source', models.CharField(choices=[('Procured', 'Procured'), ('Breeding', 'Breeding')], default='Not Specified', max_length=200, verbose_name='source')),
                ('year_retired', models.DateField(blank=True, null=True, verbose_name='year_retired')),
                ('death_date', models.DateField(blank=True, null=True, verbose_name='death_date')),
                ('assignment', models.CharField(blank=True, default='None', max_length=200, null=True, verbose_name='assignment')),
                ('status', models.CharField(choices=[('Material Dog', 'Material Dog'), ('Working Dog', 'Working Dog'), ('Adopted', 'Adopted'), ('Due-For-Retirement', 'Due-For-Retirement'), ('Retired', 'Retired'), ('Dead', 'Dead'), ('Sick', 'Sick'), ('Stolen', 'Stolen'), ('Lost', 'Lost'), ('Accident', 'Accident')], default='Material Dog', max_length=200, verbose_name='status')),
                ('training_status', models.CharField(choices=[('Puppy', 'Puppy'), ('Unclassified', 'Unclassified'), ('Classified', 'Classified'), ('On-Training', 'On-Training'), ('Trained', 'Trained'), ('For-Breeding', 'For-Breeding'), ('Breeding', 'Breeding'), ('For-Deployment', 'For-Deployment'), ('For-Adoption', 'For-Adoption'), ('Deployed', 'Deployed'), ('Light Duty', 'Light Duty'), ('Retired', 'Retired'), ('Dead', 'Dead')], default='Puppy', max_length=200, verbose_name='training_status')),
                ('training_level', models.CharField(default='Stage 0', max_length=200, verbose_name='training_level')),
                ('training_count', models.IntegerField(default=0, verbose_name='training_count')),
                ('capability', models.CharField(default='None', max_length=200, verbose_name='capability')),
                ('reproductive_stage', models.CharField(choices=[('Proestrus', 'Proestrus'), ('Estrus', 'Estrus'), ('Metestrus', 'Metestrus'), ('Anestrus', 'Anestrus')], default='Anestrus', max_length=200, verbose_name='reproductive_stage')),
                ('age_days', models.IntegerField(default=0, verbose_name='age_days')),
                ('age_month', models.IntegerField(default=0, verbose_name='age_month')),
                ('in_heat_months', models.IntegerField(default=6, verbose_name='in_heat_months')),
                ('last_proestrus_date', models.DateField(blank=True, null=True)),
                ('next_proestrus_date', models.DateField(blank=True, null=True)),
                ('estrus_date', models.DateField(blank=True, null=True)),
                ('metestrus_date', models.DateField(blank=True, null=True)),
                ('anestrus_date', models.DateField(blank=True, null=True)),
                ('litter_no', models.IntegerField(default=0, verbose_name='litter_no')),
                ('last_date_mated', models.DateField(blank=True, null=True)),
                ('handler', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Adopted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_adopted', models.DateField(auto_now_add=True, verbose_name='date_adopted')),
                ('k9', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Breed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breed', models.CharField(choices=[('Belgian Malinois', 'Belgian Malinois'), ('Dutch Sheperd', 'Dutch Sheperd'), ('German Sheperd', 'German Sheperd'), ('Golden Retriever', 'Golden Retriever'), ('Jack Russel', 'Jack Russel'), ('Labrador Retriever', 'Labrador Retriever'), ('Mixed', 'Mixed')], max_length=200, null=True, verbose_name='breed')),
                ('life_span', models.CharField(max_length=200, null=True, verbose_name='life_span')),
                ('temperament', models.CharField(max_length=200, null=True, verbose_name='temperament')),
                ('colors', models.CharField(choices=[('Black', 'Black'), ('Chocolate', 'Chocolate'), ('Yellow', 'Yellow'), ('Dark Golden', 'Dark Golden'), ('Light Golden', 'Light Golden'), ('Cream', 'Cream'), ('Golden', 'Golden'), ('Brindle', 'Brindle'), ('Silver Brindle', 'Silver Brindle'), ('Gold Brindle', 'Gold Brindle'), ('Salt and Pepper', 'Salt and Pepper'), ('Gray Brindle', 'Gray Brindle'), ('Blue and Gray', 'Blue and Gray'), ('Tan', 'Tan'), ('Black-Tipped Fawn', 'Black-Tipped Fawn'), ('Mahogany', 'Mahogany'), ('White', 'White'), ('Black and White', 'Black and White'), ('White and Tan', 'White and Tan')], max_length=200, null=True, verbose_name='colors')),
                ('weight', models.CharField(max_length=200, null=True, verbose_name='weight')),
                ('male_height', models.CharField(max_length=200, null=True, verbose_name='male_height')),
                ('female_height', models.CharField(max_length=200, null=True, verbose_name='female_height')),
                ('skill_recommendation', models.CharField(choices=[('NDD', 'NDD'), ('EDD', 'EDD'), ('SAR', 'SAR')], max_length=200, null=True, verbose_name='skill_recommendation')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Donated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_donated', models.DateField(auto_now_add=True, verbose_name='date_donated')),
                ('k9', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Litter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('litter_no', models.IntegerField(blank=True, null=True, verbose_name='litter_no')),
                ('father', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sire', to='planningandacquiring.K9')),
                ('mother', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dam', to='planningandacquiring.K9')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Mated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Breeding', max_length=200, verbose_name='status')),
                ('date_mated', models.DateField(blank=True, null=True, verbose_name='date_mated')),
                ('father', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dad', to='planningandacquiring.K9')),
                ('mother', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mom', to='planningandacquiring.K9')),
            ],
        ),
        migrations.CreateModel(
            name='K9_New_Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='first_name')),
                ('middle_name', models.CharField(max_length=200, verbose_name='middle_name')),
                ('last_name', models.CharField(max_length=200, verbose_name='last_name')),
                ('address', models.CharField(max_length=200, verbose_name='address')),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Unspecified', max_length=200, verbose_name='sex')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth_date')),
                ('email', models.EmailField(max_length=200, verbose_name='email')),
                ('contact_no', models.CharField(max_length=200, verbose_name='contact_no')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='father', to='planningandacquiring.K9')),
                ('mother', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mother', to='planningandacquiring.K9')),
                ('offspring', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Past_Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='first_name')),
                ('middle_name', models.CharField(max_length=200, verbose_name='middle_name')),
                ('last_name', models.CharField(max_length=200, verbose_name='last_name')),
                ('address', models.CharField(max_length=200, verbose_name='address')),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Unspecified', max_length=200, verbose_name='sex')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth_date')),
                ('email', models.EmailField(default='not specified', max_length=200, verbose_name='email')),
                ('contact_no', models.CharField(default='not specified', max_length=200, verbose_name='contact_no')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('date_bought', models.DateField(null=True, verbose_name='date_bought')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('organization', models.CharField(default='Personal', max_length=200, verbose_name='organization')),
                ('address', models.CharField(max_length=200, verbose_name='address')),
                ('contact_no', models.CharField(max_length=200, verbose_name='contact_no')),
            ],
        ),
        migrations.AddField(
            model_name='k9_donated',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9_Past_Owner'),
        ),
        migrations.AddField(
            model_name='k9_adopted',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9_New_Owner'),
        ),
        migrations.AddField(
            model_name='k9',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9_Supplier'),
        ),
    ]
