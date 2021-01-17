import uuid

from django.core.management import BaseCommand  # noqa
from home.models import Student, Subject, Book, Teacher  # noqa
from faker import Faker  # noqa


class Command(BaseCommand):
    help = 'Insert new students to the database'  # noqa

    def add_arguments(self, parser):
        """
        Adjust number of generating students
        """
        parser.add_argument('-l', '--len', type=int, default=10)

    def handle(self, *args, **options):
        """
        Generate some amount (default = 10) of Student object(with attributes)
        and save to the database. Use a Faker lib to fill all needed data
        """
        faker = Faker()
        for _ in range(options['len']):
            book = Book()
            book.title = uuid.uuid4()
            book.save()

            subject, _ = Subject.objects.get_or_create(title='Python')

            student = Student()

            student.name = faker.first_name()
            student.surname = faker.last_name()
            student.age = faker.random_int(10, 100)
            # student.sex = faker.bothify(text='?', letters='FM')
            student.address = faker.address()
            student.description = faker.text()
            student.birthday = faker.date(pattern='%d-%m-%Y')
            student.email = faker.email()
            student.social_url = faker.url()
            student.book = book
            student.subject = subject
            student.save()

            teacher, _ = Teacher.objects.get_or_create(name="Betty")

            teacher.save()
            teacher.students.add(student)