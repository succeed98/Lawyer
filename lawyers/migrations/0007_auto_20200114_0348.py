# Generated by Django 2.2.6 on 2020-01-14 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lawyers', '0006_auto_20200114_0327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawyer',
            name='lawyer_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lawyers.LawyerStatus'),
        ),
    ]
