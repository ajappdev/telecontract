# Generated by Django 4.2.11 on 2024-04-18 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_userprofile_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='complete_name',
        ),
    ]
