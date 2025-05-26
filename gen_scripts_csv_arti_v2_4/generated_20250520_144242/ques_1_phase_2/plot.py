import matplotlib.pyplot as plt
import numpy as np

# 1) Define the data explicitly
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# Create a figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# 2) Generate the bar plot
ax.bar(sectors, profits)

# Set title and labels with bold font and larger size
ax.set_title('Total Net Profit by Top Sectors (2019-2023)', fontweight='bold', fontsize=14)
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)
ax.set_ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Set x-axis tick labels to bold and larger size
ax.tick_params(axis='x', labelsize=12, labelcolor='black', which='both', fontweight='bold')
ax.tick_params(axis='y', labelsize=10, labelcolor='black') # Keep y-ticks normal size/weight

# 3) Add subtle horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Use tight_layout to prevent labels from overlapping
plt.tight_layout()

# 4) Save the figure as a PNG image
plt.savefig('top_sectors_net_profit.png')

# Close the plot figure
plt.close(fig)
