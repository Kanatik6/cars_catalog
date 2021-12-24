from bs4 import BeautifulSoup as B
from decimal import Decimal as D
import requests
import sys
import re

from .models import CarBrand,Car
from .utils import normalize_str, get_soup

def parse_category(type=None):
    
    url = 'https://cars.kg/offers'
    response = requests.get(url)
    if response.status_code != 200:
        print(response.status_code)
        sys.exit()
    soup = B(response.content,'html.parser')
    marks = soup.find_all('select',attrs={'class':'select','name':'vendor','id':'m_search_vendor'})[0].get_text()
    marks = marks.replace('\xa0','').split('\n')[2:-1]
    
    if type=='for_find':
        a = CarBrand.objects.values_list('brand_name')
        a = [x[0] for x in a]
        return a

# def normalize_str(str):
#     space = True
#     list_delete = list()
#     list_ = list(str.strip().replace(' ','_').replace('-',' '))
#     for index,letter in enumerate(list_):
#         if space == True and letter == '_':
#             list_delete.append(index)
#         elif space == True and letter !='_':
#             space = False
#         elif letter == '_':
#             space = True
#     list_delete = [list_.pop(value)for value in reversed(list_delete)]

#     return ''.join(list_)

def find_car_urls():
    list_of_car_urls = list()
    list_of_pages = [f'https://www.mashina.kg/search/all/?page={x}' for x in range(1,20)]
    print(list_of_pages)
    for url in list_of_pages:
        response = requests.get(url)
        soup = B(response.content,'html.parser')
        cars_table = soup.find('div',class_='search-results-table')
        a = cars_table.findAll('div', class_=['table-view-list', 'image-view', 'clr', 'label-view'])
        b = a[1].findAll('div', class_=['list-item', 'list-label', 'new-line'])
        for i in b:
            try:
                list_of_car_urls.append('https://www.mashina.kg'+i.find('a').get('href'))
            except AttributeError:
                continue
    return list_of_car_urls

def parse_car(list_of_car_url:list):
    for i in list_of_car_url:
        response = requests.get(i)
        soup = B(response.content,'html.parser')
        print(soup.find('div',class_='price-types').get_text())
        print(soup.find('div',class_='head-left clr').find('h1').get_text().replace('Продажа ',''))
        cars_attrs_table = soup.find('div',attrs={'id':'home','class':'tab-pane'})
        # print(len(cars_attrs_table))
        car_attrs = soup.find_all('div',class_='field-row clr')
        attrs_dict = dict()
        for attr in car_attrs:
            c =normalize_str(attr.get_text().strip()).split('\n')
            attrs_dict[c[0]] = c[-1]
        print(attrs_dict)
        
        not_found = 'Не указано'
        full_name = soup.find('div',class_='head-left clr').find('h1').get_text().replace('Продажа ','')
        price = soup.find('div',class_='price-types').get_text()
        
        price = D(int(price.split('\n')[1].replace('$','').replace(' ','')))
        print(price)
        url = i
        mileage = attrs_dict.get('Пробег',0)
        mileage = int(float(re.sub('\D','',str(mileage))))
        year = int(attrs_dict.get('Год_выпуска',0))
        print(i)
        
        categories_str = '-'.join(parse_category(type='for_find'))
        find = full_name.split()[0]
        t = find + '(\s\w+)*-'
        try:
            result =re.search(t,categories_str)[0][:-1]
        except Exception:
            if find == "ВАЗ":
                if "ВАЗ (Lada)" in categories_str:
                    result = 'ВАЗ (Lada)'
        brand = CarBrand.objects.get(brand_name=result)

        Car.objects.get_or_create(full_name=full_name,
                           price=price,
                           mileage=mileage,
                           year=year,
                           url=url,
                           brand=brand)
        
def up():
    list_of_urls = find_car_urls()
    parse_car(list_of_urls)
    