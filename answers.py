import psycopg2
import config


def get_answers_by_question(question_id):
    """get answers for certain question"""

    conn = None
    try:
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
