import pymysql

def reg():
    global conn, cur
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='12345', db='taxi_bot', charset='utf8')
    cur = conn.cursor()

reg()

def get_driver(user_id):
    # print('Get driver', user_id)
    cur.execute('SELECT * FROM drivers WHERE id=%s' % user_id)
    return cur.fetchone()


def get_drivers():
    # print('Get drivers')
    cur.execute('SELECT id FROM drivers')
    return [x[0] for x in cur.fetchall()]

def get_all_drivers():
    cur.execute('SELECT id, unixtime, uuid, city, region FROM drivers')
    return cur.fetchall()

def get_fit_drivers(region):
    # print('Get fit drivers', region)
    cur.execute('SELECT id, unixtime, uuid FROM drivers WHERE region="%s"' % region)
    return cur.fetchall()


def get_fit_drivers_():
    # print('Get fit drivers', region)
    cur.execute('SELECT id, unixtime, uuid FROM drivers')
    return cur.fetchall()



def get_validations():
    # print('Get validations')
    cur.execute('SELECT * FROM validations')
    return cur.fetchall()


def get_clients_ids():
    # print('Get clients ids')
    cur.execute('SELECT id FROM clients')
    return [x[0] for x in cur.fetchall()]


def get_client(user_id):
    # print('Get client', user_id)
    cur.execute('SELECT * FROM clients WHERE id=%s' % user_id)
    return cur.fetchone()


def add_validation(user_id, message_id):
    # print('Add validation', user_id, message_id)
    cur.execute('INSERT INTO validations (id, message_id) VALUES (%s, %s)' % (user_id, message_id))
    cur.connection.commit()


def create_client(user_id):
    # print('Create client', user_id)
    cur.execute('INSERT INTO clients (id) VALUES (%s)' % user_id)
    cur.connection.commit()


def create_driver(user_id, name):
    # print('Create driver', user_id, name)
    cur.execute('INSERT INTO drivers (id, name) VALUES (%s, "%s")' % (user_id, name))
    cur.connection.commit()

def set_free_driver(driver_id):
    cur.execute('UPDATE drivers SET client="0", client_order="0" WHERE id=%s' % (driver_id))
    cur.connection.commit()

def set_city(user_id, city):
    # print('Set city', user_id, city)
    cur.execute('UPDATE drivers SET city="%s" WHERE id=%s' % (city, user_id))
    cur.connection.commit()


def set_client_city(user_id, city):
    # print('Set client city', user_id, city)
    cur.execute('UPDATE clients SET city="%s" WHERE id=%s' % (city, user_id))
    cur.connection.commit()


def set_client_region(user_id, region):
    # print('Set client region')
    cur.execute('UPDATE clients SET region="%s" WHERE id=%s' % (region, user_id))
    cur.connection.commit()


def set_client_info(user_id, info):
    # print('Set client info')
    cur.execute('UPDATE clients SET info="%s" WHERE id=%s' % (info, user_id))
    cur.connection.commit()


def set_client_old(user_id, old):
    # print('Set client old', user_id, old)
    cur.execute('UPDATE clients SET old=%s WHERE id=%s' % (old, user_id))
    cur.connection.commit()


def set_photo(user_id, photo):
    # print('Set photo', user_id, photo)
    cur.execute('UPDATE drivers SET photo="%s" WHERE id=%s' % (photo, user_id))
    cur.connection.commit()


def set_is_client(user_id, is_client):
    cur.execute('UPDATE drivers SET is_client=%s WHERE id=%s' % (is_client, user_id))
    cur.connection.commit()


def set_region(user_id, region):
    # print('Set region', region)
    cur.execute('UPDATE drivers SET region="%s" WHERE id=%s' % (region, user_id))
    cur.connection.commit()


def set_unixtime(user_id, unixtime):
    # print('Set unixtime', unixtime)
    cur.execute('UPDATE drivers SET unixtime=%s WHERE id=%s' % (unixtime, user_id))
    cur.connection.commit()


def set_client_order(user_id, order):
    # print('Set order', user_id, order)
    cur.execute('UPDATE drivers SET client_order=%s WHERE id=%s' % (order, user_id))
    cur.connection.commit()


def set_client(user_id, client):
    # print('Set client', user_id, client)
    cur.execute('UPDATE drivers SET client=%s WHERE id=%s' % (client, user_id))
    cur.connection.commit()


def set_access(user_id, access):
    # print('Set access', access)
    cur.execute('UPDATE drivers SET access=%s WHERE id=%s' % (access, user_id))
    cur.connection.commit()


def set_client_uuid(user_id, uuid):
    # print('Set client uuid', user_id, uuid)
    cur.execute('UPDATE clients SET uuid="%s" WHERE id=%s' % (uuid, user_id))
    cur.connection.commit()


def add_driver_uuid(user_id, uuid):
    # print('Add driver uuid', user_id, uuid)
    driver_uuid = get_driver(user_id)[9]
    cur.execute('UPDATE drivers SET uuid="%s" WHERE id=%s' % ((driver_uuid if driver_uuid else '')+uuid, user_id))
    cur.connection.commit()


def del_account(user_id):
    # print('Del account', user_id)
    cur.execute('DELETE FROM drivers WHERE id=%s' % user_id)
    cur.connection.commit()


def clear_client(user_id):
    # print('Clear client', user_id)
    cur.execute('UPDATE clients SET city=NULL , region=NULL , info=NULL , old=NULL  WHERE id=%s' % user_id)
    cur.connection.commit()


def del_validation(user_id):
    # print('Del validation', user_id)
    cur.execute('DELETE FROM validations WHERE id=%s' % user_id)
    cur.connection.commit()


def close():
    cur.close()
    conn.close()

if __name__ == '__main__':
    close()

