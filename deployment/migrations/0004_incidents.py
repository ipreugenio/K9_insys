# Generated by Django 2.1a1 on 2019-01-31 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0003_k9_schedule_dog_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incidents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='date')),
                ('type', models.CharField(choices=[('Bomb - Related', 'Bomb - Related'), ('Drug - Related', 'Drug - Related'), ('Search and Rescue Related', 'Search and Rescue Related'), ('Others', 'Others')], default='Others', max_length=100, verbose_name='type')),
                ('remarks', models.TextField(blank=True, max_length=200, null=True, verbose_name='remarks')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deployment.Location')),
            ],
        ),
    ]
