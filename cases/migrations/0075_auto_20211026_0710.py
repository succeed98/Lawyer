# Generated by Django 2.2 on 2021-10-26 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0074_case_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='staff',
            field=models.ManyToManyField(blank=True, null=True, to='lawyers.OtherStaff'),
        ),
    ]