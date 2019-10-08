# Generated by Django 2.2.3 on 2019-10-07 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='fax',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='name',
            field=models.CharField(db_index=True, max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='npwp',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='ptkp',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='siup',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='telephone',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]