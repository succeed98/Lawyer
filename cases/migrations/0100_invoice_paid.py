# Generated by Django 2.2 on 2022-02-02 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0099_invoice_expenses'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='Paid',
            field=models.BooleanField(default=False),
        ),
    ]