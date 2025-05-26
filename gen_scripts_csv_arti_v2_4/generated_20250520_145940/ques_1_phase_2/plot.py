import matplotlib.pyplot as plt
import numpy as np

# 1) & 2) Define the data explicitly

# Data for Cumulative Net Profit
companies = [
    'Vietcombank', 'Techcombank', 'VietinBank',
    'Vinamilk', 'Masan Group', 'SABECO',
    'Vinhomes', 'Vincom Retail', 'Novaland'
]
cumulative_profits = [
    122060.19, 79851.36, 74505.80,
    50019.53, 24485.32, 23991.16,
    154168.59, 13735.19, 13416.06
]

# Data for Parent Equity Trend
years = [2019, 2020, 2021, 2022, 2023]
parent_equity_data = {
    'Vietcombank': [80954.34, 94094.98, 109186.43, 135646.08, 165012.67],
    'Techcombank': [62072.77, 74614.79, 93041.47, 113424.97, 131616.06],
    'VietinBank': [77354.82, 85439.22, 93649.51, 108316.31, 125871.82],
    'Vinamilk': [29731.26, 33647.12, 35850.11, 32816.52, 35025.74],
    'Masan Group': [51888.41, 25030.28, 42336.65, 36636.74, 38237.24],
    'SABECO': [20076.25, 21215.28, 22594.79, 24590.85, 25485.16],
    'Vinhomes': [64715.04, 89129.92, 131407.41, 148521.84, 182636.31],
    'Vincom Retail': [26953.51, 29335.82, 30650.83, 33424.69, 37826.85],
    'Novaland': [24461.07, 31932.15, 41173.11, 44817.73, 45302.85]
}

# 3) Generate Plot 1: Cumulative Net Profit Bar Chart
fig1, ax1 = plt.subplots(figsize=(12, 7))

# Plot bars
ax1.bar(companies, cumulative_profits, color='skyblue')

# Set titles and labels with bold font and larger size
ax1.set_title('Cumulative Net Profit (2019-2023) for Top Companies', fontweight='bold', fontsize=14)
ax1.set_xlabel('Company', fontweight='bold', fontsize=12)
ax1.set_ylabel('Cumulative Net Profit (Billions VND)', fontweight='bold', fontsize=12)

# Set x-axis tick labels with bold font and larger size, rotate for readability
ax1.set_xticklabels(companies, rotation=45, ha='right', fontweight='bold', fontsize=12)

# 4) Add horizontal grid lines
ax1.grid(True, axis='y', linestyle='--', alpha=0.8)

# Improve layout
plt.tight_layout()

# 5) Save the figure
plt.savefig('cumulative_net_profit_top_companies.png')
plt.close(fig1) # Close the figure to free up memory

# 3) Generate Plot 2: Parent Equity Trend Line Chart
fig2, ax2 = plt.subplots(figsize=(12, 7))

# Plot lines for each company
for company, equity_values in parent_equity_data.items():
    ax2.plot(years, equity_values, marker='o', linestyle='-', label=company)

# Set titles and labels with bold font and larger size
ax2.set_title('Parent Equity Trend (2019-2023) for Top Companies', fontweight='bold', fontsize=14)
ax2.set_xlabel('Year', fontweight='bold', fontsize=12)
ax2.set_ylabel('Parent Equity (Billions VND)', fontweight='bold', fontsize=12)

# Set x-axis tick labels (years) with bold font and larger size
ax2.set_xticks(years) # Ensure ticks are set at the correct years
ax2.set_xticklabels(years, fontweight='bold', fontsize=12)

# 4) Add horizontal grid lines
ax2.grid(True, axis='y', linestyle='--', alpha=0.8)

# Add a legend
ax2.legend(title="Company")

# Improve layout
plt.tight_layout()

# 5) Save the figure
plt.savefig('parent_equity_trend_top_companies.png')
plt.close(fig2) # Close the figure

print("Plot saved to cumulative_net_profit_top_companies.png")
print("Plot saved to parent_equity_trend_top_companies.png")
