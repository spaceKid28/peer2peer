import random
from functools import reduce
import numpy as np
from helper import sol

def main():
  solution = sol()
  # generate random list of files, and the number of people who want the files and list of people willing to provide the file
  ratio, library = solution.generate_random_preferences()
  # calculate the latency of the system (this is what we will measure)
  latency = solution.calculate_latency(ratio)
  print(f"This is the current measure of latency: {latency}. \n This is a list of the current file ratios: {ratio[:10]}")
  #
  
  

if __name__ == "__main__":
  main()
