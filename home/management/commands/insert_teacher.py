from django.core.management import BaseCommand
from faker import Faker

from home.models import Teacher


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-l', '--len', type=int, default=5)

    def handle(self, *args, **options):
        faker = Faker()
        for _ in range(options['len']):
            teacher = Teacher()
            teacher.name = faker.first_name()
            teacher.save()
