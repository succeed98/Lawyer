# Generated by Django 2.2 on 2020-10-02 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cases', '0067_auto_20200925_0521'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casefile',
            options={'ordering': ['title'], 'verbose_name': 'Case File', 'verbose_name_plural': 'Case Files'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='court',
            options={'ordering': ['name'], 'verbose_name': 'Courts', 'verbose_name_plural': 'Courts'},
        ),
        migrations.AlterModelOptions(
            name='representative',
            options={'ordering': ['title'], 'verbose_name': 'Representation', 'verbose_name_plural': 'Representations'},
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=False)),
                ('time_spent', models.IntegerField(default=0)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='cases.Case')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
