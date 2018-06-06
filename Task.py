import random

DEFAULT_WAGE = 29

class Task:
    def __init__(self, name, wage=DEFAULT_WAGE):
        self.name = name
        self.wage = wage

    def complete(self):
        if self.wage > 1:
            self.wage -= 1

        else:
            self.wage = DEFAULT_WAGE
        return self

    @property
    def time(self):
        return 29 + random.randint(0, (DEFAULT_WAGE - self.wage))
