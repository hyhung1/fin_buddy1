import matplotlib.pyplot as plt
import pandas as pd

# 1) Define the data explicitly from the provided text
data = [
    {'Ticker': 'DRC', 'Sector': 'Automobiles & Parts', '2019 Net Profit': 250.53, '2020 Net Profit': 256.32, '2021 Net Profit': 290.83, '2022 Net Profit': 307.18, '2023 Net Profit': 246.33, '2019 Parent Equity': 1632.09, '2020 Parent Equity': 1687.29, '2021 Parent Equity': 1773.93, '2022 Parent Equity': 1909.76, '2023 Parent Equity': 1851.38},
    {'Ticker': 'SVC', 'Sector': 'Automobiles & Parts', '2019 Net Profit': 233.33, '2020 Net Profit': 224.88, '2021 Net Profit': 211.33, '2022 Net Profit': 586.04, '2023 Net Profit': 44.43, '2019 Parent Equity': 1639.81, '2020 Parent Equity': 1743.13, '2021 Parent Equity': 1870.00, '2022 Parent Equity': 2455.67, '2023 Parent Equity': 2439.93},
    {'Ticker': 'HHS', 'Sector': 'Automobiles & Parts', '2019 Net Profit': 195.26, '2020 Net Profit': 286.39, '2021 Net Profit': 236.40, '2022 Net Profit': 224.61, '2023 Net Profit': 351.85, '2019 Parent Equity': 3432.06, '2020 Parent Equity': 3742.10, '2021 Parent Equity': 3942.04, '2022 Parent Equity': 4166.14, '2023 Parent Equity': 4501.28},
    {'Ticker': 'VCB', 'Sector': 'Banks', '2019 Net Profit': 18597.34, '2020 Net Profit': 18472.52, '2021 Net Profit': 22016.83, '2022 Net Profit': 29919.05, '2023 Net Profit': 33054.45, '2019 Parent Equity': 80954.34, '2020 Parent Equity': 94094.98, '2021 Parent Equity': 109186.43, '2022 Parent Equity': 135646.08, '2023 Parent Equity': 165012.67},
    {'Ticker': 'TCB', 'Sector': 'Banks', '2019 Net Profit': 10226.21, '2020 Net Profit': 12582.47, '2021 Net Profit': 18415.38, '2022 Net Profit': 20436.43, '2023 Net Profit': 18190.87, '2019 Parent Equity': 62072.77, '2020 Parent Equity': 74614.79, '2021 Parent Equity': 93041.47, '2022 Parent Equity': 113424.97, '2023 Parent Equity': 131616.06},
    {'Ticker': 'CTG', 'Sector': 'Banks', '2019 Net Profit': 9476.99, '2020 Net Profit': 13785.21, '2021 Net Profit': 14215.34, '2022 Net Profit': 16983.64, '2023 Net Profit': 20044.62, '2019 Parent Equity': 77354.82, '2020 Parent Equity': 85439.22, '2021 Parent Equity': 93649.51, '2022 Parent Equity': 108316.31, '2023 Parent Equity': 125871.82},
    {'Ticker': 'HPG', 'Sector': 'Basic Resources', '2019 Net Profit': 7578.25, '2020 Net Profit': 13506.16, '2021 Net Profit': 34520.95, '2022 Net Profit': 8444.43, '2023 Net Profit': 6800.39, '2019 Parent Equity': 47786.64, '2020 Parent Equity': 59219.79, '2021 Parent Equity': 90780.63, '2022 Parent Equity': 96112.94, '2023 Parent Equity': 102836.42},
    {'Ticker': 'HSG', 'Sector': 'Basic Resources', '2019 Net Profit': 1153.01, '2020 Net Profit': 4313.49, '2021 Net Profit': 4313.49, '2022 Net Profit': 251.32, '2023 Net Profit': 30.06, '2019 Parent Equity': 6584.12, '2020 Parent Equity': 10831.79, '2021 Parent Equity': 10831.79, '2022 Parent Equity': 10883.57, '2023 Parent Equity': 10780.17},
    {'Ticker': 'NKG', 'Sector': 'Basic Resources', '2019 Net Profit': 47.33, '2020 Net Profit': 295.27, '2021 Net Profit': 2225.26, '2022 Net Profit': -124.68, '2023 Net Profit': 117.41, '2019 Parent Equity': 3016.81, '2020 Parent Equity': 3181.02, '2021 Parent Equity': 5723.20, '2022 Parent Equity': 5319.65, '2023 Parent Equity': 5423.07},
    {'Ticker': 'GVR', 'Sector': 'Chemicals', '2019 Net Profit': 3833.36, '2020 Net Profit': 5076.35, '2021 Net Profit': 5340.05, '2022 Net Profit': 4804.15, '2023 Net Profit': 3372.86, '2019 Parent Equity': 50596.55, '2020 Parent Equity': 51430.65, '2021 Parent Equity': 51940.04, '2022 Parent Equity': 53515.56, '2023 Parent Equity': 54977.20},
    {'Ticker': 'DGC', 'Sector': 'Chemicals', '2019 Net Profit': 571.56, '2020 Net Profit': 948.07, '2021 Net Profit': 2513.78, '2022 Net Profit': 6036.98, '2023 Net Profit': 3241.66, '2019 Parent Equity': 3451.56, '2020 Parent Equity': 4067.43, '2021 Parent Equity': 6332.00, '2022 Parent Equity': 10833.65, '2023 Parent Equity': 12026.94},
    {'Ticker': 'DPM', 'Sector': 'Chemicals', '2019 Net Profit': 388.86, '2020 Net Profit': 701.62, '2021 Net Profit': 3171.52, '2022 Net Profit': 5584.89, '2023 Net Profit': 529.82, '2019 Parent Equity': 8161.44, '2020 Parent Equity': 8247.50, '2021 Parent Equity': 10713.16, '2022 Parent Equity': 14017.44, '2023 Parent Equity': 11545.20},
    {'Ticker': 'VCS', 'Sector': 'Construction & Materials', '2019 Net Profit': 1410.11, '2020 Net Profit': 1428.42, '2021 Net Profit': 1772.06, '2022 Net Profit': 1148.70, '2023 Net Profit': 846.38, '2019 Parent Equity': 3448.69, '2020 Parent Equity': 3857.82, '2021 Parent Equity': 4874.20, '2022 Parent Equity': 4868.74, '2023 Parent Equity': 4985.82},
    {'Ticker': 'VGC', 'Sector': 'Construction & Materials', '2019 Net Profit': 759.37, '2020 Net Profit': 667.31, '2021 Net Profit': 1279.08, '2022 Net Profit': 1913.04, '2023 Net Profit': 1162.24, '2019 Parent Equity': 7055.08, '2020 Parent Equity': 7024.12, '2021 Parent Equity': 8356.84, '2022 Parent Equity': 9085.43, '2023 Parent Equity': 9524.32},
    {'Ticker': 'VCG', 'Sector': 'Construction & Materials', '2019 Net Profit': 786.63, '2020 Net Profit': 1690.32, '2021 Net Profit': 519.93, '2022 Net Profit': 930.76, '2023 Net Profit': None, '2019 Parent Equity': 7738.32, '2020 Parent Equity': 7163.20, '2021 Parent Equity': 7627.62, '2022 Parent Equity': 9930.00, '2023 Parent Equity': None}, # VCG data truncated, using provided data and setting 2023 to None
]

df_wide = pd.DataFrame(data)

years = list(range(2019, 2024))

# Prepare Net Profit data for plotting
net_profit_value_vars = [f'{year} Net Profit' for year in years]
df_net_profit_long = df_wide.melt(id_vars=['Ticker', 'Sector'], value_vars=net_profit_value_vars, var_name='Year', value_name='Net Profit')
df_net_profit_long['Year'] = df_net_profit_long['Year'].str.extract('(\d+)').astype(int)

# Prepare Parent Equity data for plotting
parent_equity_value_vars = [f'{year} Parent Equity' for year in years]
df_parent_equity_long = df_wide.melt(id_vars=['Ticker', 'Sector'], value_vars=parent_equity_value_vars, var_name='Year', value_name='Parent Equity')
df_parent_equity_long['Year'] = df_parent_equity_long['Year'].str.extract('(\d+)').astype(int)

# 2) & 3) Generate the plots

# Plot Net Profit Trend
plt.figure(figsize=(12, 7))
for ticker in df_net_profit_long['Ticker'].unique():
    company_data = df_net_profit_long[df_net_profit_long['Ticker'] == ticker].sort_values('Year')
    plt.plot(company_data['Year'], company_data['Net Profit'], marker='o', linestyle='-', label=ticker)

plt.title('Net Profit Trend (2019-2023) for Top Companies per Sector', fontweight='bold', fontsize=14)
plt.xlabel('Year', fontweight='bold', fontsize=12)
plt.ylabel('Net Profit (Billions VND)', fontweight='bold', fontsize=12)
plt.xticks(years, [str(y) for y in years], fontweight='bold', fontsize=12) # Ensure all years are shown and are bold
plt.yticks(fontsize=10)
plt.legend(title='Ticker', bbox_to_anchor=(1.05, 1), loc='upper left')
# 4) Add grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)
plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout to make space for legend
# 5) Save the figure
plt.savefig('net_profit_trend.png')
plt.close()

# Plot Parent Equity Trend
plt.figure(figsize=(12, 7))
for ticker in df_parent_equity_long['Ticker'].unique():
    company_data = df_parent_equity_long[df_parent_equity_long['Ticker'] == ticker].sort_values('Year')
    plt.plot(company_data['Year'], company_data['Parent Equity'], marker='o', linestyle='-', label=ticker)

plt.title('Parent Equity Trend (2019-2023) for Top Companies per Sector', fontweight='bold', fontsize=14)
plt.xlabel('Year', fontweight='bold', fontsize=12)
plt.ylabel('Parent Equity (Billions VND)', fontweight='bold', fontsize=12)
plt.xticks(years, [str(y) for y in years], fontweight='bold', fontsize=12) # Ensure all years are shown and are bold
plt.yticks(fontsize=10)
plt.legend(title='Ticker', bbox_to_anchor=(1.05, 1), loc='upper left')
# 4) Add grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)
plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout to make space for legend
# 5) Save the figure
plt.savefig('parent_equity_trend.png')
plt.close()

print("Plots saved as net_profit_trend.png and parent_equity_trend.png")
