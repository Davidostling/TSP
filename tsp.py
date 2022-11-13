from point import Point
from helper import prims_algorithm, mst_to_adjacency_list, dfs, prims_algorithm_quadratic, tour_as_edges, two_opt_iterate, two_opt_step, calculate_total_distance_edges, simulated_annealing
from typing import List
import time


class TSP(object):
    def __init__(self, n: int) -> None:
        self.n = n
        self.points: List[Point] = list()
        self.costs = [[0.0] * n for i in range(n)]
        self.tour: List[Point] = list()

    def add_point(self, p: Point) -> None:
        for i in range(0, p.id):
            self.costs[i][p.id] = self.costs[p.id][i] = self.points[i].distanceFrom(
                p)
        self.points.append(p)

    def print_cost_matrix(self) -> None:
        for i in range(0, len(self.costs)):
            for j in range(0, len(self.costs[i])):
                print(
                    "(" + str(i) + ", " + str(j) + ") = " +
                    str(self.costs[i][j]) + " ",
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

    def christofides_tour(self) -> List[Point]:
        # Construct MST using Prim's algorithm
        mst = prims_algorithm(self.points, self.costs)
        print(mst)

    def two_approx(self) -> List[Point]:
        start_time = time.time()
        #mst = prims_algorithm_quadratic(self.points, self.costs)
        #mst_as_list = mst_to_adjacency_list(mst)
        #tour = dfs(mst_as_list, self.points[0])
        tour = self.solve_greedy()
        
        
        edges = tour_as_edges(tour)
        
        #dist_first = self.calculate_total_distance(tour)
        #print(dist_first)

        
        if len(tour) > 180:
            two_opt_iterate(edges, self.costs,start_time)
            best_edges, best_score = simulated_annealing(edges, self.costs, start_time, alpha=0.9)
         
        elif len(tour) > 100:
            best_edges, best_score = simulated_annealing(edges, self.costs, start_time, alpha=0.95)
            two_opt_iterate(best_edges, self.costs, start_time)   
        else:
            best_edges, best_score = simulated_annealing(edges, self.costs, start_time, alpha=0.999)
            two_opt_iterate(best_edges, self.costs, start_time)
        

        tour = [x[0] for x in best_edges]
        #dist_second = self.calculate_total_distance(tour)
        #print(dist_second)
        #print(best_score)
        #print(calculate_total_distance_edges(best_edges, self.costs))

        return tour


         