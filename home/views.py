from django.shortcuts import render, redirect  # noqa
from home.forms import StudentForm  # noqa
from home.models import Student  # noqa


def add_student(request):
    """
    Generates form which need to create new student.
    If the process is OK - redirect to /list page.
    """
    if request.method == 'GET':
        student_form = StudentForm()
        context = {
            'form': student_form,
        }
        return render(request, 'add_student.html', context=context)

    # Save new student's data into database
    elif request.method == 'POST':
        student_form = StudentForm(request.POST)
        # Check if the data of new student is valid
        if student_form.is_valid():
            student_form.save()
        student_form.save()
        return redirect('/list')


def show_all_students(request):
    """
    Function just show full list of students' name using '/list' - link
    """
    students = Student.objects.all()

    return render(request=request,
                  template_name='list_of_students.html',
                  context={'students': students})
