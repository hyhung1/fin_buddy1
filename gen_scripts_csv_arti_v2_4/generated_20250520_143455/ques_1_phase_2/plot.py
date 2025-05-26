import matplotlib.pyplot as plt
import pandas as pd

# 1) Build the data structure explicitly from the provided output
data_list = []
years = [2019, 2020, 2021, 2022, 2023]

# Automobiles & Parts
companies_ap = ['DRC', 'SVC', 'HHS']
equity_ap = [
    [1632.09, 1687.29, 1773.93, 1909.76, 1851.38],
    [1639.81, 1743.13, 1870.00, 2455.67, 2439.93],
    [3432.06, 3742.10, 3942.04, 4166.14, 4501.28]
]
for i, company in enumerate(companies_ap):
    for j, year in enumerate(years):
        data_list.append({'Company': company, 'Year': year, 'Parent Equity': equity_ap[i][j]})

# Banks
companies_b = ['VCB', 'TCB', 'CTG']
equity_b = [
    [80954.34, 94094.98, 109186.43, 135646.08, 165012.67],
    [62072.77, 74614.79, 93041.47, 113424.97, 131616.06],
    [77354.82, 85439.22, 93649.51, 108316.31, 125871.82]
]
for i, company in enumerate(companies_b):
    for j, year in enumerate(years):
        data_list.append({'Company': company, 'Year': year, 'Parent Equity': equity_b[i][j]})

# Basic Resources
companies_br = ['HPG', 'HSG', 'NKG']
equity_br = [
    [47786.64, 59219.79, 90780.63, 96112.94, 102836.42],
    [6584.12, 10831.79, 10831.79, 10883.57, 10780.17],
    [3016.81, 3181.02, 5723.20, 5319.65, 5423.07]
]
for i, company in enumerate(companies_br):
    for j, year in enumerate(years):
        data_list.append({'Company': company, 'Year': year, 'Parent Equity': equity_br[i][j]})

# Chemicals
companies_c = ['GVR', 'DGC', 'DPM']
equity_c = [
    [50596.55, 51430.65, 51940.04, 53515.56, 54977.20],
    [3451.56, 4067.43, 6332.00, 10833.65, 12026.94],
    [8161.44, 8247.50, 10713.16, 14017.44, 11545.20]
]
for i, company in enumerate(companies_c):
    for j, year in enumerate(years):
        data_list.append({'Company': company, 'Year': year, 'Parent Equity': equity_c[i][j]})

# Construction & Materials
companies_cm = ['VCG', 'VGC', 'VCS']
equity_cm = [
    [7738.32, 7163.20, 7627.62, 9930.66, 10241.05],
    [7055.08, 7024.12, 8356.84, 9085.43, 9524.32],
    [3448.69, 3857.82, 4874.20, 4868.74, 4985.82]
]
for i, company in enumerate(companies_cm):
    for j, year in enumerate(years):
        data_list.append({'Company': company, 'Year': year, 'Parent Equity': equity_cm[i][j]})

# Financial Services (Exclude due to all NaN in provided snippet)
# companies_fs = ['SSI', 'VND', 'VCI'] # Data is NaN, skip plotting

# Food & Beverage (Partial data for MSN in provided snippet)
companies_fb = ['VNM', 'MSN']
equity_fb = [
    [29731.26, 33647.12, 35850.11, 32816.52, 35025.74], # VNM data for all 5 years
    [51888.41, 25030.28] # MSN data only for 2019, 2020 from snippet
]
years_fb_msn = [2019, 2020] # Years available for MSN in snippet

for i, company in enumerate(companies_fb):
    if company == 'VNM':
        for j, year in enumerate(years):
             data_list.append({'Company': company, 'Year': year, 'Parent Equity': equity_fb[i][j]})
    elif company == 'MSN': # Handle partial data based on snippet
         for j, year in enumerate(years_fb_msn):
             data_list.append({'Company': company, 'Year': year, 'Parent Equity': equity_fb[i][j]})


# Create DataFrame
df_plot = pd.DataFrame(data_list)

# 2) Generate the plot
plt.figure(figsize=(12, 8))

# Plot a line for each company
for company in df_plot['Company'].unique():
    company_data = df_plot[df_plot['Company'] == company]
    # Sort by year to ensure lines are drawn correctly
    company_data = company_data.sort_values(by='Year')
    plt.plot(company_data['Year'], company_data['Parent Equity'], label=company, marker='o') # Added marker for clarity

# Set title, labels, tick properties
plt.title('Parent Equity Trend for Top Companies per Sector (2019-2023)', fontweight='bold', fontsize=14)
plt.xlabel('Year', fontweight='bold', fontsize=12)
plt.ylabel('Parent Equity (Billions VND)', fontweight='bold', fontsize=12)

# Set x-ticks to be the years and make them bold
plt.xticks(years, labels=[str(y) for y in years], fontweight='bold', fontsize=12)

# 3) Add horizontal grid lines
plt.grid(True, axis='y', linestyle='--', alpha=0.8)

# Add legend - can be tricky with many lines. Place it outside the plot area.
plt.legend(title='Company', bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout to prevent legend from overlapping
plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust rect to make space for legend

# 4) Save the figure as a PNG image
plt.savefig('parent_equity_trend_top_companies_per_sector.png')

# Close the plot figure to free memory
plt.close()
