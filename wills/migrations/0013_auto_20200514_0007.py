# Generated by Django 2.2.6 on 2020-05-14 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyers', '0012_auto_20200422_2333'),
        ('wills', '0012_auto_20200507_1853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='will',
            name='user',
        ),
        migrations.AddField(
            model_name='will',
            name='user',
            field=models.ManyToManyField(to='lawyers.Lawyer'),
        ),
    ]
