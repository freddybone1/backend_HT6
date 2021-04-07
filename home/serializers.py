from django.core.paginator import Paginator
from rest_framework import serializers

from home.models import Student, Teacher, Subject, Book


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['title']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title']


class StudentSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Student
        fields = ['name', 'age', 'email', 'subject', ]


class TeacherSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField('paginated_students')

    def paginated_students(self, obj):
        students = obj.students.all()

        pagination = Paginator(students, per_page=1)

        paginated_students = pagination.page(1)
        return StudentSerializer(instance=paginated_students, many=True).data

    class Meta:
        model = Teacher
        fields = ['name', 'students']
