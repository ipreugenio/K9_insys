# Generated by Django 2.1 on 2018-10-02 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='medicine_fullname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
