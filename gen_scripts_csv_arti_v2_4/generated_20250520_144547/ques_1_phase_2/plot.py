import matplotlib.pyplot as plt
import pandas as pd

# 1) Define the data explicitly
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# 2) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Create the bar chart
ax.bar(sectors, profits, color=['skyblue', 'lightcoral', 'lightgreen'])

# Set title and labels with bold fontweight and larger fontsize
ax.set_title('Total Net Profit by Top Sectors (2019-2023)', fontweight='bold', fontsize=14)
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)
ax.set_ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Make x-axis tick labels bold and larger
ax.tick_params(axis='x', labelsize=12, labelweight='bold')
ax.tick_params(axis='y', labelsize=10) # Keep y-ticks normal size

# 3) Add horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Improve layout
plt.tight_layout()

# 4) Save the figure as a PNG image
plt.savefig('top_sectors_net_profit.png')

# Close the plot figure
plt.close(fig)
