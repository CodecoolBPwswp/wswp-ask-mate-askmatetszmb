import database_common
from datetime import datetime


@database_common.connection_handler
def get_questions(cursor, limit_num=None):
    cursor.execute("""
                    SELECT id, title, submission_time, view_number
                    FROM question
                    ORDER BY submission_time DESC
                    LIMIT %(limit_num)s;
                   """,
                   {'limit_num': limit_num})
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_answers(cursor, question_id):
    cursor.execute("""
                    SELECT answer.submission_time, answer.id, answer.message, u.user_name
                    FROM answer LEFT JOIN users u on answer.user_id = u.id
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def display_question(cursor, id):
    cursor.execute("""
                    SELECT q.id, q.submission_time, q.view_number, q.title, q.message, u.user_name 
                    FROM question q LEFT JOIN users u on q.user_id = u.id
                    WHERE q.id = %(id)s;
                    """,
                   {'id': id})
    question = cursor.fetchone()
    return question


@database_common.connection_handler
def add_question(cursor, question_title, question_message, user_id):
    submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, title, message, user_id)
                    VALUES(%(submission_time)s, 0, %(question_title)s, %(question_message)s, %(user_id)s);
                    """,
                   {'question_title': question_title,
                    'question_message': question_message,
                    'submission_time': submission_time,
                    'user_id': user_id})


@database_common.connection_handler
def add_answer(cursor, question_id, answer_message, user_id):
    submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
                    INSERT INTO answer (submission_time, question_id, message, user_id)
                    VALUES(%(submission_time)s, %(question_id)s, %(answer_message)s, %(user_id)s);
                    """,
                   {'submission_time': submission_time,
                    'question_id': question_id,
                    'answer_message': answer_message,
                    'user_id': user_id})


@database_common.connection_handler
def view_counter(cursor, id):
    cursor.execute("""
                    SELECT view_number
                    FROM question
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


@database_common.connection_handler
def edit_answer(cursor, id, edited_answer):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(edited_answer)s
                    WHERE id = %(id)s""",
                   {'id': id, 'edited_answer': edited_answer})


@database_common.connection_handler
def add_question_comment(cursor, question_id, new_comment, user_id):
    submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time, user_id)
                    VALUES (%(question_id)s, %(new_comment)s, %(submission_time)s, %(user_id)s); 
                    """,
                   {'question_id': question_id,
                    'new_comment': new_comment,
                    'submission_time': submission_time,
                    'user_id': user_id})


@database_common.connection_handler
def get_question_comment(cursor, question_id):
    cursor.execute("""
                    SELECT submission_time, id, message
                    FROM comment
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    comments = cursor.fetchall()
    return comments


@database_common.connection_handler
def add_answer_comment(cursor, answer_id, new_comment, user_id):
    submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
                    INSERT INTO comment (answer_id, message, submission_time, user_id)
                    VALUES (%(answer_id)s, %(new_comment)s, %(submission_time)s, %(user_id)s);
                    """,
                   {'answer_id': answer_id,
                    'new_comment': new_comment,
                    'submission_time': submission_time,
                    'user_id': user_id})


@database_common.connection_handler
def get_answer_id(cursor, question_id):
    cursor.execute("""
                    SELECT id
                    FROM answer
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    ids_pack = cursor.fetchall()
    ids = [id_dict['id'] for id_dict in ids_pack]
    return ids


@database_common.connection_handler
def get_answer_comment(cursor, ids):
    answer_comments_ids = tuple(ids)
    parameter = {'answer_comments_ids': answer_comments_ids}
    cursor.execute("""
                    SELECT submission_time, message, answer_id
                    FROM comment
                    WHERE answer_id IN %(answer_comments_ids)s;
                    """,
                   parameter)
    answer_comments = cursor.fetchall()
    return answer_comments


@database_common.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {"comment_id": comment_id})


@database_common.connection_handler
def search(cursor, user_input):
    text = "%" + user_input + "%"
    parameter = {'text': text}
    cursor.execute("""
                    SELECT DISTINCT q.title, q.id
                    FROM question q
                    FULL JOIN answer a
                        ON q.id = a.question_id
                    WHERE q.title ILIKE %(text)s OR q.message ILIKE %(text)s OR a.message ILIKE %(text)s;
                    """,
                   parameter)
    result = cursor.fetchall()
    return result


@database_common.connection_handler
def register_user(cursor, user_name, password):
    registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
                    INSERT INTO users (user_name, password, registration_date)
                    VALUES (%(user_name)s, %(password)s, %(registration_date)s )
                    """,
                   {'user_name': user_name, 'password': password, 'registration_date': registration_date})


@database_common.connection_handler
def list_users(cursor):
    cursor.execute("""
                    SELECT user_name, registration_date
                    FROM users
                    ORDER BY registration_date
                    """)
    users = cursor.fetchall()
    return users


@database_common.connection_handler
def get_user_data(cursor, user_name):
    cursor.execute("""
                    SELECT id, user_name, password
                    FROM users
                    WHERE user_name = %(user_name)s
                    """,
                   {'user_name': user_name})
    user_data = cursor.fetchone()
    return user_data


