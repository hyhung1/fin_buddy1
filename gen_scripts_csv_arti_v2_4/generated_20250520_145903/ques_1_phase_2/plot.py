import matplotlib.pyplot as plt
import numpy as np

# 1) & 2) Build the data structure
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# 3) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(sectors, profits, color=['skyblue', 'lightcoral', 'lightgreen'])

# Set titles and labels with bold font and larger size
ax.set_title('Top 3 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)
ax.set_ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Set x-axis tick labels with bold font and larger size
ax.set_xticklabels(sectors, fontweight='bold', fontsize=12)

# 4) Add horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Improve layout
plt.tight_layout()

# 5) Save the figure
plt.savefig('top_sectors_net_profit.png')

# Close the plot
plt.close(fig)

print("Plot saved to top_sectors_net_profit.png")
