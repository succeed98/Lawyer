# Generated by Django 2.2 on 2022-01-19 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0088_auto_20220119_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timer',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='timer',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='timer',
            name='time_spent',
        ),
    ]