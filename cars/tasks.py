from celery import shared_task

from .parse import up as up_cars_kg
from .parse_mashina_kg import up as up_mashina_kg
from .models import Car,CarBrand

@shared_task
def up_all():
    up_mashina_kg()
    up_cars_kg('https://cars.kg/offers/')

@shared_task
def check():
    print('-')
    
# @shared_task
# def drop_base():
#     for car in Car.objects.all():
#         car.delete()
#     for brand in CarBrand.objects.all():
#         brand.delete()