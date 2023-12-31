# Generated by Django 2.2 on 2022-01-19 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0086_auto_20211115_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='timer',
            name='charge_payment',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='timer',
            name='hour_payment',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='timer',
            name='minutes_payment',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='timer',
            name='name_task',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='timer',
            name='purpose_of_task',
            field=models.CharField(max_length=9000, null=True),
        ),
        migrations.AddField(
            model_name='timer',
            name='seconds_payment',
            field=models.IntegerField(null=True),
        ),
    ]
