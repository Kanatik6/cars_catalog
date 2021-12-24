from celery import shared_task
import requests
from typing import Tuple
from bs4 import BeautifulSoup as BS
import sys
import re

from .models import Car, CarBrand


@shared_task
def check():
    for i in range(1,21):
        print(i)
    return "Done"


# принимает строку, убирает лишние пробелы, заменяет их на _ и возвращет строку
def normalize_str(str: str) -> str:
    space = True
    list_delete = list()
    list_ = list(str.strip().replace(' ','_').replace('-',' '))
    for index,letter in enumerate(list_):
        if space == True and letter == '_':
            list_delete.append(index)
        elif space == True and letter !='_':
            space = False
        elif letter == '_':
            space = True
    list_delete = [list_.pop(value)for value in reversed(list_delete)]

    return ''.join(list_)

# принимает soup атрибута, нормализует ее и возаращает название и значение в форматe str
def normalize_attr(attr_soup: BS) :
        """
        Returns parsed request data
        """
        name_value_attr = normalize_str(attr_soup.get_text(strip=True,separator='-') if bool(attr_soup.get_text(strip=True)) else 'Не задано')
        return_list = name_value_attr.split(' ')
        return return_list[0].capitalize(),return_list[1]

# Принимает url страницы и возвращает ее soup
def get_soup(url:str):
    response = requests.get(url)
    if response.status_code == 200:
        return BS(response.content,'html.parser')
    else:  
        print('Неверный url')
        sys.exit()

# Фунцкия принимает суп основного url, и возвращает список из юрлов всех страниц
def get_list_url(request_url: str):
    list_counter = 0
    returned_list = list()
    while True:
        list_counter +=1
        url= request_url.rstrip('/')+'/'+str(list_counter)
        if get_soup(url).find('p') != None:
            break
        returned_list.append(url)
        print(url)
    return returned_list
        

# принимает url пользователя и запускает все программы
def up(url):
    list_of_pages = get_list_url(url)
    list_of_results =  parse_cars(list_of_pages)
    
    Car.objects.bulk_create(list_of_results)

# * Принимает список страниц из каталога, и возвращает список словарей
def parse_cars(list_of_pages:list):
    
    list_of_results = list()
    
    for list_ in list_of_pages:
        
        soup = get_soup(list_)
        catalog_list = soup.find('div',class_='catalog-list')
        cars = catalog_list.findAll('a',class_='catalog-list-item')
        
        categories_str = '-'.join(parse_category(type='qwe'))
        
        for car in cars:
            name = car.find('span',class_='catalog-item-params').find('span',class_='catalog-item-caption').get_text(strip=True)
            price= car.find('span',class_='catalog-item-params').find('span',class_='catalog-item-price').get_text(strip=True)
            price = re.sub('\D','',price)
            full_name = ' '.join(name.split(' ')[:-1])
            
            name = full_name
            url = 'https://cars.kg'+car.get('href')
            mileage = 'Не указано'
            print(url)
            # soup.find('div',class_='col-left catalog-card-params').find('div',class_='catalog-card-chars')
            soup_ = get_soup(url)
            year = list(soup_.find('div',class_='col-left catalog-card-params').find('div',class_='catalog-card-chars'))[1]
            year = int(re.sub('\D','',year.get_text()))
            if 'км' in name:
                name = name.split()
                index =  name.index('км') -1
                mileage = str(name.pop(index))
                name.pop(index)
                name = ' '.join(name)
            # todo поменять на год
            if 'поколение' in name:
                name = name.split()
                index =  name.index('поколение') -1
                name.pop(index)
                name = ' '.join(name)
                
            first_word = ''.join(name.split()[0])
            name = ' '.join(name.split()[1:])
            
            encoded_string = name.encode("ascii", "ignore")
            decode_string = encoded_string.decode()
            decode_string = first_word+' '+decode_string
            
            if '[]' in decode_string:
                decode_string = decode_string.replace('[]','')
            find = decode_string.split()[0]
            
            t = find + '(\s\w+)*-'
            try:
                result =re.search(t,categories_str)[0][:-1]
            except Exception:
                if find == "ВАЗ":
                    if "ВАЗ (Lada)" in categories_str:
                        result = 'ВАЗ (Lada)'
                    else:
                        print(find)
                        continue
                else:
                    print(find)
                    continue
                    
            brand =CarBrand.objects.get(brand_name=result)
            # print(result)
            print(full_name,price,find,year,mileage,url)
            if  Car.objects.filter(full_name=full_name,
                                    price=price,
                                    brand=brand,
                                    year=year,
                                    mileage=mileage,
                                    url=url).exists():
                continue

            list_of_results.append(Car(full_name=full_name,
                                        price=price,
                                        brand=brand,
                                        year=year,
                                        mileage=mileage,
                                        url=url))
        print('-',list_of_results)
    Car.objects.bulk_create(list_of_results)
    return categories_str        
            
def parse_category(type=None):
    
    '''Эта функция должна парсить категории,не передаваться в таск и единственный раз активироваться, чтобы заполнить базу,
    а дальше будет работать только в случае если модель не находит ее в базе, даже после второго поиска, и если после
    повторного поиска не находит, то передает в mail и уже там я все узнаю     '''
    
    url = 'https://cars.kg/offers'
    response = requests.get(url)
    if response.status_code != 200:
        print(response.status_code)
        sys.exit()
    soup = BS(response.content,'html.parser')
    marks = soup.find_all('select',attrs={'class':'select','name':'vendor','id':'m_search_vendor'})[0].get_text()
    # тут все марки со всеми словами
    marks = marks.replace('\xa0','').split('\n')[2:-1]
    
    if type == None:
        {index:CarBrand.objects.get_or_create(brand_name=mark.strip()) for index,mark in enumerate(marks)}
        return {'Success':True}
    elif type=='qwe':
        a = CarBrand.objects.values_list('brand_name')
        a = [x[0] for x in a]
        return a

# from cars.tasks import parse_cars
# parse_cars(['https://cars.kg/offers/','https://cars.kg/offers/2'])



# from bs4 import BeautifulSoup as BS
# import requests
# response = requests.get('https://cars.kg/offers/1119080.html')
# soup = BS(response.content,'html.parser')
# table = soup.find('div',class_='col-left catalog-card-params').find('div',class_='catalog-card-chars')


# from cars.tasks import parse_cars
# parse_cars(['https://cars.kg/offers/','https://cars.kg/offers/2'])