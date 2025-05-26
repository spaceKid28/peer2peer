from functools import reduce
from helper import simulation
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

def main():

  # run the simulation under different parameters to generate different graphs
  # for runs in [100,500,1000]:
  #   for num_files in [3, 5, 10]:
  #     for perc in [.1, .25, .5]:
  #       solution = simulation(
  #           percentage_users_to_update=perc, 
  #           number_of_files_each_user_leeches_seeds=num_files,
  #           iterations_to_converge= runs
  #       )
  #       solution.build_graph()

  # Run simulation, under most appopriate_probable conditions, 
  # and see what the distribution is, of reduction in latency
  original_latencies = []
  new_latencies = []
  num_simulations = 100

  for i in range(num_simulations):
    solution = simulation(
      percentage_users_to_update=.1,
      number_of_files_each_user_leeches_seeds=5,
      iterations_to_converge=100
    )
    print(i)

    random_latency, adjusted_latency = solution.build_graph(generate_image = False)

    original_latencies.append(random_latency)
    new_latencies.append(adjusted_latency)
  # We assume latency more or less converges after 1000 runs. We run the simulation
  # an additional 1000 times (100,000 total cycles)

  # We take a look at each reduction in latency, and see what the distribution looks
  reductions = [og - new for og, new in zip(original_latencies, new_latencies)]
  print(reductions)
  plt.figure(figsize=(8, 6))

  # Box plot (shows median, quartiles, and spread)
  sns.boxplot(y=reductions, color='skyblue')

  # Strip plot (shows individual data points)
  sns.stripplot(y=reductions, color='black', alpha=0.2, jitter=True)

  plt.ylabel('Latency Reduction')
  plt.title(f'Distribution of Latency Reduction Over {num_simulations} Simulations')

  # Custom legend
  legend_elements = [
      Patch(facecolor='skyblue', edgecolor='gray', label='Box Plot: Median & Quartiles'),
      Line2D([0], [0], marker='o', color='w', label='Individual Reductions',
          markerfacecolor='black', markersize=8, alpha=0.4)
  ]
  plt.legend(handles=legend_elements, loc='upper right')
  plt.tight_layout()
  plt.savefig(
    f"""graphs/latency_reduction/num_files_{solution.number_of_files_each_user_leeches_seeds}_pct_updating_{solution.percentage_users_to_update}_iter_{solution.iterations_to_converge}.png""", dpi=300)
    
  plt.close()

  # Combine data for plotting
  data = original_latencies + new_latencies
  labels = (['Original'] * len(original_latencies)) + (['New'] * len(new_latencies))

  plt.figure(figsize=(8, 6))
  sns.swarmplot(x=labels, y=data, palette=['blue', 'red'])

  # Calculate and plot means
  mean_original = np.mean(original_latencies)
  mean_new = np.mean(new_latencies)
  plt.scatter(['Original'], [mean_original], color='black', marker='o', s=80, label='Mean Original')
  plt.scatter(['New'], [mean_new], color='black', marker='D', s=80, label='Mean New')

  plt.ylabel('Latency')
  plt.title('Swarm Plot of Original vs New Latencies')
  plt.legend()
  plt.tight_layout()
  plt.savefig(f"graphs/latency_reduction/Average Randomly generated Latency and Adjusted Latency.png", dpi = 300)


if __name__ == "__main__":
  main()
