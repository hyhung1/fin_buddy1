import matplotlib.pyplot as plt
import numpy as np

# 1) Define the data explicitly
sectors = ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources']
profits = [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]

# 2) Generate the plot
plt.figure(figsize=(10, 6)) # Set figure size for better readability

# Create bar chart
plt.bar(sectors, profits, color='skyblue')

# Set title and labels with bold font and larger size
plt.title('Top 5 Sectors by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
plt.xlabel('Sector', fontsize=12, fontweight='bold')
plt.ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Set x-axis tick labels to be bold and larger
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12) # y-ticks don't need to be bolded as per instruction

# 3) Add subtle horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 4) Save the figure
plt.savefig('top_5_sectors_net_profit.png')

# Show the plot (optional, but useful if running locally)
# plt.show()
