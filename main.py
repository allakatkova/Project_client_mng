import psycopg2


NAME_DATABASE = 'clients_management'
USER_DATABASE = 'postgres'
PASS_USER_DATABASE = 'postgres'


def create_database():
    with connect_db.cursor() as cursor_db:
        cursor_db.execute("""
                        CREATE TABLE IF NOT EXISTS clients(
                        client_id SERIAL PRIMARY KEY,
                        client_surname VARCHAR(50) NOT NULL,
                        client_name VARCHAR(50) NOT NULL,
                        client_email TEXT NOT NULL
                        );
                    """)

        cursor_db.execute("""
                        CREATE TABLE IF NOT EXISTS phones_numbers(
                        phone_number_id SERIAL PRIMARY KEY,
                        phone_number VARCHAR(11),
                        client_id INTEGER NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE
                        );
                    """)
        connect_db.commit()


def add_client(client_name, client_surname, client_email):
    with connect_db.cursor() as cursor_db:
        cursor_db.execute("""SELECT client_email FROM clients;""")
        all_clients_list = cursor_db.fetchall()
        emails_clients_list = []
        for client in all_clients_list:
            emails_clients_list.append(client[0])
        if client_email in emails_clients_list:
            print(
                f'Электронный адрес {client_email} имеется в базе данных, повторное использование запрещено!')
        else:
            cursor_db.execute("""insert into clients (client_name, client_surname, client_email)
                                     values (%s, %s, %s); """, (
                client_name, client_surname, client_email))
            connect_db.commit()


def add_phone_client(phone_number, client_email):
    with connect_db.cursor() as cursor_db:
        result = get_id_client(client_email)
        if result is None:
            print(f'Клиент с e-mail {client_email} отсутствует в базе данных')
        else:
            id_client = result[0]
            phones_list = get_all_phones()
            if phone_number in phones_list:
                print(
                    f'Номер телефона {phone_number} имеется в базе данных, повторное использование запрещено!')
            else:
                cursor_db.execute("""insert into phones_numbers (phone_number, client_id) values (%s,%s);""",
                                  (phone_number, id_client))
                connect_db.commit()


def get_all_phones():
    with connect_db.cursor() as cursor_db:
        cursor_db.execute("""SELECT phone_number FROM phones_numbers;""")
        all_phones = cursor_db.fetchall()
        phones_list = []
        for phone in all_phones:
            phones_list.append(phone[0])
        return phones_list


def get_id_client(client_email):
    with connect_db.cursor() as cursor_db:
        cursor_db.execute("""SELECT client_id FROM clients
                             WHERE client_email=%s;
                             """, (client_email,))
        result = cursor_db.fetchone()
        return result


def change_client_details(client_email, change_client_name=None, change_client_surname=None,
                          change_client_email=None):
    result = get_id_client(client_email)
    if result is None:
        print(f'Клиент с e-mail {client_email} отсутствует в базе данных')
    else:
        id_client = result[0]
        with connect_db.cursor() as cursor_db:
            if change_client_name is not None:
                cursor_db.execute("""update clients set client_name = %s
                                where client_id = %s;
                                """, (change_client_name, id_client))
            if change_client_surname is not None:
                cursor_db.execute("""update clients set client_surname = %s
                                where client_id = %s;
                                """, (change_client_surname, id_client))
            if change_client_email is not None:
                cursor_db.execute("""update clients set client_email = %s
                                where client_id = %s;
                                """, (change_client_email, id_client))
            connect_db.commit()


def delete_phone_client(phone_number, client_email, del_all_phone=False):
    with connect_db.cursor() as cursor_db:
        result = get_id_client(client_email)
        if result is None:
            print(f'Клиент с e-mail {client_email} отсутствует в базе данных')
        else:
            id_client = result[0]
            phones_list = get_all_phones()
            if del_all_phone:
                cursor_db.execute("""delete from phones_numbers where client_id=%s;""",
                                  (id_client,))
                connect_db.commit()
            else:
                if phone_number in phones_list:
                    cursor_db.execute("""delete from phones_numbers where phone_number = %s and client_id=%s;""",
                                      (phone_number, id_client))
                    connect_db.commit()
                else:
                    print(
                        f'Удаление невозможно - номер телефона {phone_number} отсутствует в базе данных!')


def delete_client(client_email):
    with connect_db.cursor() as cursor_db:
        result = get_id_client(client_email)
        if result is None:
            print(f'Клиент с e-mail {client_email} отсутствует в базе данных')
        else:
            id_client = result[0]
            delete_phone_client("", client_email, del_all_phone=True)
            cursor_db.execute("""delete from clients where client_id = %s""",
                              (id_client,))
            connect_db.commit()


def client_search(client_id=None, client_name=None, client_surname=None, client_email=None, phone_number=None):
    with connect_db.cursor() as cursor_db:
        if phone_number is not None:
            phone_number = str(phone_number)
            cursor_db.execute("""select client_id from phones_numbers where phone_number = %s;""",
                              (phone_number,))
            client_id = cursor_db.fetchall()[0][0]

        cursor_db.execute("""select client_id, client_name, client_surname, client_email from clients 
                           where client_id=%s or client_name = %s or client_surname = %s or client_email = %s; 
                        """, (client_id, client_name, client_surname, client_email))
        client_details = cursor_db.fetchall()[0]
        print(
            f'Имя клиента: {client_details[1]}, фамилия клиента: {client_details[2]}, e-mail клиента: {client_details[2]}, ID клиента: {client_details[0]}')


if __name__ == '__main__':

    with psycopg2.connect(database=NAME_DATABASE, user=USER_DATABASE, password=PASS_USER_DATABASE) as connect_db:

        create_database()

        add_client("Elena", "Drozdova", "ElenaDrozdova@mail.ru")
        add_phone_client("89025847520", "ElenaDrozdova@mail.ru")

        add_client("Sergey", "Vorozhtsov", "SergeyVorozhtsov@mail.ru")
        add_phone_client("89025847521", "SergeyVorozhtsov@mail.ru")

        add_client("Natalia", "Kremleva", "NataliaKremleva@mail.ru")
        add_phone_client("89025847522", "NataliaKremleva@mail.ru")

        add_client("Nikolay", "Kolesnik", "NikolayKolesnik@mail.ru")
        add_phone_client("89025847523", "NikolayKolesnik@mail.ru")

        add_client("Anatoly", "Krivov", "AnatolyKrivov@mail.ru")
        add_phone_client("89025847524", "AnatolyKrivov@mail.ru")

        change_client_details("SergeyVorozhtsov@mail.ru",
                              change_client_email="VorozhtsovSergey@mail.ru")

        client_search(client_email="ElenaDrozdova@mail.ru")
        client_search(phone_number="89025847521")

        client_search(client_surname="Kolesnik")
        client_search(client_name="Natalia")
        client_search(phone_number="89025847524")

        delete_phone_client("89025847520", "ElenaDrozdova@mail.ru")
        delete_client("ElenaDrozdova@mail.ru")

    connect_db.close()
