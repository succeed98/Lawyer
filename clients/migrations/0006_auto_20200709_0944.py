# Generated by Django 2.2.6 on 2020-07-09 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lawyers', '0014_auto_20200703_0956'),
        ('clients', '0005_remove_client_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='lead_professional',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lawyers.Lawyer'),
        ),
        migrations.AddField(
            model_name='client',
            name='type_of_brief',
            field=models.CharField(default='Case', max_length=250),
        ),
        migrations.AddField(
            model_name='client',
            name='client_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.ClientType'),
        ),
    ]
