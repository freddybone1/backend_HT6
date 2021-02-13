from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404  # noqa
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from home.forms import StudentForm  # noqa
from home.models import Student, Teacher, Book, Currency  # noqa
from home.tasks import send_email_celery


class AddStudent(CreateView):
    """
    Generates form which need to create new student.
    If the process is OK - redirect to /list page.
    """
    model = Student
    template_name = 'add_student.html'
    fields = ['name',
              'surname',
              'age',
              'sex',
              'address',
              'birthday',
              'email',
              'social_url',
              ]
    success_url = reverse_lazy('page_list_students')


class ShowStudent(ListView):
    """
    Function just show full list of students' name using '/list' - link
    """
    model = Student
    template_name = 'list_of_students.html'
    context_object_name = 'currency'

    def get_context_data(self, **kwargs):
        currency = Currency.objects.last()
        currency_list = [currency.value[0]['buy'], currency.value[1]['buy']]

        context = super(ShowStudent, self).get_context_data(**kwargs)
        context.update({
            'currency': currency_list,

        })
        return context

    def get_queryset(self):
        return Student.objects.all()


class UpdateStudent(UpdateView):
    model = Student
    fields = ['name',
              'surname',
              'age',
              'sex',
              'address',
              'birthday',
              'email',
              'social_url',
              ]
    template_name = 'update_student.html'
    success_url = reverse_lazy('page_list_students')


class StudentBook(View):
    def get(self, request):
        """
        Func allow to update info about student using list/up/<id>
        """

        books = Book.objects.all()
        students = Student.objects.all()

        context = {
            'books': books,
            'students': students
        }

        return render(request, 'student_books.html', context=context)


class SendEmailView(View):
    """
    Celery send an email(with template) when visit that page
    """

    def get(self, request):
        try:
            send_email_celery(['hoodback@gmail.com', ]).delay()

        except AttributeError:
            return HttpResponse('Email sent!')
