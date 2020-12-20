from django.shortcuts import render

# Create your views here.
from home.models import Student


def home(request):
    """
    Generates main page using data from db database.
     Show list of students' names
    """
    students = Student.objects.all()

    return render(request, 'index.html', context={'students': students})
