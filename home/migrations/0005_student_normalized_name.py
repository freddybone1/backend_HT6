# Generated by Django 3.1.4 on 2020-12-27 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_student_custom_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='normalized_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
