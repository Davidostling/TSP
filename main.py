import sys

num_cities = sys.stdin.readline()

cities = []
first_city = sys.stdin.readline().split()
first_city = (float(first_city[0]), float(first_city[1]), 0)
for index in range(int(num_cities)-1):
    city = sys.stdin.readline().split()
    cities.append((float(city[0]),float(city[1]), index+1))

cities.sort()
cities.insert(0, first_city)
for city in cities:
    print(city[2])