# Generated by Django 3.1.7 on 2023-06-29 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='expensecategory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
