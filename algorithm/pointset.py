# inhenced set to help get points by their x or y index easier
class PointSet:
    def __init__(self):
        self.x2y = {}
        self.y2x = {}
        self.points = set()

    def add_point(self, tuple):
        x, y = tuple
        if x in self.x2y or y in self.y2x:
            return False
        self.x2y[x] = y
        self.y2x[y] = x
        self.points.add((x, y))

    def get_by_x(self, x):
        return x, self.x2y[x]

    def get_by_y(self, y):
        return self.y2x[y], y

    def contains_x(self, x):
        return x in self.x2y

    def contains_y(self, y):
        return y in self.y2x

    def remove_point(self, point):
        x, y = point
        self.x2y.pop(x, None)
        self.y2x.pop(y, None)
        self.points.remove((x, y))

    # problem here
    # do not mix use the next function and the delete function
    # there will be error
    def __iter__(self):
        for v in sorted(self.points):  # iterate over list of values returned by sorted
            yield v
