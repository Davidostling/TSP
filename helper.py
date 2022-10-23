
'''
Helper class containing various helper functions
'''
from typing import List
from point import Point
import heapq


def prims_algorithm(points: List[Point], costs: List[List[float]]):

    # Initialize min heap with all vertices
    mst = []
    min_heap = [(float('inf'), points[i], None) for i in range(1, len(points))]

    start_vertex = (0, points[0], None)
    visited = set()
    min_heap.append(start_vertex)
    popped_vertices = 0
    heapq.heapify(min_heap)

    while(popped_vertices < len(points)):
        # Extract minimum element
        min_element = heapq.heappop(min_heap)
        while min_element[1].id in visited:
            min_element = heapq.heappop(min_heap)
        popped_vertices += 1
        visited.add(min_element[1].id)

        if min_element[2] is not None:
            mst.append((min_element[1], min_element[2]))

        # push all the neighbors of the min element with new weights
        for index, neighbor_distance in enumerate(costs[min_element[1].id]):
            if index not in visited and index != min_element[1].id:
                heapq.heappush(min_heap,
                               (neighbor_distance, points[index], min_element[1]))
    # Return a list of tuples containing points, representing the edges that make up the mst
    return mst
