import csv


class StandardWorkday(object):
    def __init__(self, day_of_week, workday_type, start_time, end_time):
        self.day_of_week = day_of_week
        self.workday_kind = workday_type
        self.start_time = start_time
        self.end_time = end_time


class StandardWorkdayImportation(object):
    def __init__(self):
        self.list_of_standard_workday = []

    def importing_standard_workday(self, day_of_week, path_name):
        with open(path_name) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.list_of_standard_workday.append(StandardWorkday(day_of_week, row[0], row[1], row[2]))
        return self.list_of_standard_workday
