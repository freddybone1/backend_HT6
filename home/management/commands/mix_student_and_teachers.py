from random import random

from django.core.management import BaseCommand

from home.models import Student, Teacher


class Command(BaseCommand):
    def handle(self, *args, **options):
        students = Student.objects.all()

        teachers = Teacher.objects.all()

        for teacher in teachers:
            for _ in range(20):
                teacher.students = random.choice(students)

