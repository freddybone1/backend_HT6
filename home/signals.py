from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.http import HttpResponse
from faker import Faker

from home.models import Student


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

@receiver(pre_delete, sender=Student)
def no_delete(sender, instance, **kwargs):
    """
    Signal doesnt allow simple user to delete any student from database
    """
    raise Exception('You haven\'t permission to delete')
