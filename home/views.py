
import csv

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from django.shortcuts import render, redirect, get_object_or_404  # noqa
from django.urls import reverse
from django.views import View

from backend_HT5.celery import simple_task

from home.forms import StudentForm, BookForm, SubjectForm  # noqa
from home.models import Student, Teacher, Book, Subject, Currency  # noqa


class AddStudent(View):
    """
    Generates form which need to create new student.
    If the process is OK - redirect to /list page.
    """

    def get(self, request):
        student_form = StudentForm()
        context = {
            'student_form': student_form,
        }
        return render(request, 'add_student.html', context=context)

    def post(self, request):
        """
        Save new student's data into database
        """
        student_form = StudentForm(request.POST)
        # Check if the data of new student is valid
        # if student_form.is_valid():
        #     student_form.save()
        # else:
        #     return HttpResponse("problem")
        student_form.save()
        return HttpResponseRedirect(reverse('page_list_students'))


class ShowStudent(View):
    """
    Function just show full list of students' name using '/list' - link
    """

    def get(self, request):
        students = Student.objects.all()
        teachers = Teacher.objects.all()
        # running celery task while enter list page
        simple_task.delay()

        # get curenncy value from db and take usd and eu value from there
        currency = Currency.objects.last()
        currency_list = [currency.value[0]['buy'], currency.value[1]['buy']]

        return render(request=request,
                      template_name='list_of_students.html',
                      context={'students': students,
                               'teachers': teachers,
                               'currency': currency_list
                               })


class UpdateStudent(View):

    def get(self, request, id):
        """
        Func allow to update info about student using list/up/<id>
        """
        student = get_object_or_404(Student, id=id)

        student_form = StudentForm(instance=student)

        context = {
            'student_form': student_form,
            'student': student,
        }

        return render(request, 'update_student.html', context=context)

    def post(self, request, id):
        """
        Function save changes in student objects in database
        """
        student = get_object_or_404(Student, id=id)

        student_form = StudentForm(request.POST, instance=student)

        if student_form.is_valid():
            student_form.save()

        return redirect(reverse('page_list_students'))


class StudentBook(View):
    def get(self, request):
        """
        Func shows all students names and their books
        and add ability to delete book and student via link
        """

        students = Student.objects.all()

        context = {
            'students': students,
        }

        return render(request, 'student_books.html', context=context)


class JsonView(View):
    def get(self, request):
        """
        func transform query set of student objects to list of dict which we are send as JSON response
        """
        students = Student.objects.all()
        return JsonResponse({"students": list(students.values(
            "name",
            "surname",
            "book__title",
            "subject__title",
        )),
        })


class CsvView(View):
    def get(self, request):
        """
        func create ad full csv file with selected data and allow user to download it

        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename='data_students.csv'"

        writer = csv.writer(response)
        writer.writerow(["Name", "Surname", "Book", 'Subject'])

        students = Student.objects.all()
        for student in students:
            writer.writerow([
                student.name,
                student.surname,
                student.book.title if student.book else None,
                student.subject.title if student.subject else None,
            ])
        return response


class MainView(View):
    def get(self, request):
        return render(request, 'main_page.html')


class StudentBookUpdate(View):
    """
    Function delete book and related student from database. Also, it allows to change title of a book
    """

    def get(self, request, id):
        student = get_object_or_404(Student, id=id)
        # Send to page form with student's book info, which we are able to change
        book = student.book
        book_form = BookForm(instance=book)
        context = {
            'student': student,
            'form': book_form,

        }
        return render(request, 'student_book_update.html', context=context)

    def post(self, request, id):
        # Make a tree to define which button was pushed
        if 'Save' in request.POST:
            student = get_object_or_404(Student, id=id)

            book = student.book
            book_form = BookForm(request.POST, instance=book)
            # Check if the form is valid
            if book_form.is_valid():
                book_form.save()
                return redirect('page_books_students')
            else:
                return HttpResponse(u'Upps, something went wrong')

        elif 'DELETE' in request.POST:
            book = get_object_or_404(Book, id=id)
            book.delete()
            return HttpResponseRedirect(reverse('page_books_students'))


class SubjectList(View):
    def get(self, request):
        subjects = Subject.objects.all()

        context = {

            'subjects': subjects,

        }
        return render(request, 'subject_list.html', context=context)


class SubjectUpdate(View):
    def get(self, request, id):
        subject = get_object_or_404(Subject, id=id)

        subject_form = SubjectForm(instance=subject)

        context = {
            'subject': subject,
            'form': subject_form,
        }
        return render(request, 'update_subject.html', context=context)

    def post(self, request, id):
        if 'Save' in request.POST:
            subject = get_object_or_404(Subject, id=id)

            subject_form = SubjectForm(request.POST, instance=subject)
            # Check if the form is valid
            if subject_form.is_valid():
                subject_form.save()
                return redirect('page_subject_list')
            else:
                return HttpResponse(u'Upps, something went wrong')
        elif 'DELETE' in request.POST:
            student = get_object_or_404(Student, id=id)
            subjects = Subject.objects.all()
            for subject in subjects:
                if student in subject.student.all():
                    subject.student.remove(student)
            return HttpResponseRedirect(reverse('page_subject_list'))
