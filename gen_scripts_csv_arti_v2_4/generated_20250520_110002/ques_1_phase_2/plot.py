import matplotlib.pyplot as plt
import numpy as np

# 2) Build the data structure
sectors = ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources']
profits = [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]

# 3) Generate the plot
plt.figure(figsize=(10, 6)) # Optional: Adjust figure size

# Create bar chart
bars = plt.bar(sectors, profits, color='skyblue')

# Set title and labels with bold font and larger size
plt.title('Top 5 Sectors by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
plt.xlabel('Sector', fontsize=12, fontweight='bold')
plt.ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Set x-axis tick labels with bold font and larger size
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12) # Y-ticks don't need to be bold usually

# 4) Add subtle horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Improve layout to prevent labels overlapping
plt.tight_layout()

# 5) Save the figure as a PNG image
plt.savefig('top_5_sectors_net_profit.png')

# Optional: Display the plot (commented out as per typical script requirement)
# plt.show()

print("Plot saved as top_5_sectors_net_profit.png")
