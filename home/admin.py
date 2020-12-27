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
        In case if he doesn't have social media link show his full name
        """
        if student.social_url:
            return format_html('<a href="{}">{} {}</a>'.format(student.social_url, student.name, student.surname))
        else:
            return '{} {}'.format(student.name, student.surname)


admin.site.register(Student, StudentAdmin)
