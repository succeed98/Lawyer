# Generated by Django 2.2 on 2021-03-26 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0013_auto_20210325_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Business Phone'),
        ),
    ]
