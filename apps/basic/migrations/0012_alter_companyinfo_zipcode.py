# Generated by Django 5.0.4 on 2024-07-19 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0011_dlvdestination_dlvmode_dlvterm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='zipcode',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Postal code'),
        ),
    ]