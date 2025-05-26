import matplotlib.pyplot as plt
import numpy as np

# Data provided from the previous turn
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# Create figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Create bar chart
bars = ax.bar(sectors, profits, color=['skyblue', 'lightcoral', 'lightgreen'])

# Set titles and labels
ax.set_title('Top 3 Sectors by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
ax.set_xlabel('Sector', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Set x-axis tick labels to be bold and larger
ax.tick_params(axis='x', labelsize=12)
for ticklabel in ax.get_xticklabels():
    ticklabel.set_fontweight('bold')

# Add horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Save the figure
plt.tight_layout() # Adjust layout to prevent labels overlapping
plt.savefig('top_sectors_profit_2019_2023.png')

# Close the plot to free up memory
plt.close(fig)
