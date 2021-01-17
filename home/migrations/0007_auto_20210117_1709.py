# Generated by Django 3.1.5 on 2021-01-17 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_student_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('students', models.ManyToManyField(related_name='teachers', related_query_name='teachers', to='home.Student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='book',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student', related_query_name='student', to='home.book'),
        ),
        migrations.AddField(
            model_name='student',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student', related_query_name='student', to='home.subject'),
        ),
    ]