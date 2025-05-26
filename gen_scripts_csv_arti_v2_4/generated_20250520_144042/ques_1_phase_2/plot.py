import matplotlib.pyplot as plt
import pandas as pd

# 1) Define the data explicitly
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# 2) Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# 3) Generate the plot (bar chart)
ax.bar(sectors, profits)

# Set title, axis labels, and x-tick labels with bold font and larger size
ax.set_title('Total Net Profit (2019-2023) by Top 3 Sectors', fontweight='bold', fontsize=14)
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)
ax.set_ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Make x-axis tick labels bold
ax.tick_params(axis='x', labelsize=12)
for label in ax.get_xticklabels():
    label.set_fontweight('bold')


# 4) Add horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 5) Save the figure as a PNG image
plt.savefig('top_3_sectors_net_profit.png')

# Close the plot figure to free memory
plt.close(fig)
