# Generated by Django 2.1a1 on 2018-11-26 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unitmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='handler',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User'),
        ),
    ]
