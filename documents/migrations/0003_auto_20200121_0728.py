# Generated by Django 2.2.6 on 2020-01-21 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lawyers', '0007_auto_20200114_0348'),
        ('documents', '0002_auto_20200121_0701'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentRecords',
            new_name='DocumentRecord',
        ),
    ]
