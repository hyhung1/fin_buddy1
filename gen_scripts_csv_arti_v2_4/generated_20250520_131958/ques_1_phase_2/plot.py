import matplotlib.pyplot as plt
import numpy as np

# 1) Define the data explicitly
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
total_profits = [736043.33, 287593.57, 126291.79]

# 2) Create the plot
plt.figure(figsize=(10, 6))
plt.bar(sectors, total_profits, color='skyblue')

# 3) Set title, axis labels, and x-axis tick labels with bold font and larger size
plt.title('Top 3 Sectors by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
plt.xlabel('Sector', fontsize=12, fontweight='bold')
plt.ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Make x-axis tick labels bold
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=10) # y-ticks don't need to be bolded as per instructions

# 4) Add horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Improve layout
plt.tight_layout()

# 5) Save the figure as a separate PNG image
plt.savefig('top_sectors_net_profit_2019_2023.png')

# Close the plot figure
plt.close()
