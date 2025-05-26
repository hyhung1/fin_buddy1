import matplotlib.pyplot as plt
import pandas as pd

# 1) Import the required libraries (done above)

# 2) Build the data structure
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
profits = [736043.33, 287593.57, 126291.79]

# It's often easier to work with pandas for plotting, even from lists
df_plot_data = pd.DataFrame({'Sector': sectors, 'Total Net Profit': profits})

# 3) Generate the plot
plt.figure(figsize=(10, 6)) # Create a new figure

# Create a bar plot
plt.bar(df_plot_data['Sector'], df_plot_data['Total Net Profit'])

# Set titles and labels with bold font and larger size
plt.title('Total Net Profit by Sector (2019-2023)', fontweight='bold', fontsize=14)
plt.xlabel('Sector', fontweight='bold', fontsize=12)
plt.ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Make x-axis tick labels bold and larger
plt.xticks(fontweight='bold', fontsize=12)
plt.yticks(fontsize=10) # Y-axis ticks don't need to be bold by instruction

# 4) Add the grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 5) Save the figure
plt.savefig('sector_net_profit_bar_chart.png')

# Optional: Display the plot (usually not needed in a script meant for saving)
# plt.show()
