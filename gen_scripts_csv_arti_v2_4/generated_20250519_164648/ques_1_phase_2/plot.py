import matplotlib.pyplot as plt

# Data for the top 5 sectors and their total net profit (2019-2023)
sectors = ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources']
net_profit = [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]

# Create the figure and axes
fig, ax = plt.subplots(figsize=(10, 6))

# Create the bar chart
ax.bar(sectors, net_profit, color='skyblue')

# Set title and labels with bold font and larger size
ax.set_title('Top 5 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)
ax.set_ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Set x-axis tick labels with bold font and larger size, potentially rotated for readability
plt.xticks(fontweight='bold', fontsize=12, rotation=45, ha='right') # Rotate for long labels

# Add horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
fig.tight_layout()

# Save the figure
plt.savefig('top_5_sectors_net_profit.png')

# Show the plot (optional, will display if not run in a non-interactive environment)
# plt.show()
