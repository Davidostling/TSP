
'''
Helper class containing various helper functions
'''
from typing import List
from point import Point
import time
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

def prims_algorithm_quadratic(points: List[Point], costs: List[List[float]]):
    mst = []
    start_vertex = (-1, points[0], None)
    # Create initial min distances from first point, represented as triples (distance, point, parent)
    min_distances = [start_vertex] + [(costs[0][i], points[i], points[0]) for i in range(1, len(points))]
    
    #print(min_distances)
    # Main loop
    for i in range(len(points) - 1):
        # Find minimum distance vertex
        min_dist = float('inf')
        best_idx = None
        for index, distance in enumerate(min_distances):
            if distance[0] < min_dist and distance[0] != -1:
                min_dist = distance[0]
                best_idx = index
        #print("Best next: ", min_distances[best_idx])
        # Add to mst
        mst.append((min_distances[best_idx][1], min_distances[best_idx][2]))
        #print(mst)
        # set distance to -1 to indicate that it has been visited
        min_distances[best_idx] = (-1, min_distances[best_idx][1], min_distances[best_idx][2])
        # Update min distances
        for idx, dist in enumerate(costs[best_idx]):
            if dist < min_distances[idx][0] and min_distances[idx][0] != -1:
                min_distances[idx] = (dist, points[idx], points[best_idx])
    return mst
        
def mst_to_adjacency_list(mst: List[tuple]):
    adjacency_list = {}
    for edge in mst:
        if edge[0].id not in adjacency_list:
            adjacency_list[edge[0].id] = []
        if edge[1].id not in adjacency_list:
            adjacency_list[edge[1].id] = []
        adjacency_list[edge[0].id].append(edge[1])
        adjacency_list[edge[1].id].append(edge[0])
    return adjacency_list

def dfs(graph, start, visited=None, path=[]):
    if visited is None:
        visited = set()
             
    visited.add(start.id)
    path.append(start)
    
    for next in graph[start.id]:
        if next.id not in visited:
            dfs(graph, next, visited, path)
    return path

def two_opt_swap(edges:List[tuple], costs: List[List[float]], first: int, second: int):
    e_1 = edges[first]
    e_2 = edges[second]
    current_cost = costs[e_1[0].id][e_1[1].id] + costs[e_2[0].id][e_2[1].id]
    new_cost = costs[e_1[0].id][e_2[0].id] + costs[e_1[1].id][e_2[1].id]

    if new_cost < current_cost:
        #print(e_1)
        #print(e_2)
        #print(f"found improvement from: {current_cost} to {new_cost}")
        #print(edges)
        edges[first] = (e_1[0],e_2[0])
        edges[second] = (e_1[1], e_2[1])
        edges[first+1:second] = list(map(lambda x : (x[1],x[0]), reversed(edges[first+1:second])))
        #print("nuevo")
        #print(edges)
        return True
    else: 
        return False

def two_opt_step(edges:List[tuple], costs: List[List[float]], start_time:float, threshold):
    improved = False
    
    for i in range(len(edges)-2):
        
        for j in range(i+1, len(edges)):
            if (time.time() - start_time) > threshold:
                return False
            performed_swap = two_opt_swap(edges, costs, i, j)
            if performed_swap:
                improved =  performed_swap
                i = j + 1
                break
                
    return improved

def two_opt_iterate(edges:List[tuple], costs: List[List[float]], start_time:float, threshold = 1.9):
    stop_time = time.time() - start_time
    improved = two_opt_step(edges, costs, start_time, threshold)
    while improved and stop_time < threshold:
        improved = two_opt_step(edges, costs, start_time, threshold)
        stop_time = time.time() - start_time

def tour_as_edges(tour:List[Point]):
    edges = []
    prev = tour[0]
    for i in range(1,len(tour)):
        edges.append((prev, tour[i]))
        prev = tour[i]
    edges.append((prev, tour[0]))
    return edges
    
