import csv
import connection
import time


def read_questions(csvfile):
    with open(csvfile, newline='') as f:
        reader = csv.DictReader(f)
        ids = []
        submission_times = []
        view_numbers = []
        titles = []
        messages = []
        rows = []
        for row in reader:
            ids.append(row['id'])
            submission_times.append(row['submission_time'])
            view_numbers.append(row['view_number'])
            titles.append(row['title'])
            messages.append(row['message'])
            rows.append(row)
        return ids, submission_times, view_numbers, titles, messages, rows


def write_question(csvfile, view_number, title, message):
    new_id = connection.create_id(csvfile)
    UnixStamp = int(time.time())
    vote_number = 0
    image = ''
    with open(csvfile, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([new_id] + [UnixStamp] + [view_number] + [vote_number] + [title] + [message] + [image])


def read_answers(csvfile):
    with open(csvfile, newline='') as f:
        reader = csv.DictReader(f)
        ids = []
        submission_times = []
        question_ids = []
        messages = []
        for row in reader:
            ids.append(row['id'])
            submission_times.append(row['submission_time'])
            question_ids.append(row['question_id'])
            messages.append(row['message'])
        return ids, submission_times, question_ids, messages


def write_answer(csvfile, id_, time, question_id, message):
    vote_number = 0
    image = ''
    with open(csvfile, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([id_] + [time] + [vote_number] + [question_id] + [message] + [image])
