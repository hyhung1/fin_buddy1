import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 1) Import the required libraries (already done above)

# 2) Define the data explicitly
data = {
    'Ticker': ['VCB', 'TCB', 'CTG', 'VHM', 'VRE', 'NVL', 'VNM', 'MSN', 'SAB'],
    'Parent Eq 2019': [80954.34, 62072.77, 77354.82, 64715.04, 26953.51, 24461.07, 29731.26, 51888.41, 20076.25],
    'Parent Eq 2020': [94094.98, 74614.79, 85439.22, 89129.92, 29335.82, 31932.15, 33647.12, 25030.28, 21215.28],
    'Parent Eq 2021': [109186.43, 93041.47, 93649.51, 131407.41, 30650.83, 41173.11, 35850.11, 42336.65, 22594.79],
    'Parent Eq 2022': [135646.08, 113424.97, 108316.31, 148521.84, 33424.69, 44817.73, 32816.52, 36636.74, 24590.85],
    'Parent Eq 2023': [165012.67, 131616.06, 125871.82, 182636.31, 37826.85, 45302.85, 35025.74, 38237.24, 25485.16]
}

df_plot = pd.DataFrame(data)

# Reshape data for easier plotting (optional but good practice for line plots)
df_plot_melted = df_plot.melt(id_vars='Ticker', var_name='Year', value_name='Parent_Equity')

# Extract year number from 'Year' column
df_plot_melted['Year_Num'] = df_plot_melted['Year'].str.extract('(\d{4})').astype(int)

# 3) Generate the plot
fig, ax = plt.subplots(figsize=(12, 7))

# Get unique tickers to iterate
tickers = df_plot['Ticker'].unique()
years = [2019, 2020, 2021, 2022, 2023]

# Plot a line for each ticker
for ticker in tickers:
    ticker_data = df_plot_melted[df_plot_melted['Ticker'] == ticker].sort_values('Year_Num')
    ax.plot(ticker_data['Year_Num'], ticker_data['Parent_Equity'], marker='o', linestyle='-', label=ticker)

# Set title and labels with bold font and larger fontsize
ax.set_title('Parent Equity (2019-2023) for Top Companies', fontsize=14, fontweight='bold')
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Parent Equity (Billions VND)', fontsize=12, fontweight='bold')

# Set x-axis ticks to be the years and make them bold and larger fontsize
ax.set_xticks(years)
plt.xticks(fontsize=12, fontweight='bold') # Correct way to set tick label font properties

# Make y-axis tick labels slightly larger for consistency (optional but improves readability)
ax.tick_params(axis='y', labelsize=10)

# Add a legend
ax.legend(title='Ticker', bbox_to_anchor=(1.05, 1), loc='upper left')

# 4) Add subtle horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Ensure layout is tight to prevent labels overlapping the legend
plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust rect to make space for the legend outside

# 5) Save the figure
plt.savefig('parent_equity_trend.png')

# Close the plot to free up memory
plt.close(fig)
