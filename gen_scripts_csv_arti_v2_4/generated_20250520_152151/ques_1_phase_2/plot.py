import matplotlib.pyplot as plt
import pandas as pd

# 1) Define the data explicitly based on the provided output
data = {
    'VCB': [80954.34, 94094.98, 109186.43, 135646.08, 165012.67],
    'CTG': [77354.82, 85439.22, 93649.51, 108316.31, 125871.82],
    'VHM': [64715.04, 89129.92, 131407.41, 148521.84, 182636.31],
    'TCB': [62072.77, 74614.79, 93041.47, 113424.97, 131616.06],
    'VNM': [29731.26, 33647.12, 35850.11, 32816.52, 35025.74],
    'MSN': [51888.41, 25030.28, 42336.65, 36636.74, 38237.24],
    'SAB': [20076.25, 21215.28, 22594.79, 24590.85, 25485.16],
    'VRE': [26953.51, 29335.82, 30650.83, 33424.69, 37826.85],
    'NVL': [24461.07, 31932.15, 41173.11, 44817.73, 45302.85]
}

years = [2019, 2020, 2021, 2022, 2023]

# Create a pandas DataFrame for easier plotting
df_plot = pd.DataFrame(data, index=years)

# 2) Generate the plot
fig, ax = plt.subplots(figsize=(12, 7))

# Plot each company's Parent Equity trend over the years
df_plot.plot(ax=ax)

# Set title and labels with bold font and larger size
ax.set_title('Parent Equity Trend (2019-2023) for Top Companies by Profit', fontweight='bold', fontsize=14)
ax.set_ylabel('Parent Equity (Billions VND)', fontweight='bold', fontsize=12)
ax.set_xlabel('Year', fontweight='bold', fontsize=12)

# Set x-axis ticks to be the specific years and make labels bold and larger
ax.set_xticks(years)
plt.xticks(fontsize=12, fontweight='bold') # Use plt.xticks for formatting

# Add a legend to identify companies
ax.legend(title='Ticker')

# 4) Add horizontal grid lines
ax.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to prevent labels overlapping
plt.tight_layout()

# 5) Save the figure
plt.savefig('parent_equity_trend_top_companies.png')

# Note: plt.show() is commented out as the prompt asks only for saving the figure.
# If you want to display the plot when running the script interactively, uncomment the line below.
# plt.show()
