class Task:
    def __init__(self, name, wage=29):
        self.name = name
        self.wage = wage

    def complete(self):
        if self.wage > 1:
            self.wage -= 1

        else:
            self.wage = 29
        return self
