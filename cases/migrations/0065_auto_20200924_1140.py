# Generated by Django 2.2 on 2020-09-24 11:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0064_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='date_received',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.RemoveField(
            model_name='case',
            name='category',
        ),
        migrations.AddField(
            model_name='case',
            name='category',
            field=models.ManyToManyField(to='cases.Category'),
        ),
    ]
