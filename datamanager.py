import database_common
from datetime import datetime


@database_common.connection_handler
def get_questions(cursor):
    cursor.execute("""
                    SELECT id,title FROM question
                    ORDER BY id;
                   """,)
    id_and_question = cursor.fetchall()
    return id_and_question


@database_common.connection_handler
def get_answers(cursor, question_id):
    cursor.execute("""
                    SELECT submission_time, id, message FROM answer
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    answers = cursor.fetchall()
    return answers


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
    submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, title, message)
                    VALUES(%(submission_time)s, 0, %(question_title)s, %(question_message)s);
                    """,
                   {'question_title': question_title, 'question_message': question_message,
                    'submission_time': submission_time})


@database_common.connection_handler
def add_answer(cursor, question_id, answer_message):
    submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
                    INSERT INTO answer (submission_time, question_id, message)
                    VALUES(%(submission_time)s, %(question_id)s, %(answer_message)s);
                    """,
                   {'submission_time': submission_time, 'question_id': question_id, 'answer_message': answer_message})


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


@database_common.connection_handler
def edit_answer(cursor, id, edited_answer):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(edited_answer)s
                    WHERE id = %(id)s""",
                   {'id': id, 'edited_answer': edited_answer})


@database_common.connection_handler
def add_question_comment(cursor, question_id, query_comment):
    submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
                    INSERT INTO comment (question_id, message, submission_time, edited_count)
                    VALUES (%(question_id)s, %(query_comment)s, %(submission_time)s, 0); 
                    """,
                   {'question_id': question_id, 'query_comment': query_comment,
                    'submission_time': submission_time})


@database_common.connection_handler
def get_question_comment(cursor, question_id):
    cursor.execute("""
                    SELECT submission_time, id, message FROM comment
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    comments = cursor.fetchall()
    return comments


@database_common.connection_handler
def add_new_comment(cursor, answer_id, new_comment):
    submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
                    INSERT INTO comment (answer_id, message, submission_time)
                    VALUES (%(answer_id)s, %(new_comment)s, %(submission_time)s);
                    """,
                   {'answer_id': answer_id, 'new_comment': new_comment,
                    'submission_time': submission_time})


@database_common.connection_handler
def get_answer_id(cursor, question_id):
    cursor.execute("""
                    SELECT id FROM answer
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    comm_answer_ids_pack = cursor.fetchall()
    ids = [dicty['id'] for dicty in comm_answer_ids_pack]
    return ids


@database_common.connection_handler
def get_answer_comment(cursor, ids):
    answer_comments_ids = tuple(ids)
    params = {'answer_comments_ids': answer_comments_ids}
    cursor.execute("""
                    SELECT submission_time, message, answer_id FROM comment
                    WHERE answer_id IN %(answer_comments_ids)s;
                    """,
                   params)
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
    params = {'text': text}
    cursor.execute("""
                    SELECT DISTINCT q.title, q.id FROM question q
                    INNER JOIN answer a on q.id = a.question_id
                    WHERE q.title ILIKE %(text)s OR q.message ILIKE %(text)s OR a.message ILIKE %(text)s;
                    """,
                   params)
    result = cursor.fetchall()
    return result
