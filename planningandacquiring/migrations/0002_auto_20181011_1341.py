# Generated by Django 2.1a1 on 2018-10-11 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planningandacquiring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='k9',
            name='breed',
            field=models.CharField(choices=[('Belgian Malinois', 'Belgian Malinois'), ('Dutch Sheperd', 'Dutch Sheperd'), ('German Sheperd', 'German Sheperd'), ('Golden Retriever', 'Golden Retriever'), ('Jack Russel', 'Jack Russel'), ('Labrador Retriever', 'Labrador Retriever'), ('Mixed', 'Mixed')], max_length=200, verbose_name='breed'),
        ),
    ]
