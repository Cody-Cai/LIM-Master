# Generated by Django 5.0.4 on 2024-07-09 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0002_paymterm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymterm',
            name='code',
            field=models.CharField(max_length=10, unique=True, verbose_name='Payment terms'),
        ),
    ]