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

# Define the range of years for the analysis
years = [2019, 2020, 2021, 2022, 2023]

# Define the exact column names as they appear in the DataFrame
ticker_col = 'Ticker\n'
company_name_col = 'Company Name\n'
sector_col = 'Sector L2\n'
net_profit_col_template = '18. Net profit/(loss) after tax\nYear: {}\nUnit: Billions VND\n'
owner_equity_col_template = 'II. OWNER\'S EQUITY\nYear: {}\nUnit: Billions VND\n'
minority_interests_col_template = '1.13. Minority interests\nYear: {}\nUnit: Billions VND\n'

# Create lists of the specific column names for the years
net_profit_cols = [net_profit_col_template.format(year) for year in years]
owner_equity_cols = [owner_equity_col_template.format(year) for year in years]
minority_interests_cols = [minority_interests_col_template.format(year) for year in years]

# Ensure all necessary columns are included in the subset
all_required_cols = [ticker_col, company_name_col, sector_col] + net_profit_cols + owner_equity_cols + minority_interests_cols
# Create a subset DataFrame to work with, to avoid modifying the original df unnecessarily and for clarity
df_subset = df[all_required_cols].copy()

# Calculate the cumulative net profit for each company over the 2019-2023 period
# Summing across axis=1 aggregates values horizontally for each row (company)
df_subset['Cumulative Net Profit 2019-2023'] = df_subset[net_profit_cols].sum(axis=1)

# Calculate Parent Equity for each year and store in new columns
# Parent Equity = Owner's Equity - Minority Interests
for year in years:
    owner_col = owner_equity_col_template.format(year)
    minority_col = minority_interests_col_template.format(year)
    parent_equity_col_name = f'Parent Equity {year}'
    # Ensure both columns exist before attempting subtraction
    if owner_col in df_subset.columns and minority_col in df_subset.columns:
         df_subset[parent_equity_col_name] = df_subset[owner_col] - df_subset[minority_col]
    else:
         # Handle cases where a required column might be missing, though typically not expected with provided headers
         df_subset[parent_equity_col_name] = float('nan') # Assign NaN if columns are missing

# Group the subset DataFrame by sector and apply a function to find the top 3 companies in each group
# nlargest(3, 'Cumulative Net Profit 2019-2023') selects the top 3 rows based on the cumulative profit column
# group_keys=False prevents the sector column from becoming part of the index in the result
top_companies_per_sector = df_subset.groupby(sector_col, group_keys=False).apply(lambda x: x.nlargest(3, 'Cumulative Net Profit 2019-2023'))

# Sort the results by sector and then by cumulative net profit within each sector for clean printing
# This ensures companies within the same sector are printed together, and the top company appears first
top_companies_per_sector = top_companies_per_sector.sort_values(by=[sector_col, 'Cumulative Net Profit 2019-2023'], ascending=[True, False])

# Print the results in the desired format
current_sector = None
# Iterate over the rows of the DataFrame containing the top companies
# Use iterrows() for iterating over DataFrame rows
for index, row in top_companies_per_sector.iterrows():
    sector = row[sector_col]

    # Print sector header only when the sector changes
    if sector != current_sector:
        # Add a blank line for separation between sectors, except before the first one
        if current_sector is not None:
            print()
        print(f"Sector: {sector}")
        current_sector = sector

    # Print company ticker, name, and their cumulative net profit
    # Access columns using row[column_name]
    print(f"  {row[ticker_col]} - {row[company_name_col]} (Cumulative Net Profit 2019-2023: {row['Cumulative Net Profit 2019-2023']:.2f} Billions VND)")

    # Print Parent Equity for each year from 2019 to 2023 for the current company
    for year in years:
        parent_equity_col_name = f'Parent Equity {year}'
        # Check if the calculated column exists before trying to access its value
        if parent_equity_col_name in row:
             parent_equity_value = row[parent_equity_col_name]
             # Check if the value is not NaN before printing with formatting
             if pd.isna(parent_equity_value):
                 print(f"    Parent Equity {year}: N/A Billions VND")
             else:
                 print(f"    Parent Equity {year}: {parent_equity_value:.2f} Billions VND")
        else:
             # This case should ideally not happen if calculation succeeded, but as a safeguard
             print(f"    Parent Equity {year}: Data Error")
