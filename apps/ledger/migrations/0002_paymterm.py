# Generated by Django 5.0.4 on 2024-06-28 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Item group')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('paym_method', models.CharField(choices=[('N', 'Net'), ('M', 'Curr.Mth.'), ('Q', 'Curr.Qtr.'), ('Y', 'Curr.Year'), ('Y', 'Curr.Week'), ('C', 'C.O.D.')], default='N', max_length=2, verbose_name='Payment method')),
                ('num_of_months', models.PositiveSmallIntegerField(default=0, help_text='Number of months past the specified method of payment', verbose_name='Months')),
                ('num_of_weeks', models.PositiveSmallIntegerField(default=0, help_text='Number of weeks past the specified method of payment', verbose_name='Weeks')),
                ('num_of_days', models.PositiveSmallIntegerField(default=0, help_text='Number of days past the specified method of payment', verbose_name='Days')),
            ],
            options={
                'verbose_name': 'Terms of payment',
            },
        ),
    ]
