# Generated by Django 5.1.1 on 2024-11-01 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='rental',
            name='start_date',
            field=models.DateField(),
        ),
    ]
