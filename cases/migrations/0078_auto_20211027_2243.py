# Generated by Django 2.2 on 2021-10-27 22:43

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0077_auto_20211027_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]