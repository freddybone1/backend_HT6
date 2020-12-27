from django.db import models
from django.db.models import Model


class Student(Model):
    """
    Student model with list of attributes
    """
    id = models.IntegerField(primary_key=True)  # noqa
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