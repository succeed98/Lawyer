# Generated by Django 2.2.6 on 2020-07-09 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_auto_20200709_0944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='type_of_brief',
        ),
    ]
