import psycopg2
import random
import string
from chat.models import Room

def match():
    connection = False
    try:
        connection = psycopg2.connect(user =  'app',
            password = 'NotAPassword!',
            host = 'localhost',
            port = '5432',
            database = 'shopaholics_anonymous')
        cursor = connection.cursor()
        print(connection.get_dsn_parameters(), "\n")
        # select_query = "select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';"
        select_query_drivers = "select * from users_user where driver_filled=True"
        cursor.execute(select_query_drivers)
        drivers = cursor.fetchall()
        select_query_orders = "select * from users_order where driver=''"
        cursor.execute(select_query_orders)
        orders = cursor.fetchall()
        queuedrivers = []
        queueorders = []
        for driver in drivers:
            queuedrivers.append(driver)
        for order in orders:
            queueorders.append(order)
        while len(queuedrivers) > 0 and len(queueorders) > 0:
            d = queuedrivers.pop(0)
            o = queuedrivers.pop(0)
            slug = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
            Room.objects.create(name='Shopper Chat', slug=slug, description="Chat with your driver")
            o.chat_room = slug
            update_query_driver_has_order = "update users_user set has_order = True where email = " + str(d[3])
            update_query_driver_is_matching = "update users_user set is_matching = False where email = " + str(d[3])
            update_query_order =  "update users_order set driver = " + str(d[3]) + "where id = " + str(o[0])
            cursor.execute(update_query_driver_has_order)
            cursor.execute(update_query_driver_is_matching)
            cursor.execute(update_query_order)
        # print(cursor.fetchall())
        # cursor.execute(select_query)
        # records = cursor.fetchall()
        # for row in records:
        #     print(row)
    except (Exception, psycopg2.Error) as error:
        print("Something went wrong")
    finally:
        if(connection):
            cursor.close()
            connection.close()
