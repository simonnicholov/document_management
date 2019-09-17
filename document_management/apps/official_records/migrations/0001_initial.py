# Generated by Django 2.2.3 on 2019-09-17 17:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import document_management.core.utils
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficialRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(db_index=True, max_length=64, unique=True)),
                ('subject', models.CharField(max_length=256)),
                ('signature_date', models.DateField(blank=True, null=True)),
                ('effective_date', models.DateField(blank=True, null=True)),
                ('expired_date', models.DateField(blank=True, null=True)),
                ('amount', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.TextField(blank=True, null=True)),
                ('job_specification', models.CharField(blank=True, max_length=256, null=True)),
                ('retention_period', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='official_records', to='documents.Document')),
            ],
        ),
        migrations.CreateModel(
            name='OfficialRecordFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=document_management.core.utils.FilenameGenerator('official_record_file'))),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('official_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='official_records.OfficialRecord')),
            ],
        ),
    ]
