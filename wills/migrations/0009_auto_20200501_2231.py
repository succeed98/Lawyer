# Generated by Django 2.2.6 on 2020-05-01 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wills', '0008_auto_20200428_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='will',
            name='client',
            field=models.CharField(default='Client Name', max_length=250),
        ),
    ]
