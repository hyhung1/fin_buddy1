import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --- Data Definition ---

# Data for Total Net Profit (Plot 1)
# Using combined labels for simpler bar plotting as requested to have all in one figure
data_profit_list = [
    {'Label': 'Banks - VCB', 'Profit': 122060.19, 'Sector': 'Banks'},
    {'Label': 'Banks - TCB', 'Profit': 79851.36, 'Sector': 'Banks'},
    {'Label': 'Banks - CTG', 'Profit': 74505.80, 'Sector': 'Banks'},
    {'Label': 'Basic Resources - HPG', 'Profit': 70850.18, 'Sector': 'Basic Resources'},
    {'Label': 'Basic Resources - HSG', 'Profit': 10061.37, 'Sector': 'Basic Resources'},
    {'Label': 'Basic Resources - NKG', 'Profit': 2560.59, 'Sector': 'Basic Resources'},
    {'Label': 'Utilities - GAS', 'Profit': 55768.74, 'Sector': 'Utilities'},
    {'Label': 'Utilities - POW', 'Profit': 11405.58, 'Sector': 'Utilities'},
    {'Label': 'Utilities - PGV', 'Profit': 9502.10, 'Sector': 'Utilities'},
    {'Label': 'Technology - FPT', 'Profit': 27964.15, 'Sector': 'Technology'},
    {'Label': 'Technology - CMG', 'Profit': 1514.55, 'Sector': 'Technology'},
    {'Label': 'Technology - SAM', 'Profit': 402.71, 'Sector': 'Technology'},
    {'Label': 'Real Estate - VHM', 'Profit': 154168.59, 'Sector': 'Real Estate'},
    {'Label': 'Real Estate - VRE', 'Profit': 13735.19, 'Sector': 'Real Estate'},
    {'Label': 'Real Estate - NVL', 'Profit': 13416.06, 'Sector': 'Real Estate'},
    {'Label': 'Chemicals - GVR', 'Profit': 22426.77, 'Sector': 'Chemicals'},
    {'Label': 'Chemicals - DGC', 'Profit': 13312.05, 'Sector': 'Chemicals'},
    {'Label': 'Chemicals - DPM', 'Profit': 10376.71, 'Sector': 'Chemicals'},
}
df_profit_combined = pd.DataFrame(data_profit_list)

# Data for Parent Equity Trend (Plot 2)
data_equity = {
    'VCB': {2019: 80954.34, 2020: 94094.98, 2021: 109186.43, 2022: 135646.08, 2023: 165012.67},
    'TCB': {2019: 62072.77, 2020: 74614.79, 2021: 93041.47, 2022: 113424.97, 2023: 131616.06},
    'CTG': {2019: 77354.82, 2020: 85439.22, 2021: 93649.51, 2022: 108316.31, 2023: 125871.82},
    'HPG': {2019: 47786.64, 2020: 59219.79, 2021: 90780.63, 2022: 96112.94, 2023: 102836.42},
    'HSG': {2019: 6584.12, 2020: 10831.79, 2021: 10831.79, 2022: 10883.57, 2023: 10780.17},
    'NKG': {2019: 3016.81, 2020: 3181.02, 2021: 5723.20, 2022: 5319.65, 2023: 5423.07},
    'GAS': {2019: 49614.53, 2020: 49499.68, 2021: 52192.73, 2022: 61173.56, 2023: 65298.62},
    'POW': {2019: 29509.31, 2020: 31266.59, 2021: 31125.38, 2022: 33281.45, 2023: 34119.43},
    'PGV': {2019: 12392.25, 2020: 14963.99, 2021: 17409.15, 2022: 17596.72, 2023: 15771.13},
    'FPT': {2019: 16799.29, 2020: 18605.67, 2021: 21417.99, 2022: 25356.12, 2023: 29933.01},
    'CMG': {2019: 2263.22, 2020: 2345.17, 2021: 2590.38, 2022: 3075.65, 2023: 3341.60},
    'SAM': {2019: 2885.35, 2020: 3467.70, 2021: 4596.50, 2022: 4603.37, 2023: 4606.07},
    'VHM': {2019: 64715.04, 2020: 89129.92, 2021: 131407.41, 2022: 148521.84, 2023: 182636.31},
    'VRE': {2019: 26953.51, 2020: 29335.82, 2021: 30650.83, 2022: 33424.69, 2023: 37826.85},
    'NVL': {2019: 24461.07, 2020: 31932.15, 2021: 41173.11, 2022: 44817.73, 2023: 45302.85},
    'GVR': {2019: 50596.55, 2020: 51430.65, 2021: 51940.04, 2022: 53515.56, 2023: 54977.20},
    'DGC': {2019: 3451.56, 2020: 4067.43, 2021: 6332.00, 2022: 10833.65, 2023: 12026.94},
    'DPM': {2019: 8161.44, 2020: 8247.50, 2021: 10713.16, 2022: 14017.44, 2023: 11545.20},
}
df_equity = pd.DataFrame.from_dict(data_equity, orient='index')
df_equity.index.name = 'Ticker'
df_equity.columns.name = 'Year'
df_equity_plot = df_equity.T # Transpose for plotting Year on x-axis

# --- Plot 1: Total Net Profit (Bar Chart with Combined Labels) ---
fig1, ax1 = plt.subplots(figsize=(15, 7))

# Sort by Sector first to group bars visually in the chart
df_profit_combined_sorted = df_profit_combined.sort_values(by='Sector')
bars = ax1.bar(df_profit_combined_sorted['Label'], df_profit_combined_sorted['Profit'])

# Set titles and labels
ax1.set_title('Total Net Profit (2019-2023) for Top Companies per Sector', fontsize=14, fontweight='bold')
ax1.set_xlabel('Company (Sector - Ticker)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Total Net Profit (Billions VND)', fontsize=12, fontweight='bold')

# Set x-axis tick labels to be bold and larger, rotate for readability
ax1.tick_params(axis='x', labelsize=12, rotation=90)
# Make the rotated x-tick labels bold
for ticklabel in ax1.get_xticklabels():
    ticklabel.set_fontweight('bold')

# Add subtle horizontal grid lines
ax1.grid(True, axis='y', linestyle='--', alpha=0.8)

plt.tight_layout() # Adjust layout to prevent labels overlapping
plt.savefig('total_net_profit_top_companies.png')
plt.close(fig1)

# --- Plot 2: Parent Equity Trend (Line Chart) ---
fig2, ax2 = plt.subplots(figsize=(12, 7))

# Plot line chart using pandas plot on the transposed DataFrame
df_equity_plot.plot(kind='line', ax=ax2, marker='o')

# Set titles and labels
ax2.set_title('Parent Equity Trend (2019-2023) for Top Companies per Sector', fontsize=14, fontweight='bold')
ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Parent Equity (Billions VND)', fontsize=12, fontweight='bold')

# Ensure x-ticks are integers (years) and bold
ax2.set_xticks(df_equity_plot.index) # Set ticks to the years
ax2.tick_params(axis='x', labelsize=12)
for ticklabel in ax2.get_xticklabels():
    ticklabel.set_fontweight('bold')

# Set y-axis tick label size
ax2.tick_params(axis='y', labelsize=12)

# Add subtle horizontal grid lines
ax2.grid(True, axis='y', linestyle='--', alpha=0.8)

# Add legend
ax2.legend(title='Company Ticker')

plt.tight_layout() # Adjust layout
plt.savefig('parent_equity_trend_top_companies.png')
plt.close(fig2)
