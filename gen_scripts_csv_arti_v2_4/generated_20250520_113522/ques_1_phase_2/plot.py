import matplotlib.pyplot as plt
import numpy as np

# 1) Define the data explicitly
sectors = ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources']
profits = [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]

# 2) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(sectors, profits, color='skyblue')

# Set title and labels with bold text and larger font size
ax.set_title('Top 5 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)
ax.set_ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Make x-axis tick labels bold and larger font size
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=10) # Keep y-ticks normal size

# 3) Add subtle horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Improve layout
plt.tight_layout()

# 4) Save the figure as a separate PNG image
plt.savefig('top_5_sectors_net_profit_2019_2023.png')

# Although not strictly required by the prompt for a stand-alone script
# that saves to a file, plt.show() is often used to display the plot
# when running the script interactively. We can include it or omit it
# as the primary goal is saving the file. Omitting it to strictly
# follow the "no plotting code" guideline beyond the save.
# plt.show()
