

from datetime import timedelta, date, datetime

# 09-07-2023 code works on the CLI just need to adjust the code with strftime and strptime


class CurrentDate:

    def __init__(self, today):
        self.today = today

    def time(self):
        return self.today

    def go_to_the_future(self, days):
        self.today = self.today + timedelta(days=days)
        return self.today

    def go_to_the_past(self, days):
        self.today = self.today - timedelta(days=days)
        return self.today 