import requests
from celery import shared_task, chain

from home.models import Currency


'''
from home.tasks import *
'''


@shared_task(max_retries=3)
def get_currency():
    """
    Парсим данные с сайта приват банка
    """
    currency_response = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
    return currency_response.json()


@shared_task
def save_currency(data):
    """
    Сохраняем данные в модель
    """
    currency = Currency()
    currency.value = data
    currency.save()
    return True


@shared_task
def parse_currency():

    chain(
        get_currency.si()
        |
        save_currency.s())()
