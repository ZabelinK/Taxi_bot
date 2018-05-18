from vklib import *
from text import *

import re, copy

def event_handle(event):
    # Отправка сообщений
    def send(text, attachment='', user_id='', forward_messages=''):
        if not user_id:
            user_id = event.user_id
        api.messages.send(user_id=user_id, message=text, attachment=attachment, forward_messages=forward_messages)

    #Получение райнов строкой
    def get_region_str(city='all'):
        st = ''
        if city == 'all':
            for city_ in access_cities:
                if access_regions.get(city_) != None:
                    for region in access_regions.get(city_):
                        st += region + ' '
        else:
            if access_regions.get(city) != None:
                for region in access_regions.get(city):
                    st += region + ' '
        return st

    #Получение первых букв райнов
    def get_region_makr(city):
        mark = []
        city_reg = copy.deepcopy(access_regions.get(city))
        for i in city_reg:
             mark.append(i[0])
        return mark

    # Обработка сообщений водителей
    def driver_handle(event):
        driver = db_manager.get_driver(event.user_id)

        if not driver[1]:
            city = event.text.lower()
            if city not in access_cities:
                city = '_'
            db_manager.set_city(event.user_id, city)
            send(need_photos)
            return None

        if not driver[3]:
            message_id = event.raw[1]
            try:
                access_key = api.messages.getById(message_ids=message_id)['items'][0]['attachments'][0]['photo'][
                    'access_key']
            except KeyError:
                send(need_photos_)
                return None
            owner_id = event.attachments['attach1'].split('_')[0]
            old_photo_id = event.attachments['attach1'].split('_')[1]
            # photo_id = api.photos.copy(owner_id=owner_id, photo_id=old_photo_id, access_key=access_key)
            db_manager.set_photo(user_id=event.user_id, photo='photo%s_%s_%s' % (owner_id, old_photo_id, access_key))
            db_manager.add_validation(event.user_id, message_id)
            if len(db_manager.get_validations()) == 1:
                send(new_request, forward_messages=db_manager.get_validations()[-1][1],
                     user_id=admin)
            send(wait_admin)
            return None

        if not driver[6]:
            send(wait_admin_)
            return None

        #Добавляем в бд город водителя
        if re.match(r'^город: [а-я]+?$', event.text.lower()):
            city_ = re.split(r': ', event.text.lower())
            if city_[1] not in access_cities:
                send(not_correct_city)
                return None
            if city_[1].lower() != driver[1]:
                db_manager.set_city(user_id=event.user_id, city=city_[1])
                db_manager.set_region(user_id=event.user_id, region='_')
            send(correct_city)
            return None

        if event.text.lower() == 'сделать заказ':
            db_manager.set_region(event.user_id, '')
            db_manager.set_is_client(event.user_id, 1)
            return 2

        if driver[10]:
            return 2

        if event.text.lower()[0] == 'с':
            if driver[1] == '_':
                send(open_taxi)
                db_manager.set_region(event.user_id, '_')
                return None

            if access_regions.get(driver[1]) == None:
                send(open_)
                db_manager.set_region(event.user_id, '_')
                return None

            r = event.text.lower()[1:]
            city_reg = get_region_makr(driver[1])

            valid_r = ''
            for reg in r:
                if reg in city_reg:
                    valid_r += reg

            if len(valid_r) == 0:
                #send(help_ + get_region_str(driver[1]))
                for reg in city_reg:
                    valid_r += reg
            #Для того чтобы получить полный названия регионов, которые указаны
            valid_r_full = ''
            city_reg_ = access_regions[driver[1]]
            for i in valid_r:
                for y in range(len(city_reg)):
                    if i == city_reg[y]:
                        valid_r_full += city_reg_[y] + ' '

            db_manager.set_region(event.user_id, valid_r)
            send(open_taxi_ + valid_r_full)
            return None

        if event.text.lower() == 'з':
            db_manager.set_region(event.user_id, '')
            db_manager.set_free_driver(event.user_id)
            send(close_taxi)
            return None

        if event.text.lower() == 'ок':
            if driver[7] == driver[8]:
                send('Вы уже приняли заказ')
                return None

            if not driver[7]:
                send('На данный момент для вас нет предложений')
                return None

            db_manager.set_region(event.user_id, '')
            db_manager.set_client_order(event.user_id, driver[7])
            db_manager.clear_client(driver[7])
            db_manager.set_unixtime(event.user_id, int(time.time()))
            send('Вы успешно приняли заказ. Постарайтесь как можно быстрее приехать к клиенту, или он захочет вызвать '
                 'другого водителя')
            send('Заказ принят. Мы оповестим вас о приезде водителя. Фотография авто:', user_id=driver[7],
                 attachment=driver[3])
            if driver[7] in db_manager.get_drivers():
                db_manager.set_is_client(driver[7], 'NULL')
            return None

        if event.text.lower() == 'п':
            if not driver[8]:
                send(hasnt_ord)
                return None

            send(note, user_id=driver[8])
            send(note_)
            return None

        if event.text.lower() == 'удалить':
            send('Ваш профиль успешно удален')
            db_manager.del_account(event.user_id)
            return None

        send(help__ + 'Доступные районы:\n' + get_region_str(driver[1]))
        return None

    # Обработка сообщений админа
    def admin_handle(event):
        if not db_manager.get_validations():
            send(hasnt_req)
            return None
        driver_id = db_manager.get_validations()[-1][0]
        if event.text == '1':
            send(first,
                 user_id=driver_id)
            db_manager.set_access(driver_id, 1)
            send(good)
            db_manager.del_validation(driver_id)

        elif event.text[0] == '2':
            remark = event.text[1:]
            send(second + remark, user_id=driver_id)
            db_manager.del_account(driver_id)
            send(good)
            db_manager.del_validation(driver_id)

        elif event.text == '3':
            send(ban, user_id=driver_id)
            api.account.banUser(user_id=driver_id)
            db_manager.del_account(driver_id)
            send(good)
            db_manager.del_validation(driver_id)

        else:
            send(incorr)
        if db_manager.get_validations():
            send(new_request, forward_messages=db_manager.get_validations()[-1][1])

    # Обработка сообщений клиентов
    def client_handle(event):
        client = db_manager.get_client(event.user_id)
        if not client:
            db_manager.create_client(event.user_id)
            send(need_data)
            client = db_manager.get_client(event.user_id)

        if not client[4]:
            db_manager.set_client_old(event.user_id, 1)
            send(locate_)
            return None

        if not client[1]:
            if event.text.lower() not in access_cities:
                db_manager.set_client_city(event.user_id, '_')
                db_manager.set_client_region(event.user_id, '_')
                send(profile)
                return None
            db_manager.set_client_city(event.user_id, event.text.lower())
            if access_regions.get(event.text.lower()) != None:
                send(locate + '\n' + get_region_str(event.text.lower()))
            else:
                db_manager.set_client_region(user_id=event.user_id, region='_')
                send(profile_)
            return None

        if not client[2]:
            if event.text.lower()[0] not in get_region_makr(client[1]):
                send(free_regions + '\n' + get_region_str(client[1]))
                return None

            db_manager.set_client_region(event.user_id, event.text.lower()[0])
            send(profile_)
            return None

        if not client[3]:
            db_manager.set_client_info(event.user_id, event.text)
            db_manager.set_client_uuid(event.user_id, uuid.uuid4())
            send(search)
            return None

    #for temp in answers:
     #   if event.text.lower().count(temp):
      #      send(answers[temp])
       #     return None

    if event.text.lower() == 'регистрация':
        if db_manager.get_driver(event.user_id):
            send(already)

            return None
        print(event.user_id)
        db_manager.add_validation(user_id=event.user_id, message_id=event.chat_id)
        db_manager.create_driver(event.user_id, api_.users.get(user_ids=event.user_id)[0]['first_name'])
        send(start)
        return None

    if event.user_id == admin:
        admin_handle(event)
        return None

    elif event.user_id in db_manager.get_drivers():
        resp = driver_handle(event)
        if resp == 2:
            client_handle(event)
        return None

    else:
        client_handle(event)
        return None


for event in longpoll.listen():
    if event.type != VkEventType.MESSAGE_NEW or event.from_me:
        continue

    event_handle(event)

    db_manager.close()
    db_manager.reg()
