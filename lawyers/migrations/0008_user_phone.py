# Generated by Django 2.2.6 on 2020-02-06 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyers', '0007_auto_20200114_0348'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='+233 24 4123 456', max_length=50),
        ),
    ]
