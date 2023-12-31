# Generated by Django 2.2.6 on 2020-03-05 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0016_document_shelf_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=500)),
                ('file', models.FileField(upload_to='doc_uploads/')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='files',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.DocFile'),
        ),
    ]
