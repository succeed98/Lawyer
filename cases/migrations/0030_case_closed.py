# Generated by Django 2.2.6 on 2020-03-03 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0029_case_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
