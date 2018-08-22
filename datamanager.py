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
