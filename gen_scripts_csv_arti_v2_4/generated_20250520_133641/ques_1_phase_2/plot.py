import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 1) Import the required libraries (matplotlib, pandas, numpy already imported)

# 2) Build the data structure explicitly from the provided text
company_data = [
    {'ticker': 'DRC', 'sector': 'Automobiles & Parts',
     'net_profit': [250.53, 256.32, 290.83, 307.18, 246.33],
     'parent_equity': [1632.09, 1687.29, 1773.93, 1909.76, 1851.38]},
    {'ticker': 'SVC', 'sector': 'Automobiles & Parts',
     'net_profit': [233.33, 224.88, 211.33, 586.04, 44.43],
     'parent_equity': [1639.81, 1743.13, 1870.00, 2455.67, 2439.93]},
    {'ticker': 'HHS', 'sector': 'Automobiles & Parts',
     'net_profit': [195.26, 286.39, 236.40, 224.61, 351.85],
     'parent_equity': [3432.06, 3742.10, 3942.04, 4166.14, 4501.28]},
    {'ticker': 'VCB', 'sector': 'Banks',
     'net_profit': [18597.34, 18472.52, 22016.83, 29919.05, 33054.45],
     'parent_equity': [80954.34, 94094.98, 109186.43, 135646.08, 165012.67]},
    {'ticker': 'TCB', 'sector': 'Banks',
     'net_profit': [10226.21, 12582.47, 18415.38, 20436.43, 18190.87],
     'parent_equity': [62072.77, 74614.79, 93041.47, 113424.97, 131616.06]},
    {'ticker': 'CTG', 'sector': 'Banks',
     'net_profit': [9476.99, 13785.21, 14215.34, 16983.64, 20044.62],
     'parent_equity': [77354.82, 85439.22, 93649.51, 108316.31, 125871.82]},
    {'ticker': 'HPG', 'sector': 'Basic Resources',
     'net_profit': [7578.25, 13506.16, 34520.95, 8444.43, 6800.39],
     'parent_equity': [47786.64, 59219.79, 90780.63, 96112.94, 102836.42]},
    {'ticker': 'HSG', 'sector': 'Basic Resources',
     'net_profit': [1153.01, 4313.49, 4313.49, 251.32, 30.06],
     'parent_equity': [6584.12, 10831.79, 10831.79, 10883.57, 10780.17]},
    {'ticker': 'NKG', 'sector': 'Basic Resources',
     'net_profit': [47.33, 295.27, 2225.26, -124.68, 117.41],
     'parent_equity': [3016.81, 3181.02, 5723.20, 5319.65, 5423.07]},
    {'ticker': 'GVR', 'sector': 'Chemicals',
     'net_profit': [3833.36, 5076.35, 5340.05, 4804.15, 3372.86],
     'parent_equity': [50596.55, 51430.65, 51940.04, 53515.56, 54977.20]},
    {'ticker': 'DGC', 'sector': 'Chemicals',
     'net_profit': [571.56, 948.07, 2513.78, 6036.98, 3241.66],
     'parent_equity': [3451.56, 4067.43, 6332.00, 10833.65, 12026.94]},
    {'ticker': 'DPM', 'sector': 'Chemicals',
     'net_profit': [388.86, 701.62, 3171.52, 5584.89, 529.82],
     'parent_equity': [8161.44, 8247.50, 10713.16, 14017.44, 11545.20]},
    {'ticker': 'VCS', 'sector': 'Construction & Materials',
     'net_profit': [1410.11, 1428.42, 1772.06, 1148.70, 846.38],
     'parent_equity': [3448.69, 3857.82, 4874.20, 4868.74, 4985.82]},
    {'ticker': 'VGC', 'sector': 'Construction & Materials',
     'net_profit': [759.37, 667.31, 1279.08, 1913.04, 1162.24],
     'parent_equity': [7055.08, 7024.12, 8356.84, 9085.43, 9524.32]}
]

years = [2019, 2020, 2021, 2022, 2023]

# Convert to DataFrame for easier plotting
df_plot_data = pd.DataFrame(company_data)

# 3) Generate the plot for Net Profit
plt.figure(figsize=(12, 8))
for index, row in df_plot_data.iterrows():
    plt.plot(years, row['net_profit'], marker='o', linestyle='-', label=f"{row['ticker']} ({row['sector']})")

plt.title('Net Profit (2019-2023) for Top Companies by Sector', fontweight='bold', fontsize=14)
plt.xlabel('Year', fontweight='bold', fontsize=12)
plt.ylabel('Net Profit (Billions VND)', fontweight='bold', fontsize=12)
# Set x-axis ticks to be the years and make them bold
plt.xticks(years, [str(year) for year in years], fontweight='bold', fontsize=12)
plt.yticks(fontsize=10) # Y-ticks don't need to be bold as per standard practice, keeping font size consistent.

# 4) Add horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Add legend outside the plot to prevent overlap
plt.legend(title='Company (Sector)', bbox_to_anchor=(1.05, 1), loc='upper left')
# Adjust layout to make space for the legend
plt.tight_layout(rect=[0, 0, 0.85, 1])

# 5) Save figure as PNG
plt.savefig('net_profit_time_series.png')

# 3) Generate the plot for Parent Equity
plt.figure(figsize=(12, 8))
for index, row in df_plot_data.iterrows():
    plt.plot(years, row['parent_equity'], marker='o', linestyle='-', label=f"{row['ticker']} ({row['sector']})")

plt.title('Parent Equity (2019-2023) for Top Companies by Sector', fontweight='bold', fontsize=14)
plt.xlabel('Year', fontweight='bold', fontsize=12)
plt.ylabel('Parent Equity (Billions VND)', fontweight='bold', fontsize=12)
# Set x-axis ticks to be the years and make them bold
plt.xticks(years, [str(year) for year in years], fontweight='bold', fontsize=12)
plt.yticks(fontsize=10)

# 4) Add horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Add legend outside the plot to prevent overlap
plt.legend(title='Company (Sector)', bbox_to_anchor=(1.05, 1), loc='upper left')
# Adjust layout to make space for the legend
plt.tight_layout(rect=[0, 0, 0.85, 1])

# 5) Save figure as PNG
plt.savefig('parent_equity_time_series.png')

# Note: plt.show() is not included as per instructions for saving script
