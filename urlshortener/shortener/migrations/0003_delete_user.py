# Generated by Django 3.2.12 on 2022-03-18 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_user_full_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
