# Generated by Django 2.2.6 on 2020-04-28 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wills', '0007_agreement_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='category',
            field=models.CharField(default='', max_length=250),
        ),
    ]
