import psycopg2
import config


def get_all_questions():
    """get questions"""

    conn = None
    try:
        params = config.db_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        query = "SELECT * from questions"
        cur.execute(query)

        rows = cur.fetchall()

        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows


def get_question_by_id(question_id):
    """get question by certain id"""

    conn = None
    try:
        params = config.db_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        query = "SELECT * from questions WHERE question_id = %s"
        cur.execute(query, (question_id,))

        rows = cur.fetchall()

        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows[0]
