import freezegun
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from home.models import Student, Teacher, Book, Subject
from home.testcases import value_for_test_read_student, value_for_test_read_books, value_for_test_read_subjects

'''
-to check test on code use library coverage:
    poetry add coverage
-check coverage with command:
    coverage run --source='home' manage.py test
-user view of collect data
    coverage html --include='home/views.py'
'''


@freezegun.freeze_time('1991-02-20 00:00:00')
class HomeStudentUnitTests(APITestCase):
    # @skip('reason to skip test') # -> use if need to skip some test at the moment
    def test_create_student(self):
        # create object
        response = self.client.post(
            reverse('students-list'),
            data={
                'name': 'Test_Student',
                'age': 21,
                'email': 'email@email.com',
                'created_at': '1991-02-20T00:00:00Z',
            }
        )
        # check if object had been created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_student(self):
        # to check template response
        Student.objects.create(name='first_student')
        Student.objects.create(name='second_student')

        response = self.client.get(reverse('students-list'))
        # check if response is equal to json (in file) what we expected
        self.assertEqual(response.json(), value_for_test_read_student)

    def test_update_student(self):
        # create object
        self.client.post(
            reverse('students-list'),
            data={
                'name': 'Test_Student',
                'age': 21,
                'email': 'email@email.com',
                'created_at': '1991-02-20T00:00:00Z',
            }
        )

        students = Student.objects.all()
        # update object`s info using its pk
        self.client.patch(reverse('students-detail', kwargs={"pk": students[0].id, }, ), data={'name': 'Change'})
        # check changes
        self.assertEqual(students[0].name, 'Change')

    def test_delete_student(self):
        # create object
        response = self.client.post(
            reverse('students-list'),
            data={
                'name': 'Test_Student',
                'age': 21,
                'email': 'email@email.com',
            }
        )
        # check if created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check creation via quantitity of objects
        students = Student.objects.all()
        self.assertEqual(students.count(), 1)
        # delete object and check deletion
        self.client.delete(reverse('students-detail', kwargs={"pk": students[0].id, }))
        students = Student.objects.all()
        self.assertEqual(students.count(), 0)


@freezegun.freeze_time('1991-02-20 00:00:00')
class HomeTeacherUnitTests(APITestCase):
    def test_create_teacher(self):
        response = self.client.post(
            reverse('teachers-list'),
            data={
                'name': 'Test_Teacher',
                'created_at': '1991-02-20T00:00:00Z',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        teachers = Teacher.objects.all()
        self.assertEqual(teachers.count(), 1)

    def test_read_teacher(self):
        response = self.client.get(reverse('teachers-list'))
        self.assertEqual(response.json(), {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_update_teacher(self):
        # create object
        self.client.post(
            reverse('teachers-list'),
            data={
                'name': 'Test_Teacher',
                'created_at': '1991-02-20T00:00:00Z',
            }
        )

        teachers = Teacher.objects.all()
        # update object`s info using its pk
        self.client.patch(reverse('teachers-detail', kwargs={"pk": teachers[0].id, }, ), data={'name': 'Change'})
        # check changes
        self.assertEqual(teachers[0].name, 'Change')

    def test_delete_teacher(self):
        # create object
        response = self.client.post(
            reverse('teachers-list'),
            data={
                'name': 'Test_Teacher',
                'created_at': '1991-02-20T00:00:00Z',
            }
        )
        # check if created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check creation via quantitity of objects
        teachers = Teacher.objects.all()
        self.assertEqual(teachers.count(), 1)
        # delete object and check deletion
        self.client.delete(reverse('teachers-detail', kwargs={"pk": teachers[0].id, }))
        teachers = Teacher.objects.all()
        self.assertEqual(teachers.count(), 0)


@freezegun.freeze_time('1991-02-20 00:00:00')
class HomeBookUnitTests(APITestCase):

    def test_create_book(self):
        # create object
        response = self.client.post(
            reverse('books-list'),
            data={
                'title': 'Test_Book',
                'created_at': '1991-02-20T00:00:00Z',
            }
        )
        # check if object had been created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_book(self):
        # to check template response
        Book.objects.create(title='first_book')
        Book.objects.create(title='second_book')

        response = self.client.get(reverse('books-list'))
        # check if response is equal to json (in file) what we expected
        self.assertEqual(response.json(), value_for_test_read_books)

    def test_update_book(self):
        # create object
        self.client.post(
            reverse('books-list'),
            data={
                'title': 'Test_Book',
                'created_at': '1991-02-20T00:00:00Z',
            }
        )

        books = Book.objects.all()
        # update object`s info using its pk
        self.client.patch(reverse('books-detail', kwargs={"pk": books[0].id, }, ), data={'title': 'Change'})
        # check changes
        self.assertEqual(books[0].title, 'Change')

    def test_delete_book(self):
        # create object
        response = self.client.post(
            reverse('books-list'),
            data={
                'title': 'Test_Book',
                'created_at': '1991-02-20T00:00:00Z',
            }
        )
        # check if created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check creation via quantitity of objects
        books = Book.objects.all()
        self.assertEqual(books.count(), 1)
        # delete object and check deletion
        self.client.delete(reverse('books-detail', kwargs={"pk": books[0].id, }))
        books = Book.objects.all()
        self.assertEqual(books.count(), 0)


@freezegun.freeze_time('1991-02-20 00:00:00')
class HomeSubjectUnitTests(APITestCase):

    def test_create_subject(self):
        # create object
        response = self.client.post(
            reverse('subjects-list'),
            data={
                'title': 'Test_Subject',
                'created_at': '1991-02-20T00:00:00Z',
            }
        )
        # check if object had been created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_book(self):
        # to check template response
        Subject.objects.create(title='first_subject')
        Subject.objects.create(title='second_subject')

        response = self.client.get(reverse('subjects-list'))
        # check if response is equal to json (in file) what we expected
        self.assertEqual(response.json(), value_for_test_read_subjects)

    def test_update_book(self):
        # create object
        self.client.post(
            reverse('subjects-list'),
            data={
                'title': 'Test_Subject',
                'created_at': '1991-02-20T00:00:00Z',
            }
        )

        subjects = Subject.objects.all()
        # update object`s info using its pk
        self.client.patch(reverse('subjects-detail', kwargs={"pk": subjects[0].id, }, ), data={'title': 'Change'})
        # check changes
        self.assertEqual(subjects[0].title, 'Change')

    def test_delete_book(self):
        # create object
        response = self.client.post(
            reverse('subjects-list'),
            data={
                'title': 'Test_subject',
                'created_at': '1991-02-20T00:00:00Z',
            }
        )
        # check if created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check creation via quantitity of objects
        subjects = Subject.objects.all()
        self.assertEqual(subjects.count(), 1)
        # delete object and check deletion
        self.client.delete(reverse('subjects-detail', kwargs={"pk": subjects[0].id, }))
        subjects = Subject.objects.all()
        self.assertEqual(subjects.count(), 0)
