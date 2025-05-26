from functools import reduce
from helper import simulation
import numpy as np

def main():

  # run the simulation under different parameters to generate different graphs
  for runs in [100,500,1000]:
    for num_files in [3, 5, 10]:
      for perc in [.1, .25, .5]:
        solution = simulation(
            percentage_users_to_update=perc, 
            number_of_files_each_user_leeches_seeds=num_files,
            iterations_to_converge= runs
        )
        solution.build_graph()

  # Run simulation, under most appopriate_probable conditions, 
  # and see what the distribution is, of reduction in latency
  
  
  solution = simulation(
    percentage_users_to_update=.1,
    number_of_files_each_user_leeches_seeds=10,
    iterations=250,
    iterations=1000
  )
  
  solution.build_graph2()


if __name__ == "__main__":
  main()
