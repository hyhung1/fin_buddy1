import matplotlib.pyplot as plt
import pandas as pd # Included for general context, though not strictly used for data definition here

# 2) build the data structure explicitly
companies = [
    "PLX",
    "PVS",
    "PVD",
    "PVC",
    "PVB",
]
profits = [
    14032.41,
    4566.90,
    783.84,
    146.78,
    88.87,
]

# 3) generate the plot
plt.figure(figsize=(10, 6)) # Adjust figure size as needed
plt.bar(companies, profits, color='teal')

# Set title with bold font and larger size
plt.title("Top 5 Companies in Oil & Gas by Total Net Profit (2019-2023)",
          fontweight='bold', fontsize=14) # Slightly larger title font

# Set axis labels with bold font and larger size
plt.xlabel("Company Ticker", fontweight='bold', fontsize=12)
plt.ylabel("Total Net Profit (Billions VND)", fontweight='bold', fontsize=12)

# Set x-axis tick labels with bold font and larger size
# Rotation might be needed depending on the length of tickers
plt.xticks(companies, fontweight='bold', fontsize=12)

# 4) add the grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 5) save the figure
plt.savefig("top_oil_gas_companies_net_profit.png")

# Close the plot to free up memory
plt.close()

print("Generated plot: top_oil_gas_companies_net_profit.png") # Optional print to confirm saving
