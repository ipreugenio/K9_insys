# Generated by Django 2.1a1 on 2019-01-31 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0005_auto_20190131_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidents',
            name='date_time',
        ),
        migrations.AddField(
            model_name='incidents',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='date'),
        ),
    ]