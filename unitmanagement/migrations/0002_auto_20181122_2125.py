# Generated by Django 2.1a1 on 2018-11-22 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20181122_2125'),
        ('profiles', '0002_auto_20181122_2125'),
        ('unitmanagement', '0001_initial'),
    ]

    operations = [
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
                ('handler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.User')),
            ],
        ),
        migrations.AddField(
            model_name='physicalexam',
            name='date_next_exam',
            field=models.DateField(blank=True, null=True, verbose_name='date_next_exam'),
        ),
        migrations.AddField(
            model_name='vaccincerecord',
            name='veterinary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AlterField(
            model_name='physicalexam',
            name='veterinary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
        migrations.AlterField(
            model_name='vaccincerecord',
            name='date_validity',
            field=models.DateField(blank=True, null=True, verbose_name='date_validity'),
        ),
    ]
