# Generated by Django 2.1.5 on 2019-03-11 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitmanagement', '0009_auto_20190310_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='handler_incident',
            name='retain_last_handler',
            field=models.BooleanField(default=False),
        ),
    ]
