# Generated by Django 2.2.6 on 2020-04-26 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wills', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='will',
            name='last_edited',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
