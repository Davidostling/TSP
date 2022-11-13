from point import Point
from typing import List
from datetime import datetime


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

    def two_opt(self, tour: List[Point]) -> List[Point]:
        improve = True
        while improve:
            improve = False
            if self._is_exit_time_reached():
                return tour
            for i in range(1, self.n - 1):
                for j in range(i + 1, self.n):
                    if self._is_exit_time_reached():
                        return tour
                    # Given A-B...C-D try A-C...B-D
                    A = tour[i - 1]
                    B = tour[i]
                    C = tour[j]
                    D = tour[(j + 1) % self.n]
                    before = self.costs[A.id][B.id] + self.costs[C.id][D.id]
                    after = self.costs[A.id][C.id] + self.costs[B.id][D.id]
                    gain = before - after
                    print("iterating + (" + str(i) + "," + str(j) + ")")
                    if gain > 0:
                        tour = self._two_opt_swap(tour, i, j)
                        improve = True
                        print("improved: ")
                        self.print(tour)
                        i = j + 1
                        break
        return tour

    def _two_opt_swap(self, tour: List[Point], p1_id: int, p2_id: int) -> List[Point]:
        if p1_id == p2_id:
            return tour
        if p1_id > p2_id:
            _tmp = p1_id
            p1_id = p2_id
            p2_id = _tmp
        tour[p1_id : p2_id + 1] = reversed(tour[p1_id : p2_id + 1])
        return tour

    def two_half_opt(self, tour: List[Point]) -> List[Point]:
        improve = True
        while improve:
            improve = False
            if self._is_exit_time_reached():
                return tour
            for i in range(0, self.n - 3):
                for j in range(i + 3, self.n):
                    if self._is_exit_time_reached():
                        return tour
                    # Given A-B-C...D-E try A-C...D-B-E
                    A = tour[i]
                    B = tour[i + 1]
                    C = tour[i + 2]
                    D = tour[j - 1]
                    E = tour[j]
                    before = (
                        self.costs[A.id][B.id]
                        + self.costs[B.id][C.id]
                        + self.costs[D.id][E.id]
                    )
                    after = (
                        self.costs[A.id][C.id]
                        + self.costs[D.id][B.id]
                        + self.costs[B.id][E.id]
                    )
                    gain = before - after
                    if gain > 0:
                        improve = True
                        _tmp = B
                        for k in range(i + 2, j):
                            tour[k - 1] = tour[k]
                        tour[j - 1] = _tmp

                    # Given A-B...C-D-E try A-D-B...C-E
                    A = tour[i]
                    B = tour[i + 1]
                    C = tour[j - 2]
                    D = tour[j - 1]
                    E = tour[j]
                    before = (
                        self.costs[A.id][B.id]
                        + self.costs[C.id][D.id]
                        + self.costs[D.id][E.id]
                    )
                    after = (
                        self.costs[A.id][D.id]
                        + self.costs[D.id][B.id]
                        + self.costs[C.id][E.id]
                    )
                    gain = before - after
                    if gain > 0:
                        improve = True
                        _tmp = D
                        for k in range(j - 2, i, -1):
                            tour[k + 1] = tour[k]
                        tour[i + 1] = _tmp
        return tour
