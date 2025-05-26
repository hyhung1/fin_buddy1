import matplotlib.pyplot as plt
import pandas as pd

# 2) Build the data structure explicitly
data = {
    'Sector': ['Banks', 'Real Estate', 'Food & Beverage'],
    'Total Net Profit (2019-2023)': [736043.33, 287593.57, 126291.79]
}
df_plot = pd.DataFrame(data)

# Sort data for better visualization (optional but good practice)
df_plot = df_plot.sort_values('Total Net Profit (2019-2023)', ascending=False)

# 3) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(df_plot['Sector'], df_plot['Total Net Profit (2019-2023)'], color=['skyblue', 'lightgreen', 'salmon'])

# Set titles and labels with specified formatting
ax.set_title('Top 3 Sectors by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
ax.set_xlabel('Sector', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Make x-tick labels bold and larger
plt.xticks(fontsize=12, fontweight='bold')

# 4) Add horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

plt.tight_layout() # Adjust layout to prevent labels overlapping

# 5) Save the figure as a separate PNG image
plt.savefig('top_3_sectors_net_profit_2019_2023.png')

# Close the plot
plt.close(fig)

print("Plot saved as top_3_sectors_net_profit_2019_2023.png")
