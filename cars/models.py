from django.db import models


class Car(models.Model):
    full_name = models.CharField(max_length=20,default="Не указано")
    price = models.DecimalField(max_digits=15,decimal_places=1,default=0)
    mileage = models.CharField(max_length=20,default='Не указано')
    breed = models.CharField(max_length=20,default='Не указано')
    url = models.URLField(max_length=100)
    brand = models.CharField(max_length=30)

    def __str__(self):
        return self.full_name

# cars = Car.objects.all().order_by('price')
# fin_cars = []



# # * Главная модель автомобиля, к которой идут все остальные параметры
# class Car(models.Model):
#     price = models.PositiveIntegerField(default=0)
#     # * serializer-validators
#     year = models.PositiveIntegerField(default=2000)
#     class Wheel(models.TextChoices):
#         LEFT = 'left'
#         RIGHT = 'right'
#     whell = models.CharField(max_length=5,choices=Wheel.choices,default=Wheel.RIGHT)

class CarBrand(models.Model):
    brand_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.brand_name
    



# cmd + d - выделение всех похожих

# сделать пару моделей с форенки, гет ор криет 
# вернуть модели
# форенки назад
# создавать как car и в качестве форенки атрибута, get_of_create