import matplotlib.pyplot as plt
import pandas as pd

# 1) Import the required libraries (done above)

# 2) Build the data structure
# Data from the previous result
sectors = ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources']
total_profit = [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]

# Create a pandas Series for easier plotting if needed, or just use lists
# data = pd.Series(total_profit, index=sectors)

# 3) Generate the plot(s)
fig, ax = plt.subplots(figsize=(10, 6))

# Create the bar chart
bars = ax.bar(sectors, total_profit, color='skyblue')

# Set title and labels with bold font and larger size
ax.set_title('Top 5 Sectors by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
ax.set_xlabel('Sector', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Make x-axis tick labels bold and larger
ax.set_xticklabels(sectors, fontsize=12, fontweight='bold')


# 4) Add the grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Improve layout
plt.tight_layout()

# 5) Save each figure as a separate PNG image
fig.savefig('top_5_sectors_net_profit.png', bbox_inches='tight')

# Optional: Display the plot (can be removed for non-interactive environments)
# plt.show()
