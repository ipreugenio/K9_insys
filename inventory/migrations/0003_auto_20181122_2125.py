# Generated by Django 2.1a1 on 2018-11-22 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20181122_2125'),
        ('inventory', '0002_auto_20181025_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='damagedequipemnt',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AddField(
            model_name='food_inventory_count',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AddField(
            model_name='food_received_trail',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AddField(
            model_name='food_subtracted_trail',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AddField(
            model_name='medicine',
            name='duration',
            field=models.IntegerField(default=0, verbose_name='duration'),
        ),
        migrations.AddField(
            model_name='medicine',
            name='used_yearly',
            field=models.IntegerField(default=0, verbose_name='used_yearly'),
        ),
        migrations.AddField(
            model_name='medicine_inventory_count',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AddField(
            model_name='medicine_received_trail',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AddField(
            model_name='medicine_subtracted_trail',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AddField(
            model_name='miscellaneous_inventory_count',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AddField(
            model_name='miscellaneous_received_trail',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AddField(
            model_name='miscellaneous_subtracted_trail',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AlterField(
            model_name='food',
            name='foodtype',
            field=models.CharField(choices=[('Adult Dog Food', 'Adult Dog Food'), ('Puppy Dog Food', 'Puppy Dog Food')], max_length=50, verbose_name='foodtype'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='med_type',
            field=models.CharField(choices=[('Tablet', 'Tablet'), ('Capsule', 'Capsule'), ('Bottle', 'Bottle'), ('Vaccine', 'Vaccine')], default='Drug', max_length=50, verbose_name='med_type'),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='uom',
            field=models.CharField(blank=True, default='unit', max_length=10, null=True, verbose_name='uom'),
        ),
    ]
