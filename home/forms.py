from django.forms import ModelForm  # noqa

from home.models import Student, Book  # noqa


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
