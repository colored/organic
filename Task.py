import datetime


class Task:
    def __init__(self, name, times, per_day, wage=100, from_time_hrs=1, till_time_hrs=23):
        self.name = name
        self.times = times
        self.per_day = per_day
        self.wage = wage
        self.from_time = 1 if from_time_hrs == '' else from_time_hrs
        self.till_time = 1 if till_time_hrs == '' else till_time_hrs

    def complete(self):
        if self.wage > 1:
            self.wage -= 1

        else:
            self.wage = 100
        return self
