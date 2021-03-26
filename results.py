import psycopg2
import config
import os

DATABASE_URL = os.getenv("DATABASE_URL")


def insert_result(user_id, answer_id):
    """insert certain answer in results"""

    conn = None
    try:
        if DATABASE_URL is not None:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            params = config.db_config()
            conn = psycopg2.connect(**params)
        cur = conn.cursor()

        query = """INSERT INTO results(result_answer, result_user)
             VALUES(%s, %s)"""

        cur.execute(query, (answer_id, user_id))

        conn.commit()

        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return

