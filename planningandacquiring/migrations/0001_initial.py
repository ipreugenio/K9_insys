
# Generated by Django 2.1a1 on 2018-11-23 05:26


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [

        ('profiles', '0001_initial'),
        ('inventory', '__first__'),

    ]

    operations = [
        migrations.CreateModel(
            name='Budget_allocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('k9_request_forecast', models.IntegerField(default=0, verbose_name='k9_request_forecast')),
                ('k9_needed_for_demand', models.IntegerField(default=0, verbose_name='k9s_needed_for_demand')),
                ('k9_cuurent', models.IntegerField(default=0, verbose_name='k9_current')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='date_created')),
                ('date_tobe_budgeted', models.DateField(verbose_name='date_tobe_budgeted')),
            ],
        ),
        migrations.CreateModel(
            name='Budget_equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='price')),
                ('budget_allocation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.Budget_allocation')),
                ('equipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Miscellaneous')),
            ],
        ),
        migrations.CreateModel(
            name='Budget_food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='price')),
                ('budget_allocation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.Budget_allocation')),
                ('food', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Food')),
            ],
        ),
        migrations.CreateModel(
            name='Budget_medicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=50, verbose_name='price')),
                ('budget_allocation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.Budget_allocation')),
                ('medicine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Medicine')),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(blank=True, null=True, verbose_name='date_from')),
                ('date_to', models.DateField(blank=True, null=True, verbose_name='date_to')),
            ],
        ),
        migrations.CreateModel(
            name='K9',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(default='Unassigned Serial Number', max_length=200, verbose_name='serial_number')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('breed', models.CharField(choices=[('Belgian Malinois', 'Belgian Malinois'), ('Dutch Sheperd', 'Dutch Sheperd'), ('German Sheperd', 'German Sheperd'), ('Golden Retriever', 'Golden Retriever'), ('Jack Russel', 'Jack Russel'), ('Labrador Retriever', 'Labrador Retriever'), ('Mixed', 'Mixed')], max_length=200, verbose_name='breed')),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Unspecified', max_length=200, verbose_name='sex')),
                ('color', models.CharField(choices=[('Brown', 'Brown'), ('Black', 'Black'), ('Gray', 'Gray'), ('White', 'White'), ('Yellow', 'Yellow'), ('Mixed', 'Mixed')], default='Unspecified', max_length=200, verbose_name='color')),
                ('birth_date', models.DateField(blank=True, verbose_name='birth_date')),
                ('age', models.IntegerField(default=0, verbose_name='age')),
                ('source', models.CharField(default='Not Specified', max_length=200, verbose_name='source')),
                ('year_retired', models.DateField(blank=True, null=True, verbose_name='year_retired')),
                ('assignment', models.CharField(default='None', max_length=200, verbose_name='assignment')),
                ('status', models.CharField(default='Material Dog', max_length=200, verbose_name='status')),
                ('training_status', models.CharField(default='Unclassified', max_length=200, verbose_name='training_status')),
                ('training_level', models.CharField(default='Stage 0', max_length=200, verbose_name='training_level')),
                ('training_count', models.IntegerField(default=0, verbose_name='training_count')),
                ('capability', models.CharField(default='None', max_length=200, verbose_name='capability')),
                ('microchip', models.CharField(default='Unassigned Microchip', max_length=200, verbose_name='microchip')),
                ('handler', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.User')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Adopted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_adopted', models.DateField(auto_now_add=True, verbose_name='date_adopted')),
                ('k9', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Donated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_donated', models.DateField(auto_now_add=True, verbose_name='date_donated')),
                ('k9', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
            ],
        ),
        migrations.CreateModel(
            name='K9_New_Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='first_name')),
                ('middle_name', models.CharField(max_length=200, verbose_name='middle_name')),
                ('last_name', models.CharField(max_length=200, verbose_name='last_name')),
                ('address', models.CharField(max_length=200, verbose_name='address')),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Unspecified', max_length=200, verbose_name='sex')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth_date')),
                ('email', models.EmailField(max_length=200, verbose_name='email')),
                ('contact_no', models.CharField(max_length=200, verbose_name='contact_no')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='father', to='planningandacquiring.K9')),
                ('mother', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mother', to='planningandacquiring.K9')),
                ('offspring', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Past_Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='first_name')),
                ('middle_name', models.CharField(max_length=200, verbose_name='middle_name')),
                ('last_name', models.CharField(max_length=200, verbose_name='last_name')),
                ('address', models.CharField(max_length=200, verbose_name='address')),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Unspecified', max_length=200, verbose_name='sex')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth_date')),
                ('email', models.EmailField(default='not specified', max_length=200, verbose_name='email')),
                ('contact_no', models.CharField(default='not specified', max_length=200, verbose_name='contact_no')),
            ],
        ),
        migrations.CreateModel(
            name='K9_Quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('date_bought', models.DateField(blank=True, null=True, verbose_name='date_bought')),
            ],
        ),
        migrations.AddField(
            model_name='k9_donated',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9_Past_Owner'),
        ),
        migrations.AddField(
            model_name='k9_adopted',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planningandacquiring.K9_New_Owner'),
        ),
    ]
