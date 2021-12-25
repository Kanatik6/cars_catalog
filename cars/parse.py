from bs4 import BeautifulSoup as BS
import requests
import sys
import re

from .models import Car, CarBrand,Counter
from .utils import get_soup

# Фунцкия принимает суп основного url, и возвращает список из юрлов всех страниц
def get_list_url(request_url: str,list_counter=0):
    returned_list = list()
    while True:
        list_counter +=1
        url= request_url.rstrip('/')+'/'+str(list_counter)
        if get_soup(url) == False:
            print(url)
            continue
        if get_soup(url).find('p') != None:
            break
        returned_list.append(url)
        print(url)
    return returned_list
        

# принимает url пользователя и запускает все программы
def up(url):
    print(parse_category())
    try:
        counter = Counter.objects.all().first().number
    except AttributeError:
        counter = 56
    print(counter)
    list_of_pages = get_list_url(url,list_counter=counter)
    parse_cars(list_of_pages)

# * Принимает список страниц из каталога, и возвращает список словарей
def parse_cars(list_of_pages:list):
    try:
        number = Counter.objects.all().first().number
        print(number,'--')
    except AttributeError:
        number = 56
        print(number)
    # for i in Counter.objects.all():
    #     i.delete()
    # list_of_pages = list_of_pages[counter.number:]
    for index,list_ in enumerate(list_of_pages):
        list_of_results = list()
        soup = get_soup(list_)
        if soup == False:
            print(list_)
            continue
        # catalog_list = soup.find('div',class_='catalog-list')
        cars = soup.findAll('a',class_='catalog-list-item')
        
        categories_str = '-'.join(parse_category(type='for_find'))
        
        for car in cars:
            name = car.find('span',class_='catalog-item-params').find('span',class_='catalog-item-caption').get_text(strip=True)
            price= car.find('span',class_='catalog-item-params').find('span',class_='catalog-item-price').get_text(strip=True)
            price = re.sub('\D','',price)
            full_name = ' '.join(name.split(' ')[:-1])
            
            name = full_name
            url = 'https://cars.kg'+car.get('href')
            mileage = 0
            print(url)
            # soup.find('div',class_='col-left catalog-card-params').find('div',class_='catalog-card-chars')
            soup_ = get_soup(url)
            if soup_ == False:
                print(url)
                continue
            year = list(soup_.find('div',class_='col-left catalog-card-params').find('div',class_='catalog-card-chars'))[1]
            year = int(re.sub('\D','',year.get_text()))
            mileage_soup = list(soup_.find('div',class_='col-left catalog-card-params').find('div',class_='catalog-card-chars'))[3]
            
            if 'Пробег' in mileage_soup.get_text():
                mileage = int(float(re.sub('\D','',mileage_soup.get_text())))
            if 'поколение' in name:
                name = name.split()
                index =  name.index('поколение') -1
                name.pop(index)
                name = ' '.join(name)
                
            try:
                first_word = ''.join(name.split()[0])
            except IndexError:
                continue
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
            print(full_name,price,find,year,mileage,url,'-'*20)
            # print(result)
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
        print('\n\n\n',list_)
        Car.objects.bulk_create(list_of_results)
        try:
            Counter.objects.all().first().delete()
        except AttributeError:
            Counter.objects.create(number=index)
        
    return categories_str        
            
def parse_category(type=None):
    url = 'https://cars.kg/offers'
    response = requests.get(url)
    if response.status_code != 200:
        print(response.status_code)
        return False
        # sys.exit()
    soup = BS(response.content,'html.parser')
    marks = soup.find_all('select',attrs={'class':'select','name':'vendor','id':'m_search_vendor'})[0].get_text()
    marks = marks.replace('\xa0','').split('\n')[2:-1]
    
    if type == None:
        for brand in marks: CarBrand.objects.get_or_create(brand_name=brand.strip())
        return {'Success':True}
    elif type=='for_find':
        a = CarBrand.objects.values_list('brand_name')
        a = [x[0] for x in a]
        return a


