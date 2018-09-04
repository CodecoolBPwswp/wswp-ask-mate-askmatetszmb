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
def get_last_five_questions(cursor):
    cursor.execute("""
                    SELECT id, title, submission_time, view_number FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;
                    """,)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def add_question(cursor, question_title, question_message):
    submission_time = datetime.now()
    cursor.execute("""
                    INSERT INTO question (submission_time, title, message)
                    VALUES(%(submission_time)s, %(question_title)s, %(question_message)s);
                    """,
                   {'question_title': question_title, 'question_message': question_message,
                    'submission_time': submission_time})


@database_common.connection_handler
def add_answer(cursor, answer_message, id):
    submission_time = datetime.now()
    cursor.execute("""
                    INSERT INTO question (submission_time, message)
                    VALUES(%(submission_time)s, %(answer_message)s);
                    """,
                   {'id': id, 'answer_message': answer_message,
                    'submission_time': submission_time})
