from django.forms import ModelForm  # noqa

from home.models import Student  # noqa


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
                  'description',
                  'social_url',
                  ]
