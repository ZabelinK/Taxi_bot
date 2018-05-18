from vklib import *


def check(client_id):
    client = db_manager.get_client(client_id)

    if not client[3]:
        return None

    all_drivers = db_manager.get_all_drivers()
    fit_drivers_ = []
    fit_drivers = []
    for driver in all_drivers:
        if client[1] == driver[3] and client[2] in driver[4]:
            fit_drivers_.append(driver)

    if not fit_drivers_:
        db_manager.clear_client(client_id)
        return 1  # Нет свободных

    for d in fit_drivers_:
        if not d[2]:
            fit_drivers.append(d)
        elif client[5] not in d[2]:
            fit_drivers.append(d)
        elif d[2][-36:] == client[5]:
            api.messages.send(user_id=d[0], message='Время принятия заказа прошло')
            db_manager.add_driver_uuid(d[0], ';')

    if not fit_drivers:
        db_manager.clear_client(client_id)
        return 2  # Никто не согласен

    unixtime = int(time.time())

    for d in fit_drivers:
        if not d[1]:
            unixtime = 0
            driver_id = d[0]
        elif d[1] <= unixtime:
            unixtime = d[1]
            driver_id = d[0]

    if (int(time.time()) - unixtime) < 30:
        return None
    db_manager.set_client(driver_id, client[0])
    db_manager.set_unixtime(driver_id, int(time.time()))
    db_manager.add_driver_uuid(driver_id, client[5])
    api.messages.send(user_id=driver_id, message='Новый заказ. Чтобы согласиться, напишите "Ок", иначе заказ удалится '
                                                 'через 30 секунд. Сообщение от клиента: %s' % client[3])


while True:
    print(db_manager.get_clients_ids(), 'clients')
    for client_id in db_manager.get_clients_ids():
        code = check(client_id)
        if code is None:
            continue

        elif code == 1:
            api.messages.send(user_id=client_id, message='На данный момент нет свободных водителей, попробуйте немного '
                                                         'позже')
            if client_id in db_manager.get_drivers():
                db_manager.set_is_client(client_id, 'NULL')

        elif code == 2:
            api.messages.send(user_id=client_id, message='К сожалнию никто не готов выполнить заказ. Попробуйте '
                                                         'изменить описание или поднять цену')
            print((client_id, db_manager.get_drivers()))
            if client_id in db_manager.get_drivers():
                db_manager.set_is_client(client_id, 'NULL')

    db_manager.close()
    db_manager.reg()
    time.sleep(30)
