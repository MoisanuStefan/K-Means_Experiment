import collections
import random
import math
import time

import matplotlib.pyplot as plt
from numpy.random import choice

import pandas as pd
RUN_COUNT = 200
objective_list = []


def euclidean_distance(a, b, squared=False):
    if ~squared:
        return pow(pow(abs(a[0] - b[0]), 2) + pow(abs(a[1] - b[1]), 2), 0.5)
    return pow(abs(a[0] - b[0]), 2) + pow(abs(a[1] - b[1]), 2)


class Kmeans:
    def __init__(self, k, data_set_filename, plus_plus=False):
        self.k = k
        self.plus_plus = plus_plus
        self.data = pd.read_csv(data_set_filename, header=0)
        self.cluster_center_list = list()
        self.cluster_list = []
        self.is_first_run = True

    # set clusters centers by choosing 5 random points
    def set_random_initial_cluster_centers(self):
        for i in range(self.k):
            random_index = random.randint(0, 499)
            self.cluster_center_list.append((self.data["x"][random_index], self.data["y"][random_index]))
        if self.is_first_run:
            plot_initial_centers(self.data, self.cluster_center_list)
            self.is_first_run = False

    # k-means++ algorithm: calculate distance from each point to all centers, choose for each point the closest center, make probability distribution, choose randomly
    def set_plus_plus_initial_cluster_centers(self):
        point_index_list = [x for x in range(500)]
        # add first random center
        random_index = random.randint(0, 499)
        self.cluster_center_list.append((self.data["x"][random_index], self.data["y"][random_index]))
        for i in range(1, self.k):
            distance_sum = 0
            distribution = []
            for j, point in self.data.iterrows():
                min_distance = 999999
                for cluster_center in self.cluster_center_list:
                    distance = float(euclidean_distance((point['x'], point['y']), cluster_center, squared=True))
                    if distance < min_distance:
                        min_distance = distance
                distribution.append(min_distance)
                distance_sum += min_distance
            distribution[:] = [x / distance_sum for x in distribution]
            max_distribution = -math.inf
            chosen_cluster_centre = 0
            index = 0
            for a in distribution:
                if a > max_distribution:
                    max_distribution = a
                    chosen_cluster_centre = index
                index += 1

            #chosen_cluster_centre = choice(a=point_index_list, size=1, p=distribution)[0]
            self.cluster_center_list.append((self.data['x'][chosen_cluster_centre], self.data['y'][chosen_cluster_centre]))
        # plot for first centers
        if self.is_first_run:
            plot_initial_centers(self.data, self.cluster_center_list)
            self.is_first_run= False


    def set_cluster_list(self):
        self.cluster_list = []
        for i in range(self.k):
            self.cluster_list.append([])
        for i, point in self.data.iterrows():
            point_tuple = (point['x'], point['y'])
            chosen_cluster_index = None
            min_euclidean_distance = 99999999
            current_cluster_index = 0
            chosen_point = None
            for cluster_center in self.cluster_center_list:
                current_distance = euclidean_distance(point_tuple, cluster_center)
                if current_distance < min_euclidean_distance:
                    min_euclidean_distance = current_distance
                    chosen_cluster_index = current_cluster_index
                    chosen_point = point_tuple
                current_cluster_index += 1
            self.cluster_list[chosen_cluster_index].append(chosen_point)

    def get_new_cluster_center_list(self):
        cluster_index = 0
        new_cluster_center_list = []
        for cluster in self.cluster_list:
            x_sum = 0
            y_sum = 0
            point_count = 0
            for point in cluster:
                x_sum += point[0]
                y_sum += point[1]
                point_count += 1
            if point_count > 0:
                new_cluster_center_list.append((x_sum / point_count, y_sum / point_count))
            else:
                new_cluster_center_list.append(self.cluster_center_list[cluster_index])
            cluster_index += 1
        return new_cluster_center_list

    def run(self):
        self.reset()
        if self.plus_plus:
            self.set_plus_plus_initial_cluster_centers()
        else:
            self.set_random_initial_cluster_centers()
        old_cluster_center_list = []
        nr_of_iterations = 0
        while collections.Counter(self.cluster_center_list) != collections.Counter(old_cluster_center_list):
            self.set_cluster_list()
            old_cluster_center_list = self.cluster_center_list
            self.cluster_center_list = self.get_new_cluster_center_list()
            nr_of_iterations += 1

        # get objective
        objective = self.get_k_mean_objective()
        # add it to the list
        objective_list.append(objective)
        print('{:15}{:20}'.format(nr_of_iterations, objective))
        return objective, nr_of_iterations

    def print_cluster_center_list(self):
        print("Cluster centers:")
        for point in self.cluster_center_list:
            print(point[0], ' ', point[1])

    def print_clusters(self):
        print("Clusters:")
        for cluster in self.cluster_list:
            print(cluster)

    def print_result(self):
        self.print_cluster_center_list()
        self.print_clusters()

    def get_k_mean_objective(self):
        cluster_index = 0
        x_squared_sum = 0
        y_squared_sum = 0
        for cluster in self.cluster_list:
            for point in cluster:
                x_squared_sum += pow(point[0] - self.cluster_center_list[cluster_index][0], 2)
                y_squared_sum += pow(point[1] - self.cluster_center_list[cluster_index][1], 2)
            cluster_index += 1
        return x_squared_sum + y_squared_sum

    def reset(self):
        self.cluster_list = []
        self.cluster_center_list = []


def initialize_points_to_scatter(points_to_scatter, kmeans_object):
    for i, point in kmeans_object.data.iterrows():
        points_to_scatter.append((point['x'], point['y']))



def plot(points_to_scatter):
    sizes = []
    colors = []
    xs = []
    ys = []
    for i in range(500):
        sizes.append(20)
        colors.append("grey")
    for i in range(RUN_COUNT * 5):
        sizes.append(10)
        colors.append("red")
    for x, y in points_to_scatter:
        xs.append(x)
        ys.append(y)
    plt.scatter(xs, ys, s=sizes, color=colors)
    plt.ylabel('y')
    plt.xlabel('x')
    plt.show()

def plot_initial_centers(data, points):
    colors = []
    sizes = []
    xs = []
    ys = []
    for i, point in data.iterrows():
        xs.append(point['x'])
        ys.append(point['y'])
    for i in range(500):
        colors.append("grey")
        sizes.append(20)
    for i in range(5):
        colors.append("blue")
        sizes.append(40)
    for x,y in points:
        xs.append(x)
        ys.append(y)
    plt.scatter(xs, ys, s=sizes, color=colors)
    plt.ylabel('y')
    plt.xlabel('x')
    plt.show()


def get_standard_deviation(avg):
    sum = 0
    for objective in objective_list:
        sum += pow(objective - avg, 2)
    return pow(sum / RUN_COUNT, 0.5)


def run_test(plus_plus_init):
    points_to_scatter = []
    objective_sum = 0
    iteration_sum = 0
    min_objective = math.inf
    kmeans = Kmeans(5, "training_data.csv", plus_plus_init)
    initialize_points_to_scatter(points_to_scatter, kmeans)
    print('{:>5}{:>15}{:>20}'.format('run', '\#iterations', 'objective'))
    begin_time = time.time()
    for i in range(RUN_COUNT):
        print('{:5}'.format(i), end='')
        objective, iterations = kmeans.run()
        if objective < min_objective:
            min_objective = objective
        objective_sum += objective
        iteration_sum += iterations
        # kmeans.print_result()
        points_to_scatter.extend(kmeans.cluster_center_list)
    end_time = time.time()
    print("min_obj: ", min_objective, "\navg_objective: ", objective_sum / RUN_COUNT, "\nstandard deviation: ",
          get_standard_deviation(objective_sum / RUN_COUNT), "\navg_iterations_till_convergence: ",
          iteration_sum / RUN_COUNT, "\nrun_time: ", end_time - begin_time)
    plot(points_to_scatter)


def main():
    print("200 runs with random cluster center init:")
    run_test(plus_plus_init=False)
    print("200 runs with K-means++ init:")
    run_test(plus_plus_init=True)


if __name__ == "__main__":
    main()
