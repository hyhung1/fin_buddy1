import matplotlib.pyplot as plt
import numpy as np

# 1) Define the data explicitly based on the provided output
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# 2) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(sectors, profits, color=['skyblue', 'lightgreen', 'lightcoral'])

# Set title and labels with bold text and larger font size
ax.set_title('Top 3 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)
ax.set_ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Make x-axis tick labels bold and larger font size
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=10) # Keep y-ticks normal size

# 3) Add subtle horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Improve layout
plt.tight_layout()

# 4) Save the figure as a separate PNG image
plt.savefig('top_3_sectors_net_profit_2019_2023.png')

# Close the plot to free up memory
plt.close(fig)
