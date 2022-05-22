from asyncore import write
import csv
import os
import sys
from collections import Counter
from tabnanny import check
from threading import local

filter_values = {'HKWasUserEntered': '1'}


def main():
    directory = sys.argv[1]
    field_names = find_common_headers(directory)
    if (len(field_names) > 0):
        with open('health_output.csv', 'w', newline='') as csvoutfile:
            writer = csv.DictWriter(csvoutfile, fieldnames=field_names)
            writer.writeheader()
            for file_name in os.listdir(directory):
                if match_file_name(file_name):
                    parse_file(os.path.join(directory, file_name),
                               field_names, writer)

def match_file_name(file_name):
    return file_name.startswith('HKWorkoutActivityType') and file_name.endswith('.csv')


def parse_file(file_name, field_names, writer):
    with open(file_name, newline='') as csvfile:
        reader = wrap_reader(csvfile)
        for row in reader:
            # if there is data that should be filtered out then we iterate over rows till we find one that is not filtered or run out of rows
            write_row = True
            for elem in filter_values.items():
                if elem[0] in row.keys() and row[elem[0]] == elem[1]:
                    write_row = False
                    break

            if write_row:
                writer.writerow(format_row(filter_fields(row, field_names)))


def filter_fields(row, field_names):
    return dict(filter(lambda elem: elem[0] in field_names, row.items()))


def format_row(row):
    for key in row.keys():
        check_strip_after_space(row, key, 'totalEnergyBurned')
        check_strip_after_space(row, key, 'HKAverageMETs')
        check_strip_after_space(row, key, 'totalDistance')
        check_strip_after_space(row, key, 'totalSwimmingStrokeCount')
    return row


def check_strip_after_space(row, key, local_key):
    if (key == local_key):
        strip_after_space(row, local_key)


def strip_after_space(row, key):
    value = row[key]
    s = value.split()
    if (len(s) > 0):
        row[key] = s[0]


def find_common_headers(directory):
    # loop through all files and collect all the header names
    headers = []
    file_count = 0
    for file_name in os.listdir(directory):
        if match_file_name(file_name):
            file_name = os.path.join(directory, file_name)
            try:
                headers.extend(parse_headers(file_name))
                file_count += 1
                print('parsing file', file_name)
            except StopIteration:
                # don't increment file count, just skip file
                print('empty file', file_name)

    # convert to a map of header to count so we can remove fields not in every file
    header_map = Counter(headers)
    header_map = dict(
        filter(lambda elem: elem[1] == file_count, header_map.items()))
    headers = header_map.keys()
    return headers


def parse_headers(file_name):
    with open(file_name, newline='') as csvfile:
        reader = wrap_reader(csvfile)
        # check for next row, will throw StopIteration exception if no rows
        row = next(reader)
        # if there is data that should be filtered out then we iterate over rows till we find one that is not filtered or run out of rows
        done = False
        while not done:
            done = True
            for elem in filter_values.items():
                if elem[0] in row.keys():
                    if row[elem[0]] == elem[1]:
                        row = next(reader)
                    done = False
            row = next(reader)

        return reader.fieldnames


def wrap_reader(csvfile):
    csvfile.readline()  # skip first line in each file since it is "sep=," for some reason and not a known CSV dialect, but Excel is fine with it
    return csv.DictReader(csvfile)


if __name__ == '__main__':
    main()
