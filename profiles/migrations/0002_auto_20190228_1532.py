# Generated by Django 2.1a1 on 2019-02-28 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='se_degree',
            field=models.CharField(max_length=200, verbose_name='se_degree'),
        ),
        migrations.AlterField(
            model_name='education',
            name='te_degree',
            field=models.CharField(max_length=200, verbose_name='te_degree'),
        ),
    ]
