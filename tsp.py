from point import Point
from typing import List
from datetime import datetime
from random import randrange


class TSP(object):
    def __init__(self, n: int) -> None:
        self.start_time = datetime.now().timestamp()
        self.max_duration = 1.9
        self.n = n
        self.points: List[Point] = list()
        self.costs = [[0.0] * n for i in range(n)]
        self.tour: List[Point] = list()

    def _is_exit_time_reached(self) -> bool:
        if datetime.now().timestamp() - self.start_time < self.max_duration:
            return False
        else:
            return True

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
        total += tour[-1].distanceFrom(tour[0])
        return total

    def print(self, tour: List[Point]) -> None:
        for i in range(len(tour)):
            print(tour[i].id)

    def solve_greedy(self) -> List[Point]:
        current_point = self.points[randrange(self.n)]
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

    def two_point_five_opt(self, tour: List[Point]) -> List[Point]:
        best_distance = self.calculate_total_distance(tour)
        improve = True
        while improve:
            improve = False
            if self._is_exit_time_reached():
                return tour
            for i in range(self.n):
                for k in range(i + 3, self.n):
                    if self._is_exit_time_reached():
                        return tour
                    p1 = tour[i]
                    p5 = tour[k]
                    p2 = tour[((i + 1) % self.n)]
                    p3 = tour[((i + 2) % self.n)]
                    p4 = tour[((k - 1) % self.n)]
                    distance = (
                        self.costs[p1.id][p2.id]
                        + self.costs[p3.id][p4.id]
                        + self.costs[p4.id][p5.id]
                    )
                    distance -= (
                        self.costs[p1.id][p3.id]
                        + self.costs[p4.id][p2.id]
                        + self.costs[p2.id][p5.id]
                    )
                    if distance > 0:
                        improve = True
                        for l in range(i + 2, k):
                            tour[((l - 1) % self.n)] = tour[l]
                        tour[((k - 1) % self.n)] = p2
                        best_distance -= distance
                    p2 = tour[((i + 1) % self.n)]
                    p3 = tour[((k - 2) % self.n)]
                    p4 = tour[((k - 1) % self.n)]
                    distance = (
                        self.costs[p1.id][p2.id]
                        + self.costs[p3.id][p4.id]
                        + self.costs[p4.id][p5.id]
                    )
                    distance -= (
                        self.costs[p1.id][p4.id]
                        + self.costs[p4.id][p2.id]
                        + self.costs[p3.id][p5.id]
                    )
                    if distance > 0:
                        improve = True
                        l = k - 2
                        while i < l:
                            tour[((l + 1) % self.n)] = tour[l]
                            l -= 1
                        tour[((i + 1) % self.n)] = p4
                        best_distance -= distance
        return tour

    def two_opt(self, tour: List[Point]) -> List[Point]:
        distance = best_distance = self.calculate_total_distance(tour)
        improve = True
        while improve:
            improve = False
            if self._is_exit_time_reached():
                return tour
            for i in range(self.n):
                for k in range(i + 1, self.n):
                    if self._is_exit_time_reached():
                        return tour
                    p1 = tour[((i - 1) % self.n)]
                    p2 = tour[i]
                    p3 = tour[k]
                    p4 = tour[((k + 1) % self.n)]

                    distance = (
                        self.costs[p1.id][p2.id]
                        + self.costs[p3.id][p4.id]
                        - (self.costs[p1.id][p3.id] + self.costs[p2.id][p4.id])
                    )

                    if distance > 0:
                        improve = True
                        _from = i
                        _to = k
                        if (_to - _from) % 2 == 0:
                            limit = int((_to - _from) / 2)
                        else:
                            limit = int((_to - _from - 1) / 2)
                        for l in range(limit + 1):
                            m = _from + l
                            n = _to - l
                            temp = tour[m]
                            tour[m] = tour[n]
                            tour[n] = temp
                        best_distance -= distance
        return tour
