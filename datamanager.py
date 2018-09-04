import database_common

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
