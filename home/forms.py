from django.forms import ModelForm  # noqa

from home.models import Student, Book, Subject  # noqa


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