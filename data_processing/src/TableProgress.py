from ExtensionHelper import ext_print


class TableProgress:
    def __init__(self, len_tables):
        self.counter = 0
        self.len_tables = len_tables

    def increase_progress(self, amount):
        self.counter += amount
        self.print_progress()

    def print_progress(self):
        value = (self.counter / self.len_tables) * 100
        if value < 10:
            progress = ('0' + str(value))[:2] + "%"
        elif value >= 100:
            progress = str(value)[:3] + "%"
        else:
            progress = str(value)[:2] + "%"
        ext_print('[OverallProgress] ' + progress)
