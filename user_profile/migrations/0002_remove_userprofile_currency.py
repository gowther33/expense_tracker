# Generated by Django 3.1.7 on 2023-08-08 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='currency',
        ),
    ]