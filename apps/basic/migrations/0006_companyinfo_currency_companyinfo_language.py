# Generated by Django 4.2.3 on 2024-03-13 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_alter_menulangname_unique_together'),
        ('basic', '0005_alter_companyinfo_mobilephone'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinfo',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='basic.currency'),
        ),
        migrations.AddField(
            model_name='companyinfo',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.language'),
        ),
    ]
