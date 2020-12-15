
from django.core.management import BaseCommand
from faker import Faker

from home.models import Student


class Command(BaseCommand):
    help = 'Insert new students to the database'

    def add_arguments(self, parser):
        parser.add_argument('-l', '--len', type=int, default=10)

    def handle(self, *args, **options):
        faker = Faker()
        for _ in range(options['len']):
            student = Student()
            student.name = faker.first_name()
            student.surname = faker.last_name()
            student.age = faker.random_int(10, 100)
            student.sex = faker.bothify(text='?', letters='FM')
            student.address = faker.address()
            student.description = faker.text()
            student.birthday = faker.date(pattern='%d-%m-%Y')
            student.email = faker.email()
            student.save()
