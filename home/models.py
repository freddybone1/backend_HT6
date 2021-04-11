from django.db import models
from django.db.models import Model


class Student(Model):
    """
    Student model with list of attributes
    """
    id = models.AutoField(primary_key=True)  # noqa
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200, blank=True)
    age = models.IntegerField(default=0, null=True, blank=True)
    sex = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    birthday = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    social_url = models.CharField(max_length=200, null=True, blank=True)
    normalized_name = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.CharField(max_length=200, null=True, blank=True)
    picture = models.ImageField(null=True, upload_to='student_photo', blank=True)

    subject = models.ForeignKey(to='home.Subject', on_delete=models.SET_NULL, null=True,
                                related_name='student', related_query_name='student')
    book = models.OneToOneField(to='home.Book', on_delete=models.CASCADE, null=True,
                                related_name='student', related_query_name='student')

    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)


class Subject(Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)


class Book(Model):
    id = models.AutoField(primary_key=True)  # noqa
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)


class Teacher(Model):
    id = models.AutoField(primary_key=True)  # noqa
    name = models.CharField(max_length=200)
    students = models.ManyToManyField(to='home.Student', related_name='teachers', related_query_name='teachers')
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)


class Currency(Model):
    id = models.AutoField(primary_key=True)
    value = models.JSONField()
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
