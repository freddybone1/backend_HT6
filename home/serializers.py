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
    students = StudentSerializer(many=True)

    class Meta:
        model = Teacher
        fields = ['name', 'students']
