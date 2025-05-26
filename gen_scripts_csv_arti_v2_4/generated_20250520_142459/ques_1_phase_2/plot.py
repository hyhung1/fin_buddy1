import matplotlib.pyplot as plt
import pandas as pd
import numpy as np # Import numpy for potential NaN handling if needed, though manual data doesn't have it here.

# 1) Define the data explicitly based on the provided text output
# Data for Cumulative Net Profit
data_profit = {
    'Company': [
        'Automobiles & Parts - DRC', 'Automobiles & Parts - SVC', 'Automobiles & Parts - HHS',
        'Banks - VCB', 'Banks - TCB', 'Banks - CTG',
        'Basic Resources - HPG', 'Basic Resources - HSG', 'Basic Resources - NKG',
        'Chemicals - GVR', 'Chemicals - DGC', 'Chemicals - DPM'
        # Note: 'Construction & Materials' data was incomplete in the input, so it's excluded.
    ],
    'Cumulative Net Profit (Billions VND)': [
        1351.19, 1300.01, 1294.51,
        122060.19, 79851.36, 74505.80,
        70850.18, 10061.37, 2560.59,
        22426.77, 13312.05, 10376.71
    ]
}
df_plot_profit = pd.DataFrame(data_profit)

# Sort for better readability in the bar chart (highest profit first)
df_plot_profit = df_plot_profit.sort_values(by='Cumulative Net Profit (Billions VND)', ascending=False).reset_index(drop=True)

# Data for Parent Equity over time
years_plot = [2019, 2020, 2021, 2022, 2023]
data_pe = {
    'Company': [
        'Automobiles & Parts - DRC',
        'Automobiles & Parts - SVC',
        'Automobiles & Parts - HHS',
        'Banks - VCB',
        'Banks - TCB',
        'Banks - CTG',
        'Basic Resources - HPG',
        'Basic Resources - HSG',
        'Basic Resources - NKG',
        'Chemicals - GVR',
        'Chemicals - DGC',
        'Chemicals - DPM'
    ],
    2019: [1632.09, 1639.81, 3432.06, 80954.34, 62072.77, 77354.82, 47786.64, 6584.12, 3016.81, 50596.55, 3451.56, 8161.44],
    2020: [1687.29, 1743.13, 3742.10, 94094.98, 74614.79, 85439.22, 59219.79, 10831.79, 3181.02, 51430.65, 4067.43, 8247.50],
    2021: [1773.93, 1870.00, 3942.04, 109186.43, 93041.47, 93649.51, 90780.63, 10831.79, 5723.20, 51940.04, 6332.00, 10713.16],
    2022: [1909.76, 2455.67, 4166.14, 135646.08, 113424.97, 108316.31, 96112.94, 10883.57, 5319.65, 53515.56, 10833.65, 14017.44],
    2023: [1851.38, 2439.93, 4501.28, 165012.67, 131616.06, 125871.82, 102836.42, 10780.17, 5423.07, 54977.20, 12026.94, 11545.20]
}
# Create DataFrame and transpose to have Years as index and Companies as columns
df_plot_pe = pd.DataFrame(data_pe).set_index('Company').T


# 3) Generate the plot(s) for each distinct metric/trend

# Figure 1: Cumulative Net Profit (Bar Chart)
plt.figure(figsize=(14, 7)) # Adjust figure size for better label visibility
plt.bar(df_plot_profit['Company'], df_plot_profit['Cumulative Net Profit (Billions VND)'])

# Add title, axis labels, and x-tick labels with bold font and larger size
plt.title("Cumulative Net Profit (2019-2023) for Top Companies per Sector", fontweight='bold', fontsize=14)
plt.xlabel("Company (Sector - Ticker)", fontweight='bold', fontsize=12)
plt.ylabel("Cumulative Net Profit (Billions VND)", fontweight='bold', fontsize=12)
# Set x-tick labels explicitly and rotate for readability
plt.xticks(df_plot_profit['Company'], rotation=45, ha='right', fontweight='bold', fontsize=12)

# 4) Add subtle horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

plt.tight_layout() # Adjust layout to prevent labels overlapping

# 5) Save the figure as a PNG image
plt.savefig('cumulative_net_profit_top_companies.png')

# Close the plot figure to free memory
plt.close()


# Figure 2: Parent Equity Trend over time (Line Chart)
plt.figure(figsize=(14, 7)) # Adjust figure size

# Plot lines directly from the transposed DataFrame
# ax=plt.gca() gets the current axes object
df_plot_pe.plot(kind='line', ax=plt.gca())

# Add title, axis labels, and x-tick labels with bold font and larger size
plt.title("Parent Equity Trend (2019-2023) for Top Companies per Sector", fontweight='bold', fontsize=14)
plt.xlabel("Year", fontweight='bold', fontsize=12)
plt.ylabel("Parent Equity (Billions VND)", fontweight='bold', fontsize=12)

# Set x-ticks to the specific years and format them
plt.xticks(years_plot, [str(year) for year in years_plot], fontweight='bold', fontsize=12)

# Add a legend to identify the companies
# Placing the legend outside the plot area
plt.legend(title='Company', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

# 4) Add subtle horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Adjust layout to make space for the legend
plt.tight_layout(rect=[0, 0, 0.85, 1]) # [left, bottom, right, top] in fractions of the figure width/height

# 5) Save the figure as a PNG image
plt.savefig('parent_equity_trend_top_companies.png')

# Close the plot figure to free memory
plt.close()
