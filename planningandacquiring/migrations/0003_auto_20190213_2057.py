# Generated by Django 2.1a1 on 2019-02-13 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planningandacquiring', '0002_auto_20190213_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget_food',
            name='food',
            field=models.CharField(choices=[('Adult', 'Adult'), ('Puppy', 'Puppy')], default='Adult', max_length=200, verbose_name='food'),
        ),
    ]
