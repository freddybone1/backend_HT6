from django.db.models.signals import pre_save
from django.dispatch import receiver

from home.models import Student


@receiver(pre_save, sender=Student)
def normalized_name(sender, instance, **kwargs):
    instance.normalized_name = '{} {}'.format(instance.name.lower(), instance.surname.lower())
