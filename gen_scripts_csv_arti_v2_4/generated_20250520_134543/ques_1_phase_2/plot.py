import matplotlib.pyplot as plt
import pandas as pd
import numpy as np # Used for handling NaN explicitly

# 1) Define the data explicitly from the provided text output
# Structure data points for easy processing
data_points = [
    {"Sector": "Automobiles & Parts", "Company": "Da Nang Rubber", "Metric": "Net Profit", "2019": 250.53, "2020": 256.32, "2021": 290.83, "2022": 307.18, "2023": 246.33},
    {"Sector": "Automobiles & Parts", "Company": "Da Nang Rubber", "Metric": "Parent Equity", "2019": 1632.09, "2020": 1687.29, "2021": 1773.93, "2022": 1909.76, "2023": 1851.38},
    {"Sector": "Automobiles & Parts", "Company": "SAVICO", "Metric": "Net Profit", "2019": 233.33, "2020": 224.88, "2021": 211.33, "2022": 586.04, "2023": 44.43},
    {"Sector": "Automobiles & Parts", "Company": "SAVICO", "Metric": "Parent Equity", "2019": 1639.81, "2020": 1743.13, "2021": 1870.00, "2022": 2455.67, "2023": 2439.93},
    {"Sector": "Automobiles & Parts", "Company": "Hoang Huy Investment Services", "Metric": "Net Profit", "2019": 195.26, "2020": 286.39, "2021": 236.40, "2022": 224.61, "2023": 351.85},
    {"Sector": "Automobiles & Parts", "Company": "Hoang Huy Investment Services", "Metric": "Parent Equity", "2019": 3432.06, "2020": 3742.10, "2021": 3942.04, "2022": 4166.14, "2023": 4501.28},
    {"Sector": "Banks", "Company": "Vietcombank", "Metric": "Net Profit", "2019": 18597.34, "2020": 18472.52, "2021": 22016.83, "2022": 29919.05, "2023": 33054.45},
    {"Sector": "Banks", "Company": "Vietcombank", "Metric": "Parent Equity", "2019": 80954.34, "2020": 94094.98, "2021": 109186.43, "2022": 135646.08, "2023": 165012.67},
    {"Sector": "Banks", "Company": "Techcombank", "Metric": "Net Profit", "2019": 10226.21, "2020": 12582.47, "2021": 18415.38, "2022": 20436.43, "2023": 18190.87},
    {"Sector": "Banks", "Company": "Techcombank", "Metric": "Parent Equity", "2019": 62072.77, "2020": 74614.79, "2021": 93041.47, "2022": 113424.97, "2023": 131616.06},
    {"Sector": "Banks", "Company": "VietinBank", "Metric": "Net Profit", "2019": 9476.99, "2020": 13785.21, "2021": 14215.34, "2022": 16983.64, "2023": 20044.62},
    {"Sector": "Banks", "Company": "VietinBank", "Metric": "Parent Equity", "2019": 77354.82, "2020": 85439.22, "2021": 93649.51, "2022": 108316.31, "2023": 125871.82},
    {"Sector": "Basic Resources", "Company": "Hoa Phat Group", "Metric": "Net Profit", "2019": 7578.25, "2020": 13506.16, "2021": 34520.95, "2022": 8444.43, "2023": 6800.39},
    {"Sector": "Basic Resources", "Company": "Hoa Phat Group", "Metric": "Parent Equity", "2019": 47786.64, "2020": 59219.79, "2021": 90780.63, "2022": 96112.94, "2023": 102836.42},
    {"Sector": "Basic Resources", "Company": "Hoa Sen Group", "Metric": "Net Profit", "2019": 1153.01, "2020": 4313.49, "2021": 4313.49, "2022": 251.32, "2023": 30.06},
    {"Sector": "Basic Resources", "Company": "Hoa Sen Group", "Metric": "Parent Equity", "2019": 6584.12, "2020": 10831.79, "2021": 10831.79, "2022": 10883.57, "2023": 10780.17},
    {"Sector": "Basic Resources", "Company": "Nam Kim Steel", "Metric": "Net Profit", "2019": 47.33, "2020": 295.27, "2021": 2225.26, "2022": -124.68, "2023": 117.41},
    {"Sector": "Basic Resources", "Company": "Nam Kim Steel", "Metric": "Parent Equity", "2019": 3016.81, "2020": 3181.02, "2021": 5723.20, "2022": 5319.65, "2023": 5423.07},
    {"Sector": "Chemicals", "Company": "Viet Nam Rubber Group", "Metric": "Net Profit", "2019": 3833.36, "2020": 5076.35, "2021": 5340.05, "2022": 4804.15, "2023": 3372.86},
    {"Sector": "Chemicals", "Company": "Viet Nam Rubber Group", "Metric": "Parent Equity", "2019": 50596.55, "2020": 51430.65, "2021": 51940.04, "2022": 53515.56, "2023": 54977.20},
    {"Sector": "Chemicals", "Company": "Ducgiang Chemicals", "Metric": "Net Profit", "2019": 571.56, "2020": 948.07, "2021": 2513.78, "2022": 6036.98, "2023": 3241.66},
    {"Sector": "Chemicals", "Company": "Ducgiang Chemicals", "Metric": "Parent Equity", "2019": 3451.56, "2020": 4067.43, "2021": 6332.00, "2022": 10833.65, "2023": 12026.94},
    {"Sector": "Chemicals", "Company": "Petrovietnam Fertilizer and Chemicals", "Metric": "Net Profit", "2019": 388.86, "2020": 701.62, "2021": 3171.52, "2022": 5584.89, "2023": 529.82},
    {"Sector": "Chemicals", "Company": "Petrovietnam Fertilizer and Chemicals", "Metric": "Parent Equity", "2019": 8161.44, "2020": 8247.50, "2021": 10713.16, "2022": 14017.44, "2023": 11545.20},
    {"Sector": "Construction & Materials", "Company": "VICOSTONE", "Metric": "Net Profit", "2019": 1410.11, "2020": 1428.42, "2021": 1772.06, "2022": 1148.70, "2023": 846.38},
    {"Sector": "Construction & Materials", "Company": "VICOSTONE", "Metric": "Parent Equity", "2019": 3448.69, "2020": 3857.82, "2021": 4874.20, "2022": 4868.74, "2023": 4985.82},
    {"Sector": "Construction & Materials", "Company": "Viglacera Corporation", "Metric": "Net Profit", "2019": 759.37, "2020": 667.31, "2021": 1279.08, "2022": 1913.04, "2023": 1162.24},
    {"Sector": "Construction & Materials", "Company": "Viglacera Corporation", "Metric": "Parent Equity", "2019": 7055.08, "2020": 7024.12, "2021": 8356.84, "2022": 9085.43, "2023": 9524.32},
    {"Sector": "Construction & Materials", "Company": "Vinaconex Group", "Metric": "Net Profit", "2019": 786.63, "2020": 1690.32, "2021": 519.93, "2022": 930.76, "2023": 396.44},
    {"Sector": "Construction & Materials", "Company": "Vinaconex Group", "Metric": "Parent Equity", "2019": 7738.32, "2020": 7163.20, "2021": 7627.62, "2022": 9930.66, "2023": 10241.05},
    {"Sector": "Financial Services", "Company": "SSI Securities", "Metric": "Net Profit", "2019": 907.10, "2020": 1255.93, "2021": 2695.07, "2022": 1697.69, "2023": 2294.47},
    {"Sector": "Financial Services", "Company": "SSI Securities", "Metric": "Parent Equity", "2019": np.nan, "2020": np.nan, "2021": np.nan, "2022": np.nan, "2023": np.nan},
    {"Sector": "Financial Services", "Company": "VNDIRECT", "Metric": "Net Profit", "2019": 382.66, "2020": 692.77, "2021": 2382.92, "2022": 1220.28, "2023": 2022.25},
    {"Sector": "Financial Services", "Company": "VNDIRECT", "Metric": "Parent Equity", "2019": np.nan, "2020": np.nan, "2021": np.nan, "2022": np.nan, "2023": np.nan},
    # Data truncated as per the provided sample
]

# Separate data for Net Profit and Parent Equity metrics
net_profit_data = [d for d in data_points if d['Metric'] == 'Net Profit']
parent_equity_data = [d for d in data_points if d['Metric'] == 'Parent Equity']

# Create DataFrames for plotting
df_net_profit = pd.DataFrame(net_profit_data).drop(columns=['Sector', 'Metric'])
df_parent_equity = pd.DataFrame(parent_equity_data).drop(columns=['Sector', 'Metric'])

years = [2019, 2020, 2021, 2022, 2023]

# 2) & 3) Generate the plot for Net Profit
plt.figure(figsize=(12, 8))
for index, row in df_net_profit.iterrows():
    company = row['Company']
    # Select only the year columns for plotting the trend line
    values = row[years].tolist()
    plt.plot(years, values, marker='o', label=company) # Added marker for clarity

# Add bold title, bold axis labels, and increase font size
plt.title('Net Profit Trend for Top Companies (2019-2023)', fontweight='bold', fontsize=14)
plt.xlabel('Year', fontweight='bold', fontsize=12)
plt.ylabel('Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Make x-axis tick labels bold and increase font size
plt.xticks(years, [str(year) for year in years], fontweight='bold', fontsize=12)
plt.yticks(fontsize=10) # Y-ticks can remain standard size

# 4) Add horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Add legend outside the plot
plt.legend(title="Company", bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout to make space for the legend
plt.tight_layout(rect=[0, 0, 0.85, 1])

# 5) Save the figure as a PNG image
plt.savefig('net_profit_trend.png')

# 2) & 3) Generate the plot for Parent Equity
plt.figure(figsize=(12, 8))
for index, row in df_parent_equity.iterrows():
    company = row['Company']
    # Select only the year columns for plotting the trend line
    values = row[years].tolist()
    # Plotting will handle NaN values by not drawing segments where data is missing
    plt.plot(years, values, marker='o', label=company)

# Add bold title, bold axis labels, and increase font size
plt.title('Parent Equity Trend for Top Companies (2019-2023)', fontweight='bold', fontsize=14)
plt.xlabel('Year', fontweight='bold', fontsize=12)
plt.ylabel('Parent Equity (Billions VND)', fontweight='bold', fontsize=12)

# Make x-axis tick labels bold and increase font size
plt.xticks(years, [str(year) for year in years], fontweight='bold', fontsize=12)
plt.yticks(fontsize=10) # Y-ticks can remain standard size

# 4) Add horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Add legend outside the plot
plt.legend(title="Company", bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout to make space for the legend
plt.tight_layout(rect=[0, 0, 0.85, 1])

# 5) Save the figure as a PNG image
plt.savefig('parent_equity_trend.png')

# Close plots to free memory (optional, but good practice in scripts)
plt.close('all')
