# Generated by Django 2.1.2 on 2018-10-11 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                ('email_address', models.EmailField(max_length=200, verbose_name='email_address')),
                ('tel_number', models.CharField(max_length=200, verbose_name='tel_number')),
                ('street', models.CharField(max_length=200, verbose_name='street')),
                ('barangay', models.CharField(max_length=200, verbose_name='barangay')),
                ('city', models.CharField(max_length=200, verbose_name='city')),
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
                ('serial_number', models.CharField(max_length=200, verbose_name='serial_number')),
                ('position', models.CharField(choices=[('Handler', 'Handler'), ('Veterinarian', 'Veterinarian'), ('Administrator', 'Administrator')], max_length=200, verbose_name='position')),
                ('rank', models.CharField(max_length=200, verbose_name='rank')),
                ('firstname', models.CharField(max_length=200, verbose_name='firstname')),
                ('lastname', models.CharField(max_length=200, verbose_name='lastname')),
                ('extensionname', models.CharField(default='None', max_length=200, verbose_name='extensionname')),
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
    ]
