# Generated by Django 2.2.6 on 2020-06-18 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0041_bill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='status',
        ),
    ]
