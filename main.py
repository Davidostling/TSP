import sys
from tsp import TSP
from point import Point


if __name__ == "__main__":
    number_of_points = int(sys.stdin.readline())
    tsp = TSP(number_of_points)
    for index in range(number_of_points):
        line_array = sys.stdin.readline().split()
        tsp.add_point(Point(float(line_array[0]), float(line_array[1])))

    #### start solving ####
    tour = tsp.solve_greedy()
    tour = tsp.two_opt(tour)
    # tour = tsp.two_half_opt(tour)
    tsp.print(tour)
    print(tsp.calculate_total_distance(tour))
