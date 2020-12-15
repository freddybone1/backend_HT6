from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from home.models import Student


def home(request):
    student = Student()
    # student.name = 'Newbee'
    # student.save()

    students = Student.objects.all()

    return render(request, 'index.html', context={'name': 'Evhen', 'students': students})
