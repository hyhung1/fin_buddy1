import matplotlib.pyplot as plt
import pandas as pd

# 1) Import required libraries (already done above)

# 2) Build the data structure based on the provided text output
# Data for Top 5 Sectors by Total Net Profit (2019-2023)
data = {
    'Sector': ['Banks', 'Real Estate', 'Food & Beverage', 'Basic Resources', 'Utilities'],
    'Total Net Profit (Billions VND)': [736043.33, 287593.57, 126291.79, 104507.20, 83154.58]
}
df_plot_data = pd.DataFrame(data)

# 3) Generate the plot
plt.figure(figsize=(12, 7)) # Create a new figure

# Create a bar chart
bars = plt.bar(df_plot_data['Sector'], df_plot_data['Total Net Profit (Billions VND)'], color='skyblue')

# Set bold and larger font size for title and labels
plt.title('Top 5 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
plt.xlabel('Sector', fontweight='bold', fontsize=12)
plt.ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Set bold and larger font size for x-axis tick labels
plt.xticks(fontweight='bold', fontsize=12)
plt.yticks(fontsize=10) # Keep y-ticks regular size

# 4) Add subtle horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 5) Save the figure as a PNG image
plt.savefig('top_5_sectors_net_profit_2019_2023.png')

# Display the plot (optional, won't show in some environments)
# plt.show()

print("Plot generated and saved as 'top_5_sectors_net_profit_2019_2023.png'")
