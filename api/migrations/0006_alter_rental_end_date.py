# Generated by Django 5.1.1 on 2024-11-26 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_vehicle_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]