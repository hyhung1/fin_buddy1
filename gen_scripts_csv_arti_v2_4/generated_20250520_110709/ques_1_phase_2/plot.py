import matplotlib.pyplot as plt
import numpy as np

# 2) Build the data structure
sectors = ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources']
profits = [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]

# 3) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(sectors, profits)

# Set title, axis labels, and x-tick labels to bold with larger font size
ax.set_title('Top 5 Sectors with Highest Net Profit (2019-2023)', fontsize=14, fontweight='bold')
ax.set_xlabel('Sector', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Make x-axis tick labels bold and larger
ax.tick_params(axis='x', labelsize=12)
for tick in ax.get_xticklabels():
    tick.set_fontweight('bold')

# 4) Add grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

plt.tight_layout() # Adjust layout to prevent labels overlapping

# 5) Save the figure
plt.savefig('top_5_sectors_profit.png')

# Display the plot (optional, for interactive environments)
# plt.show()
