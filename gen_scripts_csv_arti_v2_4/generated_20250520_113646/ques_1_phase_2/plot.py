import matplotlib.pyplot as plt
import numpy as np

# 1) Define the data explicitly based on the provided output
# Data structure: Dictionary where keys are Tickers and values are dictionaries
# containing 'sector', 'Net Profit' (yearly dict), and 'Parent Equity' (yearly dict)
data = {
    'DRC': {
        'sector': 'Automobiles & Parts',
        'Net Profit': {2019: 250.53, 2020: 256.32, 2021: 290.83, 2022: 307.18, 2023: 246.33},
        'Parent Equity': {2019: 1632.09, 2020: 1687.29, 2021: 1773.93, 2022: 1909.76, 2023: 1851.38}
    },
    'SVC': {
        'sector': 'Automobiles & Parts',
        'Net Profit': {2019: 233.33, 2020: 224.88, 2021: 211.33, 2022: 586.04, 2023: 44.43},
        'Parent Equity': {2019: 1639.81, 2020: 1743.13, 2021: 1870.00, 2022: 2455.67, 2023: 2439.93}
    },
    'HHS': {
        'sector': 'Automobiles & Parts',
        'Net Profit': {2019: 195.26, 2020: 286.39, 2021: 236.40, 2022: 224.61, 2023: 351.85},
        'Parent Equity': {2019: 3432.06, 2020: 3742.10, 2021: 3942.04, 2022: 4166.14, 2023: 4501.28}
    },
    'VCB': {
        'sector': 'Banks',
        'Net Profit': {2019: 18597.34, 2020: 18472.52, 2021: 22016.83, 2022: 29919.05, 2023: 33054.45},
        'Parent Equity': {2019: 80954.34, 2020: 94094.98, 2021: 109186.43, 2022: 135646.08, 2023: 165012.67}
    },
    'TCB': {
        'sector': 'Banks',
        'Net Profit': {2019: 10226.21, 2020: 12582.47, 2021: 18415.38, 2022: 20436.43, 2023: 18190.87},
        'Parent Equity': {2019: 62072.77, 2020: 74614.79, 2021: 93041.47, 2022: 113424.97, 2023: 131616.06}
    },
    'CTG': {
        'sector': 'Banks',
        'Net Profit': {2019: 9476.99, 2020: 13785.21, 2021: 14215.34, 2022: 16983.64, 2023: 20044.62},
        'Parent Equity': {2019: 77354.82, 2020: 85439.22, 2021: 93649.51, 2022: 108316.31, 2023: 125871.82}
    },
    'HPG': {
        'sector': 'Basic Resources',
        'Net Profit': {2019: 7578.25, 2020: 13506.16, 2021: 34520.95, 2022: 8444.43, 2023: 6800.39},
        'Parent Equity': {2019: 47786.64, 2020: 59219.79, 2021: 90780.63, 2022: 96112.94, 2023: 102836.42}
    },
    'HSG': {
        'sector': 'Basic Resources',
        'Net Profit': {2019: 1153.01, 2020: 4313.49, 2021: 4313.49, 2022: 251.32, 2023: 30.06},
        'Parent Equity': {2019: 6584.12, 2020: 10831.79, 2021: 10831.79, 2022: 10883.57, 2023: 10780.17}
    },
    'NKG': {
        'sector': 'Basic Resources',
        'Net Profit': {2019: 47.33, 2020: 295.27, 2021: 2225.26, 2022: -124.68, 2023: 117.41},
        'Parent Equity': {2019: 3016.81, 2020: 3181.02, 2021: 5723.20, 2022: 5319.65, 2023: 5423.07}
    },
    'GVR': {
        'sector': 'Chemicals',
        'Net Profit': {2019: 3833.36, 2020: 5076.35, 2021: 5340.05, 2022: 4804.15, 2023: 3372.86},
        'Parent Equity': {2019: 50596.55, 2020: 51430.65, 2021: 51940.04, 2022: 53515.56, 2023: 54977.20}
    },
    'DGC': {
        'sector': 'Chemicals',
        'Net Profit': {2019: 571.56, 2020: 948.07, 2021: 2513.78, 2022: 6036.98, 2023: 3241.66},
        'Parent Equity': {2019: 3451.56, 2020: 4067.43, 2021: 6332.00, 2022: 10833.65, 2023: 12026.94}
    },
    # Note: DPM data is incomplete in the user's provided output, excluding it.
}

years = [2019, 2020, 2021, 2022, 2023]
tickers = list(data.keys())

# 2) Generate the plot for Net Profit trends
fig_net_profit, ax_net_profit = plt.subplots(figsize=(12, 7))

for ticker in tickers:
    net_profits = [data[ticker]['Net Profit'].get(year, np.nan) for year in years] # Use get with nan for safety
    ax_net_profit.plot(years, net_profits, marker='o', label=f"{ticker} ({data[ticker]['sector']})")

# Set title and labels with bold text and larger font size
ax_net_profit.set_title('Net Profit Trend (2019-2023) for Top Companies', fontweight='bold', fontsize=14)
ax_net_profit.set_xlabel('Year', fontweight='bold', fontsize=12)
ax_net_profit.set_ylabel('Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Make x-axis tick labels bold and larger font size
plt.xticks(years, [str(year) for year in years], fontsize=12, fontweight='bold')
plt.yticks(fontsize=10) # Keep y-ticks normal size

# 3) Add subtle horizontal grid lines
ax_net_profit.grid(True, axis='y', linestyle='--', alpha=0.8)
ax_net_profit.grid(True, axis='x', linestyle='--', alpha=0.8) # Add vertical grid lines for years too

# Add legend
ax_net_profit.legend(loc='best', fontsize=9)

# Improve layout
plt.tight_layout()

# 4) Save the figure as a separate PNG image
plt.savefig('net_profit_trend_top_companies_2019_2023.png')

# Close the plot to free up memory
plt.close(fig_net_profit)


# 5) Generate the plot for Parent Equity trends
fig_parent_equity, ax_parent_equity = plt.subplots(figsize=(12, 7))

for ticker in tickers:
    parent_equities = [data[ticker]['Parent Equity'].get(year, np.nan) for year in years] # Use get with nan for safety
    ax_parent_equity.plot(years, parent_equities, marker='o', label=f"{ticker} ({data[ticker]['sector']})")

# Set title and labels with bold text and larger font size
ax_parent_equity.set_title('Parent Equity Trend (2019-2023) for Top Companies', fontweight='bold', fontsize=14)
ax_parent_equity.set_xlabel('Year', fontweight='bold', fontsize=12)
ax_parent_equity.set_ylabel('Parent Equity (Billions VND)', fontweight='bold', fontsize=12)

# Make x-axis tick labels bold and larger font size
plt.xticks(years, [str(year) for year in years], fontsize=12, fontweight='bold')
plt.yticks(fontsize=10) # Keep y-ticks normal size

# 6) Add subtle horizontal grid lines
ax_parent_equity.grid(True, axis='y', linestyle='--', alpha=0.8)
ax_parent_equity.grid(True, axis='x', linestyle='--', alpha=0.8) # Add vertical grid lines for years too

# Add legend
ax_parent_equity.legend(loc='best', fontsize=9)

# Improve layout
plt.tight_layout()

# 7) Save the figure as a separate PNG image
plt.savefig('parent_equity_trend_top_companies_2019_2023.png')

# Close the plot to free up memory
plt.close(fig_parent_equity)
