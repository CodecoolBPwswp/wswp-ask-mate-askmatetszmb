import database_common
from datetime import datetime

@database_common.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT id,title FROM question
                    ORDER BY id;
                   """)
    id_and_question = cursor.fetchall()
    return id_and_question


@database_common.connection_handler
def display_question(cursor, id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(id)s;
                    """,
                   {'id': id})
    question = cursor.fetchone()
    return question

@database_common.connection_handler
def add_question(cursor, question_title, question_message):
    submission_time = datetime.now()
    cursor.execute("""
                    INSERT INTO question (submission_time, title, message)
                    VALUES(%(submission_time)s, %(question_title)s, %(question_message)s);
                    """,
                   {'question_title': question_title, 'question_message': question_message,
                   'submission_time': submission_time})
