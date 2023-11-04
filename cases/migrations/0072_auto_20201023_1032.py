# Generated by Django 2.2 on 2020-10-23 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0011_payment_paymentmethod'),
        ('cases', '0071_paymentenquiry_paymentstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentenquiry',
            name='client',
        ),
        migrations.AddField(
            model_name='paymentenquiry',
            name='client',
            field=models.ManyToManyField(related_name='enquired_clients', to='clients.Client'),
        ),
    ]
