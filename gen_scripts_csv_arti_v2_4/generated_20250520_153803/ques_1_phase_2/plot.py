import matplotlib.pyplot as plt
import pandas as pd

# 1) Define the data explicitly
data = {
    'Banks': {
        'VCB': [80954.34, 94094.98, 109186.43, 135646.08, 165012.67],
        'TCB': [62072.77, 74614.79, 93041.47, 113424.97, 131616.06],
        'CTG': [77354.82, 85439.22, 93649.51, 108316.31, 125871.82]
    },
    'Real Estate': {
        'VHM': [64715.04, 89129.92, 131407.41, 148521.84, 182636.31],
        'VRE': [26953.51, 29335.82, 30650.83, 33424.69, 37826.85],
        'NVL': [24461.07, 31932.15, 41173.11, 44817.73, 45302.85]
    },
    'Food & Beverage': {
        'VNM': [29731.26, 33647.12, 35850.11, 32816.52, 35025.74],
        'MSN': [51888.41, 25030.28, 42336.65, 36636.74, 38237.24],
        'SAB': [20076.25, 21215.28, 22594.79, 24590.85, 25485.16]
    }
}

years = [2019, 2020, 2021, 2022, 2023]

# 2) Generate the plot
fig, ax = plt.subplots(figsize=(12, 7))

# Plot data for each company
for sector, companies in data.items():
    for ticker, values in companies.items():
        # Use a label combining ticker and sector for clarity in the legend
        ax.plot(years, values, marker='o', label=f"{ticker} ({sector})")

# 3) Add formatting
ax.set_title('Parent Equity (2019-2023) for Top Companies in Key Sectors', fontsize=14, fontweight='bold')
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Parent Equity (Billions VND)', fontsize=12, fontweight='bold')

# Make x-axis tick labels bold and larger
plt.xticks(years, fontsize=12, fontweight='bold')

# Add legend
ax.legend(title="Company (Sector)", bbox_to_anchor=(1.05, 1), loc='upper left')

# 4) Add grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# 5) Save the figure
plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout to make space for the legend
plt.savefig('parent_equity_top_companies.png')

# Display the plot (optional - typically not included in stand-alone scripts for automated execution)
# plt.show()
