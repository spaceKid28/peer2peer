from functools import reduce
from helper import sol
import numpy as np

def main():
  solution = sol()
  # generate random list of files, and the number of people who want the files and list of people willing to provide the file
  ratio = solution.generate_random_preferences()
  # calculate the latency of the system (this is what we will measure)
  latency = solution.calculate_latency(ratio)
  print(f"This is the current measure of latency: {latency}. \n This is a list of the current file ratios: {ratio[:10]}")
  # readjust based on new share ratio criteria
  new_ratio = solution.recalculate(ratio)
  new_latency = solution.calculate_latency(new_ratio)
  print(f"""This is the NEW measure of latency: {new_latency}. 
        \n 
        This is a list of the current file ratios: {new_ratio[:10]}""")
  mean = np.mean(ratio)
  lower_quartile = np.percentile(ratio, 25)
  upper_quartile = np.percentile(ratio, 75)
  minimum = np.min(ratio)
  maximum = np.max(ratio)

  print(f"Mean: {mean}")
  print(f"Lower Quartile (25th percentile): {lower_quartile}")
  print(f"Upper Quartile (75th percentile): {upper_quartile}")
  print(f"Min: {minimum}")
  print(f"Max: {maximum}")

  mean = np.mean(new_ratio)
  lower_quartile = np.percentile(new_ratio, 25)
  upper_quartile = np.percentile(new_ratio, 75)
  minimum = np.min(new_ratio)
  maximum = np.max(new_ratio)

  print(f"Mean: {mean}")
  print(f"Lower Quartile (25th percentile): {lower_quartile}")
  print(f"Upper Quartile (75th percentile): {upper_quartile}")
  print(f"Min: {minimum}")
  print(f"Max: {maximum}")

if __name__ == "__main__":
  main()
