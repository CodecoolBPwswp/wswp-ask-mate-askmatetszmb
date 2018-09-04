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


@database_common.connection_handler
def view_counter(cursor, id):
    cursor.execute("""
                    SELECT view_number FROM question
                    WHERE id = %(id)s;
                    """,
                   {'id': id})
    view_numbers = cursor.fetchone()
    view = view_numbers['view_number']
    view += 1
    cursor.execute("""UPDATE question
                      SET view_number = %(view)s
                      WHERE id = %(id)s;
                      """,
                   {'id': id, 'view': view})

