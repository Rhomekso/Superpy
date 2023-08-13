

from datetime import timedelta, date, datetime

class CurrentDate:

    def __init__(self, today):
        self.today = today

    def time(self):
        return self.today

# this moves the date forward
    def go_to_the_future(self, days):
        self.today = self.today + timedelta(days=days)
        return self.today

# this moves the date backwards
    def go_to_the_past(self, days):
        self.today = self.today - timedelta(days=days)
        return self.today 