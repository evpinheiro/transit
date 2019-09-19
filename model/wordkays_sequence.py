from deal_with_time import hour_minute
from model.workday import Workday


class WorkdaySequence:

    def __init__(self, sequence):  # list[Workday]):
        self.workday_sequence = sequence

    def get_duration(self):
        duration = 0
        for workday in self.workday_sequence:
            duration += workday.get_workday_time()
        return duration

    def show_workdays(self):
        workdays_press = []
        for workday in self.workday_sequence:
            workdays_press.append(workday.show_workday_description())
        return workdays_press


if __name__ == '__main__':
    wk1_bd = Workday(week_day='business_day', code='1M', start_time='08:00',
                     end_time='15:00', break_duration_time='00:30')
    wk1_sd = Workday(week_day='saturday', code='1M', start_time='08:10',
                     end_time='15:10', break_duration_time='00:30')
    week_sequence = WorkdaySequence([wk1_bd, wk1_sd])
    print(week_sequence.show_workdays())
    print(week_sequence.get_duration(), hour_minute(week_sequence.get_duration()))
