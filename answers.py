import psycopg2
import config
import os

DATABASE_URL = os.getenv("DATABASE_URL")


def get_answers_by_question(question_id):
    """get answers for certain question"""

    conn = None
    try:
        if DATABASE_URL is not None:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            params = config.db_config()
            conn = psycopg2.connect(**params)
        cur = conn.cursor()

        query = "SELECT * from answers WHERE answer_question = %s"
        cur.execute(query, (question_id,))

        rows = cur.fetchall()

        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows


def find_answer_id(question_id, answer_text):
    """find answer by question id and text"""

    conn = None
    try:
        if DATABASE_URL is not None:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            params = config.db_config()
            conn = psycopg2.connect(**params)
        cur = conn.cursor()

        query = "SELECT answer_id from answers WHERE answer_question = %s AND (answer_ru = %s OR answer_uz = %s)"
        cur.execute(query, (question_id, answer_text, answer_text))

        rows = cur.fetchall()

        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows[0]
