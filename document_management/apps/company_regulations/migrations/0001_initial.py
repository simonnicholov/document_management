# Generated by Django 2.2.3 on 2019-08-06 17:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import document_management.core.utils
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyRegulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=32)),
                ('subject', models.CharField(max_length=64)),
                ('effective_date', models.DateField()),
                ('expired_date', models.DateField()),
                ('category', models.PositiveSmallIntegerField(choices=[(1, 'Director Decisions'), (2, 'Circular Letter'), (3, 'Other')])),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Private'), (2, 'Public')])),
                ('total_document', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_regulations', to='locations.Location')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyRegulationFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=document_management.core.utils.FilenameGenerator('company_regulation_file'))),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('company_regulation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_regulation_files', to='company_regulations.CompanyRegulation')),
            ],
        ),
    ]
