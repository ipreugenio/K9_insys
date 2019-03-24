# Generated by Django 2.1a1 on 2019-02-23 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        ('profiles', '0001_initial'),
        ('planningandacquiring', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Handler_Incident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident', models.CharField(choices=[('Died', 'Died')], default='', max_length=100, verbose_name='incident')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('description', models.TextField(max_length=200, verbose_name='description')),
                ('handler', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User')),
            ],
        ),
        migrations.CreateModel(
            name='Health',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('problem', models.TextField(max_length=200, verbose_name='problem')),
                ('treatment', models.TextField(max_length=200, verbose_name='treatment')),
                ('status', models.CharField(default='Pending', max_length=200, verbose_name='status')),
                ('duration', models.IntegerField(blank=True, null=True, verbose_name='duration')),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
                ('veterinary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User')),
            ],
        ),
        migrations.CreateModel(
            name='HealthMedicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('time_of_day', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Night', 'Night'), ('Morning/Afternoon', 'Morning/Afternoon'), ('Morning/Night', 'Morning/Night'), ('Afternoon/Night', 'Afternoon/Night'), ('Morning/Afternoon/Night', 'Morning/Afternoon/Night')], default='', max_length=200, verbose_name='time_of_day')),
                ('duration', models.IntegerField(default=1, verbose_name='duration')),
                ('health', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unitmanagement.Health')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Medicine_Inventory')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Incident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident', models.CharField(choices=[('Died', 'Died')], default='', max_length=100, verbose_name='incident')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('description', models.TextField(max_length=200, verbose_name='description')),
                ('k9', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('Administrator', 'Administrator'), ('Veterinarian', 'Veterinarian'), ('Handler', 'Handler')], default='Administrator', max_length=100, verbose_name='position')),
                ('message', models.CharField(max_length=200)),
                ('viewed', models.BooleanField(default=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('k9', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User')),
            ],
        ),
        migrations.CreateModel(
            name='PhysicalExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cage_number', models.IntegerField(default='0', verbose_name='cage_number')),
                ('general_appearance', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Examined', 'Not Examined')], max_length=200, verbose_name='general_appearance')),
                ('integumentary', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Examined', 'Not Examined')], max_length=200, verbose_name='integumentary')),
                ('musculo_skeletal', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Examined', 'Not Examined')], max_length=200, verbose_name='musculo_skeletal')),
                ('respiratory', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Examined', 'Not Examined')], max_length=200, verbose_name='respiratory')),
                ('genito_urinary', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Examined', 'Not Examined')], max_length=200, verbose_name='genito_urinary')),
                ('nervous', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Examined', 'Not Examined')], max_length=200, verbose_name='nervous')),
                ('circulatory', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Examined', 'Not Examined')], max_length=200, verbose_name='circulatory')),
                ('digestive', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Examined', 'Not Examined')], max_length=200, verbose_name='digestive')),
                ('mucous_membrances', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Examined', 'Not Examined')], max_length=200, verbose_name='mucous_membrances')),
                ('lymph_nodes', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Examined', 'Not Examined')], max_length=200, verbose_name='lymph_nodes')),
                ('eyes', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Examined', 'Not Examined')], max_length=200, verbose_name='eyes')),
                ('ears', models.CharField(choices=[('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Examined', 'Not Examined')], max_length=200, verbose_name='ears')),
                ('remarks', models.TextField(blank=True, max_length=200, null=True, verbose_name='remarks')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('date_next_exam', models.DateField(blank=True, null=True, verbose_name='date_next_exam')),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
                ('veterinary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User')),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('concern', models.CharField(choices=[('Broken', 'Broken'), ('Lost', 'Lost'), ('Stolen', 'Stolen')], default='', max_length=100, verbose_name='concern')),
                ('remarks', models.CharField(blank=True, max_length=200, verbose_name='remarks')),
                ('request_status', models.CharField(default='Pending', max_length=200, verbose_name='request_status')),
                ('date_approved', models.DateField(blank=True, null=True, verbose_name='date_approved')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Miscellaneous')),
                ('handler', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User')),
            ],
        ),
        migrations.CreateModel(
            name='VaccinceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deworming_1', models.BooleanField(default=False)),
                ('deworming_2', models.BooleanField(default=False)),
                ('deworming_3', models.BooleanField(default=False)),
                ('deworming_4', models.BooleanField(default=False)),
                ('dhppil_cv_1', models.BooleanField(default=False)),
                ('dhppil_cv_2', models.BooleanField(default=False)),
                ('dhppil_cv_3', models.BooleanField(default=False)),
                ('heartworm_1', models.BooleanField(default=False)),
                ('heartworm_2', models.BooleanField(default=False)),
                ('heartworm_3', models.BooleanField(default=False)),
                ('heartworm_4', models.BooleanField(default=False)),
                ('heartworm_5', models.BooleanField(default=False)),
                ('heartworm_6', models.BooleanField(default=False)),
                ('heartworm_7', models.BooleanField(default=False)),
                ('heartworm_8', models.BooleanField(default=False)),
                ('anti_rabies', models.BooleanField(default=False)),
                ('bordetella_1', models.BooleanField(default=False)),
                ('bordetella_2', models.BooleanField(default=False)),
                ('dhppil4_1', models.BooleanField(default=False)),
                ('dhppil4_2', models.BooleanField(default=False)),
                ('tick_flea_1', models.BooleanField(default=False)),
                ('tick_flea_2', models.BooleanField(default=False)),
                ('tick_flea_3', models.BooleanField(default=False)),
                ('tick_flea_4', models.BooleanField(default=False)),
                ('tick_flea_5', models.BooleanField(default=False)),
                ('tick_flea_6', models.BooleanField(default=False)),
                ('tick_flea_7', models.BooleanField(default=False)),
                ('k9', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
            ],
        ),
        migrations.CreateModel(
            name='VaccineUsed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease', models.CharField(max_length=200, verbose_name='disease')),
                ('date_vaccinated', models.DateField(blank=True, null=True, verbose_name='date_vaccinated')),
                ('vaccine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Medicine')),
                ('vaccine_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unitmanagement.VaccinceRecord')),
                ('veterinary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User')),
            ],
        ),
    ]
