import csv


def get_files_to_compare(csv_file):
    # with open(csv_file_path, 'rb') as csv_file:
    #     reader = csv.reader(csv_file)
    #
    #     rows = [row for row in reader]

    reader = csv.reader(csv_file)

    rows = [row for row in reader]

    return rows

