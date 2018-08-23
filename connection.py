import time
import datamanager

timestamp = int(time.time())


def data_maker():
    ids, submission_times, view_numbers, titles, messages = datamanager.read_questions('sample_data/question.csv')
    id_title = {k: v for k, v in zip(ids, titles)}
    return id_title


def get_question_data(id_):
    ids, times, view_numbers, titles, messages = datamanager.read_questions('sample_data/question.csv')
    time = times[id_]
    view_number = view_numbers[id_]
    title = titles[id_]
    message = messages[id_]
    return time, view_number, title, message