import matplotlib.pyplot as plt
import pandas as pd

# 1) Import the required libraries (done above)

# 2) Build the data structure
data = {'Sector': ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources'],
        'Total Net Profit (Billions VND)': [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]}
df_plot = pd.DataFrame(data)

# 3) Generate the plot
plt.figure(figsize=(10, 6))
plt.bar(df_plot['Sector'], df_plot['Total Net Profit (Billions VND)'])

# Set title and labels with bold font and larger size
plt.title('Top 5 Sectors by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
plt.xlabel('Sector', fontsize=12, fontweight='bold')
plt.ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Make x-axis tick labels bold and larger
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=10) # y-ticks don't need to be bold or larger as per instructions

# 4) Add grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

plt.tight_layout() # Adjust layout to prevent labels overlapping

# 5) Save the figure
plt.savefig('top_5_sectors_net_profit.png')

# Close the plot figure
plt.close()

print("Plot saved as top_5_sectors_net_profit.png")
