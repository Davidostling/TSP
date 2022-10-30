import sys
from tsp import TSP
from point import Point


if __name__ == "__main__":
    number_of_points = int(sys.stdin.readline())
    if number_of_points < 2:
        print(0)
    else:
        tsp = TSP(number_of_points)
        for index in range(number_of_points):
            line_array = sys.stdin.readline().split()
            tsp.add_point(Point(float(line_array[0]), float(line_array[1])))

        #### start solving ####
        #tsp.print_cost_matrix()
        #tour = tsp.solve_greedy())
        #total_distance = tsp.calculate_total_distance(tour)
        
        tour = tsp.two_approx()
        
        tsp.print(tour)        

    

    
