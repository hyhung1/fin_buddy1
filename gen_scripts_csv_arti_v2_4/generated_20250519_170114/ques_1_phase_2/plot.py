import matplotlib.pyplot as plt
import numpy as np

# 2) Build the data structure
sectors = ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources']
total_profits = [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]

# 3) Generate the plot(s)
fig, ax = plt.subplots(figsize=(10, 6)) # Adjust figure size as needed

bars = ax.bar(sectors, total_profits, color='skyblue')

# Set title, axis labels, and x-tick labels to bold and larger font size
ax.set_title('Top 5 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)
ax.set_ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Set x-axis tick labels to bold and larger font size
plt.xticks(fontweight='bold', fontsize=12)
plt.yticks(fontsize=10) # Y-ticks don't need to be bolded per instructions

# 4) Add the grid lines as specified
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 5) Save each figure as a separate PNG image
plt.savefig('top_5_sectors_net_profit.png')

# Close the plot figure to free up memory
plt.close(fig)
