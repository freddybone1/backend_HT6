from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm  # noqa
from django import forms
from home.models import Student, Book, Subject, Teacher  # noqa


class StudentForm(ModelForm):
    class Meta:
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


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title',
                  ]


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['title',
                  ]


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['name',
                  ]


class StudentToSomeObject(forms.Form):
    student_id = forms.CharField(label='student_id')


class UserSignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
