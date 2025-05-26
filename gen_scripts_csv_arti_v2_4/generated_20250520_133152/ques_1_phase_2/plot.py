import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# 2) Build the data structure
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
net_profit = [736043.33, 287593.57, 126291.79]

# 3) Generate the plot(s)
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(sectors, net_profit, color=['skyblue', 'lightcoral', 'lightgreen'])

# Set title and labels with bold font and larger size
ax.set_title('Top 3 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)
ax.set_ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Make x-axis tick labels bold and larger
plt.xticks(fontweight='bold', fontsize=12)
plt.yticks(fontsize=10) # Y-ticks don't need to be bold

# Optional: Format y-axis labels for better readability (e.g., using commas)
formatter = mticker.StrMethodFormatter('{x:,.0f}')
ax.yaxis.set_major_formatter(formatter)


# 4) Add the grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout
plt.tight_layout()

# 5) Save each figure as a separate PNG image
plt.savefig('top_sectors_net_profit.png')

# Close the plot
plt.close(fig)
