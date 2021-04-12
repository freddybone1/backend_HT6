import uuid

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from faker import Faker

from home.models import Student, Book, Teacher


@receiver(pre_save, sender=Student)
def normalized_name(sender, instance, **kwargs):
    """On pre-save stage get student name and surname, then delete not approved
    symbols and make all string lower case"""
    instance.normalized_name = '{} {}'.format(instance.name.lower().strip(',.;:-_=+*&^%$#@!()`~'),
                                              instance.surname.lower().strip(',.;:-_=+*&^%$#@!()`~'))


@receiver(pre_save, sender=Student)
def which_gender(sender, instance, **kwargs):
    """
    Give to the student sex (male, female or unique), depend on his luck
    """
    faker = Faker()
    instance.sex = faker.bothify(text='?', letters='FMU')

# comment this due to add transaction to creation book with student in one time
# @receiver(pre_save, sender=Student)
# def add_book_to_new_student(sender, instance, **kwargs):
#     herd = instance.book
#     if not instance.book:
#         new_book = Book()
#         new_book.title = uuid.uuid4()
#         new_book.save()
#         instance.book = new_book

