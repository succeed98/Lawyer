# Generated by Django 2.2.6 on 2020-01-21 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lawyers', '0007_auto_20200114_0348'),
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AccessedDocument',
            new_name='DocumentRecords',
        ),
    ]
