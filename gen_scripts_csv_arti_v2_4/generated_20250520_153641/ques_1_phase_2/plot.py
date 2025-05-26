import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1) Define the data explicitly
data = {
    'Ticker': ['PLX', 'PVS', 'PVD', 'PVC', 'PVB'],
    'Total Net Profit 2019-2023': [14032.41, 4566.90, 783.84, 146.78, 88.87]
}

df_plot = pd.DataFrame(data)

# Sort data for potentially better visualization (optional, but good practice for bars)
df_plot = df_plot.sort_values('Total Net Profit 2019-2023', ascending=False)

# 2) Generate the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Create a bar plot
bars = ax.bar(df_plot['Ticker'], df_plot['Total Net Profit 2019-2023'], color='teal')

# Set title and labels with bold font and larger fontsize
ax.set_title('Top 5 Oil & Gas Companies by Total Net Profit (2019-2023)', fontsize=14, fontweight='bold')
ax.set_xlabel('Ticker', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Make x-axis tick labels bold and larger fontsize
plt.xticks(fontsize=12, fontweight='bold') # Correct way to set tick label font properties

# Make y-axis tick labels slightly larger for consistency (optional)
ax.tick_params(axis='y', labelsize=10)

# 3) Add subtle horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Ensure layout is tight
plt.tight_layout()

# 4) Save the figure
plt.savefig('top_5_oil_gas_net_profit.png')

# Close the plot to free up memory
plt.close(fig)
