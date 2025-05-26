import matplotlib.pyplot as plt
import pandas as pd

# 1) Define the data explicitly
sectors = ['Banks', 'Real Estate', 'Food & Beverage']
total_profits = [736043.33, 287593.57, 126291.79]

# Create a pandas Series for easier plotting
data = pd.Series(total_profits, index=sectors)

# 2) Generate the plot
plt.figure(figsize=(10, 6)) # Create a figure

data.plot(kind='bar', color=['skyblue', 'lightcoral', 'lightgreen'])

# Set title and labels with bold font and larger size
plt.title('Top 3 Sectors by Total Net Profit (2019-2023)', fontweight='bold', fontsize=14)
plt.xlabel('Sector', fontweight='bold', fontsize=12)
plt.ylabel('Total Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Set x-axis tick labels to bold and larger size
plt.xticks(rotation=45, ha='right', fontweight='bold', fontsize=12) # Rotate for readability

# 3) Add grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 4) Save the figure
plt.savefig('top_3_sectors_profit.png')

# Close the plot to free up memory
plt.close()

print("Plot saved as top_3_sectors_profit.png")
