from django.db import models
from django.db.models import Model


class Student(Model):
    """
    Student model with list of attributes
    """
    id = models.IntegerField(primary_key=True)  # noqa
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    birthday = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
