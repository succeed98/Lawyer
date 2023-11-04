# Generated by Django 2.2 on 2022-04-12 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cases', '0103_remove_process_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsOfEngagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_add', models.DateTimeField(auto_now=True)),
                ('upload_file', models.FileField(blank=True, null=True, upload_to='terms/')),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('case', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cases.Case')),
            ],
        ),
    ]