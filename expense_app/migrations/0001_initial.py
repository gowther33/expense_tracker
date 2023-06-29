# Generated by Django 3.1.7 on 2023-06-22 16:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime)),
            ],
            options={
                'verbose_name_plural': 'Expense Categories',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date', models.DateField(default=django.utils.timezone.localtime)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense_app.expensecategory')),
            ],
        ),
    ]
