from django.core.management import BaseCommand

from home.models import Student


class Command(BaseCommand):
    def handle(self, *args, **options):
        student = Student.objects.first()
        student.delete()