from django.db import models


class Car(models.Model):
    full_name = models.CharField(max_length=20,default="Не указано")
    price = models.DecimalField(max_digits=15,decimal_places=1,default=0)
    mileage = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=0)
    url = models.URLField(max_length=100)
    brand = models.ForeignKey('CarBrand',on_delete=models.CASCADE,related_name='cars')

    def __str__(self):
        return self.full_name


class CarBrand(models.Model):
    brand_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.brand_name


class Counter(models.Model):
    number = models.PositiveIntegerField(default=0)
# cmd + d - выделение всех похожих