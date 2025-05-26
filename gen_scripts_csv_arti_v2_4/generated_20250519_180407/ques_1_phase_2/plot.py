import matplotlib.pyplot as plt
import pandas as pd

# 2) Build the data structure explicitly
sectors = ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources']
net_profits = [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]

# Create a DataFrame for easier plotting if desired, though lists work too
# data = {'Sector': sectors, 'Total Net Profit': net_profits}
# df_plot = pd.DataFrame(data)

# 3) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(sectors, net_profits, color='skyblue')

# Set title and labels with bold font and larger size
ax.set_title('Top 5 Sectors by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
ax.set_xlabel('Sector', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Set x-tick labels with bold font and larger size
ax.set_xticklabels(sectors, rotation=45, ha='right', fontsize=12, fontweight='bold')

# 4) Add horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 5) Save the figure
plt.savefig('top_5_sectors_net_profit.png')

# Close the plot
plt.close(fig)
