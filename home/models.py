from django.db import models
from django.db.models import Model


class Student(Model):
    """
    Student model with list of attributes
    """
    id = models.AutoField(primary_key=True)  # noqa
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    age = models.IntegerField(default=0, null=True)
    sex = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=1000, null=True)
    birthday = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    social_url = models.CharField(max_length=200, null=True)
    normalized_name = models.CharField(max_length=200, null=True)
    is_active = models.CharField(max_length=200, null=True)

    subject = models.ForeignKey(to='home.Subject', on_delete=models.SET_NULL, null=True, related_name='student', related_query_name='student')
    book = models.OneToOneField(to='home.Book', on_delete=models.CASCADE, null=True, related_name='student', related_query_name='student')


class Subject(Model):
    title = models.CharField(max_length=200)


class Book(Model):
    id = models.AutoField(primary_key=True)  # noqa
    title = models.CharField(max_length=200)


class Teacher(Model):
    id = models.AutoField(primary_key=True)  # noqa
    name = models.CharField(max_length=200)
    students = models.ManyToManyField(to='home.Student', related_name='teachers', related_query_name='teachers')
