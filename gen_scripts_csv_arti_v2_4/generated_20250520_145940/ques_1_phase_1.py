import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
df = pd.read_csv(r"C:\Users\HP\Downloads\excel_bud\fin_buddy\python_backend\uploads\2023Q4_Sheet1_processed_header7.csv")
# Make cleaned aliases for columns (whitespace variants) so any reference works
orig_cols = df.columns.tolist()
strip_cols = pd.Series(orig_cols).str.strip().tolist()
collapsed_cols = (pd.Series(orig_cols)
                 .str.replace(r"\s+", " ", regex=True)
                 .str.strip()
                 .tolist())
for orig, s, c in zip(orig_cols, strip_cols, collapsed_cols):
    if s not in orig_cols and s not in df.columns:
        df[s] = df[orig]
    if c not in orig_cols and c not in df.columns:
        df[c] = df[orig]
# Remove duplicate columns if any
df = df.loc[:, ~df.columns.duplicated()]
pd.set_option('display.float_format', '{:,.0f}'.format)

import pandas as pd

# Define the target sectors identified in the previous step
target_sectors = ['Banks', 'Real Estate', 'Food & Beverage']

# Define the list of columns for Net Profit, Owner's Equity, and Minority Interests for 2019-2023
years = ['2019', '2020', '2021', '2022', '2023']
net_profit_cols = [f'18. Net profit/(loss) after tax\nYear: {year}\nUnit: Billions VND\n' for year in years]
owner_equity_cols = [f'II. OWNER\'S EQUITY\nYear: {year}\nUnit: Billions VND\n' for year in years]
minority_interests_cols = [f'1.13. Minority interests\nYear: {year}\nUnit: Billions VND\n' for year in years]

# Filter the DataFrame to include only the specified sectors
# Use .copy() to avoid SettingWithCopyWarning when adding new columns
filtered_df = df[df['Sector L2\n'].isin(target_sectors)].copy()

# Calculate the cumulative net profit for each company across the specified years
filtered_df['Cumulative Net Profit'] = filtered_df[net_profit_cols].sum(axis=1)

# Function to get the top N companies by cumulative net profit within each group
def get_top_n(group, n=3):
    # Handle cases where a sector might have fewer than N companies
    return group.nlargest(n, 'Cumulative Net Profit')

# Group by sector and apply the function to get the top 3 companies
# group_keys=False prevents adding the group key to the index
top_companies_by_sector = filtered_df.groupby('Sector L2\n', group_keys=False).apply(get_top_n)

# Ensure the index is reset to access company info easily
top_companies_by_sector = top_companies_by_sector.reset_index(drop=True)


# Calculate Parent Equity for each year for the top companies
parent_equity_output_cols = []
for i, year in enumerate(years):
    owner_col = owner_equity_cols[i]
    minority_col = minority_interests_cols[i]
    parent_equity_col_name = f'Parent Equity {year}'
    # Ensure columns exist before calculating
    if owner_col in top_companies_by_sector.columns and minority_col in top_companies_by_sector.columns:
        top_companies_by_sector[parent_equity_col_name] = top_companies_by_sector[owner_col] - top_companies_by_sector[minority_col]
        parent_equity_output_cols.append(parent_equity_col_name)
    else:
        print(f"Warning: Equity columns for {year} not found in top companies dataframe.")


# Print the results
# Iterate through rows of the top_companies_by_sector DataFrame
for index, row in top_companies_by_sector.iterrows():
    # Print the sector the company belongs to for clarity
    sector = row['Sector L2\n']
    company_name = row['Company Name\n']
    cumulative_profit = row['Cumulative Net Profit']

    print(f"Sector: {sector.strip()}") # Strip sector name for cleaner output
    print(f"  Company: {company_name.strip()}") # Strip company name for cleaner output
    print(f"  Cumulative Net Profit (2019-2023): {cumulative_profit:.2f}")

    # Print Parent Equity for each year
    for year in years:
        parent_equity_col_name = f'Parent Equity {year}'
        if parent_equity_col_name in row:
            parent_equity = row[parent_equity_col_name]
            print(f"  Parent Equity {year}: {parent_equity:.2f}")
        else:
             print(f"  Parent Equity {year}: N/A") # Indicate if data was missing
