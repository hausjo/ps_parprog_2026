import pandas as pd
import matplotlib.pyplot as plt

# load data
try:
    df = pd.read_csv('results.csv')
except FileNotFoundError:
    print("Error: results.csv not found")
    exit()

# initialize plot
plt.figure(figsize=(10, 6))

# own line for every program
programs = df['Program'].unique()

for prog in programs:
    prog_data = df[df['Program'] == prog]
    
    plt.plot(prog_data['Affinity'], prog_data['Time'], 
             marker='o', linestyle='-', label=prog)

plt.xlabel('Core Affinity]')
plt.ylabel('Execution time [s]')
plt.title('Performance Comparison on lcc3')
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)

plt.ylim(bottom=0)

plt.tight_layout()
plt.savefig('performance_plot.png', dpi=300)
print("Graph has been saved.")
plt.show()