# Generated by Django 3.1.4 on 2020-12-27 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_student_normalized_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_active',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
