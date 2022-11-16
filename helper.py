"""
Helper class containing various helper functions
"""
from typing import List
from point import Point
import random
import time


def two_opt_swap(edges: List[tuple], costs: List[List[float]], first: int, second: int):
    e_1 = edges[first]
    e_2 = edges[second]
    current_cost = costs[e_1[0].id][e_1[1].id] + costs[e_2[0].id][e_2[1].id]
    new_cost = costs[e_1[0].id][e_2[0].id] + costs[e_1[1].id][e_2[1].id]

    if new_cost < current_cost:
        # print(f"found improvement from: {current_cost} to {new_cost}")
        # print(edges)
        edges[first] = (e_1[0], e_2[0])
        edges[second] = (e_1[1], e_2[1])
        edges[first + 1 : second] = list(
            map(lambda x: (x[1], x[0]), reversed(edges[first + 1 : second]))
        )
        return True
    else:
        return False


def two_opt_step(
    edges: List[tuple], costs: List[List[float]], start_time: float, threshold
):
    improved = False

    for i in range(len(edges) - 2):

        for j in range(i + 1, len(edges)):
            if (time.time() - start_time) > threshold:
                return False
            performed_swap = two_opt_swap(edges, costs, i, j)
            if performed_swap:
                improved = performed_swap
                i = j + 1
                break

    return improved


def two_opt_iterate(
    edges: List[tuple], costs: List[List[float]], start_time: float, threshold=1.9
):
    stop_time = time.time() - start_time
    if stop_time > threshold:
        return
    improved = two_opt_step(edges, costs, start_time, threshold)
    while improved and stop_time < threshold:
        improved = two_opt_step(edges, costs, start_time, threshold)
        stop_time = time.time() - start_time


def tour_as_edges(tour: List[Point]):
    edges = []
    prev = tour[0]
    for i in range(1, len(tour)):
        edges.append((prev, tour[i]))
        prev = tour[i]
    edges.append((prev, tour[0]))
    return edges

