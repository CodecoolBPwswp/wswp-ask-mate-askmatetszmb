import time
from datamanager import read_questions

timestamp = int(time.time())

def data_maker():
    ids, submission_times, view_numbers, titles, messages = read_questions('sample_data/question.csv')
    id_title = {k: v for k, v in zip(ids, titles)}
    return id_title