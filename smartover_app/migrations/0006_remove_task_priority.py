# Generated by Django 3.1.7 on 2023-08-07 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartover_app', '0005_auto_20230719_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='priority',
        ),
    ]
