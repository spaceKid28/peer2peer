import random
from functools import reduce
import numpy as np

def main():
  # 1000 users
  # 1000 files

  #file ratio is fixed, all users change their behavior to match the file ratio
  share_ratio = .8

  # demand is a list of lists, 1000 lists, each contains 5 files
  # represents each user's demand for five files
  demand = []
  for i in range(1000):
    demand.append(random.sample(list(range(1000)), 5))

  # We will say each user has 50 files that they can share if they want to.
  files_available_to_seed = []
  for user in range(1000):
    files_available_to_seed.append(random.sample(list(range(1000)), 50))

  # files to seed
  # List of lists. 1000 lists, each 4 files long. Represents the files each user is willing to share in the network.
  # IMPORTANT, this will change in future time steps. Now, we just select 4 files from each user's library of 50 files.
  seeders = []
  for i in range(1000):
    seeders.append(random.sample(files_available_to_seed[i], 4))

  # Find the demand and supply for file.
  demand_per_file = [0] * 1000
  for li in demand:
    for i in li:
      demand_per_file[i] += 1

  seeders_per_file = [0] * 1000
  for li in seeders:
    for i in li:
      seeders_per_file[i] += 1
  
  # We will use the ratio of the number of users who want the file and the number of users who are willing to provide the file 
  # to measure the ease with which a user can download a file.

  ratio_per_file = [0] * 1000
  for i in range(1000):
    if seeders_per_file[i] == 0:
      # we are going to assign a very large number for files with no seeders. 
      ratio_per_file[i] = 20
    else:
      ratio_per_file[i] = demand_per_file[i]/seeders_per_file[i]

  
  # We are going to measure latency as the average of the squared ratios. This significantly punishes high values
  # ie files with lots of demand but very few seeders. 
  rms_latency = np.sqrt(np.mean([r**2 for r in ratio_per_file]))

  print("RMS latency (punishes outliers and no-seeder files):", rms_latency)

  # here we want to recalculate everyone's share ratio, but reward users who are providing files with high demand vs seeders ratio, and punish 
  

if __name__ == "__main__":
  main()
