import matplotlib.pyplot as plt
import numpy as np

# 2) build the data structure
sectors = ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources']
profits = [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]

# 3) generate the plot(s)
plt.figure(figsize=(10, 6)) # Set a reasonable figure size

plt.bar(sectors, profits, color='skyblue')

# Set titles and labels with specified formatting
plt.title('Top 5 Sectors by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
plt.xlabel('Sector', fontsize=12, fontweight='bold')
plt.ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Set x-axis tick labels with specified formatting
plt.xticks(fontsize=12, fontweight='bold')

# 4) add the grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

plt.tight_layout() # Adjust layout to prevent labels overlapping

# 5) save each figure as a separate PNG image
plt.savefig('top_5_sectors_profit_2019-2023.png')

# Close the plot
plt.close()

print("Plot saved as 'top_5_sectors_profit_2019-2023.png'")
