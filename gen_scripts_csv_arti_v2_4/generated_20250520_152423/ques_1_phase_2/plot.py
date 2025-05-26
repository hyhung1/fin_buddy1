import matplotlib.pyplot as plt
import pandas as pd

# 1) Define the data explicitly based on the provided output
tickers = ['PLX', 'PVS', 'PVD', 'PVC', 'PVB']
total_profits = [14032.41, 4566.90, 783.84, 146.78, 88.87]

# Although not strictly necessary for this simple chart,
# creating a structure helps manage data and align with previous examples.
# Using a dictionary or simple lists is sufficient per guidelines.
# Let's use lists for directness.

# 2) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plotting the bar chart
bars = ax.bar(tickers, total_profits, color='teal')

# 3) Set title, axis labels, and tick labels with bold font and larger size
ax.set_title('Top 5 Oil & Gas Companies by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
ax.set_ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)
ax.set_xlabel('Ticker', fontweight='bold', fontsize=12)

# Make x-axis tick labels bold and larger
plt.xticks(fontsize=12, fontweight='bold')

# 4) Add horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping (if necessary, though less likely with only 5 bars)
plt.tight_layout()

# 5) Save the figure
plt.savefig('top_oil_gas_companies_profit.png')

# Note: plt.show() is commented out as the prompt asks only for saving the figure.
# If you want to display the plot when running the script interactively, uncomment the line below.
# plt.show()
