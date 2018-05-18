from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
import re
import db_manager
import uuid
import time

token = open('token.txt', mode='r').read().strip()
# login, password = open('token.txt', mode='r').read().strip().split(':')
vk = VkApi(token=token)
vk.auth()
api = vk.get_api()
longpoll = VkLongPoll(vk)

# for get public info
token_ = '05afa85305afa85305afa8539005f84a7d005af05afa8535cefd95f1167ce5d8a60ef1f'
vk_ = VkApi(token=token_)
vk_.auth()
api_ = vk_.get_api()

# my_user_id = api.users.get()[0]['id']
admin = int(open('admin_id.txt', mode='r').read().strip())
access_cities = open('cities.txt', mode='r', encoding='utf-8').read().strip().split(';')
access_cities[0] = access_cities[0][1:]
#access_regions = dict([(r[0], r) for r in open('regions.txt', mode='r', encoding='utf-8').read().strip().split(';')])

access_regions = {}
f = open('regions.txt', mode='r', encoding='utf-8')

#Создание словаря {'город' : ['районы']}
for str in f:
    res = re.split('::', str)
    city = res[0]
    if re.match('^[^а-яА-Я]', city):
        city = city[1:]
    reg = res[1]
    reg = re.split(r';', reg)
    access_regions[city.lower()] = reg