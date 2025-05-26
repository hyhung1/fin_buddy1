import matplotlib.pyplot as plt
import pandas as pd

# 1) Define the data explicitly
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# 2) Create the plot
plt.figure(figsize=(10, 6)) # Optional: Adjust figure size

plt.bar(sectors, profits)

# 3) Add title, axis labels, and x-tick labels with bold font and larger size
plt.title("Top 3 Sectors by Total Net Profit (2019-2023)", fontweight='bold', fontsize=12)
plt.xlabel("Sector", fontweight='bold', fontsize=12)
plt.ylabel("Total Net Profit (Billions VND)", fontweight='bold', fontsize=12)
plt.xticks(sectors, fontweight='bold', fontsize=12) # Set x-tick labels explicitly

# 4) Add subtle horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

plt.tight_layout() # Adjust layout to prevent labels overlapping

# 5) Save the figure as a PNG image
plt.savefig('top_sectors_net_profit.png')

# Close the plot figure
plt.close()
