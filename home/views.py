from django.http import HttpResponse
from django.shortcuts import render, redirect  # noqa
from django.urls import reverse
from django.views import View

from home.forms import StudentForm  # noqa
from home.models import Student  # noqa


# def add_student(request):
#     """
#     Generates form which need to create new student.
#     If the process is OK - redirect to /list page.
#     """
#     if request.method == 'GET':
#         student_form = StudentForm()
#         context = {
#             'student_form': student_form,
#         }
#         return render(request, 'add_student.html', context=context)
#
#     # Save new student's data into database
#     elif request.method == 'POST':
#         student_form = StudentForm(request.POST)
#         # Check if the data of new student is valid
#         if student_form.is_valid():
#             student_form.save()
#         else:
#             return HttpResponse("problem")
#
#         return reverse('page_list_students')
#

# def show_all_students(request):
#     """
#     Function just show full list of students' name using '/list' - link
#     """
#     students = Student.objects.all()
#
#     return render(request=request,
#                   template_name='list_of_students.html',
#                   context={'students': students})
#

def update_student(request, id):
    """

        """
    if request.method == 'GET':
        student = Student.objects.get(id=id)
        student_form = StudentForm(instance=student)



        context = {
            'student_form': student_form,
        }
        return render(request, 'add_student.html', context=context)

    # Save new student's data into database
    elif request.method == 'POST':
        student_form = StudentForm(request.POST)
        # Check if the data of new student is valid
        if student_form.is_valid():
            student_form.save()
        else:
            return HttpResponse("problem")

        return redirect('/list')


class AddStudent(View):
    """
    Generates form which need to create new student.
    If the process is OK - redirect to /list page.
    """
    def get(self, request):
        student_form = StudentForm()
        context = {
            'student_form': student_form,
        }
        return render(request, 'add_student.html', context=context)

    def post(self, request):
        """
        Save new student's data into database
        """
        student_form = StudentForm(request.POST)
        # Check if the data of new student is valid
        if student_form.is_valid():
            student_form.save()
        else:
            return HttpResponse("problem")

        return reverse('page_list_students')


class ShowStudents(View):
    """
    Function just show full list of students' name using '/list' - link
    """

    def get(self, request):
        students = Student.objects.all()

        return render(request=request,
                      template_name='list_of_students.html',
                      context={'students': students})
