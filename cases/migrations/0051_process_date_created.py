# Generated by Django 2.2.6 on 2020-07-08 11:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0050_auto_20200707_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 8, 11, 50, 59, 6536, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
