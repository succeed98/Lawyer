# Generated by Django 2.2.6 on 2020-02-22 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principles', '0002_authority_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='principles',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
