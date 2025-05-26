import matplotlib.pyplot as plt
import pandas as pd # Although not strictly needed for data definition here, included for context

# 2) build the data structure explicitly
sectors = [
    "Banks",
    "Real Estate",
    "Food & Beverage",
    "Utilities",
    "Basic Resources",
]
profits = [
    736043.33,
    287593.57,
    126291.79,
    113286.29,
    99619.73,
]

# 3) generate the plot
plt.figure(figsize=(10, 6)) # Adjust figure size as needed
plt.bar(sectors, profits, color='skyblue')

# Set title with bold font and larger size
plt.title("Top 5 Sectors with Highest Total Net Profit (2019-2023)",
          fontweight='bold', fontsize=14) # Slightly larger title font

# Set axis labels with bold font and larger size
plt.xlabel("Sector", fontweight='bold', fontsize=12)
plt.ylabel("Total Net Profit (Billions VND)", fontweight='bold', fontsize=12)

# Set x-axis tick labels with bold font and larger size, maybe rotate for readability
plt.xticks(sectors, rotation=30, ha='right', fontweight='bold', fontsize=12)

# 4) add the grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 5) save the figure
plt.savefig("top_sectors_net_profit.png")

# Close the plot to free up memory
plt.close()

print("Generated plot: top_sectors_net_profit.png") # Optional print to confirm saving
