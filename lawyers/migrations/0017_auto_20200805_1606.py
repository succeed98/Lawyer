# Generated by Django 2.2.6 on 2020-08-05 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyers', '0016_auto_20200716_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawyerstatus',
            name='id',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Senior'), (2, 'Junior'), (3, 'Managing Partner'), (4, 'CEO')], primary_key=True, serialize=False),
        ),
    ]