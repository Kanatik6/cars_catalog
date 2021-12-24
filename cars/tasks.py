from celery import shared_task

from .parse import up as up_cars_kg
from .parse_mashina_kg import up as up_mashina_kg

@shared_task
def up_all():
    up_mashina_kg()
    up_cars_kg('https://cars.kg/offers/')

@shared_task
def check():
    print('-')