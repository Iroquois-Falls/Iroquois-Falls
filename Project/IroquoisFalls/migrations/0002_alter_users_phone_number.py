# Generated by Django 5.1.6 on 2025-02-25 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IroquoisFalls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone_number',
            field=models.BigIntegerField(default='0000000000'),
        ),
    ]
