# Generated by Django 3.1.5 on 2021-01-24 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='value',
            field=models.JSONField(),
        ),
    ]
