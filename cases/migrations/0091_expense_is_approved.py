# Generated by Django 2.2 on 2022-01-25 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0090_auto_20220119_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
