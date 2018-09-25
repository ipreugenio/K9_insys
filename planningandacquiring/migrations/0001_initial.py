# Generated by Django 2.1a1 on 2018-09-25 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.CharField(max_length=200, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='K9',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=200, verbose_name='serial_number')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('breed', models.CharField(max_length=200, verbose_name='breed')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='Unspecified', max_length=200, verbose_name='sex')),
                ('color', models.CharField(choices=[('Brown', 'Brown'), ('Black', 'Black'), ('Gray', 'Gray'), ('White', 'White'), ('Mixed', 'Mixed')], default='Unspecified', max_length=200, verbose_name='color')),
                ('birth_date', models.DateField(blank=True, verbose_name='birth_date')),
                ('age', models.IntegerField(default=0, verbose_name='age')),
                ('year_retired', models.DateField(blank=True, verbose_name='year_retired')),
                ('assignment', models.CharField(max_length=200, verbose_name='assignment')),
                ('microchip', models.CharField(max_length=200, verbose_name='microchip')),
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
    ]
