from functools import reduce
from helper import sol
import numpy as np

def main():
  solution = sol()
  solution.build_graph()
  solution.build_graph2()

  # mean = np.mean(ratio)
  # lower_quartile = np.percentile(ratio, 25)
  # upper_quartile = np.percentile(ratio, 75)
  # minimum = np.min(ratio)
  # maximum = np.max(ratio)

  # print(f"Mean: {mean}")
  # print(f"Lower Quartile (25th percentile): {lower_quartile}")
  # print(f"Upper Quartile (75th percentile): {upper_quartile}")
  # print(f"Min: {minimum}")
  # print(f"Max: {maximum}")

  # mean = np.mean(new_ratio)
  # lower_quartile = np.percentile(new_ratio, 25)
  # upper_quartile = np.percentile(new_ratio, 75)
  # minimum = np.min(new_ratio)
  # maximum = np.max(new_ratio)

  # print(f"Mean: {mean}")
  # print(f"Lower Quartile (25th percentile): {lower_quartile}")
  # print(f"Upper Quartile (75th percentile): {upper_quartile}")
  # print(f"Min: {minimum}")
  # print(f"Max: {maximum}")

if __name__ == "__main__":
  main()
