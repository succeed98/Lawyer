# Generated by Django 2.2 on 2020-10-02 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_auto_20201002_1154'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['name'], 'verbose_name': 'Client', 'verbose_name_plural': 'Clients'},
        ),
    ]
