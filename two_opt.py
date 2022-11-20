"""
Two opt class containing various functions
"""
from typing import List
from point import Point
import time

def tour_as_edges(tour: List[Point]):
        """ 
        Converts tour to list of edges.

        :param tour: List of points 
        :return: tour as list of edges
        """
        edges = []
        prev = tour[0]

        for i in range(1, len(tour)):
            edges.append((prev, tour[i]))
            prev = tour[i]
        edges.append((prev, tour[0]))
        return edges

def two_opt_iterate(
    edges: List[tuple], costs: List[List[float]], start_time: float, threshold=1.9
):
    """
    Iteratively improve edges by perfoming 2-opt-step.

    :param edges: List of edges
    :param costs: Matrix  of costs
    :param start_time: Start timestamp
    :param threshold: Time limit to exit function
    """
    stop_time = time.time() - start_time
    if stop_time > threshold:
        return
    improved = two_opt_step(edges, costs, start_time, threshold)
    while improved and stop_time < threshold:
        improved = two_opt_step(edges, costs, start_time, threshold)
        stop_time = time.time() - start_time


def two_opt_step(edges: List[tuple], costs: List[List[float]], start_time: float, threshold):
    """
    Iteratively try to find a swap where there is an improvent.

    :param edges: List of edges 
    :param costs: Matrix  of costs 
    :param start_time: Start timestamp  
    :param threshold: Time limit to exit function
    :return: Improved edges
    """
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


def two_opt_swap(edges: List[tuple], costs: List[List[float]], first: int, second: int):
    """
    Swap two edges to check if there is an improved cost.

    :param edges: List of edges 
    :param costs: Matrix  of costs 
    :param first: Index for first edge  
    :param second: Index for second edge
    :return: Boolean if swap is performed.
    """
    e_1 = edges[first]
    e_2 = edges[second]
    current_cost = costs[e_1[0].id][e_1[1].id] + costs[e_2[0].id][e_2[1].id]
    new_cost = costs[e_1[0].id][e_2[0].id] + costs[e_1[1].id][e_2[1].id]

    if new_cost < current_cost:
        edges[first] = (e_1[0], e_2[0])
        edges[second] = (e_1[1], e_2[1])
        edges[first + 1: second] = list(
            map(lambda x: (x[1], x[0]), reversed(edges[first + 1: second]))
        )
        return True
    else:
        return False

