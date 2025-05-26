import matplotlib.pyplot as plt
import numpy as np

# 1) Define the data explicitly
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# 2) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Create bar plot
bars = ax.bar(sectors, profits, color=['skyblue', 'lightcoral', 'lightgreen'])

# Set title and labels with bold font and larger fontsize
ax.set_title('Total Net Profit (2019-2023) by Top 3 Sectors', fontsize=14, fontweight='bold')
ax.set_xlabel('Sector', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Make x-axis tick labels bold and larger fontsize
plt.xticks(fontsize=12, fontweight='bold')

# Add subtle horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Ensure layout is tight
plt.tight_layout()

# 3) Save the figure
plt.savefig('top_3_sectors_net_profit.png')

# Close the plot to free up memory
plt.close(fig)
