# Generated by Django 4.0 on 2021-12-20 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=1, max_digits=15)),
                ('mileage', models.CharField(default='Не указано', max_length=20)),
                ('breed', models.CharField(default='Не указано', max_length=20)),
                ('url', models.URLField(max_length=100)),
                ('brand', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='CarBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=30)),
            ],
        ),
    ]
