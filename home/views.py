import csv
import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404  # noqa
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator  # noqa
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.decorators.cache import cache_page  # noqa
from django.views.generic import ListView, CreateView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from home.emails import send_email_sign_up
from home.forms import StudentForm, BookForm, SubjectForm, StudentToSomeObject, TeacherForm, UserSignUpForm  # noqa
from home.models import Student, Teacher, Book, Subject, Currency  # noqa
from home.serializers import StudentSerializer, SubjectSerializer, TeacherSerializer, BookSerializer
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
              'picture',
              ]
    success_url = reverse_lazy('page_list_students')


# @method_decorator(cache_page(settings.CHACHE_TTL), name='dispatch')
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
        """
        rewrite func to catch get data and search for navfild input an the page.
        :return: filtered queryset of students
        """
        teacher = self.request.GET.get('search_teacher')
        subject = self.request.GET.get('search_subject')
        book = self.request.GET.get('search_book')
        if teacher:
            students = Student.objects.filter(teachers__name=teacher)
            return students
        elif subject:
            students = Student.objects.filter(subject__title=subject)
            return students
        elif book:
            students = Student.objects.filter(book__title=book)
            return students

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
              'picture',
              ]
    template_name = 'update_student.html'
    success_url = reverse_lazy('page_list_students')


class StudentBook(ListView):
    """
    Func shows all students names and their books
    and add ability to delete book and student via link
    """
    model = Student
    template_name = 'student_books.html'


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


class StudentBookUpdate(UpdateView):
    model = Student
    fields = ['book']
    success_url = 'page_books_students'
    template_name = 'page_books_update'

    def post(self, request, id, **kwargs):
        """Def find and delete student in logic that we cant have student without book"""
        if 'DELETE' in self.request.POST:
            student_book = Student.objects.get(id=id)
            student_book.delete()

        return super(StudentBookUpdate, self).post(request, id)


class SubjectList(ListView):
    model = Subject
    template_name = 'subject_list.html'


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


class TeachersList(ListView):
    model = Teacher
    template_name = 'teachers_list.html'


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


class SignUpView(View):
    def get(self, request):
        sign_up_form = UserSignUpForm()
        return render(request, 'login/sign_up_form_page.html', context={
            'form': sign_up_form,
        })

    def post(self, request):
        sign_up_form = UserSignUpForm(request.POST)
        if sign_up_form.is_valid():
            # save user and make it unactive
            user = sign_up_form.save()
            user.is_active = False
            user.set_password(request.POST['password1'])
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))

            activate_url = '{}/{}/{}'.format(
                'http://localhost:8000/activate',
                uid,
                default_token_generator.make_token(user=user),
            )

            send_email_sign_up(
                recipient_list=[user.email],
                activate_url=activate_url,

            )
            return HttpResponse('Please, check your email-box')
        else:
            return HttpResponse('wrong data')


class ActivateView(View):

    def get(self, request, uid, token):
        # get user by decoded pk
        user = User.objects.get(pk=force_bytes(urlsafe_base64_decode(uid)))

        if not user.is_active and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            # no need to do this, cose save() return instance of our user
            # user = authenticate(username=user.username, password=user.password)

            login(request, user=user)
            return redirect('/list/')

        return redirect('/list/')


class SignOutView(View):

    def get(self, request):
        logout(request)
        return redirect('/list/')


class SignInView(View):

    def get(self, request):
        auth_form = AuthenticationForm()
        return render(request, 'login/sign_in.html', context={
            'form': auth_form,
        })

    def post(self, request):
        auth_form = AuthenticationForm(request.POST)

        user = authenticate(request=request, username=request.POST.get('username'),
                            password=request.POST.get('password'))
        login(request, user)
        return redirect('/list/')


# class StudentFilter(django_filters.FilterSet):
#  надо переопределить поля модели -> сделать у студентов поле учителя, чтобы фильтровать по имени учителя
# и добавить этот кастомный фильтр в ендпоинт
#     class Meta:
#         model = Student
#         fields = ('teachers__name',)


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all().order_by('name')
    serializer_class = StudentSerializer

    # add filters by model fields, this fields will not work if use custom filter
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("name", )
    # filter_class = StudentFilter
    ordering_fields = ['name', ]

    def create(self, request, *args, **kwargs):
        """
        Add transaction to create student and create a Book for him.
        In case if data is not valid transaction cancel creation of the Book
        """

        new_book = Book()
        new_book.title = uuid.uuid4()

        student_data = request.data
        student = Student.objects.create(name=student_data['name'], age=student_data['age'], email=student_data['email'])

        student.book = new_book
        with transaction.atomic():
            new_book.save()

        serializer = StudentSerializer()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all().order_by('title')
    serializer_class = SubjectSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("title", )
    ordering_fields = ['title', ]


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all().order_by('name')
    serializer_class = TeacherSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("name", )
    ordering_fields = ['name', ]


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("title", )
    ordering_fields = ['title', ]
