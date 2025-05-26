import matplotlib.pyplot as plt
import pandas as pd

# 1) Define the data
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# Create a DataFrame for easy plotting
data = pd.DataFrame({'Sector': sectors, 'Total Net Profit': profits})

# 2) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the bar chart
bars = ax.bar(data['Sector'], data['Total Net Profit'])

# 3) Add formatting
ax.set_title('Top 3 Sectors by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
ax.set_xlabel('Sector', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Make x-axis tick labels bold and larger
plt.xticks(fontsize=12, fontweight='bold')
# Keep y-axis tick labels default or format if needed, but boldness not required per instruction
# plt.yticks(fontsize=12) # Optional: make y-ticks larger

# 4) Add grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# 5) Save the figure
plt.tight_layout() # Adjust layout to prevent labels overlapping
plt.savefig('top_sectors_profit.png')

# Display the plot (optional, not required by prompt but useful for debugging)
# plt.show()
