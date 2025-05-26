import matplotlib.pyplot as plt
import pandas as pd

# 1) Define the data
tickers = ['PLX', 'PVS', 'PVD', 'PVC', 'PVB']
profits = [14032.41, 4566.90, 783.84, 146.78, 88.87]

# Create a DataFrame for plotting
data = pd.DataFrame({'Ticker': tickers, 'Total Net Profit': profits})

# 2) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the bar chart
bars = ax.bar(data['Ticker'], data['Total Net Profit'])

# 3) Add formatting
ax.set_title('Top 5 Oil & Gas Companies by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
ax.set_xlabel('Company Ticker', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Make x-axis tick labels bold and larger
plt.xticks(fontsize=12, fontweight='bold')
# Keep y-axis tick labels default

# 4) Add grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# 5) Save the figure
plt.tight_layout() # Adjust layout to prevent labels overlapping
plt.savefig('top_oil_gas_companies_profit.png')

# Display the plot (optional, not required by prompt but useful for debugging)
# plt.show()
