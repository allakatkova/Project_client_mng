import psycopg2


def create_database():
    with conn.cursor() as cur:
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS clients(
                        clients_id SERIAL PRIMARY KEY,
                        client_surname VARCHAR(50) NOT NULL,
                        client_name VARCHAR(50) NOT NULL,
                        
                        client_email text not null 
                        );
                    """)

        cur.execute("""
                        CREATE TABLE IF NOT EXISTS phone_numbers(
                        id SERIAL primary key,
                        phone_number varchar(11),
                        client_id integer not null references clients(id) on delete cascade
                        );
                    """)
        conn.commit()


if __name__ == '__main__':
    print('PyCharm')
