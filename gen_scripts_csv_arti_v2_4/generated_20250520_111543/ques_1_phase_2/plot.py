import matplotlib.pyplot as plt
import numpy as np

# 1) Import the required libraries (done above)

# 2) Build the data structure
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# 3) Generate the plot(s)
plt.figure(figsize=(10, 6)) # Set figure size for better readability

# Create bar chart for the top 3 sectors
plt.bar(sectors, profits, color='teal')

# Set title and labels with bold font and larger size
plt.title('Top 3 Sectors by Total Net Profit (2019-2023)', fontsize=12, fontweight='bold')
plt.xlabel('Sector', fontsize=12, fontweight='bold')
plt.ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Set x-axis tick labels to be bold and larger
plt.xticks(fontsize=12, fontweight='bold')

# 4) Add subtle horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 5) Save the figure
plt.savefig('top_3_sectors_net_profit.png')

# The plot is generated and saved. No need to call plt.show() in a script meant for generating files.
