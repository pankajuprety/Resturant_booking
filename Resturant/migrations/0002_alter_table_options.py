# Generated by Django 3.2.20 on 2023-08-16 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Resturant', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='table',
            options={'ordering': ['seats']},
        ),
    ]
