# Generated by Django 3.1.7 on 2023-08-25 10:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuel_calculator_app', '0003_auto_20230824_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelcalculator',
            name='fuel_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
