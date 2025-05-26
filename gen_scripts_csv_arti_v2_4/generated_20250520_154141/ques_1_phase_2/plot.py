import matplotlib.pyplot as plt
import pandas as pd

# 1) Define the data explicitly
companies = ['PLX', 'PVS', 'PVD', 'PVC', 'PVB']
total_net_profit = [14032.41, 4566.90, 783.84, 146.78, 88.87]

# 2) Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Create a bar chart
ax.bar(companies, total_net_profit, color='skyblue')

# 3) Format plot elements
ax.set_title('Top 5 Oil & Gas Companies by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
ax.set_xlabel('Company Ticker', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Set x-axis tick labels formatting
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=10) # Optional: increase y-tick font size slightly if needed

# 4) Add horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 5) Save the figure as a PNG image
plt.savefig('oil_gas_top5_net_profit.png')

# Optional: Display the plot (useful for interactive environments, though not strictly required by prompt)
# plt.show()
