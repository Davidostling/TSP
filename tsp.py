from point import Point
from helper import (
    tour_as_edges,
    two_opt_iterate,
    two_opt_step,
)
import random
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

    def compute_path(self) -> List[Point]:
        start_time = time.time()
        # mst = prims_algorithm_quadratic(self.points, self.costs)
        # mst_as_list = mst_to_adjacency_list(mst)
        # tour = dfs(mst_as_list, self.points[0])
        tour = self.solve_greedy()
        edges = tour_as_edges(tour)
        # dist_first = self.calculate_total_distance(tour)
        # print(dist_first)

        best_edges = two_opt_randomized(tour, self.costs, start_time)
        #two_opt_iterate(edges, self.costs, start_time)

        tour = [x[0] for x in edges]
        # dist_second = self.calculate_total_distance(tour)
        # print(dist_second
        return tour

    def solve_randomized_two_opt(self) -> List[Point]:
        threshold = 1.85
        start_time = time.time()
        hashed_tours = set()
        tour = self.solve_greedy()
        
        tour_hash = hash(tuple([x.id for x in tour]))
        hashed_tours.add(tour_hash)
        edges = tour_as_edges(tour)
        
        two_opt_iterate(edges, self.costs, start_time, threshold=threshold)
        best_tour = [x[0] for x in edges]
        
        best_cost = self.calculate_total_distance(best_tour)
        
       
        while time.time() - start_time < threshold:
            
            random.shuffle(tour)
            while hash(tuple([x.id for x in tour])) in hashed_tours:
                random.shuffle(tour)
            
            new_edges = tour_as_edges(tour)

            if time.time() - start_time > threshold:
                break
            two_opt_iterate(new_edges, self.costs, start_time, threshold=threshold)
            if time.time() - start_time > threshold:
                break
            new_tour = [x[0] for x in new_edges]
            new_cost = self.calculate_total_distance(new_tour)
            #print("time: ", time.time() - start_time)
            #print("current tour: ", tour)
            #print("new cost: ", new_cost)
            if new_cost < best_cost:
                best_cost = new_cost
                best_tour = new_tour
            
            tour_hash = hash(tuple([x.id for x in tour]))
            hashed_tours.add(tour_hash)
        
        
        #print("best cost: ", best_cost)
        #print("time: ", time.time() - start_time)
        return best_tour

    