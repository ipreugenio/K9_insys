# Generated by Django 2.1a1 on 2019-03-01 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0009_auto_20190301_1128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dog_request',
            name='coordinates',
        ),
        migrations.AddField(
            model_name='dog_request',
            name='latitude',
            field=models.DecimalField(decimal_places=4, max_digits=50, null=True, verbose_name='latitude'),
        ),
        migrations.AddField(
            model_name='dog_request',
            name='longtitude',
            field=models.DecimalField(decimal_places=4, max_digits=50, null=True, verbose_name='longtitude'),
        ),
        migrations.DeleteModel(
            name='Request_Coordinates',
        ),
    ]