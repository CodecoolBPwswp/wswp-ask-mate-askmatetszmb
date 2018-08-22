import csv


def read_from_csv(csvfile):
    with open(csvfile, newline='') as f:
        reader = csv.DictReader(f)
        ids = []
        submission_times = []
        view_numbers = []
        titles = []
        messages = []
        for row in reader:
            ids.append(row['id'])
            submission_times.append(row['submission_time'])
            view_numbers.append(row['view_number'])
            titles.append(row['title'])
            messages.append(row['message'])
        return ids, submission_times, view_numbers, titles, messages


def write_to_csv(csvfile, id_, time, view_number, title, message):
    vote_number = 0
    image = ''
    with open(csvfile, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([id_] + [time] + [view_number] + [vote_number] + [title] + [message] + [image])
