# Generated by Django 2.2 on 2020-10-02 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_auto_20200925_1300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['-name'], 'verbose_name': 'Client', 'verbose_name_plural': 'Clients'},
        ),
    ]