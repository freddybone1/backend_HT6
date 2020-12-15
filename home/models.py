from django.db import models
from django.db.models import Model


class Student(Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200, default='')
    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    birthday = models.CharField(max_length=200)
    email = models.CharField(max_length=200)


