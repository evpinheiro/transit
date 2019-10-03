from deal_with_time import hour_minute, minutes


class Workday:

    """
        This class can be improved for a wider workday descrition
        >>> wk1_sd = Workday('saturday', '1M', '08:10', '15:10', '00:30')
        >>> wk1_sd.get_workday_time()
        390
        >>> wk1_sd.show_workday_description()
        ('saturday', '1M', '08:10', '15:10', '06:30')
    """
    def __init__(self, week_day, code, start_time, end_time, break_duration_time=0):
        self.day_of_the_week = week_day
        self.code = code
        self.start_time = minutes(start_time)
        self.end_time = minutes(end_time)
        self.break_duration = minutes(break_duration_time)

    def get_workday_time(self):
        return self.end_time - self.start_time - self.break_duration

    def show_workday_description(self):
        return self.day_of_the_week, self.code, hour_minute(self.start_time), hour_minute(self.end_time), hour_minute(self.get_workday_time())


def import_workdays(week_day, fname):
    f = open(fname)
    content = f.readlines()
    f.close()
    workdays = []
    for line in content:
        fields = line.split(',')
        workdays.append(Workday(week_day, fields[0], fields[1], fields[2], fields[3]))
    return workdays
