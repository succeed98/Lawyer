# Generated by Django 2.2 on 2021-10-25 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0015_auto_20210329_1746'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clienttype',
            old_name='type',
            new_name='types',
        ),
    ]
