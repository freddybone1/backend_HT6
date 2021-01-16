from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404  # noqa
from django.urls import reverse
from django.views import View

from home.forms import StudentForm  # noqa
from home.models import Student  # noqa


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
        # if student_form.is_valid():
        #     student_form.save()
        # else:
        #     return HttpResponse("problem")
        student_form.save()
        return HttpResponseRedirect(reverse('page_list_students'))


class ShowStudent(View):
    """
    Function just show full list of students' name using '/list' - link
    """

    def get(self, request):
        students = Student.objects.all()

        return render(request=request,
                      template_name='list_of_students.html',
                      context={'students': students})


class UpdateStudent(View):

    def get(self, request, id):
        """
        Func allow to update info about student using list/up/<id>
        """
        student = get_object_or_404(Student, id=id)

        student_form = StudentForm(instance=student)

        context = {
            'student_form': student_form,
            'student': student,
        }

        return render(request, 'update_student.html', context=context)


    def post(self, request, id):
        """
        Function save changes in student objects in database
        """
        student = get_object_or_404(Student, id=id)

        student_form = StudentForm(request.POST, instance=student)

        if student_form.is_valid():
            student_form.save()

        return redirect(reverse('page_list_students'))
