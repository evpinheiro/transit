class RosteringProcedure:
    def __init__(self, sw_util_list, sw_saturday_list, sw_sunday_list):
        self.sw_util_list = sw_util_list
        self.sw_saturday_list = sw_saturday_list
        self.sw_sunday_list = sw_sunday_list
        self.weekly_workday_list = []

    # implement it here
    def greedy_algorithm(self):
        sw_weekend_list = self.sw_saturday_list.append(self.sw_sunday_list)
        for sw_util in self.sw_util_list:
            for sw_weekend in sw_weekend_list:
                if self.is_sw_compatible(sw_util, sw_weekend):
                    self.weekly_workday_list.append([sw_util, sw_weekend])

    def is_sw_compatible(self,  sw1, sw2):
        return sw1.end_time > sw2.start_time










