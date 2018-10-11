# Generated by Django 2.1.2 on 2018-10-09 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20181009_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_education', models.CharField(max_length=200, verbose_name='primary_education')),
                ('secondary_education', models.CharField(max_length=200, verbose_name='secondary_education')),
                ('tertiary_education', models.CharField(max_length=200, verbose_name='tertiary_education')),
                ('pe_schoolyear', models.CharField(max_length=200, verbose_name='pe_schoolyear')),
                ('se_schoolyear', models.CharField(max_length=200, verbose_name='se_schoolyear')),
                ('te_schoolyear', models.CharField(max_length=200, verbose_name='te_schoolyear')),
                ('pe_degree', models.CharField(max_length=200, verbose_name='pe_degree')),
                ('se_degree', models.CharField(max_length=200, verbose_name='pe_degree')),
                ('te_degree', models.CharField(max_length=200, verbose_name='pe_degree')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.User')),
            ],
        ),
    ]
