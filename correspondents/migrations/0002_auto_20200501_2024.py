# Generated by Django 2.2.6 on 2020-05-01 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correspondents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correspondent',
            name='date_added',
            field=models.DateTimeField(),
        ),
    ]
