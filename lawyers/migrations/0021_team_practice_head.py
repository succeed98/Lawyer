# Generated by Django 2.2 on 2020-09-24 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lawyers', '0020_auto_20200810_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='practice_head',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='practice_head', to='lawyers.Lawyer'),
        ),
    ]
