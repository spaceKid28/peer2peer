import random
from functools import reduce
def main():
  # 100 users
  # 100 files

  # demand is a list of lists, 100 lists, each contains 5 files
  demand = []
  for i in range(1000):
    demand.append(random.sample(list(range(1000)), 5))

  # seeders
  seeders = []
  for i in range(1000):
    seeders.append(random.sample(list(range(1000)), 4))
  
  demand_per_file = [0] * 1000
  for li in demand:
    for i in li:
      demand_per_file[i] += 1

  seeders_per_file = [0] * 1000
  for li in seeders:
    for i in li:
      seeders_per_file[i] += 1
  

  print(demand_per_file)
  print(seeders_per_file)

  ratio_per_file = [0] * 1000
  for i in range(1000):
    if seeders_per_file[i] == 0:
      ratio_per_file[i] = "div by zero"
    else:
      ratio_per_file[i] = demand_per_file[i]/seeders_per_file[i]
  
  print(ratio_per_file)
  


if __name__ == "__main__":
  main()
