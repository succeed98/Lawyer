# Generated by Django 2.2 on 2021-10-29 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0080_chinesewall'),
    ]

    operations = [
        migrations.AddField(
            model_name='chinesewall',
            name='mycase',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.Case'),
        ),
    ]
