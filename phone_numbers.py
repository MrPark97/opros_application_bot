import psycopg2
import config
import os

DATABASE_URL = os.getenv("DATABASE_URL")


def insert_phone_number(user_id, contact):
    """insert contact shared by user"""

    conn = None
    try:
        if DATABASE_URL is not None:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            params = config.db_config()
            conn = psycopg2.connect(**params)
        cur = conn.cursor()

        query = """INSERT INTO phone_numbers(phone_number_user_id, phone_number)
             VALUES(%s, %s)"""

        cur.execute(query, (user_id, contact))

        conn.commit()

        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return


def get_all_contacts():
    """get contacts"""

    conn = None
    try:
        if DATABASE_URL is not None:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            params = config.db_config()
            conn = psycopg2.connect(**params)
        cur = conn.cursor()

        query = "SELECT * from phone_numbers ORDER BY phone_number_id"
        cur.execute(query)

        rows = cur.fetchall()

        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows
