# Generated by Django 2.2 on 2022-03-26 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lawyers', '0027_auto_20220326_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lawyers.Team'),
        ),
    ]
