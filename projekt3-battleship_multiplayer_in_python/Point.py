class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_valid(self):
        if self.x < 1 or self.x > 10 or self.y < 1 or self.y > 10:
            return False
        return True

    @staticmethod
    def is_valid_point(x, y):
        if x < 1 or x > 10 or y < 1 or y > 10:
            return False
        return True