# Generated by Django 2.2.3 on 2019-08-15 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0001_initial'),
        ('company_regulations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveSmallIntegerField(choices=[(1, 'Director Decisions'), (2, 'Circular Letter'), (3, 'Other')])),
                ('has_approved', models.BooleanField(default=False)),
                ('approved_date', models.DateTimeField()),
                ('has_canceled', models.BooleanField(default=False)),
                ('canceled_date', models.DateTimeField()),
                ('has_viewed', models.BooleanField(default=False)),
                ('viewed_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('company_regulations', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_regulations', to='company_regulations.CompanyRegulation')),
                ('documents', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='documents.Document')),
                ('user_approval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_approval', to=settings.AUTH_USER_MODEL)),
                ('user_cancellation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_cancellation', to=settings.AUTH_USER_MODEL)),
                ('user_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_request', to=settings.AUTH_USER_MODEL)),
                ('user_view', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_view', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
