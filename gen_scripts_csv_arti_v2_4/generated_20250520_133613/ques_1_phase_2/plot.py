import matplotlib.pyplot as plt
import numpy as np

# 1) Import required libraries (already done above)

# 2) Build the data structure
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# 3) Generate the plot
plt.figure(figsize=(10, 6)) # Optional: Adjust figure size
plt.bar(sectors, profits, color='skyblue')

# Set bold title and labels with larger font size
plt.title('Top 3 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
plt.xlabel('Sector', fontweight='bold', fontsize=12)
plt.ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Set x-axis tick labels to bold with larger font size
plt.xticks(fontweight='bold', fontsize=12)
plt.yticks(fontsize=10) # Keep y-ticks regular size for clarity

# 4) Add horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

plt.tight_layout() # Adjust layout to prevent labels overlapping

# 5) Save figure as PNG
plt.savefig('top_sectors_net_profit.png')

# Display the plot (optional in a script, but useful for viewing)
# plt.show()
