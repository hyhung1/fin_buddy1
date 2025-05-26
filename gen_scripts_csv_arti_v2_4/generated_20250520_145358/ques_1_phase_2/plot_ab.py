import matplotlib.pyplot as plt
import pandas as pd

# 1) Define the data explicitly
data = {
    'Sector': ['Banks', 'Real Estate', 'Food & Beverage'],
    'Total Net Profit (2019-2023)': [736043.33, 287593.57, 126291.79]
}
df_plot_data = pd.DataFrame(data)

# 2) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(df_plot_data['Sector'], df_plot_data['Total Net Profit (2019-2023)'])

# 3) Add bold title, axis labels, and x-tick labels with larger font size
ax.set_title('Top 3 Sectors by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
ax.set_xlabel('Sector', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Make x-tick labels bold and larger
plt.xticks(fontsize=12, fontweight='bold')

# 4) Add subtle horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

plt.tight_layout() # Adjust layout to prevent labels overlapping

# 5) Save the figure as a PNG image
plt.savefig('top_3_sectors_net_profit.png')

# Close the plot figure to free up memory
plt.close(fig)
