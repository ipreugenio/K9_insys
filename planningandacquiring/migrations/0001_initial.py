# Generated by Django 2.1.2 on 2018-10-11 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='K9',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(default='Unassigned', max_length=200, verbose_name='serial_number')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('breed', models.CharField(choices=[('Akita', 'Akita'), ('Alaskan Malamute', 'Alaskan Malamute'), ('Australian Sheperd', 'Australian Sheperd'), ('Basset Hound', 'Basset Hound'), ('Bernese Mountain Dog', 'Bernese Mountain Dog'), ('Boxer', 'Boxer'), ('Bulldog', 'Bulldog'), ('Chow Chow', 'Chow Chow'), ('Dalmatian', 'Dalmatian'), ('Dobermann', 'Dobermann'), ('Englsih Mastiff', 'English Mastiff'), ('German Sheperd', 'German Sheperd'), ('Golden Retriever', 'Golden Retriever'), ('Greyhound', 'Greyhound'), ('Great Dane', 'Great Dane'), ('Labrador Retriever', 'Labrador Retriever'), ('Rottweiler', 'Rottweiler'), ('Shi Tzu', 'Shi Tzu'), ('Siberian Husky', 'Siberian Husky'), ('Mixed', 'Mixed')], max_length=200, verbose_name='breed')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='Unspecified', max_length=200, verbose_name='sex')),
                ('color', models.CharField(choices=[('Brown', 'Brown'), ('Black', 'Black'), ('Gray', 'Gray'), ('White', 'White'), ('Yellow', 'Yellow'), ('Mixed', 'Mixed')], default='Unspecified', max_length=200, verbose_name='color')),
                ('birth_date', models.DateField(blank=True, verbose_name='birth_date')),
                ('age', models.IntegerField(default=0, verbose_name='age')),
                ('source', models.CharField(default='Not Specified', max_length=200, verbose_name='source')),
                ('year_retired', models.DateField(blank=True, null=True, verbose_name='year_retired')),
                ('assignment', models.CharField(default='None', max_length=200, verbose_name='assignment')),
                ('status', models.CharField(default='Material Dog', max_length=200, verbose_name='status')),
                ('training_status', models.CharField(default='Unclassified', max_length=200, verbose_name='training_status')),
                ('capability', models.CharField(default='None', max_length=200, verbose_name='capability')),
                ('microchip', models.CharField(default='Unassigned', max_length=200, verbose_name='microchip')),
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
            name='K9_Donated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_donated', models.DateField(auto_now_add=True, verbose_name='date_donated')),
                ('k9', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
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
                ('email', models.EmailField(default='not specified', max_length=200, verbose_name='email')),
                ('contact_no', models.CharField(default='not specified', max_length=200, verbose_name='contact_no')),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.CharField(max_length=200, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='Medicine_Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('milligram', models.DecimalField(decimal_places=3, default=0, max_digits=12, verbose_name='milligram')),
                ('K9', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
            ],
        ),
        migrations.CreateModel(
            name='Miscellaneous',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.CharField(max_length=200, verbose_name='description')),
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
    ]
