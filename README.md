# K-Means_Experiment

Machine Learning course assignment: Implement k-means++, run it 200 times and compare convergence efficiency and result quality with normal K-means.</br>
After 200 runs with and without K-means++ (K = 5) initialization the program provides the following data:
  - graphs showing the chosen initial 5 centroids for each of the 200 runs with and without K_means++ init
  - statistics at the end of each 200 runs experiments:
    - minimal value of all k-means objectives
    - average k-means objective
    - standard deviation
    - average number of iterations needed for K-means/K-means++ to converge (meaning the clusterization is complete)
    - experiment run time</br>
As stated in the experiment review ( K-means++_Experiment.pdf ) the graphs show a clearly better initialization of centroids for K-means++ that leads to a better value for the minimal objective and a smaller number of iterations needed for the algorithm to stop.   

