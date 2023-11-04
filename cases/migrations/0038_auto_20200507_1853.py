# Generated by Django 2.2.6 on 2020-05-07 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0037_courtsession_purpose'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='case_number',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='court_number',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]