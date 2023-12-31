# Generated by Django 2.2 on 2020-10-21 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lawyers', '0022_auto_20201002_1154'),
        ('cases', '0069_engagementterm_expense'),
    ]

    operations = [
        migrations.CreateModel(
            name='Renumeration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('approved', models.BooleanField(default=False)),
                ('case', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='renumeration', to='cases.Case')),
                ('lead', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='renum_requests', to='lawyers.Lawyer')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]
