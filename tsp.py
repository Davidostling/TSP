from point import Point
from typing import List


class TSP(object):
    def __init__(self, n: int) -> None:
        self.n = n
        self.points: List[Point] = list()
        self.costs = [[0.0] * n for i in range(n)]
        self.tour: List[Point] = list()

    def add_point(self, p: Point) -> None:
        for i in range(0, p.id):
            self.costs[i][p.id] = self.costs[p.id][i] = self.points[i].distanceFrom(p)
        self.points.append(p)

    def print_cost_matrix(self) -> None:
        for i in range(0, len(self.costs)):
            for j in range(0, len(self.costs[i])):
                print(
                    "(" + str(i) + ", " + str(j) + ") = " + str(self.costs[i][j]) + " ",
                    end="",
                )
            print("")

    def calculate_total_distance(self, tour: List[Point]) -> float:
        total = 0.0
        for i in range(len(tour) - 1):
            total += tour[i].distanceFrom(tour[i + 1])
        return total

    def print(self, tour: List[Point]) -> None:
        for i in range(len(tour)):
            print(tour[i].id)

    def solve_greedy(self) -> List[Point]:
        current_point = self.points[0]
        self.tour.append(current_point)
        current_point.visit()
        for i in range(1, self.n):
            best_next = None
            for j in range(0, self.n):
                if not self.points[j].is_visited() and (
                    (not best_next)
                    or self.costs[current_point.id][j]
                    < self.costs[current_point.id][best_next.id]
                ):
                    best_next = self.points[j]
            current_point = best_next
            self.tour.append(best_next)
            current_point.visit()
        return self.tour
