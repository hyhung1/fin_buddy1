import matplotlib.pyplot as plt
import pandas as pd

# Data provided by the user
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# Build a simple structure (e.g., lists or dictionary)
data = {'Sector': sectors, 'Total Net Profit 2019-2023': profits}

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plotting the bar chart
bars = ax.bar(data['Sector'], data['Total Net Profit 2019-2023'], color='skyblue')

# Set title and labels with bold font and larger size
ax.set_title('Top 3 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
ax.set_ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)

# Make x-axis tick labels bold and larger
plt.xticks(fontsize=12, fontweight='bold')

# Add horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# Save the figure
plt.savefig('top_sectors_profit.png')

# Display the plot (optional, not strictly required by the prompt but good for verification)
# plt.show()
