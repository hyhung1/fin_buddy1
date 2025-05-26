import matplotlib.pyplot as plt
import numpy as np

# 1) Define the data explicitly
sectors = ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources']
net_profit = [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]

# 2) Create the plot
plt.figure(figsize=(10, 6))
bars = plt.bar(sectors, net_profit, color='skyblue')

# 3) Set chart title, axis labels, and x-tick labels with bold font and larger size
plt.title('Top 5 Sectors by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
plt.xlabel('Sector', fontsize=12, fontweight='bold')
plt.ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Set x-tick labels to bold and larger font size
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12) # Keep y-ticks normal size

# 4) Add subtle horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 5) Save the figure as a PNG image
plt.savefig('top_5_sectors_net_profit_2019_2023.png')

# Display the plot (optional, but good for interactive environments)
# plt.show()
