class CalDisplayFormat(object):
    def __init__(self):
        pass

    def percent(self, part, total):
        return self.display(part, total, 100, '{}%')

    def ten(self, part, total):
        return self.display(part, total, 10, '{}/10')

    @staticmethod
    def display(part, total, mom, display_format):
        p_speed = int((part * mom) / total)
        return display_format.format(p_speed)
