# Generated by Django 2.2.6 on 2020-06-23 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0044_auto_20200623_1026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='frequency',
            options={'ordering': ['-pk'], 'verbose_name': 'Frequency', 'verbose_name_plural': 'Frequencies'},
        ),
    ]
