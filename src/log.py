class Log:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

        difference = end_time - start_time
        self.total_time = difference.total_seconds()
