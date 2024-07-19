# Generated by Django 5.0.4 on 2024-06-06 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invent', '0004_alter_inventwarehouse_warehouse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventaisle',
            old_name='ailse',
            new_name='aisle',
        ),
        migrations.RenameField(
            model_name='inventlocation',
            old_name='ailse',
            new_name='aisle',
        ),
        migrations.AlterUniqueTogether(
            name='inventaisle',
            unique_together={('warehouse', 'aisle')},
        ),
    ]
