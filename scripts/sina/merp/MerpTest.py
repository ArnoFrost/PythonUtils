import time


class PasscodeGenerator:

    def __init__(self, interval_period, time_offset=60, code_length=6, is_created=False):
        self.interval_period = interval_period
        self.time_offset = time_offset
        self.code_length = code_length
        self.is_created = is_created

    def get_current_interval(self):
        current_time_seconds = (time.time() - self.time_offset)
        interval_period_count = current_time_seconds // self.interval_period

        if self.is_created:
            remaining_time = self.interval_period - (current_time_seconds % self.interval_period)
            print(f"Remaining time: {remaining_time} seconds")
        return int(interval_period_count)

    def get_interval_period(self):
        return self.interval_period


if __name__ == '__main__':
    passcode_generator = PasscodeGenerator(interval_period=60, code_length=6, is_created=True)
    interval = passcode_generator.get_current_interval()
    print(f"Interval: {interval}")
