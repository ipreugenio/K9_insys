# Generated by Django 2.1a1 on 2019-02-20 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0008_auto_20190220_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog_request',
            name='email_address',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='email'),
        ),
    ]