import datamanager


def data_maker():
    ids, submission_times, view_numbers, titles, messages, rows = datamanager.read_questions('sample_data/question.csv')
    id_title = {k: v for k, v in zip(ids, titles)}
    return id_title


def get_question_data(id_):
    ids, times, view_numbers, titles, messages, rows = datamanager.read_questions('sample_data/question.csv')
    time = times[id_]
    view_number = view_numbers[id_]
    title = titles[id_]
    message = messages[id_]
    return time, view_number, title, message

def create_id(file):
    ids, times, view_numbers, titles, messages, rows = datamanager.read_questions(file)
    new_id = len(ids)
    return new_id

def create_answer_id(file):
    rows = datamanager.read_answers(file)
    answer_id = len(rows)
    return answer_id


def get_answers(question_id):
    rows = datamanager.read_answers('sample_data/answer.csv')
    answers = []
    for row in rows:
        if row['question_id'] == str(question_id):
            answers.append(row['message'])
    return answers
