import math


class Point(object):

    counter = 0

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.id = Point.counter
        self.visited = False
        Point.counter += 1

    def visit(self) -> None:
        self.visited = True

    def is_visited(self) -> bool:
        return self.visited

    def distanceFrom(self, p: "Point") -> float:
        delta_x = float(self.x - p.x)
        delta_y = float(self.y - p.y)
        return math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other: "Point"):
        return self.id == other.id

    def __lt__(self, other: "Point"):
        return self.id < other.id
