import matplotlib.pyplot as plt
import pandas as pd

# 1) Import the required libraries
# Already done above

# 2) Build the data structure
# The data provided in the previous turn is explicitly defined here.
sectors = ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources']
net_profits = [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]

# Create a pandas Series for easier plotting and handling of labels
sector_profit_series = pd.Series(net_profits, index=sectors)

# 3) Generate the plot(s)
fig, ax = plt.subplots(figsize=(10, 6))

# Create a bar chart
ax.bar(sector_profit_series.index, sector_profit_series.values, color='skyblue')

# Set title and labels with bold font and larger size
ax.set_title('Top 5 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)
ax.set_ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Set x-axis tick labels with bold font and larger size
plt.xticks(sector_profit_series.index, rotation=45, ha='right', fontweight='bold', fontsize=12)


# 4) Add the grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Improve layout to prevent labels overlapping
plt.tight_layout()

# 5) Save each figure as a separate PNG image
plt.savefig('top_5_sectors_net_profit.png')

# Close the plot
plt.close(fig)
