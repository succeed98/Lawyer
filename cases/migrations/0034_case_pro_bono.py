# Generated by Django 2.2.6 on 2020-03-12 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0033_auto_20200310_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='pro_bono',
            field=models.BooleanField(default=False),
        ),
    ]
