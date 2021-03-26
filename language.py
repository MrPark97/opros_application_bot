import psycopg2
import config
import os

DATABASE_URL = os.getenv("DATABASE_URL")


def update_language(user_id, language_selected):
    """update language for user"""

    conn = None
    updated_rows = 0
    try:
        if DATABASE_URL is not None:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            params = config.db_config()
            conn = psycopg2.connect(**params)
        cur = conn.cursor()

        query = """UPDATE language
                   SET language_selected = %s
                   WHERE language_user = %s"""

        cur.execute(query, (language_selected, user_id))

        updated_rows = cur.rowcount

        conn.commit()

        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


def insert_language(user_id, language_selected):
    """insert language for user"""

    conn = None
    try:
        if DATABASE_URL is not None:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            params = config.db_config()
            conn = psycopg2.connect(**params)
        cur = conn.cursor()

        query = """INSERT INTO language(language_user, language_selected)
             VALUES(%s, %s)"""

        cur.execute(query, (user_id, language_selected))

        conn.commit()

        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return


def get_language_by_user(user_id):
    """get language for certain user"""

    conn = None
    try:
        if DATABASE_URL is not None:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            params = config.db_config()
            conn = psycopg2.connect(**params)
        cur = conn.cursor()

        query = "SELECT language_selected from language WHERE language_user = %s"
        cur.execute(query, (user_id,))

        rows = cur.fetchall()

        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows[0]


def get_language_by_type(lang_type):
    """get language by type"""

    conn = None
    try:
        if DATABASE_URL is not None:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            params = config.db_config()
            conn = psycopg2.connect(**params)
        cur = conn.cursor()

        query = "SELECT COUNT(*) from language WHERE language_selected = %s"
        cur.execute(query, (lang_type,))

        rows = cur.fetchall()

        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows[0]

