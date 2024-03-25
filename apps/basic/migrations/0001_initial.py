# Generated by Django 4.2.3 on 2024-03-01 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountryRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2, unique=True, verbose_name='country/region')),
                ('name', models.CharField(max_length=250)),
                ('en_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='english name')),
            ],
        ),
        migrations.CreateModel(
            name='Curreny',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True, verbose_name='Curreny')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
    ]
