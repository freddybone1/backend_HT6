
import csv

from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from django.shortcuts import render, redirect, get_object_or_404  # noqa

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView


from home.forms import StudentForm  # noqa
from home.models import Student, Teacher, Book, Currency  # noqa

from home.forms import StudentForm, BookForm, SubjectForm, StudentToSomeObject, TeacherForm  # noqa
from home.models import Student, Teacher, Book, Subject, Currency  # noqa
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
    

@method_decorator(cache_page(settings.CHACHE_TTL), name='dispatch')
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
        Func shows all students names and their books
        and add ability to delete book and student via link
        """

        students = Student.objects.all()

        context = {
            'students': students,
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
    """
    Class give possibility to see relations between subject and its students.
     Also you can change title of related subject and students relations.
    """

    def get(self, request, id):
        subject = get_object_or_404(Subject, id=id)

        subject_form = SubjectForm(instance=subject)
        student_form = StudentToSomeObject()

        context = {
            'subject': subject,
            'form': subject_form,
            'student_form': student_form,
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

        elif 'Add student' in request.POST:
            subjects = Subject.objects.all()
            # забираем данные из нашей кастомной формы
            form = StudentToSomeObject(request.POST)
            # забираем данные из нашей кастомной формы обязательно через .is_valid() -> .cleaned_data.get(field)
            if form.is_valid():
                # сохраняем данные из формы, которая не привязана к нашим моделям, по переменой филда из формы
                student_id = form.cleaned_data.get('student_id')
                student = get_object_or_404(Student, id=int(student_id))
                for subject in subjects:
                    if student not in subject.student.all():
                        subject.student.add(student)
                        return HttpResponseRedirect(reverse('page_subject_list'))

            else:
                return HttpResponse('Bad data format, please use only integers')


class TeachersList(View):
    def get(self, request):
        student = Student.objects.all()
        teachers = Teacher.objects.all()

        context = {
            "teachers": teachers,
            'student': student,
        }
        return render(request, 'teachers_list.html', context=context)


class TeacherUpdate(View):
    def get(self, request, id):
        teacher = get_object_or_404(Teacher, id=id)

        teacher_form = TeacherForm(instance=teacher)
        student_form = StudentToSomeObject()

        context = {
            'teacher': teacher,
            'form': teacher_form,
            'student_form': student_form,
        }
        return render(request, 'update_teacher.html', context=context)

    def post(self, request, id):
        if 'Save' in request.POST:
            teacher = get_object_or_404(Teacher, id=id)

            teacher_form = TeacherForm(request.POST, instance=teacher)

            if teacher_form.is_valid():
                teacher_form.save()
                return redirect('page_teacher_list')
            else:
                return HttpResponse(u'Upps, something went wrong')
        elif 'DELETE' in request.POST:
            student = get_object_or_404(Student, id=id)
            teachers = Teacher.objects.all()

            for teacher in teachers:
                if student in teacher.students.all():
                    teacher.students.remove(student)
            return HttpResponseRedirect(reverse('page_teacher_list'))

        elif 'Add student' in request.POST:
            teachers = Teacher.objects.all()
            form = StudentToSomeObject(request.POST)
            if form.is_valid():
                student_id = form.cleaned_data.get('student_id')
                student = get_object_or_404(Student, id=int(student_id))
                for teacher in teachers:
                    if student not in teacher.students.all():
                        teacher.students.add(student)
                        return HttpResponseRedirect(reverse('page_teacher_list'))
            else:
                return HttpResponse('Bad data format, please use only integers')
