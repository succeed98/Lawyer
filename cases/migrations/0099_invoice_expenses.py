# Generated by Django 2.2 on 2022-02-02 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0098_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='expenses',
            field=models.ManyToManyField(null=True, to='cases.Expense'),
        ),
    ]
