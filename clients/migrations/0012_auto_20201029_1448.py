# Generated by Django 2.2 on 2020-10-29 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0072_auto_20201023_1032'),
        ('clients', '0011_payment_paymentmethod'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='case',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.Case'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
