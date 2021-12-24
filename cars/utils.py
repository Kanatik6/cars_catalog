from bs4 import BeautifulSoup as BS
import requests
import sys

def get_soup(url:str):
    response = requests.get(url)
    if response.status_code == 200:
        return BS(response.content,'html.parser')
    else:  
        print('Неверный url','\n',url)
        return False
        sys.exit()

def normalize_str(str):
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
