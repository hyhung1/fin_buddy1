import matplotlib.pyplot as plt
import pandas as pd

# 1) Build the data structure
data = {'Sector': ['Banks', 'Real Estate', 'Food & Beverage'],
        'Total Net Profit 2019-2023': [736043.33, 287593.57, 126291.79]}
df_plot = pd.DataFrame(data)

# 2) Generate the plot
plt.figure(figsize=(10, 6)) # Optional: adjust figure size

# Create bar chart
bars = plt.bar(df_plot['Sector'], df_plot['Total Net Profit 2019-2023'])

# Set title, labels, and tick labels to bold and larger font size
plt.title('Top 3 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
plt.xlabel('Sector', fontweight='bold', fontsize=12)
plt.ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)
plt.xticks(rotation=0, fontweight='bold', fontsize=12) # Rotate if needed, but 0 is fine here

# 3) Add horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Optional: Adjust layout
plt.tight_layout()

# 4) Save the figure as a PNG image
plt.savefig('top_3_sectors_net_profit.png')

# Close the plot figure to free memory
plt.close()
