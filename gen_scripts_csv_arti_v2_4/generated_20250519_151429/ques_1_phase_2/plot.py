import matplotlib.pyplot as plt
import pandas as pd

# 2) Define the data explicitly
data = {
    'Sector': ['Banks', 'Real Estate', 'Food & Beverage', 'Utilities', 'Basic Resources'],
    'Total Net Profit (Billions VND)': [736043.33, 287593.57, 126291.79, 113286.29, 99619.73]
}

# Create a small DataFrame (optional, but good practice)
df_plot_data = pd.DataFrame(data)

# Sort data for better visualization (optional, but good for bar charts)
df_plot_data = df_plot_data.sort_values('Total Net Profit (Billions VND)', ascending=False)

# 3) Generate the plot
plt.figure(figsize=(10, 6)) # Set figure size for better readability

# Create a bar chart
plt.bar(df_plot_data['Sector'], df_plot_data['Total Net Profit (Billions VND)'], color='skyblue')

# Add title and labels with bold font and larger size
plt.title('Top 5 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
plt.xlabel('Sector', fontweight='bold', fontsize=12)
plt.ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Set x-axis tick labels to bold and larger size
plt.xticks(fontweight='bold', fontsize=12)
plt.yticks(fontsize=10) # Keep y-ticks normal size

# 4) Add horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 5) Save the figure
plt.savefig('top_5_sectors_net_profit.png')

# Although the script is stand-alone, in a typical interactive session you might want to display the plot
# plt.show() # Uncomment this line if you want to display the plot immediately
