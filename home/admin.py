# from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin  # noqa
from django.contrib import admin  # noqa
from django.utils.html import format_html  # noqa
from home.models import Student  # noqa


class StudentAdmin(ModelAdmin):
    list_display = ('link_to_social_url', 'email', 'birthday')

    def link_to_social_url(self, student):
        """
        Function checks if student has social media link and show his name like this link.
        In case if he doesnt have social media link show his full name
        In case if student dont have full name in database - function creates it and show to admin user
        """
        if student.social_url:
            return format_html('<a href="{}">{}</a>'.format(student.social_url, student.custom_name))
        elif student.custom_name:
            return student.custom_name
        else:
            return '{} {}'.format(student.name, student.surname)


admin.site.register(Student, StudentAdmin)
